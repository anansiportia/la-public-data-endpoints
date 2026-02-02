#!/usr/bin/env python3
import json, re, subprocess, time
from difflib import SequenceMatcher
from urllib.parse import urlparse

IN_PATH = "/Users/anansi/.openclaw/workspace/madnessbot_end_user_leads_global_100.json"
OUT_PATH = "/Users/anansi/.openclaw/workspace/madnessbot_end_user_leads_global_100_enriched.json"
SHEET_PATH = "/Users/anansi/.openclaw/workspace/madnessbot_end_user_leads_global_100_enriched_sheet_values.json"
SHEET_COMPACT_PATH = "/Users/anansi/.openclaw/workspace/madnessbot_end_user_leads_global_100_enriched_sheet_values_compact.json"
OUT_COMPACT_PATH = "/Users/anansi/.openclaw/workspace/madnessbot_end_user_leads_global_100_enriched_compact.json"

HEADERS = [
    "Tier",
    "Name",
    "Type",
    "Region",
    "Primary Channel",
    "Links",
    "Phone",
    "Email",
    "Contact Form URL",
    "Best Contact",
    "Pitch angle / CTA",
    "Notes",
]

EMAIL_RE = re.compile(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", re.I)

REGION_CODE_MAP = {
    "USA": "US",
    "UNITED STATES": "US",
    "CANADA": "CA",
    "UK": "GB",
    "UNITED KINGDOM": "GB",
    "ENGLAND": "GB",
    "SCOTLAND": "GB",
    "WALES": "GB",
    "GERMANY": "DE",
    "FRANCE": "FR",
    "SPAIN": "ES",
    "ITALY": "IT",
    "MEXICO": "MX",
    "BRAZIL": "BR",
    "SOUTH AFRICA": "ZA",
    "INDIA": "IN",
    "AUSTRALIA": "AU",
}


def shell_json(cmd, timeout_s: float = 6.5):
    p = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=timeout_s,
    )
    if p.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(cmd)}\n{p.stderr.strip()}")
    out = p.stdout.strip()
    if not out:
        return None
    return json.loads(out)


def norm_name(s: str) -> str:
    s = s or ""
    # remove parenthetical descriptors
    s = re.sub(r"\s*\([^)]*\)", "", s)
    s = s.replace("'", "").replace("\u2019", "")
    s = re.sub(r"\s+", " ", s).strip().lower()
    return s


def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, norm_name(a), norm_name(b)).ratio()


def region_code(region_str: str) -> str:
    if not region_str:
        return ""
    up = region_str.upper()
    for key, code in REGION_CODE_MAP.items():
        if key in up:
            return code
    return ""


def pick_contact_form_url(links):
    if not links:
        return ""
    # prioritize explicit contact-ish paths
    candidates = []
    for u in links:
        if not isinstance(u, str):
            continue
        path = urlparse(u).path.lower()
        score = 0
        if "contact" in path or "contatti" in path or "kontakt" in path or "contato" in path:
            score += 5
        if "about" in path:
            score += 1
        if score:
            candidates.append((score, u))
    if candidates:
        candidates.sort(reverse=True)
        return candidates[0][1]
    return ""


def is_business_entry(item):
    t = (item.get("Type") or "").lower()
    return ("shop" in t) or ("mobile mechanic" in t) or ("independent repair shop" in t)


def enrich_with_places(name, region, typ):
    # Return (phone, website, chosen_place_id, chosen_place_name)
    q_name = re.sub(r"\s*\([^)]*\)", "", name).strip()
    region_txt = region or ""
    rcode = region_code(region_txt)

    # Prefer a single fast query; fall back once.
    queries = [
        f"{q_name} {region_txt}",
        f"{q_name} {region_txt} auto repair",
    ]

    best = None
    best_meta = None

    for q in queries:
        cmd = ["goplaces", "--timeout=4s", "search", q, "--limit=8", "--keyword=auto repair", "--type=car_repair", "--json"]
        if rcode:
            cmd.insert(-1, f"--region={rcode}")

        try:
            results = shell_json(cmd)
        except Exception:
            results = []

        if not results:
            continue

        for cand in results:
            s = similarity(name, cand.get("name", ""))
            types = cand.get("types") or []
            if "car_repair" in types:
                s += 0.08
            if region_txt and isinstance(cand.get("address"), str):
                city = region_txt.split(",")[0].strip().lower()
                if city and city in cand["address"].lower():
                    s += 0.03
            if best is None or s > best:
                best = s
                best_meta = cand

        if best is not None and best >= 0.90:
            break

    if not best_meta or best is None or best < 0.60:
        return "", "", "", ""

    place_id = best_meta.get("place_id")
    if not place_id:
        return "", "", "", ""

    det_cmd = ["goplaces", "--timeout=4s", "details", place_id, "--json"]
    if rcode:
        det_cmd.insert(-1, f"--region={rcode}")
    details = shell_json(det_cmd) or {}

    phone = details.get("phone") or ""
    website = details.get("website") or ""
    return phone, website, place_id, (details.get("name") or best_meta.get("name") or "")


def extract_email(contact: str) -> str:
    if not contact:
        return ""
    m = EMAIL_RE.search(contact)
    return m.group(0) if m else ""


def best_contact(primary_channel: str, phone: str, email: str, contact_form_url: str, links):
    pc = (primary_channel or "").lower()
    if email:
        return email
    if phone and ("phone" in pc or "call" in pc or "phone/" in pc):
        return phone
    if contact_form_url:
        return contact_form_url
    if phone:
        return phone
    if links and isinstance(links, list) and links:
        return links[0]
    return ""


def main():
    with open(IN_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    enriched = []
    phone_found = 0
    website_found = 0
    email_found = 0

    # Cache Places lookups to avoid re-querying duplicates (e.g., shop + YouTube entries).
    places_cache = {}

    for idx, item in enumerate(data, 1):
        if idx % 5 == 0:
            print(f"…processed {idx}/{len(data)}", flush=True)
        name = item.get("Name", "")
        region = item.get("Region", "")
        typ = item.get("Type", "")
        links = item.get("Links") or []
        primary = item.get("Primary Channel", "")
        contact = item.get("Contact", "")

        email = extract_email(contact)
        if email:
            email_found += 1

        phone = ""
        website = ""

        if is_business_entry(item):
            cache_key = (norm_name(name), (region or "").strip().lower())
            if cache_key in places_cache:
                phone, website = places_cache[cache_key]
            else:
                try:
                    phone, website, pid, pname = enrich_with_places(name, region, typ)
                except Exception:
                    phone, website = "", ""
                places_cache[cache_key] = (phone, website)

            if phone:
                phone_found += 1
            if website:
                website_found += 1

            # If website exists and not already in links, append.
            if website and (website not in links):
                links = links + [website]

        contact_form_url = pick_contact_form_url(links)
        best = best_contact(primary, phone, email, contact_form_url, links)

        row = {
            "Tier": item.get("Tier", ""),
            "Name": name,
            "Type": typ,
            "Region": region,
            "Primary Channel": primary,
            "Links": links,
            "Phone": phone,
            "Email": email,
            "Contact Form URL": contact_form_url,
            "Best Contact": best,
            "Pitch angle / CTA": item.get("Pitch angle / CTA", ""),
            "Notes": item.get("Notes", ""),
        }
        enriched.append(row)

        # gentle throttle
        if is_business_entry(item):
            time.sleep(0.05)

    # write enriched
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(enriched, f, ensure_ascii=False, indent=2)
    with open(OUT_COMPACT_PATH, "w", encoding="utf-8") as f:
        json.dump(enriched, f, ensure_ascii=False, separators=(",", ":"))

    sheet_values = [HEADERS]
    for r in enriched:
        sheet_values.append([r.get(h, "") for h in HEADERS])
    with open(SHEET_PATH, "w", encoding="utf-8") as f:
        json.dump(sheet_values, f, ensure_ascii=False, indent=2)
    with open(SHEET_COMPACT_PATH, "w", encoding="utf-8") as f:
        json.dump(sheet_values, f, ensure_ascii=False, separators=(",", ":"))

    summary = {
        "rows": len(enriched),
        "phone_found": phone_found,
        "website_found": website_found,
        "email_found": email_found,
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
