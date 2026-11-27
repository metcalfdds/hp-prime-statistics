# The book's Draft 106: no Appendix G here (26 November 2026, evening)

The book *Statisticles* was refocused in its Draft 106 (Roger, 26 November 2026, 18:27: the book should "1) illustrate concepts to beginning students and 2) demonstrate things the HP Prime can do", and "I think we need to delete a lot of content"). Its Appendix G, "Just for fun: Sudoku, and the statistics hiding in it", went to the book's website archive, and its Appendix F, "For HP programmers", came to this repository (Roger: "The programming part can go to GitHub and a future website"). Step 7 of his plan: everything here that named Appendix G is changed, and Sudoku stays a bonus on the Loader.

| Script | What it does |
|---|---|
| `make_v2q_v1.py` | Makes, by exact replacements from PR 35's files, `tools/make_starter_pack_v6.py`, starter pack v27 (v26 with READ_ME_FIRST.txt changed in its first line and one sentence; the other 35 files byte for byte), `starter-pack/README.md`, `prime-loader/build_loader_v2q.py`, `loader_template_v2q.html` and `tests/test_loader_v2q.js`, and removes the v5, v26 and v2p files they replace. |
| `docs_d106_v1.py` | The pages: `README.md`, `CLAUDE.md`, `extras/README.md`, `extras/sudoku/README.md`, `prime-loader/README.md` and `usb/README.md`, `tools/README.md`, `docs/test-status.md` and `docs/README.md`. It stops unless the Loader's test (173 PASS, 0 FAIL) and the pages' accessibility check (32 PASS, 0 FAIL) have passed on v2q. |

The order, from the repository's top folder:

```
python3 verify/refocus_d106/make_v2q_v1.py
cd prime-loader && python3 build_loader_v2q.py ../starter-pack/HP_Prime_Statistics_Starter_Pack_v27.zip --kit PATH_TO_hp-prime-kit
node tests/test_loader_v2q.js PrimeLoader_v2q.html ../starter-pack/HP_Prime_Statistics_Starter_Pack_v27.zip > tests/test_loader_v2q_output.txt
cd .. && node tools/pages_a11y_v1.js > tools/pages_a11y_v1_output.txt      # needs axe-core
python3 verify/refocus_d106/docs_d106_v1.py
```

`docs/book/` (Draft 105's Appendix F, as Draft 105 printed it, with its references and its one figure) was written from the book's website archive (`book/website_archive/appF_for_HP_programmers_D105.md` in the book's source); the three cartoons beside it in the source were never printed, because the book leaves cartoons out, and are not copied.

The Loader v2q has not been sent to a calculator; its cable code is v2p's, unchanged.
