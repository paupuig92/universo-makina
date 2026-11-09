#!/usr/bin/env python3
"""Genera docs/ (index.html amb un set dins + sw.js, manifest i icones per fer-la anar sense cobertura).
   La versió és una empremta del contingut: si no canvia res, és la mateixa.

  python3 build.py                 → llista els sets
  python3 build.py <id>            → posa aquest set a docs/ XIFRAT (et demana el codi de l'esdeveniment)
  python3 build.py <id> --sin-cifrar → sense xifrar (només per provar en local, MAI per publicar)
  python3 build.py <id> --probar   → no genera res: diu si un codi OBRE el set que hi ha ara a docs/
  python3 build.py <id> --visible  → el codi es veu mentre l'escrius (per defecte NO es veu i es demana dues vegades)

El codi no es guarda enlloc: el poses tu cada vegada (o amb la variable UM_CODE).
Necessita «cryptography»:  python3 -m pip install --user cryptography
"""
import base64, getpass, hashlib, hmac, json, os, re, shutil, sys, time, unicodedata
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
PLAIN = "--sin-cifrar" in sys.argv
HIDDEN = "--visible" not in sys.argv
ITER = 600_000   # voltes de PBKDF2-SHA256: fa lent provar codis a l'atzar

def normaliza(c):   # igual que a l'app: sense majúscules ni espais de més (així el mòbil no et molesta)
    return " ".join(unicodedata.normalize("NFKC", c).lower().split())

if "--probar" in sys.argv:
    try:
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    except ImportError:
        sys.exit("Falta «cryptography». Executa:  python3 -m pip install --user cryptography")
    m = re.search(r"/\*SET\*/(\{.*?\})/\*SET\*/", (ROOT / "docs" / "index.html").read_text(), flags=re.S)
    enc = json.loads(m.group(1)).get("enc") if m else None
    if not enc:
        sys.exit("El docs/index.html d'ara NO està xifrat (⚠️ el set es veuria en clar).")
    code = os.environ.get("UM_CODE") or (getpass.getpass if HIDDEN else input)("Codi a provar (no es veu): " if HIDDEN else "Codi a provar: ")
    key = hashlib.pbkdf2_hmac("sha256", normaliza(code).encode(), base64.b64decode(enc["s"]), enc["i"], 32)
    try:
        AESGCM(key).decrypt(base64.b64decode(enc["n"]), base64.b64decode(enc["c"]), None)
    except Exception:
        sys.exit(f"❌ Aquest codi NO obre el set de docs/ (versió {enc['v']}). Codi provat: {len(code)} caràcters.")
    sys.exit(f"✅ Aquest codi OBRE el set de docs/ (versió {enc['v']}).")

if sid not in sets():
    sys.exit(f"No trobo sets/{sid}/set.txt")
cfg = json.loads((SETS / sid / "set.json").read_text())
cfg["id"] = sid
cfg["txt"] = (SETS / sid / "set.txt").read_text()
if PLAIN:
    data = json.dumps(cfg, ensure_ascii=False).replace("</", "<\\/")
else:
    try:
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    except ImportError:
        sys.exit("Falta «cryptography». Executa:  python3 -m pip install --user cryptography")
    ask = getpass.getpass if HIDDEN else input
    code = os.environ.get("UM_CODE") or ask(f"Codi de «{cfg.get('nom', sid)}» ({'no es veu' if HIDDEN else 'es veu'} mentre l'escrius): ")
    if len(normaliza(code)) < 8:
        sys.exit("El codi és massa curt: mínim 8 caràcters (si són 8, han de ser ALEATORIS, de gestor de contrasenyes; millor 4 paraules sense relació).")
    if not os.environ.get("UM_CODE") and HIDDEN and getpass.getpass("Torna'l a escriure: ") != code:
        sys.exit("Els dos codis no coincideixen.")
    if not HIDDEN:
        print(f"Codi: «{code}» ({len(code)} caràcters)")
    salt = hashlib.sha256(("um-salt:" + sid).encode()).digest()[:16]
    key = hashlib.pbkdf2_hmac("sha256", normaliza(code).encode(), salt, ITER, 32)
    plain = json.dumps(cfg, ensure_ascii=False).encode()
    iv = hmac.new(key, b"iv" + plain, hashlib.sha256).digest()[:12]   # mateix text → mateix xifrat (versió estable); text diferent → iv diferent
    ct = AESGCM(key).encrypt(iv, plain, None)
    b = lambda x: base64.b64encode(x).decode()
    data = json.dumps({"id": sid, "enc": {"v": hashlib.sha1(ct).hexdigest()[:8], "i": ITER, "s": b(salt), "n": b(iv), "c": b(ct)}})

src = (ROOT / "index.html").read_text()
out, n = re.subn(r"/\*SET\*/.*?/\*SET\*/", lambda m: "/*SET*/" + data + "/*SET*/", src, flags=re.S)
assert n == 1, "No trobo el marcador /*SET*/ a index.html"
DOCS = ROOT / "docs"
DOCS.mkdir(exist_ok=True)

# Versió = empremta del contingut (pàgina + set + sw.js + manifest + icones).
# Si no canvia res, la versió és la mateixa i els mòbils no es tornen a baixar l'app.
sw_src = (ROOT / "sw.js").read_text()
icons = sorted((ROOT / "assets" / "icons").glob("*.png"))
h = hashlib.sha1(out.encode() + sw_src.encode() + (ROOT / "manifest.webmanifest").read_bytes())
for f in icons:
    h.update(f.name.encode() + f.read_bytes())
version = h.hexdigest()[:8]

# Data llegible (Ajustes): la del fitxer més nou. Si la versió és la mateixa que la de docs/, es manté la data d'abans.
fonts = [ROOT / "index.html", ROOT / "sw.js", ROOT / "manifest.webmanifest", SETS / sid / "set.txt", SETS / sid / "set.json", *icons]
date = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(max(f.stat().st_mtime for f in fonts)))
prev = DOCS / "index.html"
if prev.exists():
    m = re.search(r"/\*BUILD\*/(\{.*?\})/\*BUILD\*/", prev.read_text())
    if m and json.loads(m.group(1)).get("v") == version:
        date = json.loads(m.group(1))["d"]
out, n = re.subn(r"/\*BUILD\*/.*?/\*BUILD\*/", lambda m: "/*BUILD*/" + json.dumps({"v": version, "d": date}) + "/*BUILD*/", out, flags=re.S)
assert n == 1, "No trobo el marcador /*BUILD*/ a index.html"
# CSP: en lloc de 'unsafe-inline' als scripts, només s'accepten aquests scripts exactes (hash)
hashes = " ".join("'sha256-" + base64.b64encode(hashlib.sha256(x.encode("utf-8")).digest()).decode() + "'" for x in re.findall(r"<script>(.*?)</script>", out, flags=re.S))
out, n = re.subn(r"script-src 'self' 'unsafe-inline'", lambda m: "script-src 'self' " + hashes, out, count=1)
assert n == 1, "No trobo script-src a la CSP"
assert "<script>" in out and hashes
(DOCS / "index.html").write_text(out)

# Offline: el service worker porta la versió (així el mòbil sap que hi ha canvis)
sw, n = re.subn(r"const VERSION = '[^']*';", f"const VERSION = '{version}';", sw_src)
assert n == 1, "No trobo «const VERSION = '…';» a sw.js"
(DOCS / "sw.js").write_text(sw)
shutil.copy(ROOT / "manifest.webmanifest", DOCS / "manifest.webmanifest")
shutil.copytree(ROOT / "assets" / "icons", DOCS / "assets" / "icons", dirs_exist_ok=True)
n_temes = len(re.findall(r"^\d{1,2}:\d{2}", cfg["txt"], re.M))
print(f"✓ docs/index.html amb «{cfg.get('nom')}» ({n_temes} temes, {'SENSE xifrar ⚠️' if PLAIN else 'xifrat 🔐'}) · versió {version} ({date[8:10]}/{date[5:7]} {date[11:16]})")
