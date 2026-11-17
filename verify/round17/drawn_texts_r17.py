# -*- coding: utf-8 -*-
"""drawn_texts_r17.py WALKDIR -- the texts the generic walks drew, without the walks (17 Nov 2026).
A walk as tools/text_overlap_v1.py --json writes it holds every screen with every item's place; the 31 walks of round 17
come to 381 MB (GaltonBoard's alone is 350 MB), which is no file for a repository.  tools/screen_text_v1.py needs only
the distinct texts.  For each WALKDIR/<stem>.json this script writes verify/round17/drawn/<stem>.texts.json: the sorted
list of the distinct texts that walk drew.  screen_text_v1.py --walk reads either kind of file.
records_r17.py runs this script after its walks; run by hand from the repository's root."""
import glob, io, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, 'drawn'); os.makedirs(OUT, exist_ok=True)
n = total = 0
for p in sorted(glob.glob(os.path.join(sys.argv[1], '*.json'))):
    d = json.load(open(p)); texts = set()
    for raw in d['raw'].values():
        for scr in raw['screens'].values():
            for it in scr[2]['items']:
                if 'text' in it:
                    texts.add(str(it['text']))
    stem = os.path.basename(p)[:-5]
    io.open(os.path.join(OUT, stem + '.texts.json'), 'w', encoding='utf-8').write(json.dumps(sorted(texts), ensure_ascii=False, indent=0) + '\n')
    n += 1; total += len(texts)
print('drawn/: %d programs, %d distinct drawn texts' % (n, total))
