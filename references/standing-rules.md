# Standing rules

These rules came out of several weeks of daily use. Every skill follows them.

**Precedence:** the user's latest message beats `data/profile.yml` and the
user's own notes, which beat this file, which beats the plugin defaults in
other skills. Where a value below is marked *(setting)*, the user's answer in
setup replaces it.

## 1. Before scoring anything

- **Duplicate gate.** Search `data/applications.md` and the Google Sheet for
  the company's name, short name, brand and parent company, and for the role
  title. If the company was applied to recently, skip it and say so in one
  line. A company cell starting with `@ ` means already applied. Very old
  rows (the first ~150) are old enough to re-apply. *(setting)*
- **Read the whole posting.** Never score from card text or a snippet. Read
  the structured facts (pay, states, schedule, clearance) and the full
  description first. Pay often appears only in structured data.
- **Location.** Treat a posting as remote unless the description says
  on-site, hybrid or limits location. Skip for location only when the
  posting text itself rules out the user's state.
- **Hard skips** *(setting)*: security clearances, Public Trust or credit
  checks, federal contractor work, and anything else the user lists.

## 2. Scoring

- Score 1.0 to 5.0 with the evaluate skill's A-F blocks. Be honest, not
  generous. Pass mark 3.0. *(setting)*
- Add 0.5 when the work is very simple and needs no phone calls, if the user
  wants call-free work. *(setting)*
- Also give a **hypothetical (target-state) score** with an H, such as 4.2H:
  the score the user would get with the posting's tools and duties, but no
  new certifications, classes or degrees.
- **Hard technical skills are real gaps** even when a posting says
  "familiarity" or "strong interest": coding, Git, REST or named APIs,
  interviewing engineers. Do not paper over them. *(setting, for
  non-technical users)*

## 3. What to build

| Standard score | H score | Build |
|---|---|---|
| 3.8 or higher | any | standard resume |
| 3.0 to 3.7 | any | target-state resume only |
| any | 3.6 or higher | target-state resume |
| below 3.0 | below 3.6 | nothing unless asked |

*(setting)* No cover letter unless the posting requires one or says it
matters. Before building for a passing role, open the real application page
and confirm the role is still open.

## 4. Resumes

- One page. Single column, ATS-safe (see `ats-rules.md`).
- File name `Company (Role) - Resume XX` with the user's initials. List the
  folder first and **never overwrite** an existing file.
  `scripts/build_resume.py` enforces this.
- Mirror the posting's vocabulary for things the user really did, and list
  every component they owned, but stay on one page.
- Title line format and default tool wording come from `profile.yml`.
  *(setting)*
- Name sub-skills (pivot tables, VLOOKUP) only when the posting requires
  them, at the user's real proficiency level.
- Pinned bullets in `profile.yml` go on every resume verbatim. Items in
  `never_say` never appear (an employer's client name, a department the user
  never worked in).
- Domain-only proof points (such as research experience) go only on the
  roles they suit.

## 5. Target-state resumes

These show what the user would look like with the skills a posting wants.
They're for planning what to learn. Build them only when the thresholds say
so or the user asks.

- No certifications, classes, courses or degrees.
- Only things the user could pick up in days: **one tool per category** (no
  stacking two ticketing systems), no new programming languages, no deep
  expertise.
- Tools must be plausible at the user's real employer. Research the
  posting's software first and leave out anything from a different industry.
- Duties stay within the user's real role. Don't add work that belongs to a
  separate team, such as sales, billing or renewals.
- Keep at least 2 bullets of the user's real work, and keep their real job
  title.
- Language levels stay as they are.
- Save them in `data/resumes/Target State Resumes/`. Add one short note
  listing what was added beyond the real record. Skip the warnings.

## 6. Truth

- Never invent experience, metrics, tools or stories. Use only numbers the
  user gave and can defend.
- When something is a stretch, say so plainly. In interview prep, tag each
  claim **REAL**, **PARTLY**, **WOULD** (would do it this way, never has) or
  **GAP**.

## 7. Writing

- Follow the `human-prose` skill and run its linter on every resume, letter,
  answer, role description and prep document before handing it over.
- Plain first person in the user's voice from `data/voice-profile.md`. No em
  dashes, no rule-of-three reflexes, no AI vocabulary.
- Role descriptions for application forms: plain paragraphs, no quotation
  marks, so the user can paste them.
- Several application questions pasted together belong to one form: answer
  them briefly, and use each fact once.
- Unlisted pay: estimate it and write it as `~$X-$Y/yr (est)`.

## 8. Google Sheet log

Columns: **A** company, **B** title, **C** pay, **D** score, **E** posting age
("6 days", "2 weeks"), **F** hypothetical score with H, **G** date added
(M/D/YYYY). *(setting)*

- Add a row only for roles the user is applying to or asked to log, at the
  next empty row.
- Entry method that works in Google Sheets: jump to the cell (Name Box or an
  `#gid=0&range=A<row>` URL), then for each value press F2, type, press Tab.
  Finish with Return. Pressing Delete before typing cancels autocomplete.
- Verify each new row with the sheet's CSV export
  (`/gviz/tq?tqx=out:csv`).

## 9. Application pages

- The user submits every application.
- Claude may open the page and fill ordinary fields with the form defaults
  from `profile.yml`. The street address goes only on forms for verified
  employers.
- **Stop before:** file uploads, EEO, veteran or disability disclosures, the
  final submit, passwords or new accounts, and anything about money.
- **CAPTCHA or security check: stop at once and tell the user.** Never retry
  or work around it.

## 10. Scanning HiringCafe

- The user keeps HiringCafe open with their Talent Agent searches set up,
  one tab per job type. **Never reload that tab or change its filters.**
- Use `scripts/hiringcafe/hc-capture.js`:
  1. Hook the page's own job-list responses.
  2. List the captured jobs and drop duplicates.
  3. Read full descriptions for the rest, slowly.
  4. Click **Next page**. When a tab has no more pages, move to the next
     Talent Agent tab.
- Click into a card only to get the apply link for a role that made the
  sheet. Dismiss "Mark job as applied?" (never click Yes).
- Pace it: small batches with breaks. Bulk reading has triggered a security
  check before.
- Report results, not every step.

## 11. Interview prep

Output goes in `data/interview prep/`, built from the resume the user
actually sent. Contents:
- a short talking-points page
- literal step-by-step workflows for each tool on the resume
- STAR stories using only real facts
- honest gap answers
- company research tagged HIGH, MED or LOW confidence
- questions to ask
- a "do not say" list

Build it as HTML, lint it, print it to PDF with headless Chrome, and check
the page count.

## 12. Files

Everything the user needs to keep goes in `data/`. Git ignores that folder,
so never commit or upload it. Temp and scratch folders are not durable.
