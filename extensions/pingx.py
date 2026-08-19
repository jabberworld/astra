#===istalismanplugin===
# /* coding: utf-8 */

#  Talisman plugin
#  pingX_plugin.py

# (C) 2004 Lars Strand
# Rewritten to unprivileged ICMP (SOCK_DGRAM), Python 3.

import array
import binascii
import math
import os
import select
import socket
import struct
import sys
import time

ICMP_DATA_STR = 56
ICMP_TYPE = 8
ICMP_TYPE_IP6 = 128
ICMP_CODE = 0
ICMP_CHECKSUM = 0
ICMP_ID = 0
ICMP_SEQ_NR = 0

RECV_TTL = getattr(socket, "IP_RECVTTL", None)


def handler_in_cksummary(Packet):
        if len(Packet) & 1:
                Packet = Packet + b'\0'
        words = array.array('h', Packet)
        summary = 0
        for word in words:
                summary += (word & 0xffff)
        hi = summary >> 16
        lo = summary & 0xffff
        summary = hi + lo
        summary = summary + (summary >> 16)
        return (~summary) & 0xffff


def Packet_construct(id, size, ipv6):
        if size < int(struct.calcsize("d")):
                _error("packetsize to small, must be at least %d" % int(struct.calcsize("d")))
        if ipv6:
                header = struct.pack('!BBHHH', ICMP_TYPE_IP6, ICMP_CODE, ICMP_CHECKSUM, ICMP_ID, ICMP_SEQ_NR + id)
        else:
                header = struct.pack('!BBHHH', ICMP_TYPE, ICMP_CODE, ICMP_CHECKSUM, ICMP_ID, ICMP_SEQ_NR + id)
        load = b"-- IF YOU ARE READING THIS YOU ARE A NERD! --"
        size -= struct.calcsize("d")
        rest = b""
        if size > len(load):
                rest = load
                size -= len(load)
        rest += size * b"X"
        data = struct.pack("d", time.time()) + rest
        return header + data


def PING_START(type, source, alive = 0, timeout = 1.0, ipv6 = 0, number = sys.maxsize, node = None, flood = 0, size = ICMP_DATA_STR, status_only = 0):
        repl = ''
        host = None
        noPrintIPv6adr = 1
        if ipv6:
                if not getattr(socket, 'has_ipv6', False):
                        repl +=  u'Недоступно IPv6 на данной платформе\n'
                        host = node
                else:
                        try:
                                infos = socket.getaddrinfo(node, None, socket.AF_INET6, socket.SOCK_DGRAM)
                                host = infos[0][4][0]
                                if host == node:
                                        noPrintIPv6adr = 1
                                else:
                                        noPrintIPv6adr = 0
                        except Exception:
                                repl +=  (u'Не могу найти %s: Неизвестный хост' % node)+'\n'
                                host = node
        else:
                try:
                        host = socket.gethostbyname(node)
                except Exception:
                        repl +=  (u'Не могу найти %s: Неизвестный хост' % node)+'\n'
                        host = node
        if host:
                try:
                        if int(host.split(".")[-1]) == 0:
                                repl +=  u'Нет поддержки пинга в сети'+'\n'
                except Exception:
                        repl +=  u'Пинг: ошибка, не корректный запрос'+'\n'
                        host = '0.0.0.0'
        if number == 0:
                repl +=  u'Ошибка количества пакетов на передачу: %s' % str(number)+'\n'
                return repl
        if alive:
                number = 1
        start, mint, maxt, avg, lost, tsum, tsumsq = 1, 999, 0.0, 0.0, 0, 0.0, 0.0
        if not alive:
                if ipv6:
                        if noPrintIPv6adr == 1:
                                repl += (u'Пинг: %s : %d байты (40+8+%d)' % (str(node), 40 + 8 + size, size))+'\n'
                        else:
                                repl += (u'Пинг: %s (%s): %d байты (40+8+%d)' % (str(node), str(host), 40 + 8 + size, size))+'\n'
                else:
                        repl +=  (u'Пинг: %s (%s): %d байты (20+8+%d)' % (str(node), str(host), 20 + 8 + size, size))+'\n'
        Psocket = None
        try:
                if ipv6:
                        Psocket = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM, socket.IPPROTO_ICMPV6)
                else:
                        Psocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_ICMP)
                if RECV_TTL is not None:
                        try:
                                Psocket.setsockopt(socket.IPPROTO_IP, RECV_TTL, 1)
                        except Exception:
                                pass
        except Exception as e:
                repl +=  u'Ошибка сокета: %s' % e+u' You must have ICMP ping permissions (unprivileged ICMP)'+'\n'
                return repl
        try:
                while start <= number:
                        lost += 1
                        Packet = Packet_construct(start, size, ipv6)
                        try:
                                if ipv6:
                                        Psocket.sendto(Packet, (node, 0, 0, 0))
                                else:
                                        Psocket.sendto(Packet, (node, 0))
                        except Exception as e:
                                repl +=  u'Ошибка сокета: %s' % e+'\n'
                        Pong, iwtd = "", []
                        iwtd, owtd, ewtd = select.select([Psocket], [], [], timeout)
                        ttl = None
                        if iwtd:
                                endtime = time.time()
                                if RECV_TTL is not None:
                                        Pong, ancdata, flags, address = Psocket.recvmsg(size + 48, 1024)
                                        for cmsg_level, cmsg_type, cmsg_data in ancdata:
                                                if cmsg_type == RECV_TTL:
                                                        ttl = cmsg_data[0]
                                                elif cmsg_level == socket.IPPROTO_IPV6 and cmsg_type == socket.IPPROTO_IPV6_FLOWINFO:
                                                        pass
                                else:
                                        Pong, address = Psocket.recvfrom(size + 48)
                                lost -= 1
                                if Pong:
                                        PongHeader = Pong[0:8]
                                        PongType, PongCode, PongChksum, PongID, PongSeqnr = struct.unpack("!BBHHH", PongHeader)
                                        starttime = struct.unpack("d", Pong[8:16])[0]
                                        if not PongSeqnr == start:
                                                Pong = None
                        if not Pong:
                                if alive and not status_only:
                                        repl +=  u'Нет ответа от %s (%s)' % (str(node), str(host))+'\n'
                                elif alive and status_only:
                                        return u'Шняга какая-то!'
                                else:
                                        repl +=  u'Пинг таймаут: %s (icmp_seq=%d) ' % (host, start)+'\n'
                                if number != 1 and start < number:
                                        time.sleep(flood ^ 1)
                                start += 1
                                continue
                        triptime  = endtime - starttime
                        tsum += triptime
                        tsumsq += triptime * triptime
                        maxt = max ((triptime, maxt))
                        mint = min ((triptime, mint))
                        if alive and not status_only:
                                repl +=  str(node)+' ('+str(host)+u') жив'+'\n'
                        elif alive and status_only:
                                return u'Шняга какая-то!'
                        else:
                                if ttl is None:
                                        ttl = '?'
                                if ipv6:
                                        repl += u'%d байт от %s: #=%d время=%.5f ms' % (size + 8, host, PongSeqnr, triptime * 1000)+'\n'
                                else:
                                        repl += u'%d байт от %s: #=%d ttl=%s время=%.5f мс' % (size + 8, host, PongSeqnr, ttl, triptime* 1000)+'\n'
                        if number != 1 and start < number:
                                time.sleep(flood ^ 1)
                        start += 1
        except (EOFError, KeyboardInterrupt):
                start += 1
        except Exception:
                pass
        if start != 0 or lost > 0:
                start -= 1
                if start > 0:
                        avg = tsum / start
                        vari = tsumsq / start - avg * avg
                        if start == lost:
                                plost = 100
                        else:
                                plost = (lost/start)*100
                        if not alive:
                                repl += u'\n--- %s статистика пинга ---\n' % node
                                repl += u'%d пакетов отправлено, %d пакетов принято, %d%% потеряно пакетов' % (start, start-lost, plost)+'\n'
                                if plost != 100:
                                        repl += u'Итог мин./сред./макс./разн. = %.3f/%.3f/%.3f/%.3f мс' % (mint * 1000, (tsum/start) * 1000, maxt * 1000, math.sqrt(vari) * 1000)+'\n'
        try:
                Psocket.close()
        except Exception:
                if 'LAST' in globals() and 'null' in LAST:
                        LAST['null'] += 1
        return repl


def handler_NetPING(type, source, body):
        if body:
                sicle, ipv6, flood, size = 1.0, 0, 0, ICMP_DATA_STR
                node = body.split()[0].strip()
                if body.count('-a'):
                        alive = 1
                else:
                        alive = 0
                if body.count('-c'):
                        try:
                                cis = body.split('-c=')[1].strip()
                                ci = cis.split()[0].strip()
                                if check_number(ci):
                                        count = int(ci)
                                else:
                                        count = 3
                        except Exception:
                                count = 3
                else:
                        count = 3
                try:
                        repl = PING_START(type, source, alive = alive, timeout = sicle, ipv6 = ipv6, number = count, node = node, flood = flood, size = size)
                        if not repl:
                                repl = u'Аблом!'
                except Exception:
                        repl = u'Аблом!'
                reply(type, source, repl)
        else:
                reply(type, source, u'Что пингуем?')

command_handler(handler_NetPING, 10, "pingx")