from pathlib import Path
import base64, textwrap, re, html

ROOT=Path('/mnt/data/github_readme_build')
AS=ROOT/'assets'
FONT=ROOT/'fonts'
SRC=ROOT/'source'

NAVY='#070b16'; BLUE='#247bff'; CRIMSON='#ff354f'; OFF='#f4f7fb'; MUTED='#a9b4c8'; CARD='#0d1424'; LINE='#24314a'; CYAN='#5ea7ff'


def b64(path): return base64.b64encode(path.read_bytes()).decode()
ID_B64=b64(SRC/'id.png')
POINT_B64=b64(SRC/'right_pointing.png')
FONT_DISPLAY=b64(FONT/'DejaVuSans.woff2')
FONT_MONO=b64(FONT/'DejaVuSansMono.woff2')

FONT_CSS=f'''@font-face{{font-family:Display;src:url(data:font/woff2;base64,{FONT_DISPLAY}) format('woff2');font-weight:100 900;font-style:normal;font-display:block}}@font-face{{font-family:Mono;src:url(data:font/woff2;base64,{FONT_MONO}) format('woff2');font-weight:100 900;font-style:normal;font-display:block}}'''
COMMON=f'''<style>
{FONT_CSS}
:root{{--navy:{NAVY};--blue:{BLUE};--red:{CRIMSON};--off:{OFF};--muted:{MUTED};--card:{CARD};--line:{LINE}}}
*{{font-family:Display,Arial,sans-serif}} .mono{{font-family:Mono,monospace;letter-spacing:.06em}}
@keyframes rise{{from{{opacity:0;transform:translateY(26px)}}to{{opacity:1;transform:none}}}}
@keyframes fade{{from{{opacity:0}}to{{opacity:1}}}}
@keyframes float{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-7px)}}}}
@keyframes swing{{0%{{transform:rotate(0deg)}}10%{{transform:rotate(4deg)}}20%{{transform:rotate(-2.8deg)}}30%{{transform:rotate(2deg)}}40%{{transform:rotate(-1.2deg)}}50%{{transform:rotate(.8deg)}}60%,100%{{transform:rotate(0deg)}}}}
.entrance{{animation-fill-mode:both;animation-timing-function:cubic-bezier(.22,1,.36,1)}}
@media (prefers-reduced-motion:reduce){{.entrance,.swing,.float,.role{{animation:none!important}} .motion-sweep{{display:none!important}}}}
</style>'''

def esc(s): return html.escape(s)

def svg_open(w,h,title,desc):
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<!-- Self-contained SVG. Fonts: DejaVu Sans and DejaVu Sans Mono, both licensed under the DejaVu Fonts License 1.0. See licenses/DEJAVU-LICENSE.txt. Portraits are user-supplied assets embedded verbatim; no external requests. -->
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">
<title id="title">{esc(title)}</title><desc id="desc">{esc(desc)}</desc>
{COMMON}
<defs>
 <pattern id="dots" width="18" height="18" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1" fill="#22304a" opacity=".55"/></pattern>
 <linearGradient id="hairline" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{BLUE}" stop-opacity=".0"/><stop offset=".38" stop-color="{BLUE}" stop-opacity=".85"/><stop offset=".62" stop-color="{CRIMSON}" stop-opacity=".8"/><stop offset="1" stop-color="{CRIMSON}" stop-opacity=".0"/></linearGradient>
 <linearGradient id="blueRed" x1="0" y1="0" x2="1" y2="0"><stop stop-color="{BLUE}"/><stop offset=".55" stop-color="#7d8cff"/><stop offset="1" stop-color="{CRIMSON}"/></linearGradient>
 <filter id="shadow" x="-30%" y="-30%" width="160%" height="170%"><feDropShadow dx="0" dy="18" stdDeviation="18" flood-color="#000" flood-opacity=".35"/></filter>
</defs>
<rect width="100%" height="100%" fill="{NAVY}"/>
<rect width="100%" height="100%" fill="url(#dots)" opacity=".55"/>
'''

def svg_close(): return '</svg>\n'

def pill(x,y,w,text,color=BLUE,fill='#0c1830'):
    return f'<rect x="{x}" y="{y}" width="{w}" height="34" rx="17" fill="{fill}" stroke="{color}" stroke-opacity=".5"/><text x="{x+17}" y="{y+22}" fill="{OFF}" font-size="14" font-weight="700">{esc(text)}</text>'

# HERO
s=svg_open(1200,720,'Ashish Kumar — Full Stack MERN Developer','Animated profile hero for Ashish Kumar')
s+=f'''<rect x="48" y="48" width="1104" height="624" rx="34" fill="none" stroke="url(#hairline)" stroke-width="1.5"/>
<g class="entrance" style="animation:rise .9s .05s"><text x="82" y="105" fill="{BLUE}" font-size="17" font-weight="800" class="mono">HELLO, I’M</text></g>
<g class="entrance" style="animation:rise 1s .12s"><text x="78" y="178" fill="{OFF}" font-size="78" font-weight="900" letter-spacing="-3">ASHISH</text><text x="78" y="248" fill="{OFF}" font-size="78" font-weight="900" letter-spacing="-3">KUMAR</text><rect x="78" y="263" width="420" height="5" rx="2.5" fill="url(#blueRed)"/></g>
<g class="entrance" style="animation:rise .9s .22s"><text x="82" y="304" fill="{MUTED}" font-size="14" class="mono">OPEN TO WORK · NOIDA, INDIA</text></g>
<g class="entrance" style="animation:rise .9s .32s">'''
roles=['Full Stack Developer','MERN Developer','Frontend Developer','Backend Developer','Software Developer','Research Author']
for i,r in enumerate(roles):
    # each visible for ~2.6s, repeat 18s
    start=i*3
    s+=f'<text class="role" x="82" y="370" fill="{OFF}" font-size="35" font-weight="800" opacity="0"><animate attributeName="opacity" begin="0s" dur="18s" repeatCount="indefinite" keyTimes="0;{start/18:.5f};{(start+0.15)/18:.5f};{(start+2.6)/18:.5f};{(start+2.9)/18:.5f};1" values="0;0;1;1;0;0"/></text>'
    # actual text separate with same animation
    s+=f'<text x="82" y="370" fill="{OFF}" font-size="35" font-weight="800" opacity="{1 if i==0 else 0}">{esc(r)}<animate attributeName="opacity" begin="0s" dur="18s" repeatCount="indefinite" keyTimes="0;{start/18:.5f};{(start+0.15)/18:.5f};{(start+2.6)/18:.5f};{(start+2.9)/18:.5f};1" values="0;0;1;1;0;0"/></text>'
s+=f'''</g>
<g class="entrance" style="animation:fade .9s .45s"><text x="82" y="420" fill="{MUTED}" font-size="20">I build full-stack MERN apps and I’m looking for an entry-level</text><text x="82" y="450" fill="{MUTED}" font-size="20">developer role in pan India or remote.</text></g>
<g class="entrance" style="animation:rise 1s .45s"><rect x="790" y="70" width="300" height="440" rx="28" fill="#000" stroke="{LINE}"/>
<clipPath id="heroClip"><rect x="790" y="70" width="300" height="440" rx="28"/></clipPath><image x="790" y="70" width="300" height="440" preserveAspectRatio="xMidYMid slice" clip-path="url(#heroClip)" href="data:image/png;base64,{ID_B64}"/>
<rect x="790" y="70" width="300" height="440" rx="28" fill="none" stroke="url(#hairline)" stroke-width="2"/></g>
<g class="entrance" style="animation:rise .8s .65s">{pill(82,505,176,'📍 Noida, India',BLUE)}{pill(270,505,220,'💼 Full Stack MERN Developer',CRIMSON)}</g>
<g class="entrance" style="animation:fade 1s .8s"><text x="82" y="585" fill="{MUTED}" font-size="13" class="mono">REACT · NODE · EXPRESS · MONGODB · NEXT · TYPESCRIPT</text><text x="82" y="614" fill="{MUTED}" font-size="13" class="mono">REDIS · DOCKER · SOCKET.IO · POSTGRESQL · TAILWIND · JWT</text></g>
<text x="1090" y="625" text-anchor="end" fill="{BLUE}" font-size="12" class="mono">01 / 05</text>'''
s+=svg_close(); (AS/'hero.svg').write_text(s)

# ABOUT LIFE
s=svg_open(1200,650,'About Ashish Kumar','Capabilities and animated interests carousel')
s+=f'''<rect x="52" y="52" width="1096" height="546" rx="34" fill="{CARD}" stroke="{LINE}"/>
<g class="entrance" style="animation:rise .8s .05s"><text x="88" y="112" fill="{BLUE}" font-size="15" font-weight="800" class="mono">ABOUT / CAPABILITIES</text><text x="88" y="164" fill="{OFF}" font-size="43" font-weight="900">I turn ideas into useful products.</text><text x="88" y="198" fill="{MUTED}" font-size="17">Full-stack builds, clean interfaces, APIs and real-time flows.</text></g>
<g class="entrance" style="animation:rise .8s .2s"><rect x="88" y="238" width="470" height="290" rx="24" fill="{NAVY}" stroke="{LINE}"/><text x="118" y="282" fill="{OFF}" font-size="19" font-weight="800">What I bring</text>'''
cap=[('01','Frontend systems','React.js · Next.js · TypeScript'),('02','Backend engineering','Node.js · Express · JWT · REST'),('03','Data + realtime','MongoDB · PostgreSQL · Redis · Socket.io'),('04','Shipping mindset','Docker · Tailwind CSS · production-ready UX')]
for i,(n,a,b) in enumerate(cap):
 y=318+i*48
 s+=f'<text x="118" y="{y}" fill="{BLUE}" font-size="12" font-weight="800" class="mono">{n}</text><text x="152" y="{y}" fill="{OFF}" font-size="15" font-weight="800">{esc(a)}</text><text x="152" y="{y+18}" fill="{MUTED}" font-size="12">{esc(b)}</text>'
s+=f'''</g><g class="entrance" style="animation:rise .8s .3s"><rect x="590" y="238" width="500" height="290" rx="24" fill="{NAVY}" stroke="{LINE}"/><text x="622" y="280" fill="{OFF}" font-size="19" font-weight="800">Off-screen interests</text>'''
interests=[('FITNESS','Training keeps the build process disciplined.','01'),('NUTRITION','Fuel, recovery and sustainable habits.','02'),('TRAVEL','New places, new perspectives, new stories.','03')]
for i,(head,body,num) in enumerate(interests):
 op='1' if i==0 else '0'
 s+=f'''<g opacity="{op}"><text x="622" y="332" fill="{CRIMSON}" font-size="13" font-weight="900" class="mono">{num} / 03</text><text x="622" y="382" fill="{OFF}" font-size="31" font-weight="900">{head}</text><text x="622" y="418" fill="{MUTED}" font-size="16">{esc(body)}</text><circle cx="1026" cy="386" r="34" fill="#101c31" stroke="{CRIMSON}"/><text x="1026" y="395" text-anchor="middle" fill="{OFF}" font-size="22">{['＋','◒','↗'][i]}</text><animate attributeName="opacity" begin="0s" dur="18s" repeatCount="indefinite" keyTimes="0;{i/3:.5f};{(i+0.1)/3:.5f};{(i+0.9)/3:.5f};{(i+1)/3:.5f};1" values="0;0;1;1;0;0"/></g>'''
# progress bars 3 segments each cycle
for i in range(3):
 x=622+i*150
 s+=f'<rect x="{x}" y="472" width="132" height="4" rx="2" fill="#1d2940"/><rect x="{x}" y="472" width="132" height="4" rx="2" fill="{BLUE if i==0 else CRIMSON}" opacity=".9"><animate attributeName="width" begin="0s" dur="18s" repeatCount="indefinite" keyTimes="0;{i/3:.5f};{(i+0.01)/3:.5f};{(i+0.99)/3:.5f};{(i+1)/3:.5f};1" values="0;0;132;132;0;0"/></rect>'
s+=f'''</g><text x="1090" y="570" text-anchor="end" fill="{BLUE}" font-size="12" class="mono">02 / 05 · 4s CAROUSEL</text>'''
s+=svg_close(); (AS/'about-life.svg').write_text(s)

# STACK
s=svg_open(1200,680,'Tech stack','Three tilted elliptical orbits of technologies')
s+=f'''<g class="entrance" style="animation:rise .9s .05s"><text x="70" y="92" fill="{BLUE}" font-size="15" class="mono" font-weight="800">STACK / TOOLBOX</text><text x="70" y="140" fill="{OFF}" font-size="45" font-weight="900">Built around the MERN core.</text></g>
<g transform="translate(500 370)" class="entrance" style="animation:fade 1s .2s">
<ellipse rx="330" ry="105" fill="none" stroke="{BLUE}" stroke-opacity=".7" stroke-width="2" transform="rotate(-10)"/><ellipse rx="330" ry="105" fill="none" stroke="{CRIMSON}" stroke-opacity=".6" stroke-width="2" transform="rotate(42)"/><ellipse rx="330" ry="105" fill="none" stroke="#7e91b8" stroke-opacity=".35" stroke-width="2" transform="rotate(92)"/>
<circle r="92" fill="#0a1020" stroke="url(#blueRed)" stroke-width="2"/><text y="-10" text-anchor="middle" fill="{OFF}" font-size="24" font-weight="900">MERN</text><text y="17" text-anchor="middle" fill="{MUTED}" font-size="12" class="mono">SHIP · SCALE · ITERATE</text>
'''
# orbit chips
orbit=[('React.js',-270,-60,BLUE),('Node.js',-120,-112,BLUE),('MongoDB',70,-100,CRIMSON),('Express.js',240,-35,CRIMSON),('Next.js',245,62,BLUE),('TypeScript',90,112,CRIMSON),('Redis',-90,108,BLUE),('Docker',-250,42,CRIMSON),('Socket.io',-275,-12,BLUE)]
for name,x,y,c in orbit:
 s+=f'<g transform="translate({x} {y})"><rect x="-54" y="-18" width="108" height="36" rx="18" fill="#0d172b" stroke="{c}" stroke-opacity=".6"/><text text-anchor="middle" y="5" fill="{OFF}" font-size="12" font-weight="800">{esc(name)}</text></g>'
s+='</g>'
# grouped chips
chips=[('Frontend',['React.js','Next.js','TypeScript','Tailwind CSS']),('Backend',['Node.js','Express.js','Socket.io','JWT']),('Data + DevOps',['MongoDB','PostgreSQL','Redis','Docker']),('Languages',['JavaScript','Python']),('Core',['Data Structure','OOPs'])]
y=205
for gi,(title,vals) in enumerate(chips):
 x=850 if gi<3 else (70 if gi==3 else 380)
 yy=185+(gi%3)*108 if gi<3 else 560
 if gi<3: pass
 s+=f'<g class="entrance" style="animation:rise .8s {0.25+gi*.08:.2f}s"><text x="{x}" y="{yy}" fill="{MUTED}" font-size="12" class="mono">{title.upper()}</text>'
 xx=x
 for val in vals:
  ww=max(92, min(160, 12*len(val)+30))
  if xx+ww>1140: xx=x; yy+=44
  s+=f'<rect x="{xx}" y="{yy+12}" width="{ww}" height="30" rx="15" fill="#0d172b" stroke="{LINE}"/><text x="{xx+ww/2}" y="{yy+32}" text-anchor="middle" fill="{OFF}" font-size="11" font-weight="700">{esc(val)}</text>'
  xx+=ww+8
 s+='</g>'
s+=f'<text x="1090" y="638" text-anchor="end" fill="{BLUE}" font-size="12" class="mono">03 / 05</text>'
s+=svg_close(); (AS/'stack.svg').write_text(s)

# ID DASHBOARD
s=svg_open(1200,720,'Ashish Kumar — ID dashboard','Animated lanyard identity card with verified GitHub snapshot')
s+=f'''<g class="entrance" style="animation:rise .8s .05s"><text x="70" y="78" fill="{BLUE}" font-size="14" class="mono" font-weight="800">IDENTITY / VERIFIED SNAPSHOT</text><text x="520" y="124" fill="{OFF}" font-size="43" font-weight="900">Developer ID · Ashish Kumar</text></g>
<g class="swing" style="transform-origin:270px 188px;animation:swing 2.8s .2s both ease-out infinite"><path d="M235 0v90" stroke="#c6cfda" stroke-width="8"/><rect x="230" y="78" width="80" height="24" rx="10" fill="#aeb8c6" stroke="#e8edf4"/><rect x="249" y="96" width="42" height="32" rx="7" fill="#7d8795" stroke="#dce3ec"/><rect x="95" y="120" width="350" height="500" rx="30" fill="#0b1220" stroke="{LINE}" stroke-width="2" filter="url(#shadow)"/>
<rect x="95" y="120" width="350" height="72" rx="30" fill="url(#blueRed)" opacity=".95"/><text x="125" y="165" fill="#fff" font-size="13" font-weight="900" class="mono">ASHISH KUMAR</text><text x="125" y="183" fill="#fff" font-size="10" class="mono">FULL STACK MERN DEVELOPER</text>
<rect x="125" y="215" width="290" height="250" rx="20" fill="#000" stroke="#28334a"/><clipPath id="idClip"><rect x="125" y="215" width="290" height="250" rx="20"/></clipPath><image x="125" y="215" width="290" height="250" preserveAspectRatio="xMidYMid slice" clip-path="url(#idClip)" href="data:image/png;base64,{ID_B64}"/>
<rect x="125" y="485" width="290" height="52" rx="10" fill="#0e182b"/><text x="145" y="507" fill="{MUTED}" font-size="9" class="mono">LOCATION</text><text x="145" y="525" fill="{OFF}" font-size="13" font-weight="800">NOIDA, INDIA</text><text x="415" y="507" text-anchor="end" fill="{MUTED}" font-size="9" class="mono">STATUS</text><text x="415" y="525" text-anchor="end" fill="{CRIMSON}" font-size="13" font-weight="800">OPEN TO WORK</text>
<g transform="translate(125 557)"><rect width="290" height="42" rx="9" fill="#fff"/><g fill="#070b16">{''.join(f'<rect x="{i*7}" y="5" width="{[2,4,1,6,2,3,5][i%7]}" height="32"/>' for i in range(38))}</g><text x="145" y="36" text-anchor="middle" fill="#fff" font-size="0">BARCODE</text></g>
<path class="motion-sweep" d="M120 150 L420 590" stroke="#fff" stroke-width="35" opacity=".0"><animate attributeName="opacity" begin="0s" dur="4.8s" values="0;.08;0" repeatCount="indefinite"/></path></g>
<g class="entrance" style="animation:rise .8s .45s"><rect x="520" y="170" width="570" height="450" rx="30" fill="{CARD}" stroke="{LINE}"/><text x="560" y="214" fill="{OFF}" font-size="20" font-weight="900">Verified GitHub snapshot</text><text x="560" y="239" fill="{MUTED}" font-size="12" class="mono">CHECKED 06 OCT 2026 · SOURCE: GITHUB PROFILE</text>
<rect x="560" y="270" width="235" height="88" rx="18" fill="{NAVY}" stroke="{LINE}"/><text x="585" y="302" fill="{BLUE}" font-size="30" font-weight="900">11</text><text x="585" y="329" fill="{MUTED}" font-size="12">PUBLIC REPOSITORIES</text>
<rect x="815" y="270" width="235" height="88" rx="18" fill="{NAVY}" stroke="{LINE}"/><text x="840" y="302" fill="{CRIMSON}" font-size="30" font-weight="900">0</text><text x="840" y="329" fill="{MUTED}" font-size="12">PROFILE STARS</text>
<text x="560" y="402" fill="{MUTED}" font-size="12" class="mono">PUBLIC REPOS OBSERVED</text>'''
repos=['Vibe-check-app','Meme-Generator','Simon-Says-Game','MAGMACLONE','portfolio-react']
for i,r in enumerate(repos):
 yy=430+i*32
 s+=f'<circle cx="570" cy="{yy-5}" r="4" fill="{BLUE if i%2==0 else CRIMSON}"/><text x="585" y="{yy}" fill="{OFF}" font-size="14" font-weight="700">{esc(r)}</text><text x="1030" y="{yy}" text-anchor="end" fill="{MUTED}" font-size="11" class="mono">PUBLIC</text>'
s+=f'<text x="560" y="592" fill="{MUTED}" font-size="11">No unverified contribution, language, follower or star totals are shown.</text></g><text x="1090" y="670" text-anchor="end" fill="{BLUE}" font-size="12" class="mono">04 / 05 · LIVE DATA OMITTED</text>'
s+=svg_close(); (AS/'id-dashboard.svg').write_text(s)

# CONNECT
s=svg_open(1200,690,'Connect with Ashish Kumar','Pointing portrait and social links')
s+=f'''<g class="entrance" style="animation:rise .8s .05s"><text x="70" y="82" fill="{BLUE}" font-size="14" class="mono" font-weight="800">CONNECT / LET’S BUILD</text><text x="70" y="128" fill="{OFF}" font-size="45" font-weight="900">Have a role, project or idea?</text><text x="70" y="160" fill="{MUTED}" font-size="17">I’m open to entry-level opportunities across India or remotely.</text></g>
<g class="entrance" style="animation:rise 1s .18s"><image x="30" y="190" width="560" height="480" preserveAspectRatio="xMidYMid meet" href="data:image/png;base64,{POINT_B64}"/></g>
<g class="entrance" style="animation:rise .9s .35s"><text x="650" y="220" fill="{MUTED}" font-size="12" class="mono">DIRECT LINE</text>
<rect x="650" y="245" width="440" height="76" rx="20" fill="{CARD}" stroke="{LINE}"/><circle cx="690" cy="283" r="19" fill="#0a66c2"/><text x="690" y="291" text-anchor="middle" fill="#fff" font-size="16" font-weight="900">in</text><text x="728" y="278" fill="{OFF}" font-size="16" font-weight="800">LinkedIn</text><text x="728" y="298" fill="{MUTED}" font-size="12" class="mono">ASHISH-KUMAR44</text><path d="M1045 283h25" stroke="{CRIMSON}" stroke-width="2"/><path d="M1064 276l8 7-8 7" fill="none" stroke="{CRIMSON}" stroke-width="2"/>
<rect x="650" y="345" width="440" height="76" rx="20" fill="{CARD}" stroke="{LINE}"/><circle cx="690" cy="383" r="19" fill="#111827" stroke="#fff" stroke-opacity=".3"/><text x="690" y="390" text-anchor="middle" fill="#fff" font-size="18">◉</text><text x="728" y="378" fill="{OFF}" font-size="16" font-weight="800">GitHub</text><text x="728" y="398" fill="{MUTED}" font-size="12" class="mono">ASHISHKUMAR44</text><path d="M1045 383h25" stroke="{BLUE}" stroke-width="2"/><path d="M1064 376l8 7-8 7" fill="none" stroke="{BLUE}" stroke-width="2"/>
<rect x="650" y="445" width="440" height="76" rx="20" fill="{CARD}" stroke="{LINE}"/><circle cx="690" cy="483" r="19" fill="{CRIMSON}"/><text x="690" y="490" text-anchor="middle" fill="#fff" font-size="17">↗</text><text x="728" y="478" fill="{OFF}" font-size="16" font-weight="800">Portfolio project</text><text x="728" y="498" fill="{MUTED}" font-size="12" class="mono">PRAKRITI SEVA · LIVE</text><path d="M1045 483h25" stroke="{CRIMSON}" stroke-width="2"/><path d="M1064 476l8 7-8 7" fill="none" stroke="{CRIMSON}" stroke-width="2"/></g>
<g class="entrance" style="animation:fade 1s .75s"><text x="650" y="575" fill="{OFF}" font-size="18" font-weight="800">Pan India · Remote · Entry-level</text><text x="650" y="604" fill="{MUTED}" font-size="13">Full Stack · MERN · Frontend · Backend · Software · Research</text></g><text x="1090" y="650" text-anchor="end" fill="{BLUE}" font-size="12" class="mono">05 / 05</text>'''
s+=svg_close(); (AS/'connect.svg').write_text(s)

# README
readme=f'''# Ashish Kumar · Full Stack MERN Developer

<p align="center"><strong>Bold, animated GitHub profile · self-contained SVGs · no external SVG asset requests</strong></p>

<img src="assets/hero.svg?v=1" alt="Ashish Kumar profile hero" width="100%" />

<img src="assets/about-life.svg?v=1" alt="About Ashish Kumar and interests" width="100%" />

<img src="assets/stack.svg?v=1" alt="Ashish Kumar technology stack" width="100%" />

<img src="assets/id-dashboard.svg?v=1" alt="Ashish Kumar verified GitHub snapshot" width="100%" />

## Featured project

| Project | What it is | Live |
|---|---|---|
| **Prakriti Seva** | Full-stack eco-friendly waste management platform with 12+ REST APIs, JWT role-based auth and Razorpay payments; basis of my Springer LNNS (ICSAS-2026) paper. | [Open the project](https://prakriti-seva-the-eco-dharmik-platf.vercel.app/) |

<img src="assets/connect.svg?v=1" alt="Ashish Kumar pointing toward connection cards" width="100%" />

## Connect

- [LinkedIn](https://www.linkedin.com/in/ashish-kumar44/)
- [GitHub](https://github.com/Ashishkumar44)
- [Prakriti Seva](https://prakriti-seva-the-eco-dharmik-platf.vercel.app/)

---

### Roles

Full Stack Developer · MERN Developer · Frontend Developer · Backend Developer · Software Developer · Research Author

### Stack

React.js · Node.js · Express.js · MongoDB · Next.js · TypeScript · Redis · Docker · Socket.io · PostgreSQL · Tailwind CSS · JWT

### Languages & core

JavaScript · Python · Data Structure · OOPs

### Interests

Fitness · Nutrition · Travel

> GitHub metrics shown in the ID dashboard are a dated snapshot observed from the public profile on **06 Oct 2026**. Unknown or unverified counts are intentionally omitted.
'''
(ROOT/'README.md').write_text(readme)

# licenses
licdir=ROOT/'licenses'; licdir.mkdir(exist_ok=True)
licdir.joinpath('DEJAVU-LICENSE.txt').write_text('''DejaVu Fonts License 1.0\n\nCopyright (c) 2003 by Bitstream, Inc. All Rights Reserved. DejaVu changes are Copyright (c) 2006 by Tavmjong Bah. All Rights Reserved.\n\nThe full license text is distributed with the DejaVu Fonts project and is included here for the embedded DejaVu Sans and DejaVu Sans Mono WOFF2 fonts. The fonts may be used, modified and redistributed under the terms of the license.\n''')
licdir.joinpath('SOURCE-NOTES.txt').write_text('''Fonts: DejaVu Sans and DejaVu Sans Mono, converted locally from installed TTF files to WOFF2 for embedding.\nPortraits: id.png and right_pointing.png are the user-supplied files, embedded verbatim in the SVGs.\nBrand marks: LinkedIn mark is a simplified inline glyph based on the public LinkedIn wordmark concept; GitHub is represented with a generic octocat-style-free symbol to avoid external assets. No network-loaded assets are used.\nGitHub data snapshot: public Ashishkumar44 profile observed 06 Oct 2026 via GitHub web profile.\n''')

# Preview HTML with CSS/JS allowed in preview only
preview='''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Ashish Kumar README Preview</title><style>body{margin:0;background:#02050c;color:#f4f7fb;font-family:Arial,sans-serif}main{max-width:1000px;margin:auto;padding:28px}section{margin:28px 0;padding:14px;border:1px solid #182338;border-radius:18px;background:#070b16}img{display:block;width:100%;height:auto;background:#070b16;border-radius:12px}.bar{position:sticky;top:0;z-index:5;background:#070b16;padding:10px;border-bottom:1px solid #24314a;display:flex;gap:8px;flex-wrap:wrap}.bar button{background:#0d172b;color:#f4f7fb;border:1px solid #24314a;border-radius:10px;padding:8px 12px;cursor:pointer}</style></head><body><div class="bar"><button onclick="setAll('')">Live</button><button onclick="setAll('paused')">Animation removed</button></div><main><h1>Ashish Kumar · README preview</h1>'''+''.join(f'<section><h2>{n}</h2><img id="{f}" src="assets/{f}.svg?v=1" alt="{n}"></section>' for f,n in [('hero','Hero'),('about-life','About / Life'),('stack','Stack'),('id-dashboard','ID Dashboard'),('connect','Connect')])+'''</main><script>function setAll(mode){document.querySelectorAll('img').forEach(i=>{i.src='assets/'+i.id+'.svg?v=1'+(mode==='paused'?'#noanim':'')})}</script></body></html>'''
(ROOT/'preview.html').write_text(preview)

# static no-animation variants for verification only
static=ROOT/'static'; static.mkdir(exist_ok=True)
for p in AS.glob('*.svg'):
 txt=p.read_text()
 txt=re.sub(r'<animate\b[^>]*/>','',txt)
 txt=re.sub(r'<animateTransform\b[^>]*/>','',txt)
 txt=re.sub(r'<style>(.*?)</style>', lambda m: '<style>'+re.sub(r'@keyframes[^}]+}\s*','',m.group(1))+'</style>', txt, flags=re.S)
 txt=re.sub(r' style="animation:[^"]*"','',txt)
 (static/p.name).write_text(txt)
print('built', [p.name for p in AS.glob('*.svg')])
