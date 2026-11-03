# commas_config_r5.py -- round 5 (commas in big numbers): what commas_v1.py needs to know about each program.
#   helper  the program's comma routine (its own prefix: all programs share one pool of names on the calculator)
#   fmt     the program's number formatters: each call of one is wrapped where it is made
#   skip    routines left alone: the CAS's helpers, text surgery, width measures, CAS-text builders
#   casfam  the program's CAS routine(s): a statement that calls one, or builds text that reaches one, keeps STRING raw
#   anchor  the line number (in the base version) of the newest "what changed" entry: the new block goes above it
#   title   0 when the title line is itself the newest history entry (BurrLab): the new block carries the new title
#   edits   exact replacements after the wrapping (each must match once)
DATE = '2 Nov 2026, night'

CONFIG = {
    'AgreeLab': dict(lit_yes=['More than 1500'], old='beta 1b', new='beta 1c', helper='ag_Cm', anchor=52, title_date=('(28 Oct 2026)', '(' + DATE + ')'),
                     fmt=['ag_Fx'], skip=[], casfam=[],
        edits=[('ag_Init()\nBEGIN\n', '// ---- ag_TxDb: a line of text with d-bar in it (beta 1c) ----\n// The Prime\'s font has no d with a bar (SymProbe beta 1, 2 Nov 2026), so the\n// d is drawn and then a line above it: 3 px above the top of its text cell,\n// from its left edge to 2 px short of where the d ends (DbarProbe beta 1:\n// there the bar clears the d\'s stem in fonts 1 and 2 on the Virtual\n// Calculator; nearer, it runs into the stem).  Draws tbA, d-bar, then tbB in\n// font 1, within tbW px from tbX.\nag_TxDb(tbA, tbB, tbX, tbY, tbC, tbW)\nBEGIN\n  LOCAL tbE, tbD;\n  tbE := TEXTOUT_P(tbA, G1, tbX, tbY, 1, tbC, tbW);\n  tbD := TEXTOUT_P("d", G1, tbE, tbY, 1, tbC);\n  LINE_P(G1, tbE, tbY - 3, tbD - 2, tbY - 3, tbC);\n  TEXTOUT_P(tbB, G1, tbD, tbY, 1, tbC, MAX(1, tbX + tbW - tbD));\nEND;\n\nag_Init()\nBEGIN\n'), ('    ag_Tx("bias = mean d; limits of agreement = bias " + agPM, 10, 72, agGRN);', '    ag_TxDb("bias = ", "; limits of agreement = bias " + agPM, 10, 72, agGRN, 306);   // beta 1c: d-bar'), ('  ag_Tx("bias = mean d = " + ag_Gn(agBDb) + agYU + ", SD of d: s = " + ag_Gn(agBS), 4, 44, agGRN);', '  ag_TxDb("bias = ", " = " + ag_Cm(ag_Gn(agBDb)) + agYU + ", SD of d: s = " + ag_Cm(ag_Gn(agBS)), 4, 44, agGRN, 312);   // beta 1c: d-bar'), ],
        note='The Bland-Altman bias is d-bar, not "mean d": the font has no such letter, so ag_TxDb draws a d and a bar above it (DbarProbe beta 1).',
        r2_why='every Bland-Altman screen, where "bias = mean d" is now "bias = d̄" (the d drawn, then its bar)',
        checklist=['Bland-Altman page: "bias = d̄" with the bar above the d, clear of its stem, in both lines that show the bias.']),
    'AnovaLab': dict(old='beta 1a', new='beta 1b', helper='av_Cm', anchor=51,
                     title_date=('(21 Oct 2026; beta 1 the same day)', '(' + DATE + ')'), fmt=['av_Fx'], skip=[], casfam=[],
                     nowrap=['avOSrc', 'avTSrc', 'avBSrc', 'avOTtl', 'avTTtl', 'avBTtl']),
    'BayesTree': dict(old='beta 8f', new='beta 8g', helper='bt_Cm', anchor=26,
                      fmt=['bt_NumS', 'bt_Pct', 'bt_fmtc', 'bt_fmtp', 'bt_fmtB', 'bt_fmtq'],
                      skip=['bt_Cas', 'bt_Rep', 'bt_Strip', 'bt_IsFr', 'bt_Dig', 'bt_Wrap', 'bt_FrLn', 'bt_FrS'],
                      casfam=['bt_Cas'],
        edits=[('bt_FrLn(flA, flF, flD)\nBEGIN\n', 'bt_FrLn(flA, flF, flD)\nBEGIN\n  LOCAL flC;\n  // beta 8g: the exact fraction with its commas; a comma is 3 px, about half a\n  // character (CommaProbe beta 1), so in the length test it counts a half\n  flC := DIM(bt_Cm(flF)) - DIM(flF);\n  flF := bt_Cm(flF);\n'), ('  IF DIM(flA) + DIM(flF) + DIM(flD) + 3 <= 50 THEN', '  IF DIM(flA) + DIM(flF) - flC / 2 + DIM(flD) + 3 <= 50 THEN'), ('bt_FrS(fsL, fsF)\nBEGIN\n', 'bt_FrS(fsL, fsF)\nBEGIN\n  LOCAL fsC;\n  // beta 8g: the exact fraction with its commas; in the 18-character test a\n  // comma counts a half (3 px, CommaProbe beta 1)\n  fsC := DIM(bt_Cm(fsF)) - DIM(fsF);\n  fsF := bt_Cm(fsF);\n'), ('  IF DIM(fsL) + 3 + DIM(fsF) <= 18 THEN', '  IF DIM(fsL) + 3 + DIM(fsF) - fsC / 2 <= 18 THEN'), ('    xS := " = " + btXP;', '    xS := " = " + bt_Cm(btXP);   // beta 8g: commas in the exact fraction too'), ],
        note="The CAS's exact fractions get their commas too (999/3,863), before their length is tested (bt_FrLn, bt_FrS), and in the summary returned to Home.",
        r2_why='the tree\'s short panel, where an exact fraction that just fitted its 18 characters without a comma no longer does ("1−PPV = 604/242,875") and the panel gives its digit count instead ("1−PPV: 9 digits")'),
    'BiNorm3D': dict(old='beta 1b', new='beta 1c', helper='bnCm', anchor=31, fmt=['bnF', 'bnDeg'], skip=[], casfam=[]),
    'BurrLab': dict(old='beta 1i', new='beta 1j', helper='bu_Cm', anchor=17, title=0, fmt=['bu_Fx'],
                    skip=['bu_Cas'], casfam=['bu_Cas'],
        draw=['bu_Para']),
    'CICatcher': dict(old='beta 2e', new='beta 2f', helper='cqCm', anchor=46, fmt=['cqF', 'cqNumS', 'cqLvS', 'cqPct'],
                      skip=['cqCas'], casfam=['cqCas'],
        checklist=['Its exact (CAS) page with a number of 1,000 or more in the problem still shows the exact answer, not the decimal fallback (the random runs never reached that page).']),
    'CentralLimit': dict(lit_yes=['10 to 2000'], old='beta 3d', new='beta 3e', helper='cltCm', anchor=41, fmt=['cltF'],
                         skip=['cltCas', 'cltIVal', 'cltRepl', 'cltDigits'], casfam=['cltCas'],
        checklist=['Its exact (CAS) page with a number of 1,000 or more in the problem still shows the exact answer, not the decimal fallback (the random runs never reached that page).']),
    'ChiTable': dict(old='beta 3f', new='beta 3g', helper='csCm', anchor=42,
                     fmt=['csPStr', 'csAStr', 'csSgn', 'csEStr'],
                     skip=['csCas', 'csIsFr', 'csFrDig', 'csNoZero', 'csXPText', 'csXX2Txt'], casfam=['csCas'],
        edits=[('    TEXTOUT_P("Row " + STRING(moR, 2, 0), G1, moX + 2, csPB + 4, 1, #000000h, moW);', '    // beta 3g: "Row k" where its column has room (label_fit_v1 found "Row 3" cut to\n    // "R" in an 8 px column of beta 3f), the row number alone where only that fits\n    IF moW >= 30 THEN\n      TEXTOUT_P("Row " + csCm(STRING(moR, 2, 0)), G1, moX + 2, csPB + 4, 1, #000000h, moW);\n    ELSE\n      IF moW >= 9 THEN TEXTOUT_P(csCm(STRING(moR, 2, 0)), G1, moX + 2, csPB + 4, 1, #000000h, moW); END;\n    END;'), ('    TEXTOUT_P("N = " + STRING(csN, 2, 0), G1, gmXT + 4, gmYT + 9, 2, #FFFFFFh, 72);', '    TEXTOUT_P("N = " + csCm(STRING(csN, 2, 0)), G1, gmXT + 4, gmYT + 9, IFTE(csN >= 100000, 1, 2), #FFFFFFh, 72);   // beta 3g: font 1 from 100,000, so the commas fit'), ('    xpS := "p = " + csXFr + " " + xpD;\n    IF DIM(xpS) <= xpMax THEN RETURN xpS; END;', '    // beta 3g: the exact fraction with its commas; in the length test a comma\n    // counts a half (3 px, CommaProbe beta 1)\n    xpS := "p = " + csCm(csXFr) + " " + xpD;\n    IF DIM(xpS) - (DIM(csCm(csXFr)) - DIM(csXFr)) / 2 <= xpMax THEN RETURN xpS; END;'), ('    xtS := "= " + csXX2 + " = " + STRING(ROUND(csX2, 3), 2, 3);\n    IF DIM(xtS) <= xtMax THEN RETURN xtS; END;', '    // beta 3g: commas; in the length test a comma counts a half (3 px)\n    xtS := "= " + csCm(csXX2) + " = " + csCm(STRING(ROUND(csX2, 3), 2, 3));\n    IF DIM(xtS) - (DIM(xtS) - DIM("= " + csXX2 + " = " + STRING(ROUND(csX2, 3), 2, 3))) / 2 <= xtMax THEN RETURN xtS; END;'), ('    RETURN "= " + STRING(ROUND(csX2, 3), 2, 3) + " (" + STRING(csFrDig(csXX2), 2, 0) + "-digit fraction)";', '    RETURN "= " + csCm(STRING(ROUND(csX2, 3), 2, 3)) + " (" + STRING(csFrDig(csXX2), 2, 0) + "-digit fraction)";'), ('  RETURN "= " + STRING(ROUND(csX2, 3), 2, 3);\nEND;', '  RETURN "= " + csCm(STRING(ROUND(csX2, 3), 2, 3));\nEND;')],
        note='The mosaic plot writes "Row k" only where its column has room, else the row number alone (label_fit_v1 found "Row 3" cut to "R" in beta 3f), N from 100,000 is in the small font, so its commas fit, and the exact fractions of Fisher\'s p and the chi-square get their commas before their length is tested (csXPText, csXX2Txt).',
        checklist=['Its exact (CAS) page with a number of 1,000 or more in the problem still shows the exact answer, not the decimal fallback (the random runs never reached that page).']),
    'DNAMixLR': dict(old='beta 3e', new='beta 3f', helper='dmCm', anchor=38, fmt=['dmF', 'dmBig', 'dmThS', 'dmPStr'],
                     skip=['dmCas', 'dmRepl', 'dmCom'], casfam=['dmCas'],
        checklist=['Its exact (CAS) page with a number of 1,000 or more in the problem still shows the exact answer, not the decimal fallback (the random runs never reached that page).']),
    'DataLoad': dict(old='beta 1b', new='beta 1c', helper='dd_Cm', anchor=21, fmt=['dd_Fx', 'dd_Num'],
                     skip=['dd_Names', 'dd_Span'], casfam=[]),
    'EpiStats': dict(lit_yes=['N > 2000'], old='v1.7e', new='v1.7f', helper='es_Cm', anchor=31,
                     fmt=['es_PTxt', 'es_SigTxt', 'es_FmtNum', 'es_FmtPct', 'es_FmtCI', 'es_Sgn', 'es_Cnt', 'es_PctTxt'],
                     skip=['es_Cas', 'es_XCas'], casfam=['es_Cas', 'es_XCas'],
        edits=[('    TEXTOUT_P(grS, G1, grXT + 5, grYT + 9, 2, #FFFFFFh, esGTW - 7);', '    TEXTOUT_P(grS, G1, grXT + 5, grYT + 9, IFTE(esMod <> 7 AND DIM(grS) > 10, 1, 2), #FFFFFFh, esGTW - 7);   // v1.7f: a long N in the small font, so its commas fit')],
        note="The table's N goes to the small font when it is longer than 10 characters, so its commas fit."),
    'ErrorRate': dict(old='beta 1e', new='beta 1f', helper='erlCm', anchor=46,
                      fmt=['erlFix', 'erlPctS', 'erlRateS', 'erlAlFmt', 'erlLvS'],
                      skip=['erlRepl', 'erlCas', 'erlTrCas', 'erlComma'], casfam=['erlCas', 'erlTrCas'],
        edits=[('  awW := 44 - DIM(awP);\n', "  awW := 44 - DIM(awP);\n  // beta 1f: the exact answer with its commas when it still fits on one\n  // line; a longer one keeps none, so it takes no more lines than before\n  // (beta 1d's E1: a wrapped answer pushed the page's last line out)\n  IF DIM(erlCm(awS)) <= awW THEN awS := erlCm(awS); END;\n"), ('      TEXTOUT_P(sdS, G1, sdX + IP(sdBw / 2) - 3 * DIM(sdS), sdPB + 3, 1, erlGRAY, 30);\n', '      // beta 1f: 36 px, not 30: "1,000+" with its comma is 33 px (a comma 3, a digit 6; CommaProbe)\n      TEXTOUT_P(sdS, G1, sdX + IP(sdBw / 2) - 3 * DIM(sdS), sdPB + 3, 1, erlGRAY, 36);\n')],
        note='The CAS\'s exact answers on the Exact and approximate page ("1-(999,999/1,000,000)^N") get their commas when the answer still fits on its line; one that would then need a second line keeps none, so the page never needs more than its 14 lines (beta 1d, E1). The simulation\'s bar labels may be 36 px wide, not 30, so \"1,000+\" with its comma is not cut.',
        checklist=['Exact and approximate page at RMP 1 in a million: "P(1 or more) = 1-(999,999/1,000,000)^N" on one line, and the page\'s last line, "RMP values are illustrative, not casework.", still shown.']),
    'FitCheck': dict(old='beta 1a', new='beta 1b', helper='fc_Cm', anchor=18, title_date=('(21 Oct 2026)', '(' + DATE + ')'),
                     fmt=['fc_F', 'fc_I', 'fc_Sgn'], skip=[], casfam=[]),
    'GaltonBoard': dict(old='beta 3f', new='beta 3g', helper='gbCm', anchor=41, fmt=['gbF', 'gbMuS'],
                        skip=['gbCas', 'gbIsFr', 'gbFrDig', 'gbIVal', 'gbPsLim', 'gbKfmt'], casfam=['gbCas'],
        edits=[('      bkS := gbKfmt(gbCnt(bkK + 1));', "      bkS := gbKfmt(gbCnt(bkK + 1));\n      // beta 3g: a bar wide enough shows the whole count with its comma\n      // (1,093, not 1.0k); gbKfmt's short form stays for narrow bars and pegs\n      IF gbBw >= 34 AND gbCnt(bkK + 1) >= 1000 THEN bkS := gbCm(STRING(gbCnt(bkK + 1), 2, 0)); END;")],
        note='A bar 34 px or wider shows its whole count with its comma (1,093) instead of the short form (1.0k), which stays for narrow bars and the peg counts.',
        key_funcs=['gbPsKey'],
        vc_extra=' A hand trial followed: "Drop 1,000 balls (fast)" from the menu showed "n = 1,000"; "Fill to 5,000 (MicroPython)" showed "n = 5,000" and the footer "engine: PPL (5,000 cap), 4,000 balls in 88 ms: board full"; the opening page\'s "After Galton (1873)" kept its year without a comma; the summary returned to Home read "Galton Board: 5,000 balls, R = 8, p = 0.50".'),
    'Norm3': dict(old='v2.4d', new='v2.4e', helper='n3_Cm', anchor=26, fmt=['n3_fmtp', 'n3_Fx'], skip=['n3_YWd'], casfam=[]),
    'NormExplorer': dict(old='beta 42e', new='beta 42f', helper='ne_Cm', anchor=99, fmt=['ne_Fx'], skip=['ne_YWd'], casfam=[]),
    'PowerViz': dict(old='v2.5l', new='v2.5m', helper='pv_Cm', anchor=35,
                     fmt=['pv_NStr', 'pv_NumD', 'pv_NumS', 'pv_FMT', 'pv_FMTP', 'pv_BetaS', 'pv_N80S', 'pv_TObt', 'pv_IStr', 'pv_NCFS'],
                     skip=['pv_Cas', 'pv_Rep', 'pv_Strip', 'pv_CasUse', 'pv_Wrap', 'pv_Fit'], casfam=['pv_Cas'],
        exempt_r={5014: 'a tap at the left edge of the n80 readout: its tap box starts where its text does, and "n80 = 1,392 (1,391.1)" with its commas starts at x 199, not 210, so the tap that missed it in v2.5l opens "Where n comes from"'},
        r2_why='the SE line, which gives way to its short form ("SE₀ = σ√(2/n) = 1.84") when it would reach the n₈₀ readout beside it: that readout now carries its commas ("n₈₀ = 1,392") and starts further left, and the SE line is measured with its own commas'),
    'RankLab': dict(old='beta 1b', new='beta 1c', helper='rk_Cm', anchor=59, title_date=('(28 Oct 2026)', '(' + DATE + ')'),
                    fmt=['rk_Fx', 'rk_Sg', 'rk_Num'], skip=[], casfam=[]),
    'ResampLab': dict(lit_no=['x1000'], old='beta 1c', new='beta 1d', helper='rs_Cm', anchor=47, title_date=('(28 Oct 2026)', '(' + DATE + ')'),
                      fmt=['rs_Fmt', 'rs_FmtS', 'rs_PStr', 'rs_PEq'], skip=['rs_Int', 'rs_Big', 'rs_PFr'], casfam=[],
        edits=[('rs_Drain()\nBEGIN\n', '// ---- rs_TxDb: a line of text with d-bar in it (beta 1d) ----\n// The Prime\'s font has no d with a bar (SymProbe beta 1, 2 Nov 2026), so the\n// d is drawn and then a line above it: 3 px above the top of its text cell,\n// from its left edge to 2 px short of where the d ends (DbarProbe beta 1:\n// there the bar clears the d\'s stem in fonts 1 and 2 on the Virtual\n// Calculator; nearer, it runs into the stem).  Draws tbA, d-bar, then tbB in\n// font 1, within tbW px from tbX.\nrs_TxDb(tbA, tbB, tbX, tbY, tbC, tbW)\nBEGIN\n  LOCAL tbE, tbD;\n  tbE := TEXTOUT_P(tbA, G1, tbX, tbY, 1, tbC, tbW);\n  tbD := TEXTOUT_P("d", G1, tbE, tbY, 1, tbC);\n  LINE_P(G1, tbE, tbY - 3, tbD - 2, tbY - 3, tbC);\n  TEXTOUT_P(tbB, G1, tbD, tbY, 1, tbC, MAX(1, tbX + tbW - tbD));\nEND;\n\nrs_Drain()\nBEGIN\n'), ('    TEXTOUT_P("observed " + dsN + " = " + rs_FmtS(rsObs, rsDec) + ",  Ha: " + rs_HaTxt(), G1, 4, dsY, 1, rsRED, 312);', '    IF rsMode == 2 THEN\n      // beta 1d: the paired test\'s statistic is d-bar, drawn (rs_TxDb), not "mean d"\n      rs_TxDb("observed ", " = " + rs_Cm(rs_FmtS(rsObs, rsDec)) + ",  Ha: " + rs_HaTxt(), 4, dsY, rsRED, 312);\n    ELSE\n      TEXTOUT_P("observed " + rs_Cm(dsN) + " = " + rs_Cm(rs_FmtS(rsObs, rsDec)) + ",  Ha: " + rs_HaTxt(), G1, 4, dsY, 1, rsRED, 312);\n    END;'),],
        note='The paired test\'s observed statistic is d-bar, not "mean d": the font has no such letter, so rs_TxDb draws a d and a bar above it (DbarProbe beta 1).',
        draw=['rs_Para'],
        r2_why='every paired-test screen, where "observed mean d" is now "observed d̄" (the d drawn, then its bar); nothing else',
        checklist=['Paired permutation test: "observed d̄ = …" with the bar above the d, clear of its stem.', 'x1000 on the paired test takes about as long as beta 1c did (the harness ran it slower; the calculator should not).']),
    'RiskLab': dict(lit_yes=['At most 2000', 'up to 2000'], old='beta 1b', new='beta 1c', helper='rl_Cm', anchor=45, title_date=('(28 Oct 2026)', '(' + DATE + ')'),
                    fmt=['rl_F', 'rl_I', 'rl_Sg'], skip=[], casfam=[]),
    'SampDist': dict(lit_yes=['on to 1600', 'n = 1600'], old='v2.3e', new='v2.3f', helper='sd_Cm', anchor=35, fmt=['sd_fmtp'], skip=[], casfam=[],
        r2_why='axis labels that, with their commas, would touch the label beside them and are left out by the program\'s own rule ("1,000,040", "−100,000", "12,000"; the tick stays), and one help line that gives its short form ("σ = 2.00;  σx̄ = 0.0020") when "a mean of 999,999" no longer fits'),
    'ScatterLab': dict(old='beta 2f', new='beta 2g', helper='slCm', anchor=33, fmt=['slSig', 'slFx', 'slNum'],
                       skip=['slCas', 'slRatNote', 'slRepl', 'slFitN', 'slFitT', 'slLab', 'slLabNote', 'slCxClean', 'slCxSol',
                             'slMeas'], casfam=['slCas'],
                       edits=[('IF lbK == 0 THEN RETURN slFx(lbV, lbD); END;', 'IF lbK == 0 THEN RETURN slCm(slFx(lbV, lbD)); END;'),
                              ('  RETURN STRING(lbR, 2, 0);\nEND;', '  RETURN slCm(STRING(lbR, 2, 0));\nEND;'),
                              ('fnT := fnP + slSig(fnV) + fnS;', 'fnT := fnP + slCm(slSig(fnV)) + fnS;'),
                              ('RETURN lnA + " = " + slFx(lnO, MAX(0, -lnE)) + " + label" + lnU;',
                               'RETURN lnA + " = " + slCm(slFx(lnO, MAX(0, -lnE))) + " + label" + lnU;'), ],
                       note='The axis labels, the note at an axis and the side panel group their numbers before they '
                            'measure them (slLab, slLabNote, slFitN).',
        r2_why='an axis whose labels with their commas ("400,000", "800,000") are too long for the margin, labelled in units instead ("2", "4", ×1ᴇ5), as the program does for any long label'),
    'SeizureLab': dict(old='beta 1b', new='beta 1c', helper='sz_Cm', anchor=50, title_date=('(28 Oct 2026)', '(' + DATE + ')'),
                       fmt=['sz_I', 'sz_F'], skip=[], casfam=[],
        edits=[('      TEXTOUT_P(sz_I(tpN(tpI)), G1, tpX - 8, szPB + 3, 1, szGRAY, 30);', '      TEXTOUT_P(sz_Cm(sz_I(tpN(tpI))), G1, tpX - 8 - IFTE(tpN(tpI) >= 1000, 4, 0), szPB + 3, 1, szGRAY, 30);   // beta 1c: "1,000" is a character longer: 4 px left, clear of the infinity sign')],
        note='The x label "1,000", a character longer with its comma, sits 4 px further left, clear of the infinity sign beside it.'),
    'StatDist': dict(old='v2.7h', new='v2.7i', helper='st_Cm', anchor=38, fmt=['st_fmtp', 'st_fmtx', 'st_XStr'],
                     skip=['st_Cas', 'st_IVal', 'st_Repl', 'st_Digits', 'st_LWd', 'st_FmGood', 'st_FmSub'], casfam=['st_Cas'],
        edits=[('      IF dwX >= dwR + 3 AND dwX + st_LWd(dwS) <= 322 THEN', '      IF dwX >= dwR + 3 AND dwX + st_LWd(dwS) <= IFTE(INSTRING(dwS, ",") > 0, 320, 322) THEN   // v2.7i: a label with a comma keeps to the screen'), ],
        note="An x label with a comma in it keeps to the screen's 320 px (12,000 at x 288 ran 1 px past it), and the formula page's exact fractions get their commas (st_FmWrap, st_FmAdd).",
        draw=['st_FmAdd', 'st_FmWrap'],
        r2_why='axis labels: with their commas fewer fit, so the program shows every other one ("400,000,000,000" and "800,000,000,000" where v2.7h showed "200000000000" and "600000000000"), or leaves out one that would touch its neighbour or the screen\'s edge ("12,000", "3,000"; the tick stays)'),
    'StudRange': dict(old='beta 15f', new='beta 15g', helper='sr_Cm', anchor=62, fmt=['sr_FmtF', 'sr_FmtP'], skip=[],
                      casfam=[]),
    'SurvLab': dict(old='beta 1b', new='beta 1c', helper='sv_Cm', anchor=43, title_date=('(28 Oct 2026)', '(' + DATE + ')'),
                    fmt=['sv_F', 'sv_I', 'sv_Sg', 'sv_TS'], skip=[], casfam=[]),
    'TTestLabG': dict(old='beta 1a', new='beta 1b', helper='tz_Cm', anchor=20,
                      fmt=['tz_Fmt', 'tz_FmtP', 'tz_FixD', 'tz_Num', 'tz_Sig'], skip=[], casfam=[]),
    'TTestLab': dict(old='beta 1c', new='beta 1d', helper='tt_Cm', anchor=21,
                     fmt=['tt_Fmt', 'tt_FmtP', 'tt_FixD', 'tt_Num', 'tt_Sig'], skip=[], casfam=[]),
    'TestChooser': dict(old='beta 2c', new='beta 2d', helper='tcCm', anchor=35, fmt=[], skip=[], casfam=[]),
    'TrendTest': dict(old='beta 3g', new='beta 3h', helper='trCm', anchor=32, fmt=['trFx', 'trPStr', 'trOrStr', 'trXStr', 'trNum'],
                      skip=['trCas', 'trRatNote', 'trRepl', 'trCxClean', 'trCxSol'], casfam=['trCas']),
}


def HISTORY(name, c, n_fmt, n_str):
    """the program's new "what changed" block, as comment lines"""
    first = ('// %s - %s  (%s) -- commas in big numbers.' % (name, c['new'], DATE)) if c.get('title', 1) == 0 else \
            ('// %s (%s): commas in big numbers.' % (c['new'], DATE))
    body = ('Roger, 2 Nov 2026: "always put comma delimiters in big numbers".  STRING never groups digits, whatever '
            'Home\'s setting, so a new routine, %s, puts a comma every three digits into each run of four or more '
            'digits that does not follow a decimal point: 1234567.25 shows as 1,234,567.25; decimals, exponents, '
            'years in the help text and anything the CAS reads are left alone.  %d calls of the number formatters and '
            '%d of STRING go through it where they are made, so a number is measured as it is drawn.'
            % (c['helper'], n_fmt, n_str))
    body += (' ' + c['note']) if c.get('note') else ''
    body += ' Otherwise it runs as %s did: the verify script runs both versions side by side and they take the ' \
            'same path, screen for screen (any text that differs beyond its commas is counted there, and the ' \
            'change note says why).  Harness only so far.' % c['old']
    words, lines, cur = body.split(' '), [], ''
    for w in words:
        if len(cur) + len(w) + 1 > 70:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + ' ' + w) if cur else w
    lines.append(cur)
    return first + '\n' + '\n'.join('//   ' + x for x in lines) + '\n//\n'
