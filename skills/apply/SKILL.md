---
name: apply
description: "Help fill out a job application form. Generates personalized answers for every field using your profile and evaluation. Never auto-submits. Use when someone says 'help me apply', 'fill out this application', or 'application for'."
argument-hint: "<company name or 'help me with this application'>"
user-invocable: true
disable-model-invocation: true
allowed-tools:
  - Read
  - Write
  - Glob
  - WebFetch
  - WebSearch
---

# Application Form Assistant

> Read `references/standing-rules.md` before starting. Its rules override the defaults in this skill.

Help fill out job application forms with personalized, honest answers.

**CRITICAL: NEVER auto-submit an application.** Always show the user every
answer and get explicit confirmation before any form interaction. Always stop
before any submit button.

## Step 0: Load Context

1. Read `data/profile.yml` for structured background
2. Read `data/resume.md` for full resume text
3. Find the relevant evaluation in `data/evaluations/`
4. Check `data/research/{company}.md` for company intel. **If it doesn't
   exist yet and a cover letter is needed, run it now before drafting** --
   don't skip straight to writing off the job posting alone. Do the same
   research the `research` skill does (see `skills/research/SKILL.md`):
   company history/background/mission via WebSearch, AND the "what it's
   actually like to work there" angle (recent news -- layoffs, restructuring,
   leadership changes, financial health -- plus culture/Glassdoor-style
   signals). Both angles matter: company-history facts make for a genuine,
   specific opening hook; the employee-experience angle is what keeps that
   hook accurate to the *current* company rather than an outdated or
   idealized version of it (a recent restructuring can make an old "great
   culture" framing wrong). Save findings to `data/research/{company-slug}.md` either way.
5. Check `data/resumes/` for a tailored resume file
6. Read `data/voice-profile.md` for writing style/voice, and
   `data/answer-bank.md` for real previous answers to adapt from -- prefer
   adapting a real prior answer over writing one from scratch when a close
   match exists, but always re-anchor company-specific paragraphs to the
   actual company/role at hand rather than swapping names into an old one

If no evaluation exists for this company:
> "I haven't evaluated this role yet. Want me to evaluate the posting
> first? That gives me better context for your application answers."

## Step 1: Identify the Application

Parse user input:
- **Company/role name:** Find the matching evaluation
- **"Help me with this application":** Ask which company/role, or if
  computer use is available, take a screenshot to identify the form

## Step 2: Map Common Form Fields

Generate answers for standard application fields:

| Field | Source | How to Fill |
|---|---|---|
| Name / Email / Phone | profile.yml | Direct copy |
| Resume upload | Point to file | "Upload `data/resumes/{file}.html` (or PDF if you printed it)" |
| Cover letter | Generate below | Tailored to this role |
| "Why this company?" | Research + evaluation | Specific, referencing company details |
| "Why this role?" | Evaluation Block C + narrative | Connect background to role requirements |
| Years of experience | profile.yml | Honest number |
| Salary expectations | Evaluation Block D | Use target from profile, informed by market data |
| Work authorization | profile.yml visa_status | Direct answer |
| Willing to relocate | profile.yml work_preference | Direct answer |
| Start date | Ask user | "When can you start?" |

## Step 3: Cover Letter (when needed)

Only write a cover letter when the posting requires one or says it matters.

If `data/cover letters/` holds a master letter the user approved, start from
it and keep its structure. Otherwise use this scheme:
1. **Business-letter header:** sender block, date (the day it is sent),
   recipient block (Hiring Manager or a named person, company, city/state
   only if verified, never an invented street address), "Dear Hiring
   Manager," and a "Sincerely," sign-off.
2. **Opening:** sentence one names the exact job title and the company plus
   one specific fact confirmed in a primary source (NOT "I'm excited to
   apply", no generic culture praise). Sentence two says in plain words what
   that fact does for their customers and ties it to the user's most
   relevant job. Tell the user to read the source before sending, since the
   letter says they read it.
3. **Main experience paragraph:** what the user's most relevant job was,
   what the product or service did, and one real story. If the story assumes
   the reader knows what the product does, say what it does first. End with
   a bridge sentence that names the shape of the company's problem without
   claiming industry experience the user lacks.
4. **Proof paragraph:** the user's strongest defensible number from
   `profile.yml` proof points. Add a gap paragraph only when the posting
   requires something the user lacks: state it directly, then the closest
   real experience.
5. **Close:** use the closing the user approved in `data/voice-profile.md`
   if one exists. Otherwise one short paragraph asking for an interview with
   email and phone from the profile, then "Thank you for your time and
   consideration." No "I look forward to hearing from you."

Rules:
- About 260-380 words on one page.
- Stay thematically relevant to the JD's responsibilities, but do NOT quote
  its exact phrases, team names, or department titles back at it. The exact
  job title in the first sentence and product names are fine. Paraphrase in
  the user's own words. Reusing the JD's distinctive language reads as
  AI-generated.
- Match company tone (formal for law firms, conversational for startups).
- Reference specific details from research (if available).
- Every claim must be backed by real experience from the profile.
- Write in the voice documented in `data/voice-profile.md` and follow the
  `human-prose` skill: no em dashes, no triads-of-three, vary sentence
  length, and prefer adapting a real sentence from `data/answer-bank.md`
  over generating fresh "styled" prose. Run its linter before handing over.
- **Domain proof points:** if `profile.yml` lists a proof point limited to
  certain kinds of employers (for example research involvement used only
  for health care roles), use it only for those, and only where it fits
  naturally.
- AI-detector tools flag factual duty sentences whatever the wording, so
  don't chase their sentence-level scores. Cut the genuinely formulaic
  connectors (e.g. "and that is the kind of...", a stray "At [Company],")
  and leave true, specific statements alone.

### Output

Write the HTML to `data/cover letters/{Company} - Cover Letter {Initials}.html`,
same plain human-readable naming as tailor-resume uses for resumes. Then
render a PDF into `data/cover letters/cover letters (PDF)/{Company} - Cover Letter {Initials}.pdf`
using the same headless Chrome/Edge approach documented in
`skills/tailor-resume/SKILL.md` Step 6 (find a browser binary, run
`--headless --disable-gpu --no-pdf-header-footer --print-to-pdf=...`). Create
either folder if it doesn't exist yet. After writing the HTML, check that the
content fits one page before generating the PDF (a cover letter should never
run to two pages); if it's tight, prefer tightening CSS (margins, line-height)
over cutting content, since word count is already capped (see Rules above).

## Step 4: Handle Custom Questions

For each custom application question:

**Short answer (< 500 chars):**
- Draw from evaluation blocks, profile, or research
- Be specific, not generic
- Include a number or concrete detail when possible

**"Tell me about a time..." (behavioral):**
- Check `data/answer-bank.md` and `data/star-answers.md` first for a real
  story that already fits
- Otherwise use STAR format from evaluation Block F stories
- Match the most relevant story to the question

**"What are your salary expectations?":**
- Use target from profile, informed by Block D market data
- If range requested, give profile target range
- If single number requested, give midpoint of target range

**Yes/No questions (authorization, relocation, etc.):**
- Answer directly from profile data
- If not in profile, ask the user

**EEO / demographic questions:**
- Tell the user these are optional and legally cannot affect their candidacy
- Let them answer themselves

## Step 5: Present All Answers

Show EVERY generated answer before any action:

```
## Application Answers: {Company} - {Role}

**Cover letter:**
{full text}

**"Why this company?"**
{answer}

**"Why this role?"**
{answer}

**Salary expectations:** {answer}

**Custom questions:**
1. "{question}" - {answer}
2. "{question}" - {answer}

---

Review these answers. You can:
- Ask me to revise any answer
- Copy them into the application form
- Tell me to adjust the tone
```

## Step 6: Computer Use Assistance (only if available and user requests)

If computer use is available AND the user explicitly asks for help filling
the form:

1. Navigate to the application page
2. Fill each field with the APPROVED answers only
3. Upload resume file if the form accepts it
4. **STOP before the Submit button.** Take a screenshot. Say:

> "Everything is filled in. Please review the form carefully and click
> Submit when you're ready. I won't click it for you."

If no computer use:
> "Copy the answers above into the application form. Let me know
> when you've submitted and I'll update your tracker."

## Step 7: Update Tracker

After the user confirms submission:
- Update `data/applications.md`: Status -> "Applied", Date Applied -> today
- Add note with any relevant details

> "Tracked! Your application to {company} is logged. I'll remind you
> to follow up if you haven't heard back in a week."
