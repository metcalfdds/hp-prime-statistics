# vc_back.py -- Esc until the Program Catalog stands alone (no menu, no returned line), then the highlight on StatDist
import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tools', 'vc_cloud_v1'))
import vcdrive as v  # noqa: E402
CAP = sys.argv[1]
for i in range(6):
    v.cap(CAP + 'back.png'); t = ' '.join(v.ocr(CAP + 'back.png').split())
    if t.startswith('Program Catalog') and 'Statistical' not in t and '"' not in t and 'P(X' not in t:
        break
    v.key('Esc'); time.sleep(1.2); v.settle()
print('back:', t[:80])
