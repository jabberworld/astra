# /* coding: utf-8 */
# Python 3 compatibility layer: emulates the legacy "xmpppy" module API
# (as used by the Astra / BlackSmith mark.1 bot) on top of slixmpp 1.17.

import asyncio
import copy
import random
import threading
import time
import traceback
import types as _types
import uuid
import xml.etree.ElementTree as ET

import types as _stdlib_types  # ensure the stdlib "types" module is loaded
import slixmpp
from slixmpp.stanza import Iq as _SlixIq
from slixmpp.xmlstream.handler.callback import Callback
from slixmpp.xmlstream.matcher import MatchXPath
from slixmpp.xmlstream.matcher.id import MatcherId
import xml.parsers.expat as _expat

# ---------------------------------------------------------------------------
# Exceptions (legacy xmpppy).
# ---------------------------------------------------------------------------
class NodeProcessed(Exception):
	"""Raised inside a handler to swallow the stanza."""
class Conflict(Exception):
	pass
class SystemShutdown(Exception):
	pass
class StreamError(Exception):
	pass
class HostUnknown(Exception):
	pass

# ---------------------------------------------------------------------------
# Namespaces.
# ---------------------------------------------------------------------------
NS_CLIENT, NS_MESSAGE, NS_PRESENCE, NS_IQ = "jabber:client", "jabber:client", "jabber:client", "jabber:client"
NS_VERSION = "jabber:iq:version"
NS_ROSTER = "jabber:iq:roster"
NS_TIME = "jabber:iq:time"
NS_LAST = "jabber:iq:last"
NS_PRIVACY = "jabber:iq:privacy"
NS_REGISTER = "jabber:iq:register"
NS_STATS = "http://jabber.org/protocol/stats"
NS_VCARD = "vcard-temp"
NS_AUTH = "jabber:iq:auth"
NS_AUTH_ERROR = "jabber:iq:auth:error"
NS_DISCO_INFO = "http://jabber.org/protocol/disco#info"
NS_DISCO_ITEMS = "http://jabber.org/protocol/disco#items"
NS_MUC = "http://jabber.org/protocol/muc"
NS_MUC_USER = "http://jabber.org/protocol/muc#user"
NS_MUC_ADMIN = "http://jabber.org/protocol/muc#admin"
NS_MUC_OWNER = "http://jabber.org/protocol/muc#owner"
NS_MUC_ROOMCONFIG = "http://jabber.org/protocol/muc#roomconfig"
NS_CAPS = "http://jabber.org/protocol/caps"
NS_DATA = "jabber:x:data"
NS_TIME_X = "jabber:x:delay"
NS_URN_TIME = "urn:xmpp:time"
NS_PING = "urn:xmpp:ping"
NS_RECEIPTS = "urn:xmpp:receipts"
NS_XHTML_IM = "http://jabber.org/protocol/xhtml-im"


def _nsjump(nsmap):
	obj = _types.SimpleNamespace()
	for key, value in nsmap.items():
		setattr(obj, key, value)
	return obj


protocol = _nsjump({
	"Client": None, "Node": None, "Message": None, "Presence": None,
	"Iq": None, "JID": None, "NS_": {}})


def _local(name):
	return name.rsplit("}", 1)[-1] if name.startswith("{") else name


def _find_by_local(root, names):
	"""Yield elements (including root) whose local name is in *names*."""
	if _local(root.tag) in names:
		yield root
	for sub in root.iter():
		if sub is not root and _local(sub.tag) in names:
			yield sub


class Node(object):
	"""Emulates xml.xmpppy message / presence / iq / generic nodes."""

	def __init__(self, name=None, attrs=None, payload=None, nsp=None, real=None, el=None, parent=None):
		if real is not None:
			self.el = real.xml if el is None else el
			self.real = real
		else:
			self.real = None
			self.el = el if el is not None else ET.Element(name)
			if nsp:
				self.el.set("xmlns", nsp)
			if attrs:
				for k, v in dict(attrs).items():
					if v is not None:
						self.el.set(k, str(v))
			if isinstance(payload, (str, bytes)):
				self.el.text = payload
			elif isinstance(payload, list):
				for item in payload:
					if item is not None:
						self.addChild(node=item)
		self.parent = parent

	# --- generic /
	def getName(self):
		return _local(self.el.tag)

	def getNamespace(self):
		ns = self.el.get("xmlns")
		tag = self.el.tag
		if not ns and isinstance(tag, str) and tag.startswith("{"):
			return self.el.tag[1:].split("}")[0]
		return ns

	def setNamespace(self, ns):
		self.el.set("xmlns", ns)

	def getAttrs(self):
		return dict(self.el.attrib)

	def getAttr(self, name):
		return self.el.get(name)

	def setAttr(self, name, value):
		self.el.set(name, value)

	def getData(self, default=None):
		return self.el.text

	def setData(self, data):
		self.el.text = data

	def getTag(self, name):
		for sub in _find_by_local(self.el, (name,)):
			if sub is not self.el:
				return Node(el=sub, parent=self)
		return None

	def getTags(self, name, attrs=None, namespace=None):
		result = []
		for sub in _find_by_local(self.el, (name,)):
			if sub is self.el:
				continue
			node = Node(el=sub, parent=self)
			if namespace and node.getNamespace() != namespace:
				continue
			if attrs and any(sub.get(key) != value for key, value in attrs.items()):
				continue
			result.append(node)
		return result

	def getTagAttr(self, name, attr):
		tag = self.getTag(name)
		if tag:
			return tag.getAttr(attr)
		return None

	def getTagData(self, name, default=None):
		tag = self.getTag(name)
		if tag is not None:
			return tag.getData() or default
		return default

	def getTagTag(self, name, name2):
		tag = self.getTag(name)
		if tag:
			return tag.getTag(name2)
		return None

	def setTag(self, name, namespace=None, attrs=None):
		sub = Node(name, attrs=attrs, nsp=namespace, parent=self)
		self.el.append(sub.el)
		return sub

	def setTagData(self, name, data, attrs=None):
		sub = Node(name, attrs=attrs, parent=self)
		sub.el.text = data
		self.el.append(sub.el)
		return sub

	def setTagAttr(self, name, attr, value):
		sub = self.getTag(name)
		if sub is None:
			sub = self.addChild(name)
		sub.el.set(attr, value)

	def getChildren(self):
		return [Node(el=sub, parent=self) for sub in list(self.el)]

	def getChildNodes(self):
		return self.getChildren()

	def addChild(self, name=None, attrs=None, payload=None, namespace=None, node=None, nsp=None):
		if node is not None:
			sub = node
			if isinstance(sub, Node):
				sub = sub.el
			self.el.append(sub)
			return Node(el=sub, parent=self)
		nsp = namespace or nsp
		sub = Node(name, attrs=attrs, payload=payload, nsp=nsp, parent=self)
		self.el.append(sub.el)
		return sub

	def getPayload(self):
		return self.getChildren()

	def getElementsByTagName(self, name):
		return [Node(el=sub, parent=self) for sub in _find_by_local(self.el, (name,)) if sub is not self.el]

	def getQueryChildren(self):
		q = self.getTag("query")
		return q.getChildren() if q else []

	def getQueryPayload(self):
		return self.getQueryChildren()

	def setQueryPayload(self, payload):
		q = self.getTag("query")
		if q is None:
			q = self.addChild("query")
		for sub in list(q.el):
			q.el.remove(sub)
		for item in payload:
			if isinstance(item, Node):
				item = item.el
			q.el.append(item)

	def getQueryNS(self):
		q = self.getTag("query")
		return q.getNamespace() if q else ""

	def setQueryNS(self, ns):
		q = self.getTag("query")
		if q is None:
			q = self.addChild("query")
		q.setNamespace(ns)

	def getDataChildren(self):
		return self.getChildren()

	# --- message/presence/iq attributes ---
	def getType(self):
		t = self.el.get("type")
		return t if t not in (None, "") else None

	def setType(self, value):
		self.el.set("type", value)

	def getTo(self):
		return self.el.get("to")

	def setTo(self, value):
		self.el.set("to", value)

	def getFrom(self):
		f = self.el.get("from")
		return JID(f) if f else None

	def setFrom(self, value):
		self.el.set("from", value)

	def getID(self):
		return self.el.get("id")

	def setID(self, value):
		self.el.set("id", value)

	def getTimestamp(self):
		for sub in self.el.iter():
			ns = _local_attr(sub, "xmlns")
			if sub is not self.el and (_local(sub.tag) == "delay" or _local(sub.tag) == "x") and ns in (NS_TIME_X, "jabber:x:delay"):
				return sub.get("stamp")
		return None

	def getErrorCode(self):
		err = self.getTag("error")
		return err.getAttr("code") if err else None

	# --- body / subject ---
	def getBody(self):
		body = self.getTag("body")
		return body.getData() if body is not None else None

	def setBody(self, body):
		return self.setTagData("body", body)

	def getSubject(self):
		sub = self.getTag("subject")
		return sub.getData() if sub is not None else None

	def getThread(self):
		sub = self.getTag("thread")
		return sub.getData() if sub is not None else None

	def getStatus(self, lang=None):
		sub = self.getTag("status")
		return sub.getData() if sub is not None else None

	def setStatus(self, status):
		return self.setTagData("status", status)

	def getShow(self):
		return self.el.get("show")

	def setShow(self, show):
		self.el.set("show", show)

	def getPriority(self):
		p = self.el.get("priority")
		try:
			return int(p)
		except (TypeError, ValueError):
			return None

	def setPriority(self, priority):
		self.el.set("priority", str(int(priority)))

	def getReason(self):
		return self.getStatus()

	def getError(self):
		return self.getTag("error")

	# --- MUC-specific (parsed from <x xmlns='...muc#user'><item .../>) ---
	def _muc_item(self):
		for sub in self.el.iter():
			if sub is self.el:
				continue
			if _local(sub.tag) in ("item",):
				parent = _parent_of(self.el, sub)
				if parent is not None and _local(parent.tag) == "x" and (parent.get("xmlns") in (NS_MUC_USER, None) or NS_MUC_USER in (parent.get("xmlns") or "")):
					return sub
			if _local(sub.tag) == "x" and NS_MUC_USER in (sub.get("xmlns") or ""):
				for item in sub.iter():
					if _local(item.tag) == "item":
						return item
		return None

	def getRole(self):
		item = self._muc_item()
		return item.get("role") if item is not None else None

	def getAffiliation(self):
		item = self._muc_item()
		return item.get("affiliation") if item is not None else None

	def getJid(self):
		item = self._muc_item()
		return item.get("jid") if item is not None else None

	def getNick(self):
		item = self._muc_item()
		nick = item.get("nick") if item is not None else None
		if not nick and self.getTo():
			to = str(self.getTo())
			if "/" in to:
				return to.split("/", 1)[1]
		return nick

	def getStatusCode(self):
		for sub in self.el.iter():
			if sub is self.el:
				continue
			if _local(sub.tag) == "status" and sub.get("code"):
				return sub.get("code")
		return None

	def getReporter(self):
		f = self.getFrom()
		return str(f) if f else ""

	# --- replies ---
	def buildReply(self, typ="result"):
		if self.real is not None and isinstance(self.real, _SlixIq):
			reply = _SlixIq()
			reply["to"] = self.el.get("from") or self.real.get("from") or ""
			reply["type"] = typ
			reply["id"] = self.el.get("id") or ""
			for child in list(self.real.xml):
				try:
					reply.xml.append(copy.deepcopy(child))
				except Exception:
					pass
			if typ == "result":
				reply["to"] = reply["to"]
			return Node(real=reply, el=reply.xml)
		reply = Node("iq", attrs={"type": typ, "id": self.getID()})
		frm = self.el.get("from")
		if frm:
			reply.el.set("to", frm)
		import re as _re
		for sub in list(self.el):
			reply.el.append(copy.deepcopy(sub))
		return reply

	def getNext(self):
		return None

	def toXml(self):
		return ET.tostring(self.el, encoding="unicode")

	def xml(self):
		return self.toXml()

	def __str__(self):
		try:
			return self.toXml()
		except Exception:
			return str(self.el)

	__unicode__ = __str__

	def __repr__(self):
		return "<%s %s>" % (self.__class__.__name__, self.toXml()[:100])


def _parent_of(root, sub):
	from xml.etree.ElementTree import Element
	if isinstance(sub, Element):
		for p in root.iter():
			for c in list(p):
				if c is sub:
					return p
	return None


def _local_attr(sub, name):
	return sub.get(name)


class Message(Node):
	def __init__(self, to=None, body=None, mtype=None, real=None, el=None, typ=None):
		if real is not None:
			super(Message, self).__init__(real=real, el=el)
		else:
			mtype = mtype if mtype is not None else typ
			super(Message, self).__init__("message", attrs={"to": to, "type": mtype})
			if body is not None:
				self.setTagData("body", body)

	def getMucroom(self):
		return self.getTo()

	def getMucnick(self):
		return self.getFrom() and self.getFrom().getResource()


class Presence(Node):
	def __init__(self, to=None, ptype=None, real=None, el=None, typ=None,
	             show=None, status=None):
		if real is not None:
			super(Presence, self).__init__(real=real, el=el)
		else:
			t = ptype if ptype is not None else typ
			super(Presence, self).__init__("presence", attrs={"to": to, "type": t})
			if show is not None:
				self.setShow(show)
			if status is not None:
				self.setStatus(status)


class Iq(Node):
	def __init__(self, typ=None, to=None, id=None, real=None, el=None):
		if real is not None:
			super(Iq, self).__init__(real=real, el=el)
		else:
			super(Iq, self).__init__("iq", attrs={"to": to, "type": typ, "id": id})

	def getType(self):
		t = self.el.get("type")
		return t if t not in (None, "") else None

	def getQueryChildren(self):
		return super(Iq, self).getQueryChildren()

	def getQueryPayload(self):
		return self.getQueryChildren()


def XML2Node(data):
	if isinstance(data, bytes):
		data = data.decode("utf-8", "replace")
	elif not isinstance(data, str):
		data = str(data)
	return Node(el=ET.fromstring(data))


def isResultNode(node):
	try:
		return node.getType() == "result"
	except Exception:
		return False


class JID(object):
	def __init__(self, node=None, domain=None, resource=None, **kwargs):
		if kwargs:
			node = kwargs.get("node") or node
			domain = kwargs.get("domain") or domain
			resource = kwargs.get("resource") or resource
		if node is None:
			node = ""
		node = str(node)
		if domain is None:
			if "/" in node:
				node, resource = node.split("/", 1)
			if node and "@" in node:
				user, domain = node.split("@", 1)
				node = user
			else:
				domain = node or ""
				node = ""
		if resource is None:
			resource = ""
		self.node = str(node)
		self.domain = str(domain)
		self.resource = str(resource)

	@classmethod
	def from_string(cls, jid):
		return cls(jid)

	def getNode(self):
		return self.node

	def getDomain(self):
		return self.domain

	def getResource(self):
		return self.resource

	def getStripped(self):
		if self.node:
			return "%s@%s" % (self.node, self.domain)
		return self.domain

	bare = property(lambda self: self.getStripped())
	full = property(lambda self: self.__str__())

	def __str__(self):
		base = self.getStripped()
		return "%s/%s" % (base, self.resource) if self.resource else base

	__unicode__ = __str__

	def __repr__(self):
		return self.__str__()

	def __eq__(self, other):
		return str(other) == str(self)

	def __hash__(self):
		return hash(str(self))


class Roster(object):
	def __init__(self, client):
		self.client = client

	def _stream(self):
		return self.client._stream

	def getItems(self):
		stream = self._stream()
		if stream is None:
			return []
		try:
			return [str(jid) for jid in stream.client_roster.keys()]
		except Exception:
			try:
				return list(stream.roster.items())
			except Exception:
				return []

	def Authorize(self, jid):
		stream = self._stream()
		if stream:
			stream.send_presence(ptype="subscribed", pto=str(jid))

	def Unauthorize(self, jid):
		stream = self._stream()
		if stream:
			stream.send_presence(ptype="unsubscribed", pto=str(jid))

	def Subscribe(self, jid):
		stream = self._stream()
		if stream:
			stream.send_presence(ptype="subscribe", pto=str(jid))

	def Unsubscribe(self, jid):
		stream = self._stream()
		if stream:
			stream.send_presence(ptype="unsubscribe", pto=str(jid))

	def setItem(self, jid, name, groups=None):
		stream = self._stream()
		if stream is None:
			return
		kwargs = {"name": name}
		if groups is not None:
			kwargs["groups"] = list(groups)
		try:
			stream.update_roster(jid, **kwargs)
		except Exception:
			pass

	def delItem(self, jid):
		stream = self._stream()
		if stream is None:
			return
		try:
			stream.del_roster_item(jid)
		except Exception:
			pass


class Browser(object):
	def __init__(self, client=None):
		self.client = client
		self.info = {"ids": [], "features": []}

	def PlugIn(self, client):
		self.client = client
		stream = client._stream if hasattr(client, "_stream") else None
		if stream:
			try:
				stream.register_plugin("xep_0030")
			except Exception:
				traceback.print_exc()

	def setDiscoHandler(self, data):
		items = data.get("items", []) or []
		info = data.get("info", {}) or {}
		stream = self.client._stream if self.client else None
		if not stream:
			return
		try:
			disco = stream.plugin["xep_0030"]
			for identity in info.get("ids", []) or []:
				disco.add_identity(identity.get("category", ""), identity.get("type", ""), identity.get("name", ""), "en")
			for feature in info.get("features", []) or []:
				disco.add_feature(feature)
		except Exception:
			traceback.print_exc()

	def setDiscoItemsHandler(self, items):
		pass


class HostedGroupChat(object):
	pass


class _features(object):
	@staticmethod
	def register(client, domain, fields):
		stream = getattr(client, "_stream", None)
		if stream is None:
			return None
		loop = getattr(client, "_loop", None)
		try:
			iq = _SlixIq()
			iq["to"] = domain
			iq["type"] = "set"
			iq["id"] = "leg-reg-%s" % uuid.uuid4()
			query = ET.SubElement(iq.xml, "{%s}query" % NS_REGISTER)
			for key, value in (fields or {}).items():
				child = ET.SubElement(query, "{%s}%s" % (NS_REGISTER, key))
				child.text = str(value)

			async def _do():
				return await iq.send(timeout=20)

			if loop is None:
				return None
			fut = asyncio.run_coroutine_threadsafe(_do(), loop)
			resp = fut.result(30)
			return resp is not None and resp["type"] == "result"
		except asyncio.TimeoutError:
			return False
		except Exception:
			return False

	@staticmethod
	def send_update_presence(client, show, status=""):
		stream = getattr(client, "_stream", None)
		if stream:
			stream.send_presence(pshow=show, pstatus=status)

	@staticmethod
	def setDefaultPrivacyList(client, listname):
		stream = getattr(client, "_stream", None)
		if not stream:
			return False
		try:
			query = ET.Element("{%s}query" % NS_PRIVACY)
			default = ET.SubElement(query, "default")
			default.set("name", listname)
			iq = _SlixIq()
			iq["to"] = client._jid_full or ""
			iq["type"] = "set"
			iq["id"] = "privacy-%s" % uuid.uuid4()
			iq.xml.append(query)
			_launch(iq, client)
			return True
		except Exception:
			return False


def _launch(iq, client):
	loop = getattr(client, "_loop", None)
	stream = getattr(client, "_stream", None)
	if not loop or not stream:
		return
	stream.send(iq)


class Client(object):
	def __init__(self, server=None, port=None, debug=None):
		self.server = server or ""
		self.port = int(port or 5222)
		self.debug = debug or []
		self._stream = None
		self._loop = None
		self._connected = False
		self._tls = False
		self._jid_full = ""
		self._password = ""
		self._server_tuple = None
		self._use_srv = False
		self._handlers = {}
		self.lastErr = ""
		self.lastErrCode = ""
		self.Roster = Roster(self)

	# -- legacy registration API --
	def RegisterHandler(self, ns, fn, *args):
		if ns not in ("message", "presence", "iq"):
			return ns
		self._handlers.setdefault(ns, []).append(fn)
		return ns

	def connect(self, server=(), proxy=None, secure=None, use_srv=True):
		if server is None:
			server = ()
		if isinstance(server, tuple) and len(server) and isinstance(server[0], str):
			self._server_tuple = (server[0], int(server[1]) if len(server) > 1 else self.port)
		elif isinstance(server, str):
			self._server_tuple = (server, self.port)
		else:
			self._server_tuple = None
			return False
		self._use_srv = bool(use_srv)
		return True

	def _run_loop(self):
		asyncio.set_event_loop(self._loop)
		try:
			if self._server_tuple:
				host, port = self._server_tuple
				fut = self._stream.connect(host=host, port=port)
			else:
				fut = self._stream.connect()
			self._loop.run_until_complete(fut)
			self._loop.run_forever()
		except Exception:
			traceback.print_exc()

	def _wait_session(self, timeout=45):
		loop = self._loop
		if not loop or not self._stream:
			return False
		try:
			fut = asyncio.run_coroutine_threadsafe(self._stream.session_bind_event.wait(), loop)
			fut.result(timeout)
			return True
		except Exception:
			return False

	def auth(self, jid, password, resource):
		jid = str(jid)
		if "@" in jid:
			node, domain = jid.split("@", 1)
		else:
			node = jid
			domain = self.server or ""
		resource = str(resource)
		self._jid_full = "%s@%s/%s" % (node, domain, resource)
		self._password = password
		return self._connect_real()

	def _connect_real(self):
		stream = slixmpp.ClientXMPP(self._jid_full, self._password)
		try:
			stream.verify_certificates = False
		except Exception:
			pass
		for plugin in ("xep_0077", "xep_0199"):
			try:
				stream.register_plugin(plugin)
			except Exception:
				traceback.print_exc()
		stream.add_event_handler("message", self._on_message)
		stream.add_event_handler("presence", self._on_presence)
		stream.add_event_handler("disconnected", self._on_disconnected)
		stream.add_event_handler("tls_success", self._on_tls_success)
		cb = Callback("legacy_iq", MatchXPath("{%s}iq" % NS_IQ), self._on_iq)
		try:
			stream.register_handler(cb)
		except Exception:
			traceback.print_exc()
		self._stream = stream
		self._loop = asyncio.new_event_loop()
		thread = threading.Thread(target=self._run_loop, name="xmpp-loop", daemon=True)
		thread.start()
		ok = self._wait_session()
		self._connected = ok
		return ("sasl" if ok else False)

	def _dispatch(self, fns, stanza):
		for fn in fns:
			try:
				fn(self, stanza)
			except NodeProcessed:
				pass
			except (SystemExit, KeyboardInterrupt):
				raise
			except Exception:
				traceback.print_exc()

	def _on_message(self, ev):
		self._dispatch(self._handlers.get("message", []), Message(real=ev))

	def _on_presence(self, ev):
		self._dispatch(self._handlers.get("presence", []), Presence(real=ev))

	def _on_iq(self, ev):
		self._dispatch(self._handlers.get("iq", []), Iq(real=ev))

	def _on_disconnected(self, ev):
		self._connected = False

	def _on_tls_success(self, ev):
		self._tls = True

	def isTls(self):
		if self._tls:
			return True
		stream = self._stream
		if not stream:
			return False
		try:
			return isinstance(stream.socket, __import__("ssl").SSLSocket)
		except Exception:
			return False

	def sendInitPresence(self):
		stream = self._stream
		if not stream:
			return
		try:
			if self._loop and self._loop.is_running():
				self._loop.call_soon_threadsafe(stream.send_presence)
			else:
				stream.send_presence()
		except Exception:
			traceback.print_exc()
		self._get_roster_async()

	def _get_roster_async(self):
		loop = self._loop
		stream = self._stream
		if not loop or not stream:
			return
		try:
			async def _get_roster():
				return await stream.get_roster()
			asyncio.run_coroutine_threadsafe(_get_roster(), loop)
		except Exception:
			traceback.print_exc()

	def send(self, stanza):
		stream = self._stream
		if not stream:
			return False
		if isinstance(stanza, Node):
			data = stanza.toXml()
		elif isinstance(stanza, str):
			data = stanza
		elif isinstance(stanza, bytes):
			data = stanza.decode("utf-8", "replace")
		else:
			data = str(stanza)
		try:
			if self._loop and self._loop.is_running():
				self._loop.call_soon_threadsafe(stream.send, data)
			else:
				stream.send(data)
			return True
		except Exception:
			traceback.print_exc()
			return False

	def SendAndCallForResponse(self, stanza, func, args=None, timeout=30):
		args = args or {}
		stream = self._stream
		if isinstance(stanza, Node):
			iid = stanza.getID()
			if not iid:
				iid = "leg-%s" % uuid.uuid4()
				stanza.setID(iid)
		else:
			iid = str(time.time() * 1000)
		if not stream:
			_thread = threading.Thread(target=lambda: func(self, None, **args), daemon=True)
			_thread.start()
			return
		handler_name = "legacy_resp_%s" % iid
		completed = threading.Event()

		def _handler(xml):
			if completed.is_set():
				return
			completed.set()
			try:
				stream.remove_handler(handler_name)
			except Exception:
				pass
			self._dispatch([lambda c, s: func(c, s, **args)], Iq(real=xml))

		cb = Callback(handler_name, MatcherId(iid), _handler)
		stream.register_handler(cb)
		self.send(stanza)

		def _timeout():
			if completed.wait(timeout):
				return
			completed.set()
			try:
				stream.remove_handler(handler_name)
			except Exception:
				pass
			try:
				func(self, None, **args)
			except Exception:
				traceback.print_exc()

		threading.Thread(target=_timeout, name="legacy-iq-timeout", daemon=True).start()

	def Process(self, timeout=1):
		time.sleep(timeout)

	def isConnected(self):
		stream = self._stream
		if not stream:
			return False
		try:
			if stream.session_bind_event.is_set() and not stream.disconnected.done():
				return True
			return False
		except Exception:
			return self._connected

	def disconnect(self):
		stream = self._stream
		if not stream:
			return
		try:
			if self._loop:
				asyncio.run_coroutine_threadsafe(stream.disconnect(), self._loop).result(8)
		except Exception:
			traceback.print_exc()
		self._connected = False

	def __str__(self):
		return self._jid_full or (self.server or "Client")


# Populate late attribute cross references (legacy allows xmpp.protocol.X or
# xmpp.X interchangeably).
features = _features()
simplexml = _types.SimpleNamespace(XML2Node=XML2Node,
								   xml=_types.SimpleNamespace(parsers=_types.SimpleNamespace(expat=_expat)))

browser = _types.SimpleNamespace(Browser=Browser)

debug = _types.SimpleNamespace(colors_enabled=True)

NS = {"CLIENT": NS_CLIENT, "MESSAGE": NS_MESSAGE, "PRESENCE": NS_PRESENCE, "IQ": NS_IQ,
	  "VERSION": NS_VERSION, "ROSTER": NS_ROSTER, "TIME": NS_TIME, "LAST": NS_LAST,
	  "PRIVACY": NS_PRIVACY, "REGISTER": NS_REGISTER, "STATS": NS_STATS, "VCARD": NS_VCARD,
	  "DISCO_INFO": NS_DISCO_INFO, "DISCO_ITEMS": NS_DISCO_ITEMS, "MUC": NS_MUC,
	  "MUC_USER": NS_MUC_USER, "MUC_ADMIN": NS_MUC_ADMIN, "MUC_OWNER": NS_MUC_OWNER,
	  "MUC_ROOMCONFIG": NS_MUC_ROOMCONFIG, "CAPS": NS_CAPS, "DATA": NS_DATA,
	  "URN_TIME": NS_URN_TIME, "PING": NS_PING}

protocol.Client = Client
protocol.Node = Node
protocol.Message = Message
protocol.Presence = Presence
protocol.Iq = Iq
protocol.JID = JID
protocol.NS_ = NS
