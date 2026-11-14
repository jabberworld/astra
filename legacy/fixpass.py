# batch py3 fixes for extensions
import re, glob, os

def norm_indent(lead):
    col = 0
    for ch in lead:
        col += 8 if ch == '\t' else 1
    return ' '*col

def fix(path):
    raw = open(path, 'rb').read()
    if raw.startswith(b'\xef\xbb\xbf'):
        raw = raw[3:]
        bom = True
    else:
        bom = False
    s = raw.decode('utf-8', 'replace')
    lines = s.split('\n')
    out = []
    for ln in lines:
        m = re.match(r'^([ \t]*)(.*)$', ln)
        lead, rest = m.group(1), m.group(2)
        nl = norm_indent(lead) + rest
        # print statements
        pm = re.match(r'^( *)(print)\b(?![ (])', nl)
        if pm:
            nl = pm.group(1) + 'print(' + nl[len(pm.group(0)):] + ')'
        out.append(nl)
    s = '\n'.join(out)
    # except A, B -> except A as b  OR  except (A, B):
    def fix_except(mo):
        lead, pre, expr, var = mo.group(1), mo.group(2), mo.group(3), mo.group(4)
        expr = expr.strip()
        var = var.strip()
        if ',' in expr:
            return lead + 'except (' + expr + '):'
        return lead + 'except ' + expr + ' as ' + var + ':'
    s = re.sub(r'(^ *)except((?: +[A-Za-z_][A-Za-z0-9_.]*)+),\s*([A-Za-z_][A-Za-z0-9_]*)([ \t]*):', fix_except, s, flags=re.M)
    # exec stmt
    s = re.sub(r'^( *)exec( +)(.+?)\s+in\s+(.+?)\s*$', lambda mo: mo.group(1)+'exec('+mo.group(3)+', '+mo.group(4)+')', s, flags=re.M)
    # octal literals
    s = re.sub(r'\b0([0-7]{2,})\b', r'0o\1', s)
    # xrange
    s = re.sub(r'\bxrange\b', 'range', s)
    # has_key
    s = re.sub(r'(\b[A-Za-z_][A-Za-z0-9_]*(?:\[[^\]]*\])*)\.has_key\(([^()]*)\)', r'\2 in \1', s)
    # urllib fixes (rough), detailed per-file after
    s = s.replace('from urllib import urlopen', 'from urllib.request import urlopen')
    s = s.replace('from urllib import urlencode', 'from urllib.parse import urlencode')
    s = s.replace('import urllib2', 'import urllib.request as urllib2')
    s = s.replace('import urllib, urllib2', 'import urllib.request, urllib.parse')
    s = s.replace('from urllib2 import urlopen', 'from urllib.request import urlopen')
    s = s.replace('from urllib2 import ', 'from urllib.request import ')
    # MIMEText
    s = s.replace('from email.MIMEText import MIMEText', 'from email.mime.text import MIMEText')
    s = s.replace('import email.MIMEText as MIMEText', 'import email.mime.text')
    open(path, 'w', encoding='utf-8').write(s)
    return bom

changed = 0
for p in glob.glob('extensions/*.py'):
    fix(p)
    changed += 1
print('fixed', changed, 'files')
