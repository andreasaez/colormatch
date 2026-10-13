# Color match

![Color match: share an item, get matching traditional Japanese colours](assets/colormatch.gif)

A fun little Claude skill to help you match outfits.

You have a mustard jumper, a pair of dusty rose trousers, or a bag in a colour you love, and no idea what to wear with it. Show Claude a screenshot or describe the colour, and Color match suggests 3 to 5 colours that go with it. Each one comes with its traditional Japanese name, an English name, and a hex code.

## How it works

1. Share a photo or screenshot of the item, or describe its colour.
2. Claude reads the colour and runs a small lookup script that does the colour maths.
3. You get a mix of matches across five roles:
   - **Complementary:** opposite on the colour wheel, for contrast
   - **Neutral:** a calm base that lets your item lead
   - **Seasonal:** a colour suited to spring, summer, autumn, or winter
   - **Analogous:** a close neighbour, for a tonal look
   - **Curated:** a colour that a designer paired with your item's colour in a hand-made palette

The script finds the candidates. Claude picks the final set and writes the reason for each one. You decide how the matches fit your wardrobe, and you can add the occasion or season if you want Claude to factor it in.

## Example

> What goes with this mustard jumper?

Mustard yellow, around #D9A21B, warm and earthy.

- **Cobalt blue**, #1B52D9, complementary. Blue sits opposite yellow and makes the mustard look richer.
- **Konkikyō (紺桔梗)**, midnight blue, #191F45, neutral. A dark base that lets the jumper lead.
- **Shironeri (白練)**, warm cream, #FFDDCA, curated. Soft and light, keeps the look warm.
- **Kuchiba-iro (朽葉色)**, fallen-leaf orange, #D57835, curated. A tonal step from mustard for a cohesive look.
- **Kakishibu-iro (柿渋色)**, persimmon brown, #934337, autumn. Earthy and muted, a natural seasonal partner.

Cobalt and midnight blue give a sharper contrast. Cream, orange, and persimmon keep it warm and tonal.

When a target colour has no close Japanese relative, as with the bright cobalt above, Claude names it in plain English and gives the exact hex.

## What's inside

```
color-match/
  SKILL.md                         the workflow Claude follows
  scripts/match.py                 colour maths and palette lookup (Python 3, standard library only)
  references/japanese-colours.json 100 traditional Japanese colours
  references/kulr-palettes.json    72 curated palettes from Kulr
```

Run the lookup yourself:

```
python3 color-match/scripts/match.py "#D9A21B"
python3 color-match/scripts/match.py "#D9A21B" --season autumn
python3 color-match/scripts/match.py "#D9A21B" --json
```

The script converts the hex to Lab, rotates the hue to find role candidates, and snaps each one to the nearest Japanese colour. It forgives saturation differences, because traditional colours run muted and a bright complement should still land on a close relative. It also finds Kulr palettes that contain your colour and offers their other swatches as curated pairings.

## Install

**Claude Code:** copy the `color-match` folder into `~/.claude/skills/`. The lookup script needs `python3`.

**Claude apps:** zip the `color-match` folder and upload it where you add custom skills in Claude.

Then ask Claude what goes with something you want to wear. If Claude cannot run the script, it picks matches by hand from the 25-colour set in `SKILL.md`.

## The palette

The skill draws on 100 traditional Japanese colours (wa-iro). The first 25 are the original set, from ai-iro indigo to fuji-iro wisteria, and the lookup prefers them whenever they fit nearly as well as a wider match. The other 75 come from Wikipedia's [Traditional colors of Japan](https://en.wikipedia.org/wiki/Traditional_colors_of_Japan) list, thinned so that no two sit close together. Each added colour has a short English name, and `references/japanese-colours.json` records the Wikipedia gloss alongside it.

Sources vary on exact hex values for these colours, so treat them as close guides.

## Credits

- Curated palettes come from [Kulr](https://kulr.app/explore), a free colour tool. The snapshot holds 72 garment-friendly palettes from 13 October 2026. Kulr publishes its palettes as free for personal and commercial use.
- Traditional colour names and values come from Wikipedia's [Traditional colors of Japan](https://en.wikipedia.org/wiki/Traditional_colors_of_Japan).
