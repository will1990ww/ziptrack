/* =====================================================================
   Balcony Master — Cloudflare Worker: secure form endpoint
   ---------------------------------------------------------------------
   A production alternative to FormSubmit. Validates uploads server-side
   (type, size, count), blocks spam (honeypot + basic rate note), then
   emails you via MailChannels (free from Cloudflare Workers) OR forwards
   to your CRM/webhook. No customer data is stored on disk.

   DEPLOY (5 min):
   1. dash.cloudflare.com -> Workers & Pages -> Create -> Worker.
   2. Paste this file. Set these Variables (Settings -> Variables):
        TO_EMAIL   = enquiry@lionsin.com.sg
        FROM_EMAIL = no-reply@lionsin.com.sg   (must be on your domain)
        ALLOW_ORIGIN = https://www.lionsin.com.sg
   3. (MailChannels now needs a domain lockdown DNS TXT record — see
      https://developers.cloudflare.com/ ; or swap sendEmail() for your
      provider: Resend, SendGrid, Postmark, or a Google Apps Script URL.)
   4. Route it, e.g. https://form.lionsin.com.sg/  (Workers route/subdomain).
   5. In the website form, change action="" to your Worker URL and keep
      method="POST" enctype="multipart/form-data". Remove the FormSubmit
      hidden fields (_subject/_next/_template) — this Worker handles them.
   ===================================================================== */

const MAX_FILES = 6;
const MAX_FILE_BYTES = 10 * 1024 * 1024;      // 10 MB each
const MAX_TOTAL_BYTES = 25 * 1024 * 1024;     // 25 MB total
const ALLOWED_TYPES = ["image/jpeg", "image/png", "image/webp", "application/pdf"];
const ALLOWED_EXT = ["jpg", "jpeg", "png", "webp", "pdf"];

// File "magic number" signatures (defence-in-depth: don't trust the MIME/ext alone)
function sniff(bytes) {
  const b = new Uint8Array(bytes.slice(0, 12));
  const hex = (n) => b[n].toString(16).padStart(2, "0");
  if (b[0] === 0xff && b[1] === 0xd8 && b[2] === 0xff) return "image/jpeg";
  if (b[0] === 0x89 && b[1] === 0x50 && b[2] === 0x4e && b[3] === 0x47) return "image/png";
  if (b[0] === 0x25 && b[1] === 0x50 && b[2] === 0x44 && b[3] === 0x46) return "application/pdf"; // %PDF
  if (b[0] === 0x52 && b[1] === 0x49 && b[2] === 0x46 && b[3] === 0x46 &&
      b[8] === 0x57 && b[9] === 0x45 && b[10] === 0x42 && b[11] === 0x50) return "image/webp"; // RIFF....WEBP
  return null;
}
const esc = (s) => String(s || "").replace(/[<>&]/g, (c) => ({ "<": "&lt;", ">": "&gt;", "&": "&amp;" }[c]));

export default {
  async fetch(request, env) {
    const origin = env.ALLOW_ORIGIN || "*";
    const cors = {
      "Access-Control-Allow-Origin": origin,
      "Access-Control-Allow-Methods": "POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type, X-BM-Ajax",
    };
    if (request.method === "OPTIONS") return new Response(null, { headers: cors });
    if (request.method !== "POST") return new Response("Method not allowed", { status: 405, headers: cors });

    let form;
    try { form = await request.formData(); }
    catch { return json({ ok: false, error: "Bad form data" }, 400, cors); }

    // Honeypot: silently accept (don't tell bots)
    if (form.get("company_website") || form.get("_honey")) return json({ ok: true }, 200, cors);

    // Required fields
    const name = (form.get("name") || "").toString().trim();
    const mobile = (form.get("mobile") || "").toString().trim();
    const property = (form.get("property") || "").toString().trim();
    const service = (form.get("service") || "").toString().trim();
    if (!mobile || !/[0-9]{7,}/.test(mobile.replace(/\s/g, "")))
      return json({ ok: false, error: "Valid mobile number required" }, 422, cors);
    if (!property) return json({ ok: false, error: "Property type required" }, 422, cors);
    if (form.get("consent") == null) return json({ ok: false, error: "Consent required" }, 422, cors);

    // Validate files
    const files = form.getAll("attachments").filter((f) => f && typeof f === "object" && "arrayBuffer" in f);
    if (files.length > MAX_FILES) return json({ ok: false, error: "Too many files (max " + MAX_FILES + ")" }, 422, cors);
    let total = 0; const attachments = [];
    for (const f of files) {
      if (!f.size) continue;
      if (f.size > MAX_FILE_BYTES) return json({ ok: false, error: f.name + " is over 10 MB" }, 422, cors);
      total += f.size;
      if (total > MAX_TOTAL_BYTES) return json({ ok: false, error: "Total upload over 25 MB" }, 422, cors);
      const ext = (f.name.split(".").pop() || "").toLowerCase();
      if (!ALLOWED_EXT.includes(ext)) return json({ ok: false, error: "Blocked file type: " + f.name }, 422, cors);
      const buf = await f.arrayBuffer();
      const real = sniff(buf);
      if (!real || !ALLOWED_TYPES.includes(real))
        return json({ ok: false, error: "File content check failed: " + f.name }, 422, cors);
      const safeName = f.name.replace(/[^a-zA-Z0-9._-]/g, "_").slice(0, 80);
      attachments.push({ filename: safeName, type: real, content: b64(buf) });
    }

    const summary =
      `New balcony enquiry\n\nName: ${name || "-"}\nMobile: ${mobile}\nProperty: ${property}\nService: ${service || "-"}\n` +
      `Files: ${attachments.length}\nTime: ${new Date().toISOString()}`;

    try {
      await sendEmail(env, summary, attachments, name, mobile);
    } catch (e) {
      return json({ ok: false, error: "Send failed", detail: String(e) }, 502, cors);
    }
    // JS (fetch) requests get a clean JSON 200; no-JS native form POSTs get a redirect.
    if (request.headers.get("x-bm-ajax")) return json({ ok: true }, 200, cors);
    return Response.redirect((env.THANKYOU_URL || "https://www.lionsin.com.sg/thank-you.html"), 303);
  },
};

function json(o, status, cors) {
  return new Response(JSON.stringify(o), { status, headers: { "Content-Type": "application/json", ...cors } });
}
function b64(buf) {
  let s = ""; const b = new Uint8Array(buf);
  for (let i = 0; i < b.length; i++) s += String.fromCharCode(b[i]);
  return btoa(s);
}
// MailChannels (free from CF Workers). Swap for Resend/SendGrid if preferred.
async function sendEmail(env, text, attachments, name, mobile) {
  const body = {
    personalizations: [{ to: [{ email: env.TO_EMAIL }] }],
    from: { email: env.FROM_EMAIL, name: "Balcony Master Website" },
    reply_to: { email: env.TO_EMAIL, name: name || mobile },
    subject: "New balcony enquiry — lionsin.com.sg",
    content: [{ type: "text/plain", value: text }],
    attachments: attachments.map((a) => ({ filename: a.filename, type: a.type, content: a.content })),
  };
  const r = await fetch("https://api.mailchannels.net/tx/v1/send", {
    method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body),
  });
  if (!r.ok) throw new Error("MailChannels " + r.status + " " + (await r.text()));
}
