#!/usr/bin/env python3
"""Genera docs/ (index.html amb un set dins + sw.js, manifest i icones per fer-la anar sense cobertura).

  python3 build.py                 → llista els sets
  python3 build.py <id>            → posa aquest set a docs/ (el que es publicarà)
"""
import hashlib, json, re, shutil, sys, time
from pathlib import Path

ROOT = Path(__file__).parent
SETS = ROOT / "sets"

def sets():
    return sorted(p.name for p in SETS.iterdir() if (p / "set.txt").exists())

if len(sys.argv) < 2:
    for s in sets():
        cfg = json.loads((SETS / s / "set.json").read_text())
        print(f"  {s:32} {cfg.get('nom','')}  ({cfg.get('inici') or 'sense hora'})")
    sys.exit(0)

sid = sys.argv[1]
if sid not in sets():
    sys.exit(f"No trobo sets/{sid}/set.txt")
cfg = json.loads((SETS / sid / "set.json").read_text())
cfg["id"] = sid
cfg["txt"] = (SETS / sid / "set.txt").read_text()
data = json.dumps(cfg, ensure_ascii=False).replace("</", "<\\/")

src = (ROOT / "index.html").read_text()
out, n = re.subn(r"/\*SET\*/.*?/\*SET\*/", lambda m: "/*SET*/" + data + "/*SET*/", src, flags=re.S)
assert n == 1, "No trobo el marcador /*SET*/ a index.html"
DOCS = ROOT / "docs"
DOCS.mkdir(exist_ok=True)
(DOCS / "index.html").write_text(out)

# Offline: service worker amb una versió nova a cada build (així el mòbil sap que hi ha canvis)
version = time.strftime("%Y%m%d-%H%M%S") + "-" + hashlib.sha1(out.encode()).hexdigest()[:8]
sw, n = re.subn(r"const VERSION = '[^']*';", f"const VERSION = '{version}';", (ROOT / "sw.js").read_text())
assert n == 1, "No trobo «const VERSION = '…';» a sw.js"
(DOCS / "sw.js").write_text(sw)
shutil.copy(ROOT / "manifest.webmanifest", DOCS / "manifest.webmanifest")
shutil.copytree(ROOT / "assets" / "icons", DOCS / "assets" / "icons", dirs_exist_ok=True)
n_temes = len(re.findall(r"^\d{1,2}:\d{2}", cfg["txt"], re.M))
print(f"✓ docs/index.html amb «{cfg.get('nom')}» ({n_temes} temes) · offline v{version}")
