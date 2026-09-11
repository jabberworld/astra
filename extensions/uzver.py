#===istalismanplugin===
# ~*~ coding: utf-8 ~*~

UZVER = {}

def load_uzver(*list):
        global UZVER
        try:
                with file('dynamic/uzver.txt', 'r') as fp: UZVER = eval(fp.read())
        except:
                UZVER = {}
                with file('dynamic/uzver.txt', 'w') as fp: fp.write(str(UZVER))


register_stage1_init(load_uzver)