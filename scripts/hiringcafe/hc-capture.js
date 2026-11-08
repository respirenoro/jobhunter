// HiringCafe capture helpers. Paste into the HiringCafe tab with the browser's
// JavaScript tool. Re-run after any page reload, since a reload drops the hook.
//
// How it works:
// 1. __hcHook() wraps window.fetch so every /api/ai-search/hydrate-jobs response
//    the page itself loads (one bulk response per tab or page) is kept in
//    window.__hcJobs, keyed by job id. No cards are clicked.
// 2. __hcList() prints one compact line per captured job, so duplicates can be
//    checked against the tracker and the sheet before anything is read in full.
// 3. __hcRead([ids]) fetches /api/job-description?id=<id> for each id, slowly,
//    and prints a FACTS header plus the full description text (no cap).
// 4. Click the page's own "Next page" button or switch Talent Agent tabs; the
//    hook keeps capturing.
//
// Settings: set window.__HOME_STATE (e.g. "Ohio") before reading so postings
// whose state list leaves out your state print a blocker instead of text.
// HiringCafe's internal API can change. If these calls stop returning data,
// fall back to opening each card and reading the side panel.

window.__HOME_STATE = window.__HOME_STATE || '';
window.__hcJobs = window.__hcJobs || {};

window.__hcHook = () => {
  if (window.__hcHooked) return 'already hooked';
  const orig = window.fetch;
  window.fetch = async (...args) => {
    const res = await orig(...args);
    try {
      const url = String(args[0] && args[0].url ? args[0].url : args[0]);
      if (url.includes('/api/ai-search/hydrate-jobs')) {
        res.clone().json().then((j) => {
          const walk = (o, d = 0) => {
            if (!o || typeof o !== 'object' || d > 6) return;
            if (Array.isArray(o)) { o.forEach((x) => walk(x, d + 1)); return; }
            if (o.id && (o.v5_processed_job_data || o.job_information)) { window.__hcJobs[o.id] = o; return; }
            Object.values(o).forEach((x) => walk(x, d + 1));
          };
          walk(j);
        }).catch(() => {});
      }
    } catch (e) {}
    return res;
  };
  window.__hcHooked = true;
  return 'hooked; now page or switch tabs so the page loads jobs';
};

window.__hcFacts = (n) => {
  const p = n.v5_processed_job_data || {};
  const money = (a, b, suf) => (a == null && b == null) ? null
    : (a == null ? '' : Math.round(a).toLocaleString()) + (b != null && b !== a ? '-' + Math.round(b).toLocaleString() : '') + suf;
  const pay = money(p.yearly_min_compensation, p.yearly_max_compensation, '/yr')
    || money(p.hourly_min_compensation, p.hourly_max_compensation, '/hr') || 'NOT LISTED';
  const states = (p.workplace_states || []).map((s) => s.replace(', US', ''));
  return [
    'PAY: ' + pay,
    'TYPE: ' + (p.commitment || []).join('/') + ' | ' + p.workplace_type + ' | seniority=' + p.seniority_level,
    'LOCATION: ' + (p.formatted_workplace_location || '').slice(0, 160) + ' | states(' + states.length + ')=' + states.join(',').slice(0, 200),
    'YOE: ' + p.min_industry_and_role_yoe + ' | certs=' + JSON.stringify(p.licenses_or_certifications || []),
    'DEMANDS: oral=' + p.oral_communication_level + ' | travel=' + p.air_travel_requirement + ' | eve=' + p.evening_shift_work + ' night=' + p.overnight_work + ' on-call=' + p.on_call_requirement,
    'OTHER: clearance=' + p.security_clearance + ' | visa=' + p.visa_sponsorship + ' | tools=' + (p.technical_tools || []).join(', ').slice(0, 200),
    'PUBLISHED: ' + p.estimated_publish_date + ' | APPLY: ' + (n.apply_url || ''),
  ].join('\n');
};

window.__hcBlocker = (n) => {
  const p = n.v5_processed_job_data || {};
  const states = (p.workplace_states || []).map((s) => s.replace(', US', ''));
  const why = [];
  if (n.is_expired) why.push('POSTING EXPIRED');
  if (window.__HOME_STATE && states.length > 0 && !states.includes(window.__HOME_STATE)) why.push('STATE LIST LEAVES OUT ' + window.__HOME_STATE);
  if (p.security_clearance && !['None', 'Not Mentioned'].includes(p.security_clearance)) why.push('CLEARANCE: ' + p.security_clearance);
  if (p.workplace_type && !/remote/i.test(p.workplace_type)) why.push('NOT REMOTE: ' + p.workplace_type);
  return why;
};

window.__hcList = () => Object.values(window.__hcJobs).map((n) => {
  const p = n.v5_processed_job_data || {};
  const pay = p.yearly_min_compensation ? '$' + Math.round(p.yearly_min_compensation / 1000) + 'k' : (p.hourly_min_compensation ? '$' + p.hourly_min_compensation + '/hr' : '-');
  const title = (n.job_information && n.job_information.title) || p.core_job_title || '';
  const co = (n.enriched_company_data && n.enriched_company_data.name) || p.company_name || '';
  return n.id + ' | ' + co + ' | ' + title + ' | ' + pay;
}).join('\n');

// Reads full descriptions with a pause between calls. Keep batches small and
// take breaks between them: bulk reading has triggered HiringCafe's security
// check before. If a security check or CAPTCHA appears, stop and tell the user.
window.__hcRead = async (ids, gapMs = 3500) => {
  const out = [];
  for (const id of ids) {
    const n = window.__hcJobs[id] || { id };
    let desc = '';
    try {
      const j = await fetch('/api/job-description?id=' + encodeURIComponent(id)).then((r) => r.json());
      const info = (j.job && j.job.job_information) || j.job_information || {};
      desc = (info.description || '').replace(/<[^>]+>/g, ' ').replace(/&nbsp;|&#xa0;/g, ' ').replace(/\s+/g, ' ').trim();
    } catch (e) { desc = '!! description fetch failed: ' + e; }
    const why = window.__hcBlocker(n);
    out.push('######## ' + id + '\n' + window.__hcFacts(n) + '\n'
      + (why.length ? 'BLOCKER (text not printed): ' + why.join(' | ') : 'TEXT (' + desc.length + ' chars, full): ' + desc));
    await new Promise((r) => setTimeout(r, gapMs));
  }
  return out.join('\n\n');
};

// Gets the employer apply URL behind HiringCafe's "Apply now" button without
// letting it open a new tab: records the URL window.open would have opened.
window.__hcCaptureOpen = () => {
  window.__hcOrigOpen = window.__hcOrigOpen || window.open;
  window.__hcOpened = null;
  window.open = (u) => { window.__hcOpened = String(u); return null; };
  return 'click Apply now, then read window.__hcOpened and call __hcRestoreOpen()';
};
window.__hcRestoreOpen = () => { if (window.__hcOrigOpen) window.open = window.__hcOrigOpen; return window.__hcOpened; };
