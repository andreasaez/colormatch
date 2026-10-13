---
name: "color-match"
description: "Suggests 3 to 5 colours that pair with a clothing item, using traditional Japanese colour names alongside complementary, neutral, and seasonal colour theory. Use when someone shares a photo or describes a garment colour and asks what goes with it."
---

# Color match

Help people pair colours for clothing. Read the item's colour, run the lookup script, then suggest 3 to 5 colours that work with it. Each suggestion pairs a Japanese colour name with its English name and a short reason. Keep the focus on colour matching: the user decides how the matches fit their wardrobe, and adds occasion or season themselves when it matters to them.

The script does the colour maths and the palette lookup. Claude reads the item colour from the photo, picks the final set, and writes the reasons.

## Workflow

1. **Read the item colour.** From a screenshot or photo, name the main colour in plain English with an approximate hex value. For a pattern or multi-colour item, name the dominant colour and the one or two accents, and match against the dominant colour unless the user says otherwise. From a text description ("dusty rose trousers"), take the colour as stated and give a hex value that fits it.

2. **Run the lookup.** From this skill's folder:

   ```
   python3 scripts/match.py "#D9A21B"
   ```

   Add `--season autumn` (or spring, summer, winter) when the user names a season. The script returns:
   - Candidates for each role (complementary, analogous, neutral, seasonal), each snapped to the nearest traditional Japanese colour. The palette holds 100 colours, and the 25-colour book set wins whenever it fits nearly as well.
   - Curated pairings: colours from Kulr palettes that contain the item colour, also snapped to Japanese names.

   Go straight to suggestions. The user corrects the colour reading if it looks off, so lead with the matches.

3. **Pick 3 to 5 matches that cover different roles:**
   - **Complementary:** from the opposite side of the colour wheel, for contrast.
   - **Neutral:** low saturation, so the item leads.
   - **Seasonal:** a colour suited to a time of year. Spring is light and clear, summer is cool and soft, autumn is warm and muted, winter is deep and high-contrast.
   - **Analogous:** a neighbouring colour on the wheel, for a tonal, cohesive look.
   - **Curated:** a colour from a Kulr palette that contains the item colour. A human designer paired these, so they add confidence to a match.

   Aim for at least three different roles across the set. Skip near-identical colours. A colour that shows up both as a role candidate and in a curated palette makes a strong pick.

4. **Name each match.** Use the Japanese name when the script marks the fit as good. When it marks a fit as loose, the Japanese palette has no close relative: use a plain English name and the exact hex the script reports. The traditional names enrich the suggestion, so a forced match makes it worse.

5. **Handle near-neutral items.** For cream, grey, black, or white, the script skips complementary and analogous roles. Build the set from neutral, seasonal, and curated pairings.

6. **Format each match** on its own line:
   **Romaji (kanji)**, English name, hex, role. One short sentence on why it works with the item.
   For loose fits: **English name**, hex, role. One short sentence.

7. **Close with one line** on how to use the set, when it adds something (for example, which matches give a bolder look and which a softer one). Keep the reply under about 150 words unless the user asks for more.

When the surface can render inline visuals, add a simple swatch strip showing the item colour followed by the matches, since hex codes alone show no colour.

If the script cannot run, pick matches by hand using the role definitions above and the palette below. Opposite pairs on the wheel: yellow and violet, orange and blue, red and green.

## Palette

These 25 colours are the book set. The script works from `references/japanese-colours.json`, which holds these plus 75 more traditional colours, so more matches land on a real Japanese name. Use this list when picking by hand.

Hex values come from Wikipedia's "Traditional colors of Japan" list. Published sources disagree on exact values for these colours, so present them as approximate.

**Blues**
- Ai-iro (藍色), indigo, #264348
- Kon (紺), deep navy, #192236
- Ruri-iro (瑠璃色), lapis blue, #1F4788
- Asagi-iro (浅葱色), light blue-green, #48929B
- Sora-iro (空色), sky blue, #4D8FAC
- Sabi-asagi (錆浅葱), muted grey-teal, #6A7F7A
- Onando-iro (御納戸色), dark slate teal, #364141

**Reds and pinks**
- Karakurenai (唐紅), crimson, #C91F37
- Benihi (紅緋), scarlet, #F35336
- Momo-iro (桃色), peach pink, #F47983
- Sakura-iro (桜色), cherry blossom pink, #FCC9B9
- Ebicha (海老茶), maroon brown, #5E2824

**Yellows and oranges**
- Yamabuki-iro (山吹色), golden yellow, #FFA400
- Ukon-iro (鬱金色), turmeric, #E69B3A
- Kihada (黄蘖), soft yellow, #F3C13A
- Kuchiba-iro (朽葉色), fallen-leaf orange, #D57835

**Greens**
- Mo'egi (萌黄), fresh green, #5B8930
- Uguisu-iro (鶲色), olive, #645530

**Browns and neutrals**
- Kakishibu-iro (柿渋色), persimmon brown, #934337
- Tobi-iro (鳶色), dark red-brown, #4C221B
- Rikyūcha (利休茶), muted taupe, #826B58
- Sumi-iro (墨色), ink black, #27221F
- Shironeri (白練), warm cream, #FFDDCA

**Purples**
- Fuji-iro (藤色), wisteria, #89729E
- Murasaki (紫), deep purple, #4F284B

**Seasonal leanings**
- Spring: sakura-iro, mo'egi, sora-iro, kihada
- Summer: asagi-iro, ruri-iro, fuji-iro, sabi-asagi
- Autumn: kuchiba-iro, ukon-iro, uguisu-iro, kakishibu-iro, rikyūcha
- Winter: kon, sumi-iro, karakurenai, murasaki

## Data sources

- `references/japanese-colours.json` holds the 25-colour book set (flagged `core`) plus 75 colours from Wikipedia's "Traditional colors of Japan", thinned so no two added colours sit close together. Each entry carries romaji, kanji, a short English name, the Wikipedia gloss, hex, and a season where one fits. To add a colour, append an entry in the same shape.
- `references/kulr-palettes.json` holds 72 garment-friendly palettes from [Kulr](https://kulr.app/explore), snapshot of 13 October 2026. Kulr publishes its palettes as free for personal and commercial use. Neon, game, dashboard, UI-system, and brand palettes stay out, since they target screens more than wardrobes.
- To refresh or extend the snapshot, add palettes to `references/kulr-palettes.json` in the same shape (name, five hex colours, tags).

## Example

User uploads a photo of a mustard jumper.

Mustard yellow, around #D9A21B, warm and earthy.

- **Cobalt blue**, #1B52D9, complementary. Blue sits opposite yellow and makes the mustard look richer.
- **Konkikyō (紺桔梗)**, midnight blue, #191F45, neutral. A dark base that lets the jumper lead.
- **Shironeri (白練)**, warm cream, #FFDDCA, curated. Soft and light, keeps the look warm.
- **Kuchiba-iro (朽葉色)**, fallen-leaf orange, #D57835, curated. A tonal step from mustard for a cohesive look.
- **Kakishibu-iro (柿渋色)**, persimmon brown, #934337, autumn. Earthy and muted, a natural seasonal partner.

Cobalt and midnight blue give a sharper contrast. Cream, orange, and persimmon keep it warm and tonal.
