#!/usr/bin/env python3
"""verify_sources.py — TIP-NEWS-REALTIME Task 6 · validate shape sources.yaml (fail-loud exit 2).
KHÔNG cào (scheduler #2 dựng sau) — chỉ kiểm config hợp-lệ: mỗi nguồn đủ trường, tier/stratum/branch
enum, và url là BÀI CỤ-THỂ (có path), không phải domain root (bài học seed #3)."""
import sys
from pathlib import Path
from urllib.parse import urlparse
import yaml

HERE = Path(__file__).resolve().parent
F = HERE / "sources.yaml"
TIER = {"A", "B", "C"}
STRAT = {"vietnam", "world", "china"}
BRANCH = {"policy", "market", "incident"}


def main():
    if not F.exists():
        sys.exit("SOURCES_MISSING: sources.yaml không tồn-tại")
    doc = yaml.safe_load(F.read_text(encoding="utf-8")) or {}
    srcs = doc.get("sources") or []
    if not srcs:
        sys.exit("SOURCES_EMPTY: sources.yaml không có nguồn nào")
    for i, s in enumerate(srcs):
        tag = f"source#{i} ({s.get('outlet','?')})"
        for k in ("url", "stratum", "branch", "tier", "outlet"):
            if not s.get(k):
                sys.exit(f"SOURCE_FIELD_MISSING · {tag}: thiếu {k!r}")
        if s["tier"] not in TIER:
            sys.exit(f"SOURCE_TIER_BAD · {tag}: tier {s['tier']!r} ∉ A/B/C")
        if s["stratum"] not in STRAT:
            sys.exit(f"SOURCE_STRATUM_BAD · {tag}: stratum {s['stratum']!r} ∉ vietnam/world/china")
        if s["branch"] not in BRANCH:
            sys.exit(f"SOURCE_BRANCH_BAD · {tag}: branch {s['branch']!r} ∉ policy/market/incident")
        u = urlparse(s["url"])
        path = u.path.strip("/")
        # bài CỤ-THỂ = có path đủ dài HOẶC có query (gov/CMS để doc-id trong ?docid=...). Root THẬT = cả hai rỗng.
        if (not path or len(path) < 4) and not u.query:
            sys.exit(f"SOURCE_URL_ROOT · {tag}: url {s['url']!r} là domain root, cần BÀI cụ-thể (gov root fetch rỗng)")
    print(f"SOURCES PASS: {len(srcs)} nguồn · đủ trường · tier/stratum/branch enum · url là bài cụ-thể (0 root).")


if __name__ == "__main__":
    main()
