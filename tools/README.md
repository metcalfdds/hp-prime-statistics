# Tools

Every program in this repository passes these checks before it is pasted onto a calculator. They are plain Python 3, and only `ppl_run_v3c.py` needs more (see below).

| File | What it does |
| --- | --- |
| `ppl_gate_v1a.py` | **The gate.** `python3 ppl_gate_v1a.py NEW.txt [ORIGINAL.txt]` runs the four checks below and the fleet name check, and prints PASS or the lines to look at. It uses hp-prime-kit's linter and interpreter if it can find them (JordiRigau/hp-prime-kit); without them those two steps are skipped. |
| `ppl_check_v3.py` | An error-code tally. E2 is block balance; E3 is more than six names on a LOCAL line; E6 is a LOCAL out of place; E8 is a lowercase exponent or `=` used for `==`; E10 is an INPUT into something that is not a variable; E11 is a name that is a built-in command, ignoring case, as the calculator does. Usage: `python3 ppl_check_v3.py whitelist.json,HP_Prime_Builtin_Names.txt FILE.txt`. |
| `lint_ppl.py` | Structural lint: block balance, LOCAL sizes, INPUT counts, the CHOOSE pattern, EXPORT discipline. Its "no function named <file>" and EXPORT-discipline lines are expected noise for most programs. |
| `fleet_names_v2.py` | **The shared-pool check.** All programs on a Prime share one pool of routine names, so two programs that both define `NiceNum` can run each other's. Run `python3 fleet_names_v2.py *.txt` over every program you install. It reports collisions, helpers without their program's tag, files that mix two tags, and helper names that are built-ins. |
| `HP_Prime_Builtin_Names.txt` | The built-in names the checks compare against. |
| `ppl_run_v3c.py` + `ppl_run_v3c_README.md` | **A run harness**: it runs a PPL program on the PC like a student at the keys. A script supplies keys, taps, drags, CHOOSE picks and INPUT answers. The statistics built-ins are backed by SciPy, and `CAS("...")` is answered by desktop Giac, the engine inside the Prime's CAS (`apt-get install xcas` gives `icas`). It records every screen drawn. It needs hp-prime-kit's interpreter, SciPy, and, for CAS calls, Giac. Since v3b and v3c it follows what the Prime's firmware did on the emulator: `CAS(variable)` comes back unevaluated, CAS answers are printed the Prime's way, soft-key taps under `WAIT(-1)` arrive as clicks, and the chi-square and F built-ins refuse a fractional df. Agreement in the harness is not agreement on the device, but it has caught real bugs before a paste. |

The checks are only as good as their rules, and those rules come from the device. When the calculator disagrees with a tool, the calculator wins, and the rule gets fixed and written into `docs/lessons-learned_v7h.md`.
