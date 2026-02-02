// OpenClaw hook transform: Gmail filter
// - Quiet hours: 23:00–08:00 America/Los_Angeles
// - Newsletter-ish: skip if it looks like bulk mail (very heuristic)
// Return null to skip the hook entirely.

function hourInTZ(date, timeZone) {
  const parts = new Intl.DateTimeFormat("en-US", {
    timeZone,
    hour: "2-digit",
    hour12: false,
  }).formatToParts(date);
  const hh = parts.find((p) => p.type === "hour")?.value;
  return hh ? Number(hh) : date.getHours();
}

function str(x) {
  return typeof x === "string" ? x : "";
}

function looksLikeNewsletter({ from, subject, snippet, body }) {
  const text = `${from}\n${subject}\n${snippet}\n${body}`.toLowerCase();

  // Strong-ish indicators
  const needles = [
    "unsubscribe",
    "manage preferences",
    "email preferences",
    "view in browser",
    "marketing",
    "you are receiving this",
    "update your preferences",
    "privacy policy",
  ];

  if (needles.some((n) => text.includes(n))) return true;

  // Weak indicators (require a couple)
  const weak = ["newsletter", "promo", "promotion", "sale", "deal", "% off", "free shipping", "limited time"];
  const weakHits = weak.filter((n) => text.includes(n)).length;
  if (weakHits >= 2) return true;

  // From address patterns
  const fromLower = from.toLowerCase();
  if (fromLower.includes("no-reply") || fromLower.includes("noreply")) {
    if (text.includes("unsubscribe") || text.includes("preferences")) return true;
  }

  return false;
}

export default async function transform(ctx) {
  const tz = "America/Los_Angeles";
  const hour = hourInTZ(new Date(), tz);

  const msg0 = (ctx?.payload?.messages && ctx.payload.messages[0]) || {};
  const from = str(msg0.from);
  const subject = str(msg0.subject);
  const snippet = str(msg0.snippet);
  const body = str(msg0.body);

  // Quiet hours: 11pm–8am local
  // Allow test pings to bypass quiet hours.
  const subjLower = subject.toLowerCase();
  const isTestPing = subjLower.startsWith("ping") || subjLower.includes("test");
  if (!isTestPing && (hour >= 23 || hour < 8)) {
    // If you want an exception list later (e.g., specific senders), add it here.
    return null;
  }

  // Newsletter block
  if (looksLikeNewsletter({ from, subject, snippet, body })) {
    return null;
  }

  // No overrides needed; proceed with base mapping.
  return {};
}
