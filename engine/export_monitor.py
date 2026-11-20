#!/usr/bin/env python3
"""export_monitor.py — refinery → portal bridge for Mode L (the "World Monitor" map layer).

ONE-WAY: reads the built lae-{vn,world,cn} registries, emits every entity that carries a `location`
to portal/content/lae-monitor.json — the data file the portal's build_monitor.py renders. The portal
never writes back; this is the wall in strategy §8 (Mode L reads data, data takes nothing from Mode L).

Each emitted point is a REAL registry entity with provenance (url + tier + source). An entity without a
location simply does not plot (honest — no fabricated glow). Geocoding is a CURATED keyword→lat/lon
table (no live geocoder) so the output is deterministic and the portal build stays reproducible.

Run:  python3 export_monitor.py [out.json]   (default: the portal content path below)
"""
import json, sys, collections, pathlib

HERE = pathlib.Path(__file__).resolve().parent
DOMAINS = ["lae-vn", "lae-world", "lae-cn"]
DEFAULT_OUT = pathlib.Path("/Users/os/RtR/rtr-news/portal/content/lae-monitor.json")

# Curated place table: (keyword found in the `location` string, lat, lon, en label, vn label).
# Ordered — the FIRST keyword that appears in a location wins, so the specific site (Saigon Hi-Tech /
# Thu Duc) is matched before the generic city it sits in (HCMC). Coords are approximate centroids.
GEO = [
    ("Saigon Hi-Tech",  10.851, 106.797, "Thu Duc City, HCMC",      "TP Thủ Đức, TP HCM"),
    ("Thu Duc",         10.851, 106.797, "Thu Duc City, HCMC",      "TP Thủ Đức, TP HCM"),
    ("Điện Biên",       21.386, 103.017, "Dien Bien, Vietnam",      "Điện Biên"),
    ("Gia Bình",        21.061, 106.201, "Gia Binh, Bac Ninh",      "Gia Bình, Bắc Ninh"),
    ("Bắc Ninh",        21.061, 106.201, "Gia Binh, Bac Ninh",      "Gia Bình, Bắc Ninh"),
    ("Nga My",          21.458, 105.954, "Phu Binh, Thai Nguyen",   "Phú Bình, Thái Nguyên"),
    ("Thái Nguyên",     21.458, 105.954, "Phu Binh, Thai Nguyen",   "Phú Bình, Thái Nguyên"),
    ("TP HCM",          10.776, 106.701, "Ho Chi Minh City",        "TP HCM"),
    ("HCMC",            10.776, 106.701, "Ho Chi Minh City",        "TP HCM"),
    ("Thâm Quyến",      22.543, 114.058, "Shenzhen, China",         "Thâm Quyến, TQ"),
    ("Shenzhen",        22.543, 114.058, "Shenzhen, China",         "Thâm Quyến, TQ"),
    ("Quảng Châu",      23.129, 113.264, "Guangzhou, China",        "Quảng Châu, TQ"),
    ("Guangzhou",       23.129, 113.264, "Guangzhou, China",        "Quảng Châu, TQ"),
    ("Vịnh lớn",        22.800, 113.400, "Greater Bay Area, China", "Vùng Vịnh lớn (GBA)"),
    ("GBA",             22.800, 113.400, "Greater Bay Area, China", "Vùng Vịnh lớn (GBA)"),
    ("Dubai",           25.253,  55.365, "Dubai (DXB), UAE",        "Dubai (DXB), UAE"),
    ("DXB",             25.253,  55.365, "Dubai (DXB), UAE",        "Dubai (DXB), UAE"),
    ("Cotswold",        51.668,  -2.057, "Cotswold, United Kingdom","Cotswold, Anh"),
    ("Gavião",         -21.840, -48.500, "São Paulo state, Brazil", "São Paulo, Brazil"),
    ("São Paulo",      -21.840, -48.500, "São Paulo state, Brazil", "São Paulo, Brazil"),
    ("Bruchsal",        49.124,   8.598, "Bruchsal, Germany",       "Bruchsal, Đức"),
    ("Munich",          48.137,  11.576, "Munich area, Germany",    "Munich, Đức"),
    ("United States",   39.830, -98.580, "United States",           "Hoa Kỳ"),
]


def geocode(location):
    for kw, lat, lon, en, vn in GEO:
        if kw in location:
            return lat, lon, en, vn
    return None


def load_entities(domain):
    """Group claims by entity → {field: value}. First value per (entity,field); first claim with a
    capture.url is the representative source. Matches how the points need name/type/status/source."""
    rows = [json.loads(l) for l in (HERE / "domains" / domain / "claims.jsonl")
            .read_text(encoding="utf-8").splitlines() if l.strip()]
    by = collections.OrderedDict()
    for r in rows:
        by.setdefault(r["entity"], []).append(r)
    out = []
    for ent, rs in by.items():
        f = {}
        for r in rs:
            f.setdefault(r["field"], r.get("value"))
        src = next(({"url": (r.get("capture") or {}).get("url"),
                     "source": (r.get("capture") or {}).get("source"),
                     "tier": r.get("tier")}
                    for r in rs if (r.get("capture") or {}).get("url")), None)
        fetched = [(r.get("capture") or {}).get("fetched_at") for r in rs
                   if (r.get("capture") or {}).get("fetched_at")]
        out.append((ent, f, src, max(fetched) if fetched else None))
    return out


def main(out_path):
    points = []
    non_located = []
    skipped = []
    last_capture = None
    for domain in DOMAINS:
        for ent, f, src, fetched in load_entities(domain):
            if fetched and (last_capture is None or fetched > last_capture):
                last_capture = fetched
            loc = f.get("location")
            if not loc:
                # STEP 5 stream: real, sourced, but un-mappable (a decree sits nowhere on a map).
                # Surface it beside the map rather than hide it — no entity vanishes, no point invented.
                non_located.append({
                    "name": f.get("name") or ent,
                    "entity_type": f.get("entity_type"),
                    "stratum": f.get("stratum"),
                    "tier": (src or {}).get("tier"),
                    "scope": f.get("scope"),
                    "issuer": f.get("issuer"),
                    "doc_id": f.get("doc_id"),
                    "source": (src or {}).get("source"),
                    "url": (src or {}).get("url"),
                })
                continue
            geo = geocode(loc)
            if not geo:
                skipped.append((domain, ent, loc))
                continue
            lat, lon, place_en, place_vn = geo
            points.append({
                "name": f.get("name") or ent,
                "entity_type": f.get("entity_type"),
                "stratum": f.get("stratum"),
                "status": f.get("status"),
                "sector": f.get("sector"),
                "location": loc,
                "place_en": place_en,
                "place_vn": place_vn,
                "lat": round(lat, 3),
                "lon": round(lon, 3),
                "date": f.get("date"),
                "source": (src or {}).get("source"),
                "url": (src or {}).get("url"),
                "tier": (src or {}).get("tier"),
                "map_layer": True,
            })
    # deterministic order: stratum (vn, world, china) then name
    order = {"vietnam": 0, "world": 1, "china": 2}
    points.sort(key=lambda p: (order.get(p["stratum"], 9), p["name"]))
    non_located.sort(key=lambda p: (order.get(p["stratum"], 9),
                                    p.get("entity_type") or "", p["name"]))
    doc = {
        "generated_by": "refinery/export_monitor.py",
        "note": "Mode L source. Each point is a real registry entity with provenance; entities without "
                "a location do not plot but are listed in non_located. Geocode is a curated table.",
        "last_capture": last_capture,   # max fetched_at across the registry — the REAL 'last updated'
        "count": len(points),
        "non_located_count": len(non_located),
        "points": points,
        "non_located": non_located,
    }
    out_path = pathlib.Path(out_path)
    out_path.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    by_stratum = collections.Counter(p["stratum"] for p in points)
    print(f"export_monitor: {len(points)} points + {len(non_located)} non-located → {out_path}")
    print(f"  by stratum: {dict(by_stratum)} · last_capture={last_capture}")
    if skipped:
        print(f"  SKIPPED (located but un-geocoded — add to GEO table):")
        for d, e, l in skipped:
            print(f"    [{d}] {e[:40]} · location={l!r}")
    else:
        print("  every located entity geocoded (0 dropped).")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else DEFAULT_OUT))
