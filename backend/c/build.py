import os
import platform
import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parent
include_dir = root / 'include'
src_dir = root / 'src'
build_dir = root / 'build'

build_dir.mkdir(exist_ok=True)

if platform.system() == 'Windows':
    compiler = 'cl.exe'
    output = build_dir / 'riskengine.dll'
    command = [
        compiler,
        '/nologo',
        '/O2',
        '/I', str(include_dir),
        '/LD',
        '/Fe:' + str(output),
        str(src_dir / 'risk_engine.c'),
    ]
else:
    compiler = 'gcc'
    output = build_dir / 'libriskengine.so'
    command = [
        compiler,
        '-O2',
        '-fPIC',
        '-shared',
        '-I', str(include_dir),
        '-o', str(output),
        str(src_dir / 'risk_engine.c'),
    ]

print('Running C build command:')
print(' '.join(command))

result = subprocess.run(command, cwd=str(root))
if result.returncode != 0:
    print('C build failed. Ensure a C compiler is installed on the current system.', file=sys.stderr)
    raise SystemExit(result.returncode)

print(f'C library built at: {output}')
