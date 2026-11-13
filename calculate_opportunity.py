#!/usr/bin/env python3
"""Calculate final opportunity scores with competition research."""

import json
from datetime import datetime

# Competition research results based on Google search saturation
# low = few specific results, brand is new/unknown
# med = moderate presence, some review sites
# high = heavily saturated, many affiliate pages and review sites
competition = {
    "Feilaira": "high",        # Dozens of review sites, newsires, blogs, lovable pages
    "Blinzador": "high",       # Multiple news sites, malware tips, heavy promotion
    "MindWake": "med",         # Some review articles, fewer than top competitors
    "Nail Defender": "med",    # Mixed results with similar products, moderate presence
    "Youth Within": "low",     # Almost no specific results, mixed with other "Youth" products
    "Glyco Barrier": "med",    # Some dedicated pages but mixed with "Glyco" products
    "PhemmePure": "med",       # Several review articles, niche women's health
    "Lipo Jelly": "low",       # Almost no specific results, confused with LipoJaro
    "Thermo Ignite": "low",    # No specific results, mixed with Thermo Burn Pro
    "Nuubu Detox Foot Patches": "high",  # Massive saturation, years of affiliate spam
    "HorseFil": "high",        # Heavy affiliate spam, multiple news wires
    "Military Honey": "low",   # Zero specific results, brand new
    "Flow Strong": "low",      # Minimal specific results, mostly other "Flow" products
    "Soda Steel": "low",       # Zero specific results, entirely new
    "Mind Honey Trick": "med", # Mixed with similar honey/brain products
}

comp_score_map = {"low": 30, "med": 15, "high": 0}

# Load scored products
with open("/home/claude/homecleandeals/scored_products.json") as f:
    products = json.load(f)

# Calculate opportunity for top 15 (and all products)
for p in products:
    name = p["name"]
    comp = competition.get(name, "med")  # default to med if not researched
    comp_pts = comp_score_map[comp]
    opportunity = round((p["score"] + comp_pts) / 1.7, 1)
    p["competition"] = comp
    p["comp_score"] = comp_pts
    p["opportunity"] = opportunity

# Re-sort by opportunity score
products.sort(key=lambda x: x["opportunity"], reverse=True)

# Re-rank
for i, p in enumerate(products):
    p["opp_rank"] = i + 1

print(f"\n{'='*90}")
print(f"GURUMEDIA OPPORTUNITY DASHBOARD - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
print(f"Total products analyzed: {len(products)}")
print(f"{'='*90}\n")

print(f"{'Rank':<5} {'Product':<38} {'Score':>6} {'Comp':>5} {'CompPts':>8} {'Opport':>8} {'Cat':<15} {'Geos':>5} {'Payout':>8}")
print("-" * 100)

for p in products[:25]:
    print(f"{p['opp_rank']:<5} {p['name'][:37]:<38} {p['score']:>6} {p['competition']:>5} {p['comp_score']:>8} {p['opportunity']:>8.1f} {p['category']:<15} {p['geo_count']:>5} ${p['payout']:>6}")

# Top 5 summary
print(f"\n{'='*90}")
print("TOP 5 OPORTUNIDADES DO DIA")
print(f"{'='*90}\n")
for p in products[:5]:
    print(f"  {p['opp_rank']}. {p['name']}")
    print(f"     Opportunity: {p['opportunity']:.1f} | Score: {p['score']} | Competition: {p['competition']}")
    print(f"     Category: {p['category']} | Geos: {p['geo_count']} | Payout: ${p['payout']}")
    print(f"     Tags: {', '.join(p['tags']) if p['tags'] else 'None'}")
    print(f"     Geos: {', '.join(p['geos'][:10])}{'...' if len(p['geos']) > 10 else ''}")
    print()

# Stats
categories = {}
for p in products:
    cat = p["category"]
    categories[cat] = categories.get(cat, 0) + 1

print(f"\nDistribuição por categoria:")
for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
    print(f"  {cat}: {count}")

low_comp = sum(1 for p in products if p.get("competition") == "low")
med_comp = sum(1 for p in products if p.get("competition") == "med")
high_comp = sum(1 for p in products if p.get("competition") == "high")
print(f"\nTop 15 Competition: Low={low_comp}, Med={med_comp}, High={high_comp}")

# Save final data
with open("/home/claude/homecleandeals/opportunity_data.json", "w") as f:
    json.dump(products, f, indent=2)

print(f"\nSaved opportunity data to opportunity_data.json")
