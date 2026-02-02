# MEMORY.md - Long-Term Memory

## 2026-02-01 — OpenClaw + MadnessBot Ops
- OpenClaw Control UI is exposed on LAN at http://192.168.1.155:18789/ with gatewayUrl ws://192.168.1.155:18789; insecure auth allowed (token still required). Tokenized URL works for first login; bookmark without token works after it’s stored in browser localStorage.
- Google Places key is configured; goplaces works. HubSpot integration installed and authenticated; portalId 245059996 (na2). Created private app “OpenClaw Affiliate Outreach.”
- HubSpot: Affiliate Recruiting pipeline created (id 1913318101). Starter plan cap = 2 pipelines (cannot add third). End-user deals live in default Sales pipeline (dealstage appointmentscheduled). Custom deal property mb_campaign added for campaign separation (end_user_acquisition).
- Google Sheet system of record: https://docs.google.com/spreadsheets/d/1kEpuM0bJRPZ5QJMi6oI10Arw3Tw6wd-M5YCNuv_wn-o/edit (Sheet1 affiliates, Sheet2 end-user leads).
- End-user leads (100) enriched via Google Places and imported; links stored as pipe-delimited string in Sheets; HubSpot contacts updated (email conflicts stripped).
- GitHub backup: repo https://github.com/anansiportia/openclaw-workspace is private; nightly cron job runs 2:00 AM America/Los_Angeles (job id 4405cc8d-78cc-4b73-9d23-9ef6c602dcc4).
- Reddit: logged in as u/Careless-Mail-6308; display name “MadnessBot.” r/MechanicAdvice is target; drafts only, approval required before posting.
- Default model currently set to openai-codex/gpt-5.2-codex; Kimi K2 Thinking available via Moonshot.
