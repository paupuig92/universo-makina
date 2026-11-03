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
| `sw.js` · `manifest.webmanifest` · `assets/` | Funciona sense cobertura (service worker), icona a la pantalla d'inici i logo d'UM. `build.py` els copia a `docs/` i canvia la versió a cada build. |
| `build.py` | `python3 build.py` llista els sets · `python3 build.py <id>` genera `docs/index.html` amb aquest set. |
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
- Barra de pestanyes a baix: **Ahora** (tema, compte enrere, «Siguientes» i botons `−10 s / +10 s / Prevista / Reiniciar`, sempre just a sobre de la barra), **Setlist** (s'obre al tema que sona; tira fixa a dalt amb tema + temps) i **Ajustes**. Es recorda l'última pestanya.
- L'app va sola amb el rellotge del mòbil. Hora d'inici que mana, per ordre: 1) sincronitzat a mà (**Empezar ahora**, ±10 s) → 2) data i hora posades a **Ajustes → Inicio** (es guarda en aquell mòbil) → 3) l'`inici` del `set.json`.
- Guardar una data/hora nova a Ajustes treu l'ajust a mà (pregunta abans). «Usar la del archivo» torna a l'`inici`. «Prevista» / «Quitar ajuste» treu només l'ajust a mà. El desfase es mostra amb el signe dels botons (−0:20 = el set va 20 s enrere).
- A Ajustes també: **Avisos** (a sota), dades del set i versió. L'avís «Deshacer» surt a dalt (no tapa els botons).
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
- **Copiar**: copia el text per passar-lo al Mac (per actualitzar `sets/<id>/set.txt`).
- **Pestanya Setlist → Editar**: toca un tema → títol, marca (+1…), inici/fi, «Mover los siguientes», «Añadir detrás», «Borrar» (amb «Adelantar los siguientes»). Reescriu el mateix text (una sola font).
- **Els canvis només viuen en aquell mòbil** (localStorage `um.txt.<id>`): no canvien el fitxer ni els altres mòbils. Es veu l'etiqueta «Editada · data / Solo en este móvil.» (Ajustes i Setlist) amb **Volver al original** (pregunta abans). Cada guardat té «Deshacer».
- Canviar-la en directe no trenca la sincronia: les hores són des de l'inici del set i el tema que sona es recalcula al moment.
- Un forat entre temes es mostra com a «Pausa»; l'editor ho avisa igualment.

## Disseny (regles: mantenir-les en qualsevol canvi)
Com els cartells d'UM, sec i sense «capa IA». Les regles també són al principi del `<style>` d'`index.html`.
- **Colors**: negre càlid `--ink`, crema (`--fg`, `--bone`), grisos `--dim`/`--mute`. **Un sol taronja** `#ff4514` per al grafisme (▲, barra de pestanyes, progrés, rètols petits) i l'**acció principal** (Empezar ahora, Guardar de l'editor, Reiniciar armat, errors/borrar). Seleccions (segments, marques, interruptors) en crema, no taronja.
- **Color de part només on és dada**: barra de parts, etiqueta «PARTE N», hora i línia de la llista, franja i separador de canvi de part. El marc, la barra de pestanyes i la resta són sempre taronja/crema.
- **Formes**: cantonades rectes a tot arreu (sense targetes arrodonides). Info en blocs separats per **una** línia d'1 px. Un sol panell per pantalla (el tema actual).
- **Lletra**: Helvetica Neue bold. Rètols petits en MAJÚSCULES amb `letter-spacing` ≤ .03em (mai espaiats amples, mai condensada). Compte enrere i títol del tema sense cap adorn, grans i llegibles.
- **Recursos de marca permesos (només aquí)**: ▲ a les 4 cantonades del marc principal (tema actual i pantalles d'abans/després); llista tipus «tour dates» (hora en color + títol en crema) per al Setlist i «Siguientes»; capçalera de cartell a les pantalles d'abans/després (`DOM ● 00:00 A 05:00` / `01.11.2026` a l'esquerra, lloc / ciutat a la dreta, logo); franja tipus «SOLD OUT» a tota l'amplada per al canvi de part i el fi del set.
- **Prohibit**: més triangles, dobles línies, ▼ als títols, frases d'ajuda sota cada control, gra, brillantors/glows, gradients de fons, batecs infinits, glifs decoratius (▶ ◂ ▸ ★ ↻ ＋ ✓ ✕) als textos.
- **Textos**: castellà natural i curt. Sense explicacions llargues; on es guarda només al mòbil, «Solo en este móvil.».
- **iPhone (pantalla d'inici)**: la fila de botons d'Ahora és `position:sticky` a sobre de la barra (`--tabh` + zona segura); franja negra sota la barra d'estat (`body:after`); marges de scroll del Setlist amb la zona segura. Provar amb insets reals (59/34, 47/34, SE 20/0, apaïsat) abans de publicar.
- **Seguretat**: `index.html` porta una Content-Security-Policy al `<head>` (només el mateix domini + Google Fonts). Si s'afegeix cap recurs extern, cal ampliar-la i mirar que la consola no doni errors.

## Regles
- **Crear el repo de GitHub o publicar res: SEMPRE preguntar a en Pau abans.**
- Secrets mai es llegeixen ni es mostren.
- No tocar res de `02 MidnightApp` des d'aquest projecte.

## Pendent / decidir
- Per a qui és: en Pau en directe, l'equip o el públic (canvia la pantalla, no les dades).
- Repo nou `paupuig92/universo-makina` + GitHub Pages (espera OK).
- Possibles: pantalla gran per a LED/VJ, sincronitzar tots els mòbils alhora (servidor; també per compartir la setlist editada).
