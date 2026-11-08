# Career Ops

A Claude plugin that runs a job search with you. It scans job boards,
scores each posting against your real background, and builds a tailored
one-page resume for the ones worth applying to. It also logs everything in a
Google Sheet and writes in your own voice. You submit every application
yourself.

Start with [QUICKSTART.md](QUICKSTART.md) or the Word version,
[Career Ops Quickstart.docx](Career%20Ops%20Quickstart.docx), which opens in
Google Docs.

## Install

```bash
git clone https://github.com/respirenoro/jobhunter.git
claude --plugin-dir ./jobhunter
```

Then say **"set up my profile"**. Setup takes 20-30 minutes, because it
collects your full work history, writing samples and settings, not just a
resume.

## What's inside

| Part | What it does |
|---|---|
| `skills/evaluate` | Scores a posting 1.0-5.0 (A-F blocks) plus a hypothetical "H" score |
| `skills/tailor-resume` | One-page, ATS-safe resume tailored to the posting |
| `skills/scan`, `skills/triage` | Scans career pages and HiringCafe, then triages the results |
| `skills/apply` | Drafts application answers and fills ordinary form fields, then stops before submit |
| `skills/research`, `outreach`, `compare`, `track` | Company briefs, outreach drafts, side-by-side comparisons, the tracker |
| `skills/human-prose` | Rules and a linter that strip AI-writing tells from everything it writes for you |
| `references/standing-rules.md` | The rules every skill follows: scoring, build thresholds, target-state limits, honesty, sheet logging, stop points |
| `scripts/build_resume.py` | Builds the resume HTML and PDF, refuses to overwrite, and checks the page count |
| `scripts/hiringcafe/hc-capture.js` | Reads HiringCafe's job lists and full descriptions without clicking every card |

## Ground rules

- It never invents experience, numbers or tools.
- It never submits, uploads, fills disclosure sections, enters passwords,
  creates accounts or solves CAPTCHAs.
- Your data lives in `data/`, which git ignores.

## Requirements

- Claude Code with browser tools, for scanning and filling forms
- Python 3, for the resume builder and the prose linter
- Chrome or Edge, for PDF output

## License

MIT. See [ATTRIBUTION.md](ATTRIBUTION.md).
