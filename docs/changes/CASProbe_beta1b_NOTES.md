# CASProbe beta 1b: notes

*Roger Metcalf, 2026. Written with AI assistance (Anthropic Claude). 17 October 2026.*

**Beta 1b supersedes beta 1a.** Read `CASProbe_beta1a_NOTES.md` for the test list; every test keeps its number. Only the call form changes.

## Why

Beta 1a ran on the HP Prime Virtual Calculator 2.4.2 (build 2026-09-09) on 17 October 2026. It reported **"CAS available: no"** and skipped T11–T41. The CAS was working; the probe's yardstick was wrong:

| Test | What happened |
|---|---|
| T04 `CAS(comb(100,50))` written in the program | Evaluated, but crossed into Home as the real 1.00891344546E29 |
| T06 `CAS(s)`, s a LOCAL string | **Handed the text back unevaluated**: `"comb(100,50)"` |
| T07 the fleet's `xxCas` as written | The same: unevaluated |
| T08 `EXPR("CAS(" + q + s + q + ")")` | **Evaluated**, but crossed back as the 12-digit real |
| T09 `EXPR("CAS.eval(" + q + s + q + ")")` | The same |

Typed by hand in Home on the emulator:

| Expression | Answer |
|---|---|
| `STRING(EXPR("CAS(\"comb(8,4)/2^8\")"))` | `35/128` |
| `TYPE(EXPR("CAS(\"comb(8,4)/2^8\")"))` | 8 |
| `EXPR("CAS(\"string(comb(100,50))\")")` | `100891344545564193334812497256`, all 30 digits |
| `STRING(EXPR("CAS(\"factor(6*cft^2+7*cft+2)\")"))` | `(2*cft+1)*(3*cft+2)` |

**So:** the CAS works from a program only through text that EXPR reads, and a big integer survives only if the CAS turns it into a string first.

## What beta 1b changes

- T06–T09 ask for `string(comb(100,50))`.
- `cxCall` forms 2 and 3 wrap every CAS text in `string(...)`. T11–T41 now run through that form, which is the one the fleet would use.
- `cxObj` (T12's TYPE test) is unchanged, so it still reports the natural type of an unwrapped answer.
- Version strings, the header, and the advice lines in `cxPickForm`.

**Gate:** `ppl_gate_v1a` PASS. The harness (`ppl_run_v3a`) does **not** yet model the two emulator facts above: it evaluates `CAS(s)` from a variable, and it keeps big integers exact. Until it does, a harness pass on CAS code proves less than it seems.

## What it means for round 2 (provisional until beta 1b runs)

Every round-2 program's `xxCas` must change from

```
cR := STRING(CAS(xxS));
```

to

```
cR := STRING(EXPR("CAS(" + CHAR(34) + "string(" + xxS + ")" + CHAR(34) + ")"));
```

and keep the quote-stripping that follows. The rest of the CAS kit (xxIStr, the undef/"rror" check, the decimal fallback, the check against the program's own numbers) stays. As written, the round-2 `xxCas` would hand back its own input text. The cross-check against the program's numbers should catch that and fall back to decimals, but the CAS page would never show.
