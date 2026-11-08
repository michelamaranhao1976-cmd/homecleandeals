#!/usr/bin/env python3 -I
"""Process and score new GuruMedia offers."""
import json

# New products found from Affbank/OfferVault that are NOT in the current dashboard
# These are from the most recent GuruMedia listings (Nov 2026)
new_products = [
    {
        "name": "Malkko Prostapure Advantage",
        "cat": "Nutra / Male",
        "geos": "US,UK,CA,AU,NZ,IE,DE,FR,IT,ES,NL,BE,AT,CH,SE,DK,FI,NO,PT,GR,MX,BR,ZA,IL,AR,CL",
        "tags": "VSL",
        "offerCount": 2,
        "newestId": 34545,
    },
    {
        "name": "WellaNaturals Whipped Tallow Balm",
        "cat": "Nutra / Skin",
        "geos": "US,UK,CA,AU,NZ,IE,DE,FR,IT,ES,NL,BE,AT,CH,SE,DK,FI,NO,PT,GR,MX,BR,ZA,IL,AR",
        "tags": "Checkout Event Tracking",
        "offerCount": 2,
        "newestId": 34550,
    },
    {
        "name": "SheremArt Spirit Birds",
        "cat": "eCommerce / Product",
        "geos": "US,UK,CA,AU,NZ,IE,DE,FR,NL,BE,AT,CH,SE,DK,FI,NO,PT,GR,MX,ZA,IL,AR",
        "tags": "Checkout Event Tracking",
        "offerCount": 1,
        "newestId": 34548,
    },
    {
        "name": "Hotjak Portable Heater",
        "cat": "eCommerce / Product",
        "geos": "US,UK,CA,AU,NZ,IE,DE,FR,NL,BE,AT,CH,SE,DK,FI,NO,PT,GR,MX,ZA,IL,AR",
        "tags": "Direct Checkout",
        "offerCount": 1,
        "newestId": 34542,
    },
    {
        "name": "NovuBurn",
        "cat": "Nutra / Diet",
        "geos": "US",
        "tags": "VSL",
        "offerCount": 1,
        "newestId": 34555,
    },
    {
        "name": "NovuBrainPlus",
        "cat": "Nutra / Brain",
        "geos": "US",
        "tags": "VSL",
        "offerCount": 1,
        "newestId": 34556,
    },
    {
        "name": "Healtyco GLP Slim",
        "cat": "Nutra / Diet",
        "geos": "US,CA",
        "tags": "Direct Checkout",
        "offerCount": 1,
        "newestId": 34552,
    },
    {
        "name": "BloodPril",
        "cat": "Health",
        "geos": "US",
        "tags": "VSL",
        "offerCount": 1,
        "newestId": 34558,
    },
    {
        "name": "Slenza",
        "cat": "Nutra / Diet",
        "geos": "DE,AT,CH,BE",
        "tags": "Localized",
        "offerCount": 3,
        "newestId": 34540,
    },
    {
        "name": "Gentle Patches Dopamine Patches",
        "cat": "Health",
        "geos": "US,UK,CA,AU,NZ",
        "tags": "Checkout Event Tracking",
        "offerCount": 1,
        "newestId": 34535,
    },
    {
        "name": "ExtendTecc Wifi Repeater",
        "cat": "eCommerce / Product",
        "geos": "US,CA",
        "tags": "Checkout Event Tracking",
        "offerCount": 1,
        "newestId": 34546,
    },
    {
        "name": "PestVault Mouse Repellent Pouches",
        "cat": "eCommerce / Product",
        "geos": "US",
        "tags": "Checkout Event Tracking",
        "offerCount": 1,
        "newestId": 34544,
    },
    {
        "name": "AutoBank 360",
        "cat": "Biz Opp",
        "geos": "US,UK,CA,AU,NZ",
        "tags": "VSL",
        "offerCount": 1,
        "newestId": 34538,
    },
    {
        "name": "Veluna GLP-1 Booster",
        "cat": "Nutra / Diet",
        "geos": "DE",
        "tags": "Direct Checkout",
        "offerCount": 1,
        "newestId": 34536,
    },
    {
        "name": "GLPure GLP-1",
        "cat": "Nutra / Diet",
        "geos": "DE",
        "tags": "Direct Checkout",
        "offerCount": 1,
        "newestId": 34534,
    },
    {
        "name": "Osanix",
        "cat": "Nutra / Diet",
        "geos": "SE",
        "tags": "Direct Checkout",
        "offerCount": 1,
        "newestId": 34537,
    },
    {
        "name": "Virex",
        "cat": "Nutra / Diet",
        "geos": "DE",
        "tags": "Direct Checkout",
        "offerCount": 1,
        "newestId": 34533,
    },
    {
        "name": "MachoMacho",
        "cat": "Nutra / Male",
        "geos": "DE,AT,CH",
        "tags": "Localized",
        "offerCount": 3,
        "newestId": 34539,
    },
    {
        "name": "Perforan Male Enhancement Capsules",
        "cat": "Nutra / Male",
        "geos": "FR",
        "tags": "Localized",
        "offerCount": 1,
        "newestId": 34541,
    },
    {
        "name": "Smileslim",
        "cat": "Nutra / Diet",
        "geos": "FR",
        "tags": "Direct Checkout",
        "offerCount": 1,
        "newestId": 34543,
    },
    {
        "name": "Ketogenica Keto",
        "cat": "Nutra / Diet",
        "geos": "FI",
        "tags": "Direct Checkout",
        "offerCount": 1,
        "newestId": 34532,
    },
    {
        "name": "GlutaDrops",
        "cat": "Nutra / Diet",
        "geos": "FI",
        "tags": "Direct Checkout",
        "offerCount": 1,
        "newestId": 34531,
    },
]


def score_product(p):
    geos_list = p["geos"].split(",")
    geo_count = len(geos_list)
    score = 0

    # Each geo = 5 points
    score += geo_count * 5

    # US present = +15, UK = +10
    if "US" in geos_list:
        score += 15
    if "UK" in geos_list:
        score += 10

    # Category bonuses
    cat = p["cat"]
    if "Health" in cat:
        score += 10
    elif "eCommerce" in cat:
        score += 12
    elif "Diet" in cat or "Brain" in cat or "Skin" in cat or "Hair" in cat:
        score += 8
    elif "Male" in cat or "Women" in cat:
        score += 6

    # Tags
    tags = p["tags"]
    if "VSL" in tags:
        score += 15
    if "Checkout Event Tracking" in tags:
        score += 10
    if "Direct Checkout" in tags:
        score += 5

    # Offer variants (max 30)
    variant_bonus = min(p["offerCount"] * 3, 30)
    score += variant_bonus

    # ID bonus
    nid = p["newestId"]
    if nid > 34300:
        score += 10
    if nid > 34350:
        score += 5

    p["score"] = score
    p["geoCount"] = geo_count
    return p


# Score all new products
for p in new_products:
    score_product(p)

# Sort by score
new_products.sort(key=lambda x: x["score"], reverse=True)

# Print results
print("=" * 80)
print(f"NEW PRODUCTS FOUND: {len(new_products)}")
print("=" * 80)
for i, p in enumerate(new_products, 1):
    print(f"\n{i}. {p['name']}")
    print(f"   Category: {p['cat']}")
    print(f"   Geos ({p['geoCount']}): {p['geos']}")
    print(f"   Tags: {p['tags']}")
    print(f"   Offers: {p['offerCount']}")
    print(f"   Score: {p['score']}")

# Output as JSON for dashboard update
print("\n\n=== JSON FOR DASHBOARD ===")
output = []
for p in new_products:
    output.append({
        "name": p["name"],
        "cat": p["cat"],
        "geos": p["geos"],
        "tags": p["tags"],
        "offerCount": p["offerCount"],
        "newestId": p["newestId"],
        "score": p["score"],
        "geoCount": p["geoCount"],
    })
print(json.dumps(output, indent=2))

# Top 15 for competition research
print("\n\n=== TOP 15 FOR COMPETITION RESEARCH ===")
for i, p in enumerate(new_products[:15], 1):
    print(f"{i}. {p['name']} (score: {p['score']})")
