#!/usr/bin/env python3
"""Restore pinned public source dependencies; never fetch game files."""
import json,subprocess
from pathlib import Path
root=Path(__file__).resolve().parents[1];deps=json.loads((root/'dependencies.json').read_text())
def ensure_patch(name,dest,patch):
 args=['git','-C',str(dest),'apply','--ignore-space-change']
 if subprocess.run([*args,'--reverse','--check',str(patch)],capture_output=True).returncode==0:return
 check=subprocess.run([*args,'--check',str(patch)],capture_output=True,text=True)
 if check.returncode:raise SystemExit(f'{name}: cannot apply compatibility patch {patch}\n{check.stderr}')
 subprocess.run([*args,str(patch)],check=True)
for name in ('kinoko','noclip','gclib','citro3d'):
 dest=root/'vendor'/name;entry=deps[name]
 if dest.exists():
  actual=subprocess.check_output(['git','-C',str(dest),'rev-parse','HEAD'],text=True).strip()
  if actual!=entry['commit']:raise SystemExit(f'{name}: unexpected revision; refusing to overwrite existing checkout')
 else:
  subprocess.run(['git','clone','--no-checkout',entry['url'],str(dest)],check=True)
  subprocess.run(['git','-C',str(dest),'checkout','--detach',entry['commit']],check=True)
 if name=='kinoko':ensure_patch(name,dest,root/'patches/kinoko-arm11.patch')
 if name=='citro3d':ensure_patch(name,dest,root/entry['patch'])
print('Source dependencies ready. Run npm ci and install requirements.txt into a project virtualenv.')
