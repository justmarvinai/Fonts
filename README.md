# Formwerk

**Formwerk** is a bold industrial grotesque in the spirit of Mona Sans, made for posters, social ads and loud artwork, with even strokes, a large x-height and wide capitals that keep it readable in running text.

![Formwerk specimen](specimen/preview.png)

## Weights

| Style   | Weight class | Stem (units) | Use |
|---------|-------------:|-------------:|-----|
| Regular | 400 | 86  | Body text, captions |
| Medium  | 500 | 113 | UI, subheads, small text on images |
| Bold    | 700 | 148 | Headlines |
| Fat     | 900 | 188 | Posters, social ads, display |

## Design

- **Even strokes:** horizontals are 0.87× the stems in Regular and 0.80× in Fat, close to Mona Sans. There is just enough optical correction that bars look as heavy as stems.
- **Flush shoulders:** arches and bowls leave the stem flush with a high crotch. There are no spurs or deep notches at the joints.
- **Flat terminals:** c, e, s, a, C, G, S, 2, 3, 5, 6, 9 end in horizontal cuts. The t, f, j and r hooks use a short angled cut.
- **Softly squared rounds:** the bowls are superellipses, rounder than a box and squarer than a circle.
- **Grotesque details:** a double-storey `a` with a flat-topped bowl, a single-storey `g`, a `G` with a spur, a short crossing `Q` tail, curved `3` `6` `9`, square dots, and a round `ß` with a matching capital `ẞ`.
- **Display extras:** arrows `→ ← ↑ ↓ ↗ ↘` and tabular figures that line up in prices and dates.

## Character set (281 characters per weight)

- `A–Z`, `a–z`, `0–9` (tabular lining figures)
- German: `Ä Ö Ü ä ö ü ß ẞ`
- Western European: `À Á Â Ã Å Æ Ç È É Ê Ë Ì Í Î Ï Ð Ñ Ò Ó Ô Õ Ø Œ Ù Ú Û Ý Þ Ÿ` and their lowercase forms
- Central European and Turkish: `Č Ć Ď Ě Ğ İ ı Ł Ń Ň Ő Ř Ś Ş Š Ť Ů Ű Ź Ż Ž`, macrons, breves and more
- Punctuation: `. , : ; … ! ? ¡ ¿ ' " ‘ ’ “ ” ‚ „ ‹ › « » - – — _ ( ) [ ] { } / \ | ¦ · •`
- Symbols: `@ # % & * § ¶ © ® ™ ° + − × ÷ = ± < > ^ ~ ¬ µ ª º ¹ ² ³ ½ ¼ ¾`
- Currency: `$ € £ ¥ ¢ ¤`

## OpenType features

- `kern`: automatic class kerning (AV, To, LT, T., “A and so on)
- `ss01` / `salt`: single-storey `a`, including all accented forms

```css
.poster { font-family: "Formwerk"; font-weight: 900; font-feature-settings: "ss01" 1; }
```

## Files

```
fonts/otf/        Formwerk-{Regular,Medium,Bold,Fat}.otf    desktop (CFF outlines)
fonts/ttf/        Formwerk-{Regular,Medium,Bold,Fat}.ttf    desktop / apps (autohinted)
fonts/webfonts/   .woff2 and .woff                          web
specimen/         index.html (open in a browser), preview.png
source/           the Python sources that generate every glyph
```

To install on desktop, open the `.otf` files (macOS: Font Book, Windows: right-click → Install). In apps, Medium and Fat show up as separate families ("Formwerk Medium", "Formwerk Fat"). Apps that support typographic families group all four under "Formwerk".

### Web

```css
@font-face { font-family: "Formwerk"; font-weight: 400; src: url("Formwerk-Regular.woff2") format("woff2"); }
@font-face { font-family: "Formwerk"; font-weight: 500; src: url("Formwerk-Medium.woff2") format("woff2"); }
@font-face { font-family: "Formwerk"; font-weight: 700; src: url("Formwerk-Bold.woff2") format("woff2"); }
@font-face { font-family: "Formwerk"; font-weight: 900; src: url("Formwerk-Fat.woff2") format("woff2"); }
```

## Metrics

UPM 1000 · cap height 720 · x-height 526 (Regular) to 544 (Fat) · ascender 752 · descender −212

## Building from source

The fonts are generated parametrically. Every glyph is constructed from rectangles, superellipses and diagonal strokes that are merged with boolean operations, and all four weights come from the same code with different stem and width parameters (`source/params.py`).

```sh
pip install -r requirements.txt
python3 source/build.py            # all weights → fonts/
python3 source/build.py Bold       # a single weight
python3 source/specimen.py         # regenerate specimen/index.html
python3 source/sheet.py proof.png 120 "Hamburgefonstiv"   # quick multi-weight proof image
```

| File | Contents |
|------|----------|
| `source/geom.py` | primitives and boolean helpers |
| `source/params.py` | per-weight parameters (stems, metrics, spacing) |
| `source/lower.py`, `upper.py`, `figures.py`, `symbols.py`, `extra.py` | glyph construction |
| `source/accents.py` | diacritics and accented letters |
| `source/features.py` | kerning (from outline profiles) and `ss01` |
| `source/build.py` | font compilation (OTF, TTF, WOFF2, WOFF) |
| `source/sheet.py`, `compare.py`, `kerncheck.py` | proof images and kerning spot checks |

## License

Formwerk is licensed under the [SIL Open Font License 1.1](OFL.txt). You can use it freely in personal and commercial work, and bundle or embed it.
