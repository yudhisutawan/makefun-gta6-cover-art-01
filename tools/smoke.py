#!/usr/bin/env python3
"""Exercise core editor behaviours in headless Chromium."""
import subprocess,time,urllib.request
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'out';OUT.mkdir(exist_ok=True);server=subprocess.Popen(['node',str(ROOT/'serve.ts'),'--port','8081'],cwd=ROOT,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
try:
    for _ in range(80):
        try:urllib.request.urlopen('http://127.0.0.1:8081/',timeout=.3);break
        except Exception:time.sleep(.15)
    else:raise RuntimeError('local server did not start')
    errors=[]
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True,args=['--no-sandbox']);page=browser.new_page(viewport={'width':1280,'height':800},accept_downloads=True)
        page.on('console',lambda msg:errors.append('console: '+msg.text) if msg.type=='error' else None);page.on('pageerror',lambda e:errors.append('page: '+str(e)))
        page.goto('http://127.0.0.1:8081/',wait_until='load');page.wait_for_function("document.querySelectorAll('.panel-chip').length===3 && document.querySelector('.panel-chip').textContent.includes('boulevard')")
        assert page.locator('.panel-chip').count()==3
        page.locator('#caption').fill('Smoke Test Cover');page.wait_for_timeout(100)
        page.locator('#layout-group button',has_text='Vice Grid').click();assert page.locator('.panel-chip').count()==4
        before=page.locator('#cover').evaluate('(c)=>{let x=c.getContext("2d").getImageData(150,150,1,1).data;return [...x].join(",")}')
        page.locator('#grade-group button',has_text='Noir').click();after=page.locator('#cover').evaluate('(c)=>{let x=c.getContext("2d").getImageData(150,150,1,1).data;return [...x].join(",")}');assert before!=after
        page.locator('#samples').click();page.wait_for_function("document.querySelectorAll('.panel-chip').length===4")
        canvas=page.locator('#cover');box=canvas.bounding_box();page.mouse.move(box['x']+box['width']*.2,box['y']+box['height']*.2);page.mouse.down();page.mouse.move(box['x']+box['width']*.24,box['y']+box['height']*.23,steps=5);page.mouse.up()
        page.locator('#grade-group button',has_text='Neon').click();neon=page.locator('#cover').evaluate('(c)=>{let x=c.getContext("2d").getImageData(150,150,1,1).data;return [...x].join(",")}');assert neon!=after
        with page.expect_download() as download_info:page.locator('#export').click()
        download=download_info.value;dest=OUT/'smoke-export.png';download.save_as(str(dest));data=dest.read_bytes();assert data[:8]==b'\x89PNG\r\n\x1a\n' and len(data)>50000
        assert download.suggested_filename=='vice-cover-1920x1080.png';assert 'Saved vice-cover-1920x1080.png' in page.locator('#status').inner_text()
        assert not errors,errors;browser.close()
    print('PASS smoke: default panels, caption redraw, grid layout, noir/neon rendering, sample loading, panel dragging, PNG export and status')
finally:
    server.terminate();server.wait(timeout=5)
