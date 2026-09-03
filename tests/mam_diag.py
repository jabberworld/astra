# -*- coding: utf-8 -*-
# One-off diagnostic for MUC MAM (XEP-0313) on jabberworld.info / ejabberd 26.07.
# Connects with slixmpp (xep_0313 + xep_0059), joins the room, issues manual
# MAM queries (various RSM variants incl. paging) and logs every raw incoming
# stanza to dynamic/mam_diag_raw.txt + a readable log to dynamic/mam_diag.txt.

import asyncio
import os
import sys
import time
import xml.etree.ElementTree as ET

import slixmpp
from slixmpp.xmlstream.handler.callback import Callback
from slixmpp.xmlstream.matcher import MatchXPath
import slixmpp.exceptions

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_LOG = os.path.join(HERE, "dynamic", "mam_diag_raw.txt")
DIAG_LOG = os.path.join(HERE, "dynamic", "mam_diag.txt")
ALL_LOG = os.path.join(HERE, "dynamic", "mam_diag_all.txt")
CLIENT_NS = "jabber:client"

JID = "astra-opencode@jabberworld.info"
PASSWORD = "JjBwEa7wbM6ZI"
RESOURCE = "mamdiag"
SERVER = "jabberworld.info"
PORT = 5223

ROOM = "astra-test@conference.jabberworld.info"
ROOM_NICK = "Astra"
MAM_NS = "urn:xmpp:mam:2"
RSM_NS = "http://jabber.org/protocol/rsm"
FORWARD_NS = "urn:xmpp:forward:0"
SID_NS = "urn:xmpp:sid:0"
DATA_NS = "jabber:x:data"


class MamDiag(slixmpp.ClientXMPP):
    def __init__(self):
        super().__init__("%s/%s" % (JID, RESOURCE), PASSWORD)
        self.raw = []
        self.all_count = 0
        self.register_plugin("xep_0030")
        self.register_plugin("xep_0059")
        self.register_plugin("xep_0313")
        self.register_plugin("xep_0045")
        self.register_plugin("xep_0199")
        self.add_event_handler("session_start", self.on_start)
        self.add_event_handler("muc::%s::presence" % ROOM, self.on_room_presence)
        self._room_joined = asyncio.Event()
        self._session_ready = asyncio.Event()

    def log(self, text):
        line = "[%s] %s\n" % (time.strftime("%H:%M:%S", time.gmtime()), text)
        with open(DIAG_LOG, "a") as fp:
            fp.write(line)
        print(line, end="")
        sys.stdout.flush()

    def _low(self, kind, stanza):
        try:
            elem = getattr(stanza, "xml", None)
            if elem is None and hasattr(stanza, "root"):
                elem = stanza.root
            if elem is None:
                elem = stanza
            if hasattr(elem, "tag"):
                raw = ET.tostring(elem, encoding="unicode").replace("\n", " ")
            else:
                raw = str(elem).replace("\n", " ")
        except Exception:
            try:
                raw = str(stanza).replace("\n", " ")
            except Exception:
                raw = "<no-xml>"
        self.all_count += 1
        with open(ALL_LOG, "a") as fp:
            fp.write("[%s.%03d] LOW %s: %s\n"
                     % (time.strftime("%H:%M:%S", time.gmtime()), time.time() % 1 * 1000, kind, raw))
        # Detect MAM result stanzas among messages.
        if kind == "message":
            try:
                result = elem.find("{%s}result" % MAM_NS)
            except Exception:
                result = None
            if result is not None:
                qid = result.get("queryid")
                self.log(">>> LOW-LEVEL MAM RESULT message queryid=%s tag=%s" % (qid, result.tag))

    def on_low_message(self, xml):
        self._low("message", xml)

    def on_low_iq(self, xml):
        self._low("iq", xml)

    def setup_low_handlers(self):
        self.register_handler(Callback("diag_msg", MatchXPath("{%s}message" % CLIENT_NS), self.on_low_message))
        self.register_handler(Callback("diag_iq", MatchXPath("{%s}iq" % CLIENT_NS), self.on_low_iq))

    def on_start(self, event):
        self.log("session_start; sending initial presence")
        self.send_presence()
        self.get_roster()
        self._session_ready.set()

    def on_room_presence(self, presence):
        if presence["muc"]["nick"] == ROOM_NICK and presence["type"] != "error":
            self._room_joined.set()
            self.log("joined room as %s/%s" % (ROOM, ROOM_NICK))

    async def wait_ready(self, timeout=25):
        try:
            await asyncio.wait_for(self._session_ready.wait(), timeout)
        except asyncio.TimeoutError:
            self.log("ERROR: session not ready")

    async def wait_join(self, timeout=15):
        try:
            await asyncio.wait_for(self._room_joined.wait(), timeout)
        except asyncio.TimeoutError:
            self.log("WARN: did not observe room-join presence in %ss" % timeout)

    def build_mam_iq(self, iq_id, max_items=None, before=None, after=None, query_check=True):
        iq = self.make_iq(id=iq_id, ito=ROOM, itype="set", iquery=MAM_NS)
        query = iq.xml.find("{%s}query" % MAM_NS)
        query.set("queryid", iq_id)
        if query_check:
            form = ET.SubElement(query, "{%s}x" % DATA_NS)
            form.set("type", "submit")
            field = ET.SubElement(form, "{%s}field" % DATA_NS)
            field.set("var", "FORM_TYPE")
            field.set("type", "hidden")
            value = ET.SubElement(field, "{%s}value" % DATA_NS)
            value.text = MAM_NS
        if max_items is not None or before is not None or after is not None:
            rsm = ET.SubElement(query, "{%s}set" % RSM_NS)
            if max_items is not None:
                m = ET.SubElement(rsm, "{%s}max" % RSM_NS)
                m.text = str(max_items)
            if before is not None:
                if before:
                    b = ET.SubElement(rsm, "{%s}before" % RSM_NS)
                    b.text = before
                else:
                    ET.SubElement(rsm, "{%s}before" % RSM_NS)
            if after is not None:
                a = ET.SubElement(rsm, "{%s}after" % RSM_NS)
                a.text = after
        return iq

    async def do_mam_query(self, label, iq_id, max_items=None, before=None, after=None):
        self.log("=== QUERY %s id=%s max=%s before=%s after=%s ==="
                 % (label, iq_id, max_items, repr(before), repr(after)))
        iq = self.build_mam_iq(iq_id, max_items=max_items, before=before, after=after, query_check=True)
        print("SENDING: " + ET.tostring(iq.xml, encoding="unicode").replace("\n", " "))
        try:
            resp = await iq.send(timeout=10)
        except slixmpp.exceptions.IqTimeout:
            self.log("QUERY TIMEOUT (no iq reply within 10s)")
            return None
        except Exception as exc:
            self.log("QUERY ERROR: %r" % exc)
            return None
        self.log("QUERY reply type=%s id=%s" % (resp["type"], resp["id"]))
        resp_xml = resp.xml
        fin = resp_xml.find("{%s}fin" % MAM_NS)
        if fin is None:
            self.log("QUERY: no <fin> in reply; full xml:")
            self.log("    " + ET.tostring(resp_xml, encoding="unicode").replace("\n", " "))
            return None
        complete = fin.get("complete")
        count = first = last = None
        rsm = fin.find("{%s}set" % RSM_NS)
        if rsm is not None:
            count = rsm.findtext("{%s}count" % RSM_NS)
            first = rsm.findtext("{%s}first" % RSM_NS)
            last = rsm.findtext("{%s}last" % RSM_NS)
        self.log("FIN complete=%s count=%s first=%s last=%s" % (complete, count, first, last))
        # Give the server time to deliver any result <message> stanzas after <fin>.
        await asyncio.sleep(2.0)
        self.log("after settle: total low stanzas=%d" % self.all_count)
        return {"complete": complete, "count": count, "first": first, "last": last}

    async def run(self):
        await self.wait_ready()
        # Join the room as a participant to match bot behaviour.
        self.log("joining %s as %s" % (ROOM, ROOM_NICK))
        self.plugin["xep_0045"].join_muc(ROOM, ROOM_NICK)
        await self.wait_join()
        self.log("room presence observed")

        # Variant 1: plain <max>3</max> (no before) - like the bot.
        r1 = await self.do_mam_query("plain-max-no-before", "diag-1", max_items=3)

        # Variant 1b: continue paging with <after> using the 'last' token from r1.
        if r1 and r1.get("last"):
            await self.do_mam_query("after-page", "diag-1b", max_items=3, after=r1["last"])

        # Variant 2: <max>3</max> with empty <before/> (last page).
        r2 = await self.do_mam_query("before-empty", "diag-2", max_items=3, before="")

        # Variant 2b: continue paging backwards with non-empty <before> using r2's first token.
        if r2 and r2.get("first"):
            await self.do_mam_query("before-token", "diag-2b", max_items=3, before=r2["first"])

        # Variant 3: no max at all (server default) - see if results are returned.
        await self.do_mam_query("no-max-no-rsm", "diag-3")

        await asyncio.sleep(3.0)
        self.log("total low-level stanzas captured: %d" % self.all_count)
        self.log("DONE")


async def amain():
    client = MamDiag()
    await client.connect(SERVER, PORT)
    client.setup_low_handlers()
    try:
        await client.run()
    finally:
        try:
            fut = client.disconnect()
            if fut is not None:
                await fut
        except Exception:
            pass


def main():
    path = os.path.join(HERE, "dynamic")
    if not os.path.isdir(path):
        os.makedirs(path, exist_ok=True)
    for f in (RAW_LOG, DIAG_LOG, ALL_LOG):
        try:
            open(f, "w").close()
        except Exception:
            pass
    try:
        asyncio.run(amain())
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
