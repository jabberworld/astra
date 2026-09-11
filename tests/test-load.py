import sys, os, traceback
sys.path.insert(0, '/home/opencode/workspace/astra')
import astra
os.chdir('/home/opencode/workspace/astra')

good, bad = [], []
for plugin in sorted(os.listdir('extensions')):
    if not plugin.endswith('.py'):
        continue
    path = 'extensions/' + plugin
    try:
        data = open(path, encoding='utf-8', errors='replace').read(20)
    except Exception:
        data = ''
    plug = plugin.split('.')[0]
    if '# BS mark.1' in data or 'talis' in data:
        try:
            code = compile(open(path, encoding='utf-8', errors='replace').read(), path, 'exec')
            exec(code, astra.__dict__)
            good.append(plug)
        except Exception as e:
            tb = traceback.format_exc(limit=4).strip().split('\n')
            bad.append((plug, e.__class__.__name__, str(e)[:140]))
print('== LOADED OK (%d) ==' % len(good))
for g in sorted(good):
    print('  OK ', g)
print('== FAILED (%d) ==' % len(bad))
for b in bad:
    print('  FAIL', b[0], '|', b[1], '|', b[2])
print('commands registered:', len(astra.COMMAND_HANDLERS))
