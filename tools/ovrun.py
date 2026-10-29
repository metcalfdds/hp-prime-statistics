#!/usr/bin/env python3
"""ovrun.py verify.py -- run a verify script under the overlap recorder in-process and print the
compact listing (no JSON on disk: for the very large runs)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import text_overlap_v1 as T, ovlib
err, secs = T.run_script(sys.argv[1], '/dev/null')
rep = T.report()
if err: print('driver error:', err)
ovlib.listing(rep)
