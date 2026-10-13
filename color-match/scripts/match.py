#!/usr/bin/env python3
"""Colour-match lookup for the color-match skill.

Takes the hex of a clothing item and returns candidate pairings by role
(complementary, analogous, neutral, seasonal), plus pairings from curated
Kulr palettes that contain the item colour. Every candidate is snapped to the
nearest traditional Japanese colour from the palette in SKILL.md.

Usage:
    python3 match.py "#D9A21B"
    python3 match.py "#D9A21B" --json
    python3 match.py "#D9A21B" --season autumn
"""
import argparse
import colorsys
import json
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GOOD_FIT = 22      # soft distance at or below this: use the Japanese name as is
KULR_REACH = 24    # a Kulr palette counts as containing the item colour within this delta E
TOO_SIMILAR = 14   # candidates closer than this to the item colour are skipped
LOW_CHROMA = 12    # item chroma below this counts as near-neutral
CORE_BIAS = 6      # a book-set colour wins when within this delta E of the best wider match


# ---------- colour maths ----------

def hex_to_rgb(h):
    h = h.strip().lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    if not re.fullmatch(r"[0-9A-Fa-f]{6}", h):
        raise ValueError(f"not a hex colour: {h!r}")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def rgb_to_hex(rgb):
    return "#" + "".join(f"{round(max(0, min(1, c)) * 255):02X}" for c in rgb)


def rgb_to_lab(rgb):
    def lin(c):
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (lin(c) for c in rgb)
    x = (0.4124 * r + 0.3576 * g + 0.1805 * b) / 0.95047
    y = (0.2126 * r + 0.7152 * g + 0.0722 * b)
    z = (0.0193 * r + 0.1192 * g + 0.9505 * b) / 1.08883

    def f(t):
        return t ** (1 / 3) if t > 0.008856 else 7.787 * t + 16 / 116
    fx, fy, fz = f(x), f(y), f(z)
    return (116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz))


def delta_e(a, b):
    return math.dist(a, b)


def soft_distance(a, b, chroma_weight=0.5):
    """Delta E that forgives saturation differences.

    Traditional Japanese colours are muted. A bright cobalt complement should
    land on lapis blue, so lightness and hue count in full and chroma at half."""
    dl = a[0] - b[0]
    ca, cb = math.hypot(a[1], a[2]), math.hypot(b[1], b[2])
    dc = ca - cb
    dh2 = max(0.0, (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2 - dc ** 2)
    return math.sqrt(dl ** 2 + (chroma_weight * dc) ** 2 + dh2)


def chroma(lab):
    return math.hypot(lab[1], lab[2])


def rotate_hue(rgb, degrees):
    h, l, s = colorsys.rgb_to_hls(*rgb)
    return colorsys.hls_to_rgb((h + degrees / 360) % 1, l, s)


def hue_deg(rgb):
    return colorsys.rgb_to_hls(*rgb)[0] * 360


def hue_gap(a, b):
    d = abs(a - b) % 360
    return min(d, 360 - d)


# ---------- data ----------

def load_japanese():
    """Read references/japanese-colours.json. Returns (colours, seasons).

    Colours flagged core are the original book set. The rest extend it so
    more targets land on a real Japanese name."""
    path = ROOT / "references" / "japanese-colours.json"
    if not path.exists():
        sys.exit("Missing references/japanese-colours.json")
    data = json.loads(path.read_text(encoding="utf-8"))
    colours = []
    seasons = {}
    for c in data["colours"]:
        rgb = hex_to_rgb(c["hex"])
        colours.append({
            "romaji": c["romaji"],
            "kanji": c["kanji"],
            "english": c["english"],
            "hex": c["hex"].upper(),
            "core": bool(c.get("core")),
            "rgb": rgb,
            "lab": rgb_to_lab(rgb),
        })
        if c.get("season"):
            seasons.setdefault(c["season"], []).append(c["romaji"].lower())
    return colours, seasons


def load_kulr():
    path = ROOT / "references" / "kulr-palettes.json"
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    for p in data["palettes"]:
        p["labs"] = [rgb_to_lab(hex_to_rgb(c)) for c in p["colors"]]
    return data["palettes"]


# ---------- matching ----------

def snap(rgb, japanese):
    """Nearest traditional colour to rgb."""
    lab = rgb_to_lab(rgb)
    best = min(japanese, key=lambda j: soft_distance(lab, j["lab"]))
    de = soft_distance(lab, best["lab"])
    # Stay with the book set when it fits nearly as well as the wider palette.
    core = [j for j in japanese if j["core"]]
    if core and not best["core"]:
        best_core = min(core, key=lambda j: soft_distance(lab, j["lab"]))
        core_de = soft_distance(lab, best_core["lab"])
        if core_de <= de + CORE_BIAS:
            best, de = best_core, core_de
    return {
        "target": rgb_to_hex(rgb),
        "name": f'{best["romaji"]} ({best["kanji"]})',
        "english": best["english"],
        "hex": best["hex"],
        "delta_e": round(de, 1),
        "fit": "good" if de <= GOOD_FIT else "loose",
    }


def dedupe_by_name(cands):
    """Keep one entry per Japanese name, the closest fit."""
    best = {}
    for c in cands:
        if c["name"] not in best or c["delta_e"] < best[c["name"]]["delta_e"]:
            best[c["name"]] = c
    return list(best.values())


def role_candidates(item_rgb, item_lab, japanese, seasons, season=None):
    out = {}
    # Near-neutral items (cream, grey, black) have no meaningful hue to rotate.
    out["low_chroma"] = chroma(item_lab) < LOW_CHROMA
    if out["low_chroma"]:
        out["complementary"] = []
        out["analogous"] = []
    else:
        out["complementary"] = [snap(rotate_hue(item_rgb, 180), japanese)]
        out["analogous"] = dedupe_by_name(
            [snap(rotate_hue(item_rgb, d), japanese) for d in (-30, 30)])

    neutrals = [j for j in japanese if chroma(j["lab"]) < 30
                and delta_e(item_lab, j["lab"]) > TOO_SIMILAR]
    ranked = []
    if neutrals:
        contrast = max(neutrals, key=lambda j: abs(j["lab"][0] - item_lab[0]))
        ranked.append(contrast)
        item_h = math.degrees(math.atan2(item_lab[2], item_lab[1]))
        harmony = min((j for j in neutrals if j is not contrast),
                      key=lambda j: hue_gap(math.degrees(math.atan2(j["lab"][2], j["lab"][1])), item_h),
                      default=None)
        if harmony:
            ranked.append(harmony)
    out["neutral"] = [{
        "target": j["hex"],
        "name": f'{j["romaji"]} ({j["kanji"]})',
        "english": j["english"],
        "hex": j["hex"],
        "delta_e": 0.0,
        "fit": "good",
    } for j in ranked]

    by_key = {j["romaji"].lower(): j for j in japanese}
    item_h = hue_deg(item_rgb)
    harmony_hues = [(item_h + d) % 360 for d in (-30, 30, 120, -120, 180)]
    season_names = [season] if season else list(seasons)
    seasonal = {}
    for s in season_names:
        pool = [by_key[k] for k in seasons.get(s, []) if k in by_key
                and delta_e(item_lab, by_key[k]["lab"]) > TOO_SIMILAR]
        if not pool:
            continue

        def score(j):
            h = hue_deg(j["rgb"])
            gap = min(hue_gap(h, t) for t in harmony_hues)
            return gap - 0.2 * abs(j["lab"][0] - item_lab[0])
        j = min(pool, key=score)
        seasonal[s] = {
            "target": j["hex"],
            "name": f'{j["romaji"]} ({j["kanji"]})',
            "english": j["english"],
            "hex": j["hex"],
            "delta_e": 0.0,
            "fit": "good",
        }
    out["seasonal"] = seasonal
    return out


def kulr_pairings(item_lab, palettes, japanese, limit=3):
    hits = []
    for p in palettes:
        dists = [delta_e(item_lab, lab) for lab in p["labs"]]
        d = min(dists)
        if d <= KULR_REACH:
            hits.append((d, p, dists.index(d)))
    hits.sort(key=lambda t: t[0])
    out = []
    seen = set()
    for d, p, idx in hits:
        mates = []
        for i, c in enumerate(p["colors"]):
            if i == idx or c in seen:
                continue
            if delta_e(item_lab, p["labs"][i]) <= TOO_SIMILAR:
                continue
            mates.append({**snap(hex_to_rgb(c), japanese), "kulr_hex": c})
        mates = dedupe_by_name(mates)
        if not mates:
            continue
        seen.update(m["kulr_hex"] for m in mates)
        out.append({
            "palette": p["name"],
            "tags": p["tags"],
            "matched_swatch": p["colors"][idx],
            "distance": round(d, 1),
            "pairings": mates,
        })
        if len(out) == limit:
            break
    return out


# ---------- output ----------

def fmt(c):
    base = f'{c["name"]}, {c["english"]}, {c["hex"]}'
    if c["fit"] == "loose":
        return f'{base}  [loose fit, dE {c["delta_e"]}: exact colour {c["target"]}, name it in plain English]'
    return base


def print_text(item_hex, roles, kulr):
    print(f"Item {item_hex}")
    if roles["low_chroma"]:
        print("\nNear-neutral item: complementary and analogous roles skipped. "
              "Lean on neutral, seasonal and curated pairings.")
    else:
        print("\nComplementary")
        for c in roles["complementary"]:
            print("  " + fmt(c))
        print("Analogous")
        for c in roles["analogous"]:
            print("  " + fmt(c))
    print("Neutral")
    for c in roles["neutral"]:
        print("  " + fmt(c))
    print("Seasonal")
    for s, c in roles["seasonal"].items():
        print(f"  {s}: " + fmt(c))
    print("\nCurated pairings (Kulr palettes that contain the item colour)")
    if not kulr:
        print("  none within reach, use the roles above")
    for k in kulr:
        print(f'  {k["palette"]} (swatch {k["matched_swatch"]}, dE {k["distance"]})')
        for m in k["pairings"]:
            print("    " + fmt(m) + f' <- {m["kulr_hex"]}')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("hex", help="item colour, e.g. #D9A21B")
    ap.add_argument("--season", choices=["spring", "summer", "autumn", "winter"],
                    help="return only this season's pick")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--no-kulr", action="store_true", help="skip the curated palette lookup")
    args = ap.parse_args()

    try:
        item_rgb = hex_to_rgb(args.hex)
    except ValueError as e:
        sys.exit(str(e))
    item_lab = rgb_to_lab(item_rgb)
    item_hex = rgb_to_hex(item_rgb)

    japanese, seasons = load_japanese()
    roles = role_candidates(item_rgb, item_lab, japanese, seasons, args.season)
    kulr = [] if args.no_kulr else kulr_pairings(item_lab, load_kulr(), japanese)

    if args.json:
        print(json.dumps({"item": item_hex, "roles": roles, "kulr": kulr}, ensure_ascii=False, indent=1))
    else:
        print_text(item_hex, roles, kulr)


if __name__ == "__main__":
    main()
