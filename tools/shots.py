#!/usr/bin/env python3
"""Capture deterministic browser scenes and enforce screenshot gate limits."""
import json, subprocess, time, urllib.request
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]; shots=json.loads((ROOT/'shots.json').read_text()); out=ROOT/'screenshots';out.mkdir(exist_ok=True)
server=subprocess.Popen(['node',str(ROOT/'serve.ts'),'--port','8080'],cwd=ROOT,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
try:
    for _ in range(80):
        try: urllib.request.urlopen('http://127.0.0.1:8080/',timeout=.3);break
        except Exception: time.sleep(.15)
    else: raise RuntimeError('local server did not start')
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True,args=['--no-sandbox'])
        for scene in shots:
            page=browser.new_page(viewport={'width':scene['width'],'height':scene['height']},device_scale_factor=1)
            page.goto('http://127.0.0.1:8080/?'+scene['query'],wait_until='load');page.wait_for_function('window.__shotReady === true',timeout=20000);page.wait_for_timeout(300)
            path=out/scene['name'];page.screenshot(path=str(path),type='jpeg',quality=85);print(f"{path.name}: {path.stat().st_size} bytes, {scene['width']}x{scene['height']}");page.close()
        browser.close()
    okay=True
    for scene in shots:
        pth=out/scene['name'];w,h=scene['width'],scene['height'];good=pth.stat().st_size<=262144 and max(w,h)<=1280 and min(w,h)>=480
        print(f"{'PASS' if good else 'FAIL'} caps {pth.name}");okay &= good
    print(f"{'PASS' if okay else 'FAIL'} all screenshot caps")
    if not okay: raise SystemExit(1)
finally:
    server.terminate();server.wait(timeout=5)
