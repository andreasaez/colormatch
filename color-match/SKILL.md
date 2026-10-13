---
name: "color-match"
description: "Suggests 3 to 5 colours that pair with a clothing item, using traditional Japanese colour names alongside complementary, neutral, and seasonal colour theory. Use when someone shares a photo or describes a garment colour and asks what goes with it."
---

# Color match

Help people pair colours for clothing. Read the item's colour, then suggest 3 to 5 colours that work with it. Each suggestion pairs a Japanese colour name with its English name and a short reason. Keep the focus on colour matching: the user decides how the matches fit their wardrobe, and adds occasion or season themselves when it matters to them.

## Workflow

1. **Read the item colour.** From a screenshot or photo, name the main colour in plain English with an approximate hex value. For a pattern or multi-colour item, name the dominant colour and the one or two accents, and match against the dominant colour unless the user says otherwise. From a text description ("dusty rose trousers"), take the colour as stated and give a hex value that fits it.

2. **Go straight to suggestions.** The user corrects the colour reading if it looks off, so lead with the matches.

3. **Pick 3 to 5 matches that cover different roles:**
   - **Complementary:** from the opposite side of the colour wheel, for contrast. Yellow pairs with violet, orange with blue, red with green.
   - **Neutral:** low saturation, so the item leads. Ink, navy, grey-greens, and creams all work.
   - **Seasonal:** a colour suited to a time of year. Spring is light and clear, summer is cool and soft, autumn is warm and muted, winter is deep and high-contrast.
   - **Analogous:** a neighbouring colour on the wheel, for a tonal, cohesive look.

   Aim for at least three different roles across the set, and avoid two near-identical colours.

4. **Name each match from the palette below.** When no palette colour fits well, use a plain English name and give it a hex value. The traditional names are there to enrich the suggestion, so a forced match makes it worse.

5. **Format each match** on its own line:
   **Romaji (kanji)**, English name, hex, role. One short sentence on why it works with the item.

6. **Close with one line** on how to use the set, when it adds something (for example, which matches give a bolder look and which a softer one). Keep the reply under about 150 words unless the user asks for more.

When the surface can render inline visuals, add a simple swatch strip showing the item colour followed by the matches, since hex codes alone show no colour.

## Palette

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

## Example

User uploads a photo of a mustard jumper.

Mustard yellow, around #D9A21B, warm and earthy.

- **Fuji-iro (藤色)**, wisteria, #89729E, complementary. Violet sits opposite yellow and makes the mustard look richer.
- **Kon (紺)**, deep navy, #192236, neutral. A dark, classic base that lets the jumper lead.
- **Shironeri (白練)**, warm cream, #FFDDCA, neutral. Soft and light, keeps the look warm.
- **Uguisu-iro (鶲色)**, olive, #645530, autumn. Earthy and muted, a natural seasonal partner.
- **Kuchiba-iro (朽葉色)**, fallen-leaf orange, #D57835, analogous. A tonal step from mustard for a cohesive look.

Wisteria and navy give a sharper contrast. Olive and fallen-leaf orange keep it warm and tonal.