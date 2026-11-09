import sys
import os
sys.path.insert(0, os.environ.get('HPKIT', '/tmp/kit/hp-prime-kit-HEAD'))   # hp-prime-kit (CLAUDE.md: setting up a session)
from hpkit.numbers import read_hpmat
def read(path):
    return read_hpmat(open(path, 'rb').read())
if __name__ == '__main__':
    m = read(sys.argv[1]); print(type(m), len(m)); print(m[:3])
