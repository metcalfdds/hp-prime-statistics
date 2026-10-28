# ResampLab beta 1b (26 Oct 2026)

One change from beta 1a: the plotting routine `rs_PX` is renamed `rs_Pix` (23 places). The Prime reads names without regard to case, so `rs_PX` and the Home export `RS_PX` were one name: a possible syntax error on paste, or a wrong call at run time. A case-insensitive scan of every routine, EXPORT and file-level LOCAL name in the fleet found it (the same scan found RiskLab beta 1's `rl_HL` / `RL_HL`); the gate and the harness do not catch this. Nothing else changed.

Checks: gate PASS against beta 1a; `verify_ResampLab_beta1b.py` (beta 1a's script pointed at beta 1b, header check updated): 767 checks, 0 failures; the case scan finds no pair. The device checklist is beta 1a's (`ResampLab_beta1a_NOTES.md`). Not run on a calculator.
