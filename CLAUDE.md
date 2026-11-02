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
- L'app calcula el tema segons l'hora del mòbil i l'`inici` del set.
- **▶ Empieza ahora** sincronitza el set amb la realitat (es guarda en aquell mòbil). `−10 s / +10 s` per afinar. «Hora prevista» ho torna a l'`inici`.

## Regles
- **Crear el repo de GitHub o publicar res: SEMPRE preguntar a en Pau abans.**
- Secrets mai es llegeixen ni es mostren.
- No tocar res de `02 MidnightApp` des d'aquest projecte.

## Pendent / decidir
- Per a qui és: en Pau en directe, l'equip o el públic (canvia la pantalla, no les dades).
- Repo nou `paupuig92/universo-makina` + GitHub Pages (espera OK).
- Possibles: offline (service worker), icona, editor del setlist al mòbil, pantalla gran per a LED/VJ, sincronitzar tots els mòbils alhora (servidor).
