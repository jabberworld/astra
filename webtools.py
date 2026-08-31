# coding: utf-8

# BlackSmith-bot module.
# © simpleApps, 21.05.2012.
# Python 3 port.
# This module contains main web\
# functions for site parsing.

import re
from urllib.request import Request, urlopen
from html.entities import name2codepoint as htmlname2codepoint

import requests

try:
	from config import NETWORK_PROXY, NETWORK_TIMEOUT
except ImportError:
	NETWORK_PROXY, NETWORK_TIMEOUT = None, 20

UserAgents = {"OperaMini": "Opera/9.60 (J2ME/MIDP; Opera Mini/4.2.13337/724; U; ru)",  # Opera Mini 4.2 User-Agent
			  "Firefox": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0"}

## HTML Unescape and <br> tag replace.
edefs = dict()

for Name, Numb in htmlname2codepoint.items():
	edefs[Name] = chr(Numb)

del Name, Numb

compile_ehtmls = re.compile(r"&(#?[xX]?(?:[0-9a-fA-F]+|\w{1,8}));")

def uHTML(data):
	if data.count("&"):

		def e_sb(co):
			co = co.group(1)
			if co.startswith("#"):
				if chr(120) == co[1].lower():
					Char, c06 = co[2:], 16
				else:
					Char, c06 = co[1:], 10
				try:
					Numb = int(Char, c06)
					assert (-1 < Numb < 65535)
					Char = chr(Numb)
				except:
					Char = edefs.get(Char, "&%s;" % co)
			else:
				Char = edefs.get(co, "&%s;" % co)
			return Char

		data = compile_ehtmls.sub(e_sb, data)
	data = re.sub("</?br */?>", "\n", data)
	return data

## Opening urls.
def decode_page(data):
	if isinstance(data, bytes):
		for enc in ('utf-8', 'cp1251', 'windows-1251', 'koi8-r', 'cp866'):
			try:
				return data.decode(enc)
			except (UnicodeDecodeError, LookupError):
				continue
		return data.decode('utf-8', 'replace')
	return data

def read_link(link):
	return read_url(link)

def read_url(link, Browser = None):
	headers = {"User-Agent": Browser} if Browser else {}
	proxies = {'http': NETWORK_PROXY, 'https': NETWORK_PROXY} if NETWORK_PROXY else None
	data = requests.get(link, headers = headers, proxies = proxies,
	                    timeout = NETWORK_TIMEOUT).content
	return decode_page(data)

## Parsing.
def re_search(body, s0, s2, s1 = r"(?:.|\s)+"):
	comp = re.compile("%s(%s?)%s" % (s0, s1, s2), 16)
	body = comp.search(body)
	if body:
		body = (body.group(1)).strip()
	return body

## Get HTML tag.
def getTagData(tag, data):
	pattern = re.compile("<%(tag)s.*?>(.*?)</%(tag)s>" % vars(), flags=re.S+re.IGNORECASE)
	tagData = pattern.search(data)
	if tagData:
		tagData = tagData.group(1)
	return tagData or " "

def getTagArg(tag, argv, data):
	pattern = re.compile("<%(tag)s.*? %(argv)s=[\"']?(.*?)[\"']?\">(.*?)</%(tag)s>" % vars(), flags=re.S+re.IGNORECASE)
	tagData = pattern.search(data)
	if tagData:
		tagData = tagData.group(1)
	return tagData or " "

def stripTags(data, subBy = str(), pattern = "<[^<>]+>"):
	pattern = re.compile(pattern)
	return pattern.sub(subBy, data)

## IDNA tool.
def IDNA(text, encode = True):
	if "://" in text:
		text = text.split("://")[1]
	if encode:
		text = unicode_fix(text).encode("idna").decode("ascii")
	else:
		text = bytes(text, "ascii").decode("idna")
	return text

def unicode_fix(text):
	if isinstance(text, bytes):
		return text.decode("utf-8", "replace")
	return str(text)

## Format size.
def byteFormat(size):
	if size < 1024: return '%sb' % int(size)
	for t in ('kB','MB','GB'):
		size = size / 1024.0
		if size < 1024: break
	return '%.2f%s' % (size,t)