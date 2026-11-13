#!/usr/bin/env python3
"""Score GuruMedia affiliate offers and produce ranked output."""

import json
import re

# Raw data from Affbank, Affpaying, and OfferVault scraping
raw_offers = [
    # Affbank page 1 (most recent, sorted newest first)
    {"name": "Feilaira", "category": "Health", "tags": ["VSL"], "geos": ["MX","US","CA","AU","DE","UK","CH","AT","NL","BE","SE","NO","DK","FI","IE","NZ","FR","IT","ES","PT","PL","CZ","HU","RO","BG","IL"], "payout": 195, "variants": 1},
    {"name": "Blinzador", "category": "Health", "tags": ["VSL"], "geos": ["MX","US","CA","AU","DE","UK","CH","AT","NL","BE","SE","NO","DK","FI","IE","NZ","FR","IT","ES","PT","PL","CZ","HU","RO","BG","IL"], "payout": 195, "variants": 1},
    {"name": "HorseFil", "category": "Nutra/Male", "tags": ["VSL"], "geos": ["MX","US","CA","AU","DE","UK","CH","AT","NL","BE","SE","NO","DK","FI","IE","NZ","FR","IT","ES","PT","PL","CZ","HU","RO","BG","IL"], "payout": 235, "variants": 1},
    {"name": "MindWake", "category": "Health", "tags": ["VSL"], "geos": ["MX","US","CA","AU","DE","UK","CH","AT","NL","BE","SE","NO","DK","FI","IE","NZ","FR","IT","ES","PT","PL","CZ","HU","RO","BG","IL"], "payout": 215, "variants": 1},
    {"name": "Nail Defender", "category": "Health", "tags": ["VSL"], "geos": ["MX","US","CA","AU","DE","UK","CH","AT","NL","BE","SE","NO","DK","FI","IE","NZ","FR","IT","ES","PT","PL","CZ","HU","RO","BG","IL"], "payout": 215, "variants": 1},
    {"name": "Youth Within", "category": "Health", "tags": ["VSL"], "geos": ["MX","US","CA","AU","DE","UK","CH","AT","NL","BE","SE","NO","DK","FI","IE","NZ","FR","IT","ES","PT","PL","CZ","HU","RO","BG","IL"], "payout": 215, "variants": 1},
    {"name": "Mind Honey Trick", "category": "Health", "tags": ["Direct Checkout"], "geos": ["MX","US","CA","AU","DE","UK","CH","AT","NL","BE","SE","NO","DK","FI","IE","NZ","FR","IT","ES","PT","PL","CZ","HU","RO","BG","IL"], "payout": 215, "variants": 1},
    {"name": "Glyco Barrier", "category": "Health", "tags": ["VSL"], "geos": ["MX","US","CA","AU","DE","UK","CH","AT","NL","BE","SE","NO","DK","FI","IE","NZ","FR","IT","ES","PT","PL","CZ","HU","RO","BG","IL"], "payout": 215, "variants": 1},
    {"name": "Lipo Jelly", "category": "Nutra/Diet", "tags": ["VSL"], "geos": ["MX","US","CA","AU","DE","UK","CH","AT","NL","BE","SE","NO","DK","FI","IE","NZ","FR","IT","ES","PT","PL","CZ","HU","RO","BG","IL"], "payout": 220, "variants": 1},
    {"name": "Military Honey", "category": "Nutra/Male", "tags": ["VSL"], "geos": ["MX","US","CA","AU","DE","UK","CH","AT","NL","BE","SE","NO","DK","FI","IE","NZ","FR","IT","ES","PT","PL","CZ","HU","RO","BG","IL"], "payout": 235, "variants": 1},
    {"name": "Flow Strong", "category": "Nutra/Male", "tags": ["VSL"], "geos": ["MX","US","CA","AU","DE","UK","CH","AT","NL","BE","SE","NO","DK","FI","IE","NZ","FR","IT","ES","PT","PL","CZ","HU","RO","BG","IL"], "payout": 215, "variants": 1},
    {"name": "Thermo Ignite", "category": "Nutra/Diet", "tags": ["VSL"], "geos": ["MX","US","CA","AU","DE","UK","CH","AT","NL","BE","SE","NO","DK","FI","IE","NZ","FR","IT","ES","PT","PL","CZ","HU","RO","BG","IL"], "payout": 220, "variants": 1},
    {"name": "Soda Steel", "category": "Nutra/Male", "tags": ["VSL"], "geos": ["MX","US","CA","AU","DE","UK","CH","AT","NL","BE","SE","NO","DK","FI","IE","NZ","FR","IT","ES","PT","PL","CZ","HU","RO","BG","IL"], "payout": 230, "variants": 1},
    {"name": "Driftly", "category": "Health", "tags": ["Direct Checkout", "Checkout Event Tracking"], "geos": ["AT","DE","CH","NL","BE","FR","IT","ES","PT","SE","NO","DK","FI","IE"], "payout": 60, "variants": 1},
    {"name": "Clensy", "category": "Health", "tags": ["Direct Checkout", "Checkout Event Tracking"], "geos": ["AT","DE","CH","NL","BE","FR","IT","ES","PT","SE","NO","DK","FI","IE"], "payout": 60, "variants": 1},
    {"name": "Pb-Sin 18 Diet Supplements", "category": "Nutra/Diet", "tags": [], "geos": ["IT"], "payout": 75, "variants": 1},
    {"name": "LevelsRx GLP1", "category": "Health", "tags": [], "geos": ["US"], "payout": 325, "variants": 1},
    {"name": "X-All Washing Machine Cleaner", "category": "eCommerce", "tags": [], "geos": ["DE","AT"], "payout": 22, "variants": 1},
    {"name": "PhemmePure", "category": "Health", "tags": ["VSL"], "geos": ["MX","US","CA","AU","DE","UK","CH","AT","NL","BE","SE","NO","DK","FI","IE","NZ","FR","IT","ES","PT","PL","CZ","HU","RO","BG","IL"], "payout": 150, "variants": 1},
    {"name": "Sun Coast Sciences Total Package Serum", "category": "Health", "tags": ["Checkout Event Tracking"], "geos": ["AU","US","CA","UK","NZ","IE","DE","AT"], "payout": 55, "variants": 1},
    {"name": "Hearth & Haven Heater", "category": "eCommerce", "tags": ["Checkout Event Tracking"], "geos": ["AU","US","CA","UK","NZ","IE","DE"], "payout": 70, "variants": 1},
    {"name": "Corevalin", "category": "Health", "tags": ["Direct Checkout"], "geos": ["IL","CA","AU","FR","BE","CH"], "payout": 85, "variants": 3},
    {"name": "Power Heat Pro", "category": "eCommerce", "tags": ["Checkout Event Tracking"], "geos": ["DE","AT","CH"], "payout": 107, "variants": 1},
    {"name": "Mobiflexi Joint Support", "category": "Health", "tags": [], "geos": ["US","CA","AU"], "payout": 85, "variants": 3},
    {"name": "Keilini Portable Heater", "category": "eCommerce", "tags": ["Direct Checkout"], "geos": ["FR","SE","UK","DE","AT","NL","NO","DK"], "payout": 55, "variants": 4},
    # Affpaying additional
    {"name": "HeatGuard Gloves", "category": "eCommerce", "tags": [], "geos": ["FR"], "payout": 40, "variants": 1},
    {"name": "Arterix Blood Support Capsules", "category": "Health", "tags": ["Direct Checkout"], "geos": ["NO","DK","SE","FI"], "payout": 65, "variants": 2},
    {"name": "MetaBrew Diet Coffee", "category": "Nutra/Diet", "tags": [], "geos": ["DE","AT","CH"], "payout": 55, "variants": 1},
    {"name": "Fitralin", "category": "Nutra/Diet", "tags": ["Direct Checkout"], "geos": ["FR","BE"], "payout": 60, "variants": 1},
    {"name": "Truly Free Home Laundry Wash", "category": "eCommerce", "tags": [], "geos": ["US"], "payout": 30, "variants": 1},
    # OfferVault similar (recently seen on GuruMedia)
    {"name": "Revintis Forte Gummies", "category": "Health", "tags": ["Direct Checkout"], "geos": ["SE"], "payout": 65, "variants": 1},
    {"name": "OdorCrush Limescale Prevention Tablets", "category": "eCommerce", "tags": [], "geos": ["US","UK","DE","AU","CA","NZ","FR","SE","NO"], "payout": 45, "variants": 1},
    {"name": "Wamoma Smart Thermometer", "category": "eCommerce", "tags": [], "geos": ["US"], "payout": 50, "variants": 1},
    {"name": "Nuubu Detox Foot Patches", "category": "Health", "tags": [], "geos": ["US","UK","DE","AU","CA","NZ","FR","IT","ES","SE","NO","DK","FI","IE","NL","BE","AT","CH","PT","PL","CZ","HU","RO","BG","IL","MX"], "payout": 40, "variants": 5},
    {"name": "Glycopezil", "category": "Health", "tags": ["VSL"], "geos": ["US"], "payout": 90, "variants": 1},
    {"name": "Gentle Patches Dopamine Patches", "category": "Health", "tags": [], "geos": ["US","UK","CA","AU","NZ"], "payout": 55, "variants": 1},
    {"name": "Glyvera", "category": "Health", "tags": ["Direct Checkout"], "geos": ["DE","AT"], "payout": 70, "variants": 1},
    {"name": "VacTonic", "category": "eCommerce", "tags": [], "geos": ["US"], "payout": 55, "variants": 1},
    {"name": "Velomi GLP-1 Gummies", "category": "Nutra/Diet", "tags": [], "geos": ["SE"], "payout": 60, "variants": 1},
    {"name": "PureHealth Research Complete Vision", "category": "Health", "tags": ["VSL"], "geos": ["US"], "payout": 80, "variants": 1},
    {"name": "TestoBoost", "category": "Nutra/Male", "tags": [], "geos": ["IT"], "payout": 65, "variants": 1},
    {"name": "Vigora XL", "category": "Nutra/Male", "tags": [], "geos": ["FR"], "payout": 70, "variants": 1},
    {"name": "Omnipurge", "category": "Health", "tags": [], "geos": ["ES"], "payout": 60, "variants": 1},
    {"name": "Keilini Heater Pro", "category": "eCommerce", "tags": ["Direct Checkout"], "geos": ["UK","DE","AT","NL","FR"], "payout": 55, "variants": 2},
    {"name": "LeviaPatch", "category": "Nutra/Diet", "tags": [], "geos": ["UK"], "payout": 50, "variants": 1},
    {"name": "Testo Blue", "category": "Nutra/Male", "tags": [], "geos": ["NL"], "payout": 60, "variants": 1},
    {"name": "Glumentrol Capsules", "category": "Health", "tags": [], "geos": ["FR"], "payout": 55, "variants": 1},
    {"name": "Vivera SanoFlex Forte", "category": "Health", "tags": [], "geos": ["CH"], "payout": 65, "variants": 1},
    {"name": "GLPControl Plus", "category": "Nutra/Diet", "tags": [], "geos": ["FR","BE"], "payout": 58, "variants": 1},
    {"name": "Gluco Wave Glycogen Control", "category": "Health", "tags": ["VSL"], "geos": ["UK"], "payout": 55, "variants": 1},
]

# Deduplicate by product name (merge geos and variants)
products = {}
for offer in raw_offers:
    name = offer["name"]
    if name in products:
        p = products[name]
        p["geos"] = list(set(p["geos"] + offer["geos"]))
        p["tags"] = list(set(p["tags"] + offer["tags"]))
        p["variants"] += offer.get("variants", 1)
        p["payout"] = max(p["payout"], offer["payout"])
    else:
        products[name] = {
            "name": name,
            "category": offer["category"],
            "tags": list(set(offer["tags"])),
            "geos": list(set(offer["geos"])),
            "payout": offer["payout"],
            "variants": offer.get("variants", 1),
        }

# Scoring algorithm
def score_product(p):
    score = 0
    breakdown = []

    # Each geo = 5 points
    geo_pts = len(p["geos"]) * 5
    score += geo_pts
    breakdown.append(f"geos({len(p['geos'])}x5)={geo_pts}")

    # US present = +15
    if "US" in p["geos"]:
        score += 15
        breakdown.append("US=+15")

    # UK = +10
    if "UK" in p["geos"]:
        score += 10
        breakdown.append("UK=+10")

    # Category bonuses
    cat = p["category"]
    if cat == "Health":
        score += 10
        breakdown.append("Health=+10")
    elif cat == "eCommerce":
        score += 12
        breakdown.append("eCommerce=+12")
    elif cat == "Nutra/Diet":
        score += 8
        breakdown.append("Nutra/Diet=+8")
    elif cat == "Nutra/Male":
        score += 6
        breakdown.append("Nutra/Male=+6")

    # Tag bonuses
    for tag in p["tags"]:
        if "VSL" in tag:
            score += 15
            breakdown.append("VSL=+15")
        if "Checkout Event Tracking" in tag:
            score += 10
            breakdown.append("CET=+10")
        if "Direct Checkout" in tag:
            score += 5
            breakdown.append("DirectCheckout=+5")

    # Variant bonus: +3 each, max 30
    variant_pts = min(p["variants"] * 3, 30)
    score += variant_pts
    breakdown.append(f"variants({p['variants']}x3,cap30)={variant_pts}")

    p["score"] = score
    p["breakdown"] = ", ".join(breakdown)
    return score

# Score all products
for p in products.values():
    score_product(p)

# Sort by score descending
ranked = sorted(products.values(), key=lambda x: x["score"], reverse=True)

# Output
print(f"\n{'='*80}")
print(f"GURUMEDIA OFFERS SCORING - {len(ranked)} unique products")
print(f"{'='*80}\n")

for i, p in enumerate(ranked[:30], 1):
    geo_str = ", ".join(sorted(p["geos"]))
    tag_str = ", ".join(p["tags"]) if p["tags"] else "None"
    print(f"#{i:2d} | Score: {p['score']:3d} | {p['name']}")
    print(f"     Cat: {p['category']} | Tags: {tag_str}")
    print(f"     Geos ({len(p['geos'])}): {geo_str}")
    print(f"     Payout: ${p['payout']} | Variants: {p['variants']}")
    print(f"     Breakdown: {p['breakdown']}")
    print()

# Save top 15 for competition research
top15 = ranked[:15]
print("\n--- TOP 15 FOR COMPETITION RESEARCH ---")
for i, p in enumerate(top15, 1):
    print(f"{i}. {p['name']} (score={p['score']}, cat={p['category']})")

# Save data as JSON for later use
with open("/home/claude/homecleandeals/scored_products.json", "w") as f:
    json.dump([{
        "rank": i+1,
        "name": p["name"],
        "category": p["category"],
        "tags": p["tags"],
        "geos": sorted(p["geos"]),
        "geo_count": len(p["geos"]),
        "payout": p["payout"],
        "variants": p["variants"],
        "score": p["score"],
    } for i, p in enumerate(ranked)], f, indent=2)

print(f"\nSaved {len(ranked)} scored products to scored_products.json")
