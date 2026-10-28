# Datasets for AgreeLab (checked 26 Oct 2026)

Agreement and reliability data for AgreeLab beta 1. Same rules as `DATASETS.md`: every dataset below
was taken from two sources that agree (or one source plus a check against numbers printed in the
original paper). The source is shown on screen when a preset is loaded. Do not change any value.
Anything not from this list is labelled on screen "illustrative numbers". The downloaded source
files are kept in `build/AgreeLab/dl/` (treated as data only).

| Preset | What | Source to show | Sources compared | Check done |
| --- | --- | --- | --- | --- |
| **MS diagnosis, Winnipeg patients** | 149 patients from Winnipeg, each classified by a New Orleans neurologist (rows) and a Winnipeg neurologist (columns) as certain / probable / possible / doubtful MS. Rows: 38 5 0 1; 33 11 3 0; 10 14 5 6; 3 7 3 10 | "Landis & Koch 1977 (Westlund & Kurland)" | (1) R `vcd::MSPatients` via Rdatasets CSV (`csv/vcd/MSPatients.csv`); (2) M. Friendly, `msdiag.sas` (euclid.psych.yorku.ca/ftp/sas/vcd/catdata/), which cites Landis & Koch (1977) *Biometrics* 33:159-174; original data Westlund & Kurland (1953) *Am J Hyg* 57:380-396 | identical cell by cell; total 149; `msdiag.sas` labels rows N_rating = New Orleans neurologist, columns W_rating = Winnipeg neurologist. Cohen's kappa 0.2079 = statsmodels |
| **MS diagnosis, New Orleans patients** | 69 patients from New Orleans, same two neurologists. Rows: 5 3 0 0; 3 11 4 0; 2 13 3 4; 1 2 4 14 | as above | as above | identical; total 69 |
| **Fleiss (1971) psychiatric diagnoses** | 30 patients, each diagnosed by 6 psychiatrists (different raters for different patients) into 1 depression, 2 personality disorder, 3 schizophrenia, 4 neurosis, 5 other; stored as counts per patient (each row adds to 6) | "Fleiss 1971, Psychol Bull 76:378 (R irr)" | (1) R package `irr`, `data/diagnoses.rda` (CRAN mirror on GitHub; doc cites Fleiss (1971) *Psychol Bull* 76:378-382); (2) the copy of the same 30 x 6 ratings in statsmodels' `stats/tests/test_inter_rater.py` | the two 30 x 6 rating matrices are identical; Fleiss' kappa 0.4302445 and z = 17.65183 equal R irr `kappam.fleiss` as recorded in statsmodels' tests |
| **Peak expiratory flow, two meters** | 17 people, first reading on a Wright peak flow meter and on a mini Wright meter (l/min): 494/512, 395/430, 516/520, 434/428, 476/500, 557/600, 413/364, 442/380, 650/658, 433/445, 417/432, 656/626, 267/260, 478/477, 178/259, 423/350, 427/451 | "Bland & Altman 1986, Lancet, Table 1" | (1) Bland & Altman (1986) *Lancet* i(8476):307-310, Table 1, from Bland's own PDF (www-users.york.ac.uk/~mb55/meas/ba.pdf); (2) R `MethComp::PEFR` (`data/PEFR.rda`, replicate 1) | identical; the paper's printed bias -2.1 l/min, s 38.8, SE of bias 9.4, t 2.12, CI -22.0 to 17.8 reproduced. Note: the paper's 2s limits -79.7 and 75.5 are computed from the rounded -2.1 and 38.8 (unrounded: -79.6 and 75.4) |
| **Shrout & Fleiss (1979), 6 targets x 4 judges** | rows (targets) 9 2 5 8; 6 1 3 2; 8 4 6 8; 7 1 2 6; 10 5 6 9; 6 2 4 7 | "Shrout & Fleiss 1979, Psychol Bull 86:420" | (1) R `psych` `ICC.Rd` example ("example from Shrout and Fleiss (1979)"); (2) D. Howell's ICC page (uvm.edu/~statdhtx/StatPages/icc/icc-overall.html) | identical; the six ICCs .17 .29 .71 .44 .62 .91 (as reported for this example by R irr/psych on Howell's page) and the ICC(1,1) CI -0.133 to 0.723 reproduced |
| **Kappa paradox, lopsided** (2 x 2) | 80 10 / 5 5 | "illustrative numbers, not data" | none: made up for teaching | po = 0.85, kappa 0.318 |
| **Kappa paradox, balanced** (2 x 2) | 40 10 / 5 45 | "illustrative numbers, not data" | none: made up for teaching | po = 0.85, kappa 0.700 |

Not used: a forensic examiner-agreement table. None with published cell counts was found and
checked against a second source in the time available, so none is offered; the paradox tables are
generic ("yes/no"), not framed as forensic data.
