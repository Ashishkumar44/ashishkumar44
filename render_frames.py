from pathlib import Path
import re, subprocess
from lxml import etree
ROOT=Path('/mnt/data/github_readme_build'); AS=ROOT/'assets'; OUT=ROOT/'previews'; OUT.mkdir(exist_ok=True)
TIMES=[0,2,5,9,13]
roles=['Full Stack Developer','MERN Developer','Frontend Developer','Backend Developer','Software Developer','Research Author']

def strip_anim(t):
 t=re.sub(r'<animate\b[^>]*/>','',t); t=re.sub(r'<animateTransform\b[^>]*/>','',t)
 t=re.sub(r'<style>(.*?)</style>',lambda m:'<style>'+re.sub(r'@keyframes[^}]+}\s*','',m.group(1))+'</style>',t,flags=re.S)
 t=re.sub(r' style="animation:[^"]*"','',t)
 return t

def frame(stem,t):
 raw=(AS/f'{stem}.svg').read_text(); raw=strip_anim(raw)
 if stem=='hero':
  active=min(int(t//3),5)
  # all role texts are y=370; set active by exact text when present, otherwise class-role dummies hidden
  def repl(m):
   attrs=m.group(1); content=m.group(2)
   if content.strip() in roles:
    op='1' if content.strip()==roles[active] else '0'
    attrs=re.sub(r'opacity="[^"]*"',f'opacity="{op}"',attrs)
   else:
    attrs=re.sub(r'opacity="[^"]*"','opacity="0"',attrs)
   return '<text'+attrs+'>'+content+'</text>'
  raw=re.sub(r'<text([^>]*y="370"[^>]*)>([^<]*)</text>',repl,raw)
 elif stem=='about-life':
  active=int((t%12)//4)
  # identify groups containing 01/03 etc
  def grp(m):
   g=m.group(0); n=int(re.search(r'<text[^>]*>(0[1-3]) / 03</text>',g).group(1)); op='1' if n-1==active else '0'; g=re.sub(r'<g opacity="[^"]*">',f'<g opacity="{op}">',g,1); return g
  raw=re.sub(r'<g opacity="[01]">.*?</g>',grp,raw,flags=re.S)
 elif stem=='id-dashboard':
  # damped settle + gentle swing approximation
  seq={0:0,2:2.6,5:-1.1,9:1.4,13:-0.6}; ang=seq[t]
  raw=raw.replace('<g class="swing" style="transform-origin:270px 188px;animation:swing 2.8s .2s both ease-out infinite">',f'<g transform="rotate({ang} 270 188)">')
 return raw

for stem in ['hero','about-life','stack','id-dashboard','connect']:
 for t in TIMES:
  p=ROOT/f'_frame_{stem}_{t}.svg'; p.write_text(frame(stem,t))
  subprocess.run(['inkscape',str(p),'--export-filename',str(OUT/f'{stem}-{t}s.png'),'--export-width','1200'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,check=True)
  p.unlink()
print('Rendered timestamp verification frames:',len(TIMES)*5)
