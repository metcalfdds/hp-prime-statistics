import sys, re, glob, json, os, signal
sys.setrecursionlimit(20000)
sys.path.insert(0, 'tools')
from ppl_run_v3e import Harness, KEY
ROUT = {
 'AgreeLab':['ag_Help'], 'AnovaLab':['av_Help'], 'BayesTree':['bt_HelpView'], 'BiNorm3D':['bnHelp'],
 'BurrLab':['bu_Help'], 'CICatcher':['cqHelp'], 'CentralLimit':['cltHelp'], 'ChiTable':['csHelp'],
 'DNAMixLR':['dmHelp'], 'EpiStats':['es_Help_About','es_Help_Table','es_Help_SensSpec','es_Help_RiskOdds','es_Help_CI','es_Help_MH','es_Help_Kappa','es_Help_Variables','es_Help_Grid','es_Help_Pages','es_Help_Prev','es_Help_Read','es_Help_Forest','es_Help_Exact','es_Help_SE'],
 'ErrorRate':['erlHelp'], 'FitCheck':['fc_Help'], 'GaltonBoard':['gbHelp'], 'Norm3':['n3_Help'],
 'NormExplorer':['ne_HelpPages'], 'RankLab':['rk_Help'], 'ResampLab':['rs_Help'], 'RiskLab':['rl_Help'],
 'SampDist':['sd_showHelp'], 'ScatterLab':['slHelp'], 'ExhibitLab':['sz_Help'], 'StatDist':['st_show_help','st_ABHelp'], 'TDist3D':['tdHelp'],
 'StudRange':['sr_HelpMode'], 'SurvLab':['sv_Help'], 'TestChooser':['tcHelp'], 'TrendTest':['trHelp'], 'PowerViz':['pv_ShowHelp'], 'TTestLab':['tt_Help'], 'TTestLabG':['tz_Help'], 'DataLoad':['dd_Help'],
}
out = {}
MAIN={'NormExplorer':'NormExp()','PowerViz':'POWERVIZ()','TTestLab':'TTESTLAB()','TTestLabG':'TTESTLABG()','DataLoad':'DATALOAD()','Norm3':'Norm3(0,1,1.96)'}
class TO(Exception): pass
def alarm(*a): raise TO()
signal.signal(signal.SIGALRM, alarm)
for f in sorted(sys.argv[2:]):
    name = os.path.basename(f).split('_')[0]
    if name not in ROUT: continue
    pages = []
    for r in ROUT[name]:
        try:
            signal.alarm(90)
            h = Harness(f, idle_key=4, on_unverified='warn')
            try: h.execute(MAIN.get(name, name + '()'))
            except Exception as e: pass
            h.screens[:] = []
            for i in range(60): h.press(30)
            try:
                if name in ('AgreeLab','AnovaLab'):
                    for k in range(1, 10):
                        try: h.execute('%s(%d)' % (r, k))
                        except Exception as e: break
                else: h.call(r)
            except Exception as e: pages.append(['[call %s stopped: %s]' % (r, str(e)[:80])])
            signal.alarm(0)
            seen = set()
            for s in h.screens:
                ls = [l for l in s.lines() if l.strip()]
                key = '\n'.join(ls)
                if ls and key not in seen:
                    seen.add(key); pages.append(ls)
        except TO:
            pages.append(['[call %s timed out]' % r])
        except Exception as e:
            pages.append(['[load/call %s failed: %s]' % (r, str(e)[:80])])
    out[name] = pages
    print(name, len(pages), sum(len(p) for p in pages), flush=True)
json.dump(out, open(sys.argv[1],'w'), ensure_ascii=False, indent=1)
