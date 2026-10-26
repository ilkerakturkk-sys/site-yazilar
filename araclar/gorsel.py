#!/usr/bin/env python3
"""Blog kapak görseli: sitenin ortak üslubunda 1400x900 WebP üretir.

Kullanım:
  python3 araclar/gorsel.py --sahne sahne.svg --cikti yazilar/gorseller/2026-10-28-ornek-v1.webp [--gunes 1090,220,110 | --gunes yok] [--tepe | --tepesiz]

sahne.svg yalnızca sahnenin iç öğelerini içerir (<svg> etiketi olmadan). Renkler {sage}, {deep} gibi
adlarla yazılır; arka plan, güneş ve tepeler bu betik tarafından eklenir. Örnekler: araclar/ornekler/*.svg
"""
import argparse, os, shutil, subprocess, sys, tempfile

P = dict(bg1="#eef2ea", bg2="#f6efe1", sage="#a8c4b1", sage2="#7fa08b", deep="#587a66", ink="#2c4537",
         sand="#e8c98f", rope="#c9a46a", rope2="#9c7a45", slate="#9aa7b4", rose="#d9a79f", cream="#fbf7ee", lilac="#c9b6d6")

def build(inner, sun=(1090, 220, 110), hills=True):
    s = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1400 900" width="1400" height="900">'
         f'<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{P["bg1"]}"/><stop offset="1" stop-color="{P["bg2"]}"/></linearGradient></defs>'
         '<rect width="1400" height="900" fill="url(#bg)"/>')
    if sun: s += f'<circle cx="{sun[0]}" cy="{sun[1]}" r="{sun[2]}" fill="{P["sand"]}" opacity=".6"/>'
    if hills:
        s += f'<path d="M0 620 C 260 560 520 600 760 580 C 1000 560 1200 525 1400 560 L1400 900 L0 900 Z" fill="{P["sage"]}"/>'
        s += f'<path d="M0 715 C 300 680 640 720 900 702 C 1120 688 1280 664 1400 680 L1400 900 L0 900 Z" fill="{P["sage2"]}"/>'
    return s + inner.format(**P) + '</svg>'

def to_png(svg_path, png_path):
    try:
        import cairosvg  # pip install cairosvg
        cairosvg.svg2png(url=svg_path, write_to=png_path, output_width=1400, output_height=900); return 'cairosvg'
    except Exception:
        pass
    if shutil.which('rsvg-convert'):
        subprocess.run(['rsvg-convert', '-w', '1400', '-h', '900', '-o', png_path, svg_path], check=True); return 'rsvg-convert'
    js = ("const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1400,height:900}});"
          f"await p.goto('file://{os.path.abspath(svg_path)}');await p.screenshot({{path:'{os.path.abspath(png_path)}'}});await b.close();}})();")
    subprocess.run(['node', '-e', js], check=True); return 'playwright'

def main():
    a = argparse.ArgumentParser()
    a.add_argument('--sahne', required=True); a.add_argument('--cikti', required=True)
    a.add_argument('--gunes', default='1090,220,110'); a.add_argument('--tepesiz', action='store_true')
    o = a.parse_args()
    inner = open(o.sahne, encoding='utf-8').read()
    sun = None if o.gunes == 'yok' else tuple(int(x) for x in o.gunes.split(','))
    svg = build(inner, sun, not o.tepesiz)
    d = tempfile.mkdtemp(); sp = os.path.join(d, 'k.svg'); pp = os.path.join(d, 'k.png')
    open(sp, 'w', encoding='utf-8').write(svg)
    how = to_png(sp, pp)
    from PIL import Image
    os.makedirs(os.path.dirname(o.cikti) or '.', exist_ok=True)
    Image.open(pp).convert('RGB').save(o.cikti, 'WEBP', quality=82)
    print('Kaydedildi:', o.cikti, '(', how, ')')

if __name__ == '__main__':
    main()
