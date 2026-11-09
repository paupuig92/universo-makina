# Universo Makina (web app de sets en directe)

Parla en català amb en Pau, curt i clar, amb emojis. **La UI de l'app és en castellà.** En Pau té nivell bàsic de codi.

Web app per a iPhone que segueix un set de DJ en directe: el tema que sona, quant li queda, els següents, la part (amb el seu color) i el setlist sencer.
Neix de la prova del set makina dins la Midnight App (31-10-2026, perfil Pau, 199 temes, 5 parts). **És un projecte separat: no toca la Midnight App.**

## Fitxers
| Fitxer | Què és |
|---|---|
| `index.html` | Tota l'app (HTML+CSS+JS). Porta un set de prova entre `/*SET*/ … /*SET*/`. |
| `sets/<id>/set.txt` | El setlist en text (format de sota). Un per set. |
| `sets/<id>/set.json` | Nom, lloc i hora d'inici (`inici`, amb zona: `2026-11-01T00:00:00+01:00`). |
| `sw.js` · `manifest.webmanifest` · `assets/` | Funciona sense cobertura (service worker), icona a la pantalla d'inici i logo d'UM. `build.py` els copia a `docs/`. La versió és una empremta del contingut (pàgina, set, sw.js, manifest, icones): si no canvia res, és la mateixa i els mòbils no rebaixen l'app. A Ajustes surt «Versión del dd/mm hh:mm · empremta». |
| `build.py` | `python3 build.py` llista els sets · `python3 build.py <id>` genera `docs/index.html` amb aquest set **xifrat** (et demana el codi). `--sin-cifrar` = només per provar. |
| `docs/` | El que es publicarà (GitHub Pages), quan en Pau doni l'OK. |

## Format del setlist (igual que les tasques de la Midnight App, s'hi pot copiar)
```
# Part 1
[rosa]
00:00:00-00:01:40 1. INTRO Universo Makina Vol 2
00:01:40-00:03:20 2. +1 DJ Sisu & D-Vstor – Thank You Master
```
- Hores = temps des de l'inici del set (`H:MM:SS` o `MM:SS`). L'hora final és opcional.
- `# …` = nova part · `[color]` = color de la part: rojo, naranja, amarillo, verde, cian, azul, lila, rosa.
- `+1`, `-2`… al davant del títol = marca d'en Pau (es mostra com a etiqueta).

## Com funciona
- Barra de pestanyes a baix: **Ahora** (tema, compte enrere, «Siguientes» i botons `−10 s / +10 s / Programado / Parar` en directe i `Empezar` + `−10 s / +10 s / Programado` abans o parat, sempre just a sobre de la barra), **Setlist** (s'obre al tema que sona; tira fixa a dalt amb tema + temps) i **Ajustes**. Es recorda l'última pestanya.
- L'app va sola amb el rellotge del mòbil. Hora d'inici que mana, per ordre: 0) **Parar** (passa per sobre de tot) → 1) sincronitzat a mà (**Empezar**, ±10 s) → 2) data i hora posades a **Ajustes → Inicio** (es guarda en aquell mòbil) → 3) l'`inici` del `set.json`.
- Guardar una data/hora nova a Ajustes treu l'ajust a mà (pregunta abans). «Usar la del archivo» torna a l'`inici`. «Programado» (Ahora i Ajustes) treu l'ajust a mà i el «Parado» i torna a l'hora programada. El desfase es mostra amb el signe dels botons (−0:20 = el set va 20 s enrere).
- **Parar** (en directe, també en Pausa): dos tocs en 3 s («¿Parar?»), l'app deixa de seguir el rellotge i surt **«Parado»** amb el botó gran **Empezar**. Es guarda per set a `um.stop.<id>` (aguanta recarregar) i no toca l'ajust a mà ni l'hora guardada (Deshacer ho torna exacte). El treuen: **Empezar**, **Programado** i guardar data/hora (o «Usar la del archivo») a Ajustes. Parat no surten avisos. També a **Ajustes → Directo** (amb «Reiniciar ahora», dos tocs, i «Programado»).
- Per què «Prevista» ja no hi és: en Pau va triar `Empezar / Parar / Programado`; «Reiniciar» només és a Ajustes (Parar + Empezar fan el mateix des d'Ahora). Les columnes de la fila no són iguals (`.8/.8/1.5/.9fr`) perquè «Programado» hi càpiga a 375 px i apaïsat.
- A Ajustes també: **Avisos** (a sota), dades del set i versió. L'avís «Deshacer» surt a dalt (no tapa els botons).
- **Guia «Añádela a la pantalla de inicio»** a dalt d'Ajustes: només a l'iPhone obert des de Safari (no a l'app de la icona); «Entendido» la treu (`um.guia`). Safari i l'app de la icona tenen la memòria separada.
- **Com sap si hi ha versió nova**: compara la versió de la pàgina (`BUILD.v`) amb la de `sw.js` del servidor (llegida sense memòries). Si són diferents: fa venir el service worker nou i recarrega; si en 20 s no ho aconsegueix, esborra la memòria offline i recarrega de la xarxa (mai es queda enganxada una versió vella). Ho fa en obrir l'app, cada 2 min, en tornar-hi i amb el botó.
- **Actualizar app**: com a molt 8 s buscant (sense cobertura → «Sin conexión…»). L'app també busca versió nova cada 2 min amb la pantalla encesa i en tornar-hi. Sense cap tema sonant es recarrega sola; si sona un tema o l'editor és obert, surt l'avís **«Versión nueva» + Actualizar** (no es recarrega mai sola a mig set).
- Canviar de pestanya: primer amunt i després el contingut (si no, a l'iPhone la barra de baix es mou).
- Entre dos temes amb forat (fi < inici del següent) surt **«Pausa»** amb el compte enrere al següent. «Fin del set» només després de l'últim tema.

## Avisos (Ajustes → Avisos)
- Dins de l'app i amb la pantalla encesa (sense servidor no hi ha notificacions amb el mòbil bloquejat).
- Interruptor general + per tipus, cadascun amb la seva antelació: **Cada tema** (5–30 s: número i marc en taronja), **Cambio de parte** (30 s–5 min: franja a tota l'amplada del color de la part nova), **Temas con campana** (10 s–1 min: «Ahora viene…» amb la campana), **Marcas +/−** (Todas / Solo + / Solo −; usa els segons de «Cada tema»), **Fin del set** (1/5/10 min).
- **Por parte**: apaga «Cada tema» i «Marcas» dins d'una part (els altres avisos segueixen).
- Si en coincideixen uns quants, mana: fin del set > cambio de parte > tema marcado > marca > cada tema. Una sola franja (a sobre de la barra de progrés: no tapa el compte enrere ni els botons) i un sol marc gruixut (només els últims 30 s; fa un cop en entrar, sense batec infinit).
- **Vibración** (l'iPhone no vibra des d'una web; Android sí) i **Sonido** (pitet; a l'iPhone cal un toc a la pantalla per activar-lo). **Probar aviso** ensenya tots els tipus.
- **Campana** a cada tema de la pestanya Setlist (o «Avisarme de este tema» a Editar → tema). Es guarda per set (`um.star.<id>`) per part + títol: aguanta canvis d'hores, de marca i d'altres línies; si se li canvia el títol des de la fitxa, la segueix.
- Tot es guarda al mòbil: `um.avisos` (l'antic `um.aviso` hi passa sol).

## Editar la setlist al mòbil
- **Ajustes → Setlist → Editar setlist**: editor de text a pantalla sencera (mateix format de dalt, s'hi pot enganxar de la Midnight App o del Google Doc). Mentre escrius diu partes/temas/durada i llista els errors (vora taronja: línies que no es poden llegir) i avisos (vora groga: solapa, va enrere, forat, color desconegut, tema sense part). Tocar-ne una porta a la línia.
- Guardar amb línies il·legibles demana «Guardar igual»; si no hi ha cap tema, no deixa guardar. «Cancelar» amb canvis cal tocar-lo dos cops.
- **Desplazar tiempos desde**: des del tema N, ± mm:ss (mou aquell i tots els següents; l'anterior s'empalma). Després, Guardar.
- **Enviar** (o **Copiar** si el mòbil no té full de compartir): obre el full de compartir de l'iPhone (AirDrop al Mac, Notas, Copiar…) per actualitzar `sets/<id>/set.txt`.
- **Esborrany**: el que s'escriu a l'editor es guarda sol (`um.draft.<id>`); si l'iPhone tanca l'app abans de Guardar, en tornar a obrir l'editor surt «Recuperado el texto sin guardar.». S'esborra en Guardar o Cancelar.
- **Pestanya Setlist → Editar**: toca un tema → títol, marca (+1…), inici/fi, «Mover los siguientes», «Añadir detrás», «Borrar» (amb «Adelantar los siguientes»). Reescriu el mateix text (una sola font).
- **Els canvis només viuen en aquell mòbil** (localStorage `um.txt.<id>`): no canvien el fitxer ni els altres mòbils. Es veu l'etiqueta «Editada · data / Solo en este móvil.» (Ajustes i Setlist) amb **Volver al original** (pregunta abans). Cada guardat té «Deshacer».
- Canviar-la en directe no trenca la sincronia: les hores són des de l'inici del set i el tema que sona es recalcula al moment.
- Un forat entre temes es mostra com a «Pausa»; l'editor ho avisa igualment.

## Disseny (regles: mantenir-les en qualsevol canvi)
Com els cartells d'UM, sec i sense «capa IA». Les regles també són al principi del `<style>` d'`index.html`.
- **Colors**: negre càlid `--ink`, crema (`--fg`, `--bone`), grisos `--dim`/`--mute`. **Un sol taronja** `#ff4514` per al grafisme (▲, barra de pestanyes, progrés, rètols petits) i l'**acció principal** (Empezar, Guardar de l'editor, Parar/Reiniciar armat, errors/borrar). Seleccions (segments, marques, interruptors) en crema, no taronja.
- **Color de part només on és dada**: barra de parts, etiqueta «PARTE N», hora i línia de la llista, franja i separador de canvi de part. El marc, la barra de pestanyes i la resta són sempre taronja/crema.
- **Formes**: cantonades rectes a tot arreu (sense targetes arrodonides). Info en blocs separats per **una** línia d'1 px. Un sol panell per pantalla (el tema actual).
- **Lletra**: Helvetica Neue bold. Rètols petits en MAJÚSCULES amb `letter-spacing` ≤ .03em (mai espaiats amples, mai condensada). Compte enrere i títol del tema sense cap adorn, grans i llegibles.
- **Recursos de marca permesos (només aquí)**: ▲ a les 4 cantonades del marc principal (tema actual i pantalles d'abans/després); llista tipus «tour dates» (hora en color + títol en crema) per al Setlist i «Siguientes»; capçalera de cartell a les pantalles d'abans/després (`DOM ● 00:00 A 05:00` / `01.11.2026` a l'esquerra, lloc / ciutat a la dreta, logo); franja tipus «SOLD OUT» a tota l'amplada per al canvi de part i el fi del set.
- **Prohibit**: més triangles, dobles línies, ▼ als títols, frases d'ajuda sota cada control, gra, brillantors/glows, gradients de fons, batecs infinits, glifs decoratius (▶ ◂ ▸ ★ ↻ ＋ ✓ ✕) als textos.
- **Textos**: castellà natural i curt. Sense explicacions llargues; on es guarda només al mòbil, «Solo en este móvil.».
- **iPhone (pantalla d'inici)**: barra d'estat **`black`** (no `black-translucent`: amb la translúcida l'iOS 26 difumina la franja de dalt). A dalt hi ha `<div class="topedge">`, fixa, d'un sol color, que **rep tocs** (sense `pointer-events:none` ni pseudo-element: si no, l'iOS la difumina). `--sat` = zona segura + 22 px només si n'hi ha (icones velles posades amb la translúcida); `--top` = alçada de la franja (mín. 12 px en vertical, 0 en apaïsat) i és el que fan servir la tira del Setlist, els marges de scroll, l'editor i l'avís. L'iPhone llegeix el meta **només en afegir la icona** (per canviar-lo cal esborrar-la i tornar-la a afegir). La fila de botons d'Ahora és `position:sticky` a sobre de la barra (`--tabh` + zona segura). Provar amb insets reals (0 amb `black`; 59/34, 47/34, SE 20/0, apaïsat) abans de publicar.
- **Tacte**: botons, barra i tira sense selecció ni lupa; `touchstart` buit perquè Safari faci `:active`; `overflow-x:clip` (no `hidden`: trenca els sticky); amb l'editor obert el fons no es mou (`html:has(>body.modal)`).
- **Lletra**: només les del sistema (Helvetica Neue → Helvetica → Arial → system-ui). Res de Google Fonts: bloquejava la primera pantalla.
- **Seguretat**: `index.html` porta una Content-Security-Policy al `<head>` (només el mateix domini). Si s'afegeix cap recurs extern, cal ampliar-la i mirar que la consola no doni errors.

## Regles
- **Crear el repo de GitHub o publicar res: SEMPRE preguntar a en Pau abans.**
- Secrets mai es llegeixen ni es mostren.
- No tocar res de `02 MidnightApp` des d'aquest projecte.

## Pendent / decidir
- Per a qui és: en Pau en directe, l'equip o el públic (canvia la pantalla, no les dades).
- Repo nou `paupuig92/universo-makina` + GitHub Pages (espera OK).
- Possibles: pantalla gran per a LED/VJ, sincronitzar tots els mòbils alhora (servidor; també per compartir la setlist editada).

## Codi d'accés (setlist xifrat, opció A · 06-11-2026)
- Cada esdeveniment té un **codi** (mínim 8 caràcters; recomanat: frase de 4 paraules. Un codi de 8 ha de ser ALEATORI, de gestor de contrasenyes: si és una paraula amb números es pot endevinar sense connexió). `build.py <id>` xifra el set (nom, lloc, hora i text) amb AES-GCM; la clau surt del codi (PBKDF2-SHA256, 600.000 voltes). Al repo públic i a `docs/` **només hi ha text il·legible**. El codi no es guarda enlloc (ni al repo ni a cap fitxer): es posa a mà a la Terminal (o amb `UM_CODE=…`). Necessita `python3 -m pip install --user cryptography`.
- A l'app: si no hi ha el set desxifrat al mòbil surt «Código de acceso». Es desxifra al mòbil, es guarda (`um.set.<id>` + `um.key.<id>`) i no cal tornar-lo a escriure; si surt un set nou (mateix codi) s'obre sol. **Ajustes → Bloquear app** (dos tocs) esborra el set i el codi d'aquest mòbil. Majúscules i espais de més no importen.
- Honest: això és confidencialitat real, **no hi ha rols**: qui té el codi ho veu tot, i les edicions són locals a cada mòbil. Un codi curt es pot forçar sense connexió: sempre frases llargues. Per canviar un codi: tornar a fer `build.py` amb el nou i repartir-lo.
- **El text en clar no ha d'anar a GitHub**: `sets/` i `UNIVERSO-MAKINA-BRIEF.md` són al `.gitignore` (només viuen al Mac). Si algun cop apareix `set.txt` al repo, parar i avisar.
- CSP: `build.py` posa el hash dels scripts a `script-src` (sense `'unsafe-inline'`). Si es canvia un `<script>`, cal tornar a fer el build. La pàgina porta `noindex`.
