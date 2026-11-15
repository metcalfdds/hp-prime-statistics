# A printed book of tables as one more reference (15 November 2026)

The book is Zwillinger and Kokoska, *CRC Standard Probability and Statistics Tables and Formulae* (Chapman & Hall/CRC, 2000). Its tables were recomputed, 39,164 printed values in 57 tables, for two reasons: to have one more reference for the fleet's arithmetic that owes nothing to SciPy's authors or to us, and to see how far a printed table can be trusted. The findings are in [`docs/dev/crc-table-check-2026-11-15.md`](../../docs/dev/crc-table-check-2026-11-15.md).

None of the book's text is here. The scripts read the reader's own copy.

## To run it again

```
pip install scipy pymupdf pillow
mkdir -p work
pdftotext -layout YOUR_COPY.pdf work/all.txt          # one page per form feed; page numbers are the PDF's
cd tools
python3 crc_check_v1.py ../work/all.txt ../work/part1.json     # normal, t, chi-square
python3 crc_check_v2.py ../work/all.txt ../work/part2.json     # F, binomial, Poisson
python3 crc_check_v3.py YOUR_COPY.pdf ../work/part3.json       # studentized range (sideways pages, read with PyMuPDF)
python3 crc_check_v4.py ../work/all.txt ../work/part4.json     # Mann-Whitney probabilities
python3 crc_check_v5.py; python3 crc_check_v6.py; python3 crc_check_v7.py; python3 crc_check_v8.py
python3 crc_bartlett_v1.py table; python3 crc_dunnett2_v1.py; python3 crc_finney_v1.py
python3 crc_orthpoly_v1.py; python3 crc_spearman_v1.py
python3 crc_summary_v1.py          # work/summary.json and the list of tables
python3 crc_model_v1.py            # work/model.json: Poisson and negative binomial fits, the intervals
```

`crc_check_v8.py duncan` takes about ten minutes (SciPy's studentized range). `crc_spearman_mc.py 1000 20 11` and `2000 30 12` are the two simulations (one and two billion permutations). `crop.py` renders part of a page for a look at a flagged cell (set `CRC_PDF`).

Our own routines beside the book (set `HPKIT` as in `CLAUDE.md`):

```
python3 crc_studrange_ours.py REPO ../work/part3.json ../work/part3_ours.json     # StudRange's sr_SRCrit through the harness, about an hour
python3 crc_ranklab_ours.py REPO ../work/part4.json                              # RankLab's rk_MWNull on the probability table
python3 crc_ours_v2.py REPO ranklab                                              # rk_SRNull, rk_KdNull, rk_SpPerm, rk_MWNull
python3 crc_ours_v2.py REPO hpstats                                              # hpstats.py: Clopper-Pearson and the studentized range (slow)
```

## What is kept here

- `tools/`: the scripts, as they were run.
- `work/summary.json`: each table with its pages, the values read, the values off by one in the last place, the values wrong by more, and a note; wrong values page by page.
- `work/model.json`: the fits and intervals of the error model.

The page parsers are written for this book's text layer and nothing else. A printed value counts as right if it is the true value rounded to the places printed, as off by one if it misses by one unit in the last place, and as wrong otherwise.

Nothing here was run on a calculator. The harness is a PC model.
