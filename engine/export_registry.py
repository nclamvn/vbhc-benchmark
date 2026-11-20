#!/usr/bin/env python3
"""export_registry.py — refinery → portal LAE registry ingest (TIP-FP1.5).

ONE-WAY (strategy §8 wall): reads the 3 lae domains, builds each registry via refinery.build (so the
provenance the REF1–4 work established — per-field tier/source/state and the DISPUTED cells — is kept,
NOT flattened), and emits portal/content/lae-registry.json. DATA ONLY: no card/page/desk render (that
is FP1). The portal reads this file; refinery never reads the portal.

Run:  python3 export_registry.py [out.json]   (default: the portal content path below)
"""
import json, sys, pathlib, collections
import refinery

HERE = pathlib.Path(__file__).resolve().parent
DOMAINS = ["lae-vn", "lae-world", "lae-cn"]
DEFAULT_OUT = pathlib.Path("/Users/os/RtR/rtr-news/portal/content/lae-registry.json")

# convenience fields surfaced at the entity head (each STILL carries full provenance inside fields{})
HEAD = ["name", "stratum", "status", "scope", "sector", "date", "location",
        "issuer", "doc_id", "role", "unit", "value", "denominator", "severity", "cause"]


def _val(cell):
    return cell.get("value") if cell.get("state") in ("sourced", "corroborated") else None


def _strongest(tiers):
    order = [t for t in tiers if t in ("A", "B", "C")]
    return min(order) if order else (tiers[0] if tiers else None)   # A<B<C


def main(out_path):
    entities = []
    by_ts = collections.Counter()
    for domain in DOMAINS:
        ddir = HERE / "domains" / domain
        cfg, claims = refinery.load_domain(ddir)
        # R_EXPORT_UNVERIFIED (TIP-NEWS-REALTIME Task 4) — claim auto-draft PHẢI qua người-xác ngữ-cảnh
        # trước khi ra portal (§1.4: gate-máy bắt span/tier; mắt-người bắt quote-out-of-context). Claim
        # trích-tay REF1→5 không mang cờ auto_draft → miễn; chỉ auto-draft chưa human_verified bị chặn.
        unverified = [c for c in claims if c.get("auto_draft") and not c.get("human_verified")]
        if unverified:
            ex = unverified[0]
            sys.exit(f"R_EXPORT_UNVERIFIED · {domain}: {len(unverified)} claim auto-draft CHƯA human_verified "
                     f"(vd entity={ex.get('entity')!r} field={ex.get('field')!r}) — chạy review.py duyệt staging trước export.")
        registry = refinery.build(cfg, claims)                 # provenance + disputed preserved
        # raw captures keyed (canonical entity, field) — to carry url + fetched_at, not just source/tier
        cap = collections.defaultdict(list)
        for c in claims:
            ent = refinery.canonicalize(cfg, c["entity"])
            capd = c.get("capture") or {}
            cap[(ent, c["field"])].append({"source": capd.get("source"), "tier": c.get("tier"),
                                           "url": capd.get("url"), "date": capd.get("fetched_at")})
        for ent, rec in registry.items():
            fields_out = {}
            for f, cell in rec["fields"].items():
                if cell["state"] == "null":
                    continue                                   # honest-null: absent field is simply absent
                srcs = cap.get((ent, f), [])
                fo = {"state": cell["state"], "value": cell.get("value"),
                      "tier": _strongest([s["tier"] for s in srcs]),
                      "sources": srcs}
                if cell["state"] == "disputed":
                    fo["claims"] = cell.get("claims")          # keep the competing values, do NOT pick one
                fields_out[f] = fo
            head = {k: _val(rec["fields"].get(k, {"state": "null"})) for k in HEAD}
            et, strat = rec["entity_type"], head.get("stratum")
            by_ts[(et, strat)] += 1
            entities.append({"entity": ent, "entity_type": et, **head, "fields": fields_out})
    entities.sort(key=lambda e: ((e.get("stratum") or ""), (e.get("entity_type") or ""), e["entity"]))
    doc = {
        "generated_by": "refinery/export_registry.py",
        "wall": "portal <- refinery (one-way); refinery is the source of truth, portal is a mirror",
        "count": len(entities),
        "by_type_stratum": {f"{et}|{st}": n for (et, st), n in sorted(by_ts.items(), key=lambda x: str(x[0]))},
        "entities": entities,
    }
    out_path = pathlib.Path(out_path)
    out_path.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"export_registry: {len(entities)} LAE entities → {out_path}")
    for (et, st), n in sorted(by_ts.items(), key=lambda x: (str(x[0][1]), str(x[0][0]))):
        print(f"   {str(st):10} {str(et):16} {n}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else DEFAULT_OUT))
