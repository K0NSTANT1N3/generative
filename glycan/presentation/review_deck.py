"""Check deck geometry/text and render contact sheets after PDF export.

Optional dependencies: pymupdf, Pillow. No scientific performance is tested here.
"""
from pathlib import Path
import json
import re
import pymupdf
from PIL import Image, ImageDraw
from pptx import Presentation

OUT=Path(__file__).resolve().parent
pdf=pymupdf.open(OUT/'glycan_project_presentation.pdf')
deck=Presentation(OUT/'glycan_project_presentation.pptx')
issues=[]
norm=lambda s:re.sub(r'[^a-zA-Z0-9]','',s).lower()
if len(pdf)!=len(deck.slides):issues.append({'type':'page_count'})
for i,(page,slide) in enumerate(zip(pdf,deck.slides),1):
 text=norm(page.get_text())
 for sh in slide.shapes:
  if sh.left<0 or sh.top<0 or sh.left+sh.width>deck.slide_width+10000 or sh.top+sh.height>deck.slide_height+10000:
   issues.append({'slide':i,'type':'off_slide','text':getattr(sh,'text','')[:70]})
  if sh.has_text_frame and len(norm(sh.text))>20 and norm(sh.text) not in text:
   issues.append({'slide':i,'type':'visible_text_mismatch','text':sh.text[:150]})
 for b in page.get_text('blocks'):
  if b[1]<0 or b[3]>page.rect.height:
   issues.append({'slide':i,'type':'pdf_bounds','text':b[4][:70]})

for start in range(0,len(pdf),12):
 canvas=Image.new('RGB',(1280,800),'#d6dce4');draw=ImageDraw.Draw(canvas)
 for k in range(start,min(start+12,len(pdf))):
  pix=pdf[k].get_pixmap(matrix=pymupdf.Matrix(.44,.44),alpha=False)
  im=Image.frombytes('RGB',(pix.width,pix.height),pix.samples);im.thumbnail((410,172))
  x=(k-start)%3*426;y=(k-start)//3*200
  canvas.paste(im,(x+8,y+18));draw.text((x+10,y+2),str(k+1),fill='black')
 canvas.save(OUT/f'review_{start//12+1}.png')

selected=[0,2,4,17,22,23,27,29,33]
canvas=Image.new('RGB',(1500,900),'#101c2d');draw=ImageDraw.Draw(canvas)
for j,k in enumerate(selected):
 pix=pdf[k].get_pixmap(matrix=pymupdf.Matrix(.7,.7),alpha=False)
 im=Image.frombytes('RGB',(pix.width,pix.height),pix.samples);im.thumbnail((486,274))
 x=j%3*500;y=j//3*300
 canvas.paste(im,(x+7,y+18));draw.text((x+9,y+3),f'{k+1:02d}',fill='#4de0c1')
canvas.save(OUT/'preview.png')
result={'slide_count':len(deck.slides),'pdf_page_count':len(pdf),'issues':issues,
 'method':'PPTX geometry; visible per-shape text against PDF extraction; rendered contact sheets',
 'limitations':'Does not validate biological claims or guarantee aesthetic quality; visual inspection is separate.'}
(OUT/'quality_review.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
if issues:raise SystemExit(1)
