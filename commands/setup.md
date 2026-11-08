---
name: setup
description: "Set up your job search profile. Paste your resume or answer a few questions. Takes 20-30 minutes; the more detail, the better the resumes. Needed before evaluating jobs."
argument-hint: "[--reset to start over]"
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Glob
---

# Set Up Your Profile

Walk the user through creating their job search profile. Conversational,
friendly, zero jargon. This is the first thing a new user does.

## Step 0: Check Existing

Read `data/profile.yml`. If it exists and no --reset flag:

> "You're already set up! Here's a quick summary of your profile:
>
> **{Name}** — {Current title} at {Company}
> Looking for: {Target role}
>
> Want to update it? Say 'setup --reset' to start fresh,
> or tell me what to change and I'll update just that part."

If --reset flag or file doesn't exist, continue to Step 1.

## Step 1: Welcome

> "Let's set up your job search profile. This helps me evaluate jobs,
> tailor resumes, and write messages that actually sound like you.
>
> **Fastest way:** Paste your resume below (text or PDF content) and
> I'll pull everything from it automatically.
>
> **Or** I can ask you a few questions instead. What do you prefer?"

## Step 2A: Resume Ingestion (preferred path)

If the user pastes resume content:

1. Parse the resume into structured data:
   - Name, contact info, LinkedIn URL
   - Work history (each role: title, company, dates, bullet points)
   - Education (degree, school, year)
   - Skills (extract all mentioned skills and tools)
   - Certifications/licenses (if any)
   - Projects or portfolio items (if listed)

2. Save the raw resume text to `data/resume.md` as a reference document.

3. Ask follow-up questions for fields NOT in the resume:
   - "What kind of role are you looking for next?"
   - "Where are you willing to work? (Remote, specific city, flexible)"
   - "What's your target salary range? (Skip if you'd rather not say)"
   - "Anything else I should know? Career change, gap to explain, special situation?"

4. Continue to Step 2C.

## Step 2B: Conversational Collection (fallback)

If the user prefers questions, ask these one at a time. Wait for each answer.

1. "What's your name?"
2. "What do you do right now? (Job title and company, or 'between jobs')"
3. "Walk me through your last 2-3 roles briefly. For each: title, company,
   how long, and one or two things you accomplished."
4. "What kind of role are you looking for? (Job title, industry)"
5. "Where are you willing to work? (City, remote, hybrid, relocate)"
6. "How many years of work experience total?"
7. "What are your strongest skills? (Top 5-10)"
8. "Any certifications or licenses? (Skip if none)"
9. "What's your salary range? (Target and minimum, or skip)"
10. "Got a LinkedIn profile URL?"
11. "Anything else? (Career change, gap, special circumstances, portfolio)"

## Step 2C: Go deeper than the resume (always do this)

A resume holds about a third of what someone has done. Ask for the rest, one
job at a time, and save it under `work_history_detail` in the profile:

> "Now tell me everything about **{job}** that isn't on your resume. I'll
> only ever use what you tell me, so more is better:
> - what the company does and who its customers were
> - every duty, even small or occasional ones
> - every tool or system you used, and how well you know it
> - numbers you can defend (percentages, volumes, team sizes)
> - things you did NOT do, so I never claim them
> - how much was phone, chat, email or tickets"

Then ask:
1. "Is there a bullet that must appear on every resume word for word?"
   (`pinned_bullets`)
2. "Anything I must never mention, such as a client's name or a department
   you didn't work in?" (`never_say`)
3. "Any experience that should only show for certain kinds of jobs, like
   research experience for health care roles?" (`domain_proof_points`)

## Step 2D: Voice

> "Paste two or three things you wrote yourself, such as an old cover
> letter, answers to application questions, or a LinkedIn About section. I'll
> match that voice."

Save them to `data/answer-bank.md`. Write a short `data/voice-profile.md`
describing how they write: sentence length, formality, words they use, and
words they never use. Every draft also follows the `human-prose` skill.

## Step 2E: Settings

Walk through `settings` in `references/profile-schema.md`. Show each default
from `references/standing-rules.md` and ask the user to keep or change it:
- pay floor, home state, kinds of work to avoid
- score thresholds for the standard and target-state resumes
- target-state limits (the default is no certifications, classes or degrees,
  only skills they could learn in days, and one tool per category)
- resume title format
- form defaults (application source, work authorization, sponsorship,
  travel)

## Step 2F: Google Sheet and HiringCafe

1. Ask for the Google Sheet link. If they have no sheet yet, tell them to
   create one with row 1: Company | Title | Pay | Score | Posting age |
   Hypothetical score (H) | Date added. Save the link in `settings`.
2. For HiringCafe scanning, tell them to:
   - sign in at hiring.cafe in the browser Claude controls
   - create one Talent Agent search per job type and set the filters
   - leave that tab open; Claude never reloads it or changes filters

## Step 3: Build Profile

Construct `data/profile.yml` from collected data. Follow the schema in
references/profile-schema.md exactly.

Key rules:
- Populate `work_history` with actual role details, not just titles
- Extract quantified achievements into `proof_points`
- Auto-detect persona modifiers:
  - If graduated within last 2 years: `recent_graduate: true`
  - If previous roles are in a different industry than target: `career_changer: true`
  - If gap > 1 year in work history: `career_returner: true`
  - If visa_status is anything other than citizen/permanent resident: `international: true`
- Generate `narrative.headline` from their experience (one compelling line)
- Generate `narrative.superpowers` from their strongest skills/achievements

Write the completed profile to `data/profile.yml`.

## Step 4: Confirm

Show the user a summary:

> "Here's what I have:
>
> **{Name}** — {Current title} at {Company}
> **Experience:** {years} years
> **Looking for:** {Target role} in {industries}
> **Location:** {preference}
> **Key skills:** {top 5}
> **Salary target:** {range}
>
> **Work history:**
> - {Role 1} at {Company} ({dates})
> - {Role 2} at {Company} ({dates})
> - ...
>
> This look right? I can fix anything now, or you can update later."

Wait for confirmation. Fix any corrections.

## Step 5: Next Steps

> "You're all set! Here's what to do next:
>
> **Option 1:** Paste a job posting (URL or text) and I'll evaluate how well
> you match.
>
> **Option 2:** Say 'scan [company name]' to search their career page for
> openings.
>
> **Option 3:** Say 'help' to see everything I can do."

Create `data/applications.md` if it doesn't exist:

```markdown
# Job Applications

| Date Added | Date Applied | Company | Role | Score | Status | Evaluation | Notes |
|---|---|---|---|---|---|---|---|
```
