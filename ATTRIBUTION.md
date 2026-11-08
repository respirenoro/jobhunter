# Attribution

career-ops-plugin is a Claude Cowork adaptation of
[career-ops](https://github.com/santifer/career-ops) by santifer.

The original career-ops is a Claude Code skill for job search automation,
featuring the A-F scoring rubric, ATS-optimized resume generation, and
application tracking system that this plugin builds upon.

## What we adapted

- Blocks A-F evaluation system (generalized for all industries)
- ATS compliance rules for resume generation
- Application state machine and tracking
- Outreach 3-part message structure (hook + proof + proposal)
- "Never fabricate, never auto-submit" ethical principles

## What we changed

- Converted from Claude Code skill to Cowork plugin format
- Replaced 6 tech-specific archetypes with 15 industry-general archetypes
- Replaced Playwright/Node dependencies with computer use + WebFetch
- Added resume ingestion (paste your resume, Claude parses it)
- Added conversational setup wizard for non-technical users
- Redesigned output for Cowork's GUI (tables, checkboxes, scannable format)
- Added persona modifiers (recent grad, career changer, international)
- Added pipeline triage skill for bulk evaluation of scan results

## License

Both the original career-ops and this adaptation are MIT licensed.

## Career Ops 2.0 additions

Built on top of [career-ops-plugin](https://github.com/andrewshwetzer/career-ops-plugin)
by Andrew Shwetzer (MIT):

- `references/standing-rules.md`: rules from several weeks of daily use
  (duplicate gate, hypothetical scores, build thresholds, target-state
  limits, honesty tags, sheet logging, stop points)
- `skills/human-prose`: writing rules and a linter based on Wikipedia's
  "Signs of AI writing" field guide
  (https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing). The catalogue
  summarizes that page, which is licensed CC BY-SA 4.0.
- `scripts/build_resume.py` and `scripts/hiringcafe/hc-capture.js`
- A deeper setup flow (full history, voice samples, settings)
