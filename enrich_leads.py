import json, re, ssl, time, socket, signal, os
from urllib.parse import urlparse, urljoin
from urllib.request import Request, urlopen
from html.parser import HTMLParser

INPUT_PATH = "/Users/anansi/.openclaw/workspace/madnessbot_end_user_leads_global_100.json"
OUTPUT_PATH = "/Users/anansi/.openclaw/workspace/madnessbot_end_user_leads_global_100_enriched.json"
SHEET_PATH = "/Users/anansi/.openclaw/workspace/madnessbot_end_user_leads_global_100_enriched_sheet_values.json"

socket.setdefaulttimeout(6)

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0 Safari/537.36"

EMAIL_RE = re.compile(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", re.I)
PHONE_RE = re.compile(r"(?:(?:\+\s?\d{1,3})|(?:\(\s?\d{1,4}\s?\))|\d{2,4})[\s\-\.]*(?:\d[\s\-\.]*){6,12}\d")

CONTACT_HINTS = [
    "contact", "contact-us", "contactus", "kontakt", "contatti", "contatto", "contato", "contac", "impressum",
    "get-in-touch", "enquiries", "inquiries", "support", "help", "locations", "location", "schedule", "booking"
]

COMMON_CONTACT_PATHS = [
    "/contact", "/contact/", "/contact-us", "/contact-us/", "/contactus", "/contactus/",
    "/kontakt", "/kontakt/", "/contatti", "/contatti/", "/contatto", "/contatto/",
]

ctx = ssl.create_default_context()
ctx.check_hostname = True
ctx.verify_mode = ssl.CERT_REQUIRED

class Timeout(Exception):
    pass

def _alarm_handler(signum, frame):
    raise Timeout()

signal.signal(signal.SIGALRM, _alarm_handler)

class LinkExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs = []
    def handle_starttag(self, tag, attrs):
        if tag.lower() != "a":
            return
        d = dict(attrs)
        href = d.get("href")
        if href:
            self.hrefs.append(href)

def fetch(url, timeout=6):
    try:
        req = Request(url, headers={"User-Agent": UA, "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"})
        with urlopen(req, timeout=timeout, context=ctx) as resp:
            ctype = resp.headers.get("Content-Type", "")
            data = resp.read(1_500_000)
        m = re.search(r"charset=([\w\-]+)", ctype, re.I)
        enc = m.group(1) if m else "utf-8"
        try:
            return data.decode(enc, errors="replace")
        except Exception:
            return data.decode("utf-8", errors="replace")
    except Exception:
        return None

def root_domain_for(url):
    return urlparse(url).netloc.lower()

def same_domain(url, root_domain):
    try:
        return urlparse(url).netloc.lower().endswith(root_domain)
    except Exception:
        return False

def canonicalize_phone(s):
    s2 = re.sub(r"[^0-9+]+", "", s)
    digits = re.sub(r"\D", "", s2)
    if len(digits) < 7:
        return None
    if s2.count("+") > 1:
        s2 = "+" + re.sub(r"\+", "", s2)
    return s2

def extract_contacts(html):
    html = html or ""
    emails = set(m.group(0) for m in EMAIL_RE.finditer(html))
    emails = set(e for e in emails if not e.lower().endswith("example.com"))
    phones = set()
    for m in PHONE_RE.finditer(html):
        ph = canonicalize_phone(m.group(0))
        if ph:
            phones.add(ph)
    return emails, phones

def extract_internal_links(base_url, html, root_domain):
    if not html:
        return []
    parser = LinkExtractor()
    try:
        parser.feed(html)
    except Exception:
        return []
    out = []
    for href in parser.hrefs:
        href = href.strip()
        if not href or href.startswith("mailto:") or href.startswith("tel:"):
            continue
        full = urljoin(base_url, href).split('#')[0]
        if same_domain(full, root_domain):
            out.append(full)
    seen = set()
    uniq = []
    for u in out:
        if u in seen:
            continue
        seen.add(u)
        uniq.append(u)
    return uniq

def pick_best_email(emails):
    if not emails:
        return None
    prefs = ["info@", "contact@", "service@", "support@", "hello@", "sales@", "booking@", "appointments@"]
    for p in prefs:
        for e in emails:
            if e.lower().startswith(p):
                return e
    return sorted(emails, key=lambda x: (len(x), x.lower()))[0]

def pick_best_phone(phones):
    if not phones:
        return None
    def score(p):
        digits = len(re.sub(r"\D", "", p))
        return (0 if p.strip().startswith("+") else 1, -digits, p)
    return sorted(phones, key=score)[0]

def choose_contact_pages(explicit_links, homepage, internal_links):
    pages = []
    for u in explicit_links:
        low = u.lower()
        if any(h in low for h in CONTACT_HINTS):
            pages.append(u)
    if homepage:
        pages.append(homepage)

    contactish = []
    other = []
    for u in internal_links:
        low = u.lower()
        if any(h in low for h in CONTACT_HINTS):
            contactish.append(u)
        elif any(k in low for k in ["about", "locations", "location", "hours", "directions"]):
            other.append(u)

    pages.extend(contactish[:2])
    pages.extend(other[:1])

    if homepage and not contactish:
        for p in COMMON_CONTACT_PATHS:
            pages.append(urljoin(homepage, p))

    seen = set()
    uniq = []
    for u in pages:
        if u in seen:
            continue
        seen.add(u)
        uniq.append(u)
    return uniq[:5]

def youtube_about_url(y):
    if "/about" in y:
        return y
    return y.rstrip("/") + "/about"

def enrich_one(item, polite_delay=0.08, per_lead_seconds=20):
    # hard cap time spent per lead
    signal.alarm(per_lead_seconds)
    try:
        links = item.get("Links") or []
        website_links = [u for u in links if "youtube.com" not in u and "youtu.be" not in u]
        youtube_links = [u for u in links if "youtube.com" in u or "youtu.be" in u]

        emails = set()
        phones = set()
        contact_form_url = None
        source_notes = []

        homepage = website_links[0] if website_links else None
        root_domain = root_domain_for(homepage) if homepage else None

        homepage_html = fetch(homepage) if homepage else None
        time.sleep(polite_delay)

        internal_links = extract_internal_links(homepage, homepage_html, root_domain) if (homepage and root_domain and homepage_html) else []
        pages_to_fetch = choose_contact_pages(website_links, homepage, internal_links)

        for url in pages_to_fetch:
            html = homepage_html if (url == homepage) else fetch(url)
            time.sleep(polite_delay)
            if not html:
                continue
            e, ph = extract_contacts(html)
            if e:
                emails |= e
                source_notes.append(f"email(s) on {url}")
            if ph:
                phones |= ph
                source_notes.append(f"phone(s) on {url}")

            if not contact_form_url:
                low = url.lower()
                if any(h in low for h in ["contact", "contact-us", "contactus", "kontakt", "contatt", "contato"]):
                    contact_form_url = url

        for y in youtube_links[:2]:
            about = youtube_about_url(y)
            html = fetch(about)
            time.sleep(polite_delay)
            if not html:
                continue
            e, ph = extract_contacts(html)
            if e:
                emails |= e
                source_notes.append(f"email(s) on YouTube About {about}")
            if ph:
                phones |= ph
                source_notes.append(f"phone(s) on YouTube About {about}")

        best_email = pick_best_email(emails)
        best_phone = pick_best_phone(phones)

        if best_email and best_phone:
            best_contact = f"Email ({best_email}) + Phone ({best_phone})"
        elif best_email:
            best_contact = f"Email ({best_email})"
        elif best_phone:
            best_contact = f"Phone ({best_phone})"
        elif contact_form_url:
            best_contact = "Website contact form"
        else:
            best_contact = item.get("Contact") or item.get("Primary Channel") or ""

        notes = item.get("Notes") or ""
        if source_notes:
            notes = (notes + ("; " if notes else "") + " | ".join(sorted(set(source_notes))))

        return {
            "Tier": item.get("Tier"),
            "Name": item.get("Name"),
            "Type": item.get("Type"),
            "Region": item.get("Region"),
            "Primary Channel": item.get("Primary Channel"),
            "Links": links,
            "Phone": best_phone,
            "Email": best_email,
            "Contact Form URL": contact_form_url,
            "Best Contact": best_contact,
            "Pitch angle / CTA": item.get("Pitch angle / CTA"),
            "Notes": notes,
        }
    except Timeout:
        # return minimally structured row
        return {
            "Tier": item.get("Tier"),
            "Name": item.get("Name"),
            "Type": item.get("Type"),
            "Region": item.get("Region"),
            "Primary Channel": item.get("Primary Channel"),
            "Links": item.get("Links"),
            "Phone": None,
            "Email": None,
            "Contact Form URL": None,
            "Best Contact": item.get("Contact") or item.get("Primary Channel") or "",
            "Pitch angle / CTA": item.get("Pitch angle / CTA"),
            "Notes": (item.get("Notes") or "") + ("; timed out while fetching pages"),
        }
    finally:
        signal.alarm(0)

def compute_counts(enriched):
    phone = sum(1 for r in enriched if r.get("Phone"))
    email = sum(1 for r in enriched if r.get("Email"))
    both = sum(1 for r in enriched if r.get("Phone") and r.get("Email"))
    neither = sum(1 for r in enriched if (not r.get("Phone")) and (not r.get("Email")))
    return {"phone": phone, "email": email, "both": both, "neither": neither}

def main():
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    enriched = []

    total = len(data)
    for i, item in enumerate(data, 1):
        out = enrich_one(item)
        enriched.append(out)

        has_phone = bool(out.get("Phone"))
        has_email = bool(out.get("Email"))
        print(f"{i}/{total} {out.get('Name')}: phone={'Y' if has_phone else 'n'} email={'Y' if has_email else 'n'}")

        if i % 10 == 0:
            with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
                json.dump(enriched, f, ensure_ascii=False, indent=2)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(enriched, f, ensure_ascii=False, indent=2)

    header = [
        "Tier", "Name", "Type", "Region", "Primary Channel", "Links", "Phone", "Email",
        "Contact Form URL", "Best Contact", "Pitch angle / CTA", "Notes"
    ]
    rows = [header]
    for r in enriched:
        rows.append([
            r.get("Tier"),
            r.get("Name"),
            r.get("Type"),
            r.get("Region"),
            r.get("Primary Channel"),
            json.dumps(r.get("Links"), ensure_ascii=False),
            r.get("Phone"),
            r.get("Email"),
            r.get("Contact Form URL"),
            r.get("Best Contact"),
            r.get("Pitch angle / CTA"),
            r.get("Notes"),
        ])

    with open(SHEET_PATH, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)

    counts = compute_counts(enriched)
    print("COUNTS", counts)

if __name__ == "__main__":
    main()
