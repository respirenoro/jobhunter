---
name: tailor-resume
description: "Generate an ATS-optimized resume tailored to a specific job posting. Creates clean HTML you can print to PDF. Works for any industry. Use when someone says 'tailor my resume', 'make me a resume', 'create a resume for', or 'update my resume for'."
argument-hint: "<company name or 'for the latest evaluation'>"
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Glob
---

# Tailor Your Resume

> Read `references/standing-rules.md` before starting. Its rules override the defaults in this skill.

Generate an ATS-optimized resume customized for a specific job posting.
Read references/ats-rules.md before generating any HTML.

## Step 0: Load Context

1. Read `data/profile.yml` for structured background data
2. Read `data/resume.md` if it exists (full resume text for detail)
3. Find the target evaluation:
   - If the user specified a company/role, search `data/evaluations/` for a match
   - If "latest" or no argument, use the most recent evaluation file
   - If ambiguous, list recent evaluations and ask which one
4. If no evaluation exists:
   > "I need to evaluate the job first so I know what to emphasize.
   > Paste the job posting and I'll assess it, then generate your resume."

## Step 1: Keyword Extraction

From the evaluation + JD, extract 15-20 keywords that ATS systems scan for:

- Exact phrases from "Required Qualifications" (highest priority)
- Industry-standard terms (not creative synonyms)
- Certifications, tools, methodologies named in the JD
- Action verbs that match the responsibilities section

## Step 2: Detect Language & Locale

- JD in English + US company: Letter paper (8.5" x 11")
- JD in English + non-US: A4
- JD in another language: match that language, use A4
- Resume language MUST match JD language

## Step 3: Build Resume Content

Using the evaluation's Block E (Tailoring Plan) as a guide, construct
each resume section from profile data:

### Professional Summary (3-4 lines)
- Open with years of experience + core identity
- Include 3-5 top keywords from the JD naturally
- End with a forward-looking statement connecting to this specific role
- Use the narrative.headline from profile as a starting point

### Experience Section
- Include all roles from work_history, most relevant FIRST
- For each role: Company, Title, Dates on one line
- 3-5 bullets per role, ordered by relevance to THIS JD
- Each bullet: Action verb + what you did + quantified result
- Mirror JD language exactly (if JD says "project management",
  write "project management", not "programme management")
- Pull specific numbers from proof_points and work_history highlights
- **Pinned bullets:** if `profile.yml` marks a bullet as pinned (for
  example the one sentence that says what a product actually does, which
  the other bullets assume the reader knows), include it verbatim on every
  resume. Never append clauses to it. Cut a different bullet if space runs
  short.
- **Banned items:** never use anything `profile.yml` lists under
  `never_say` (an employer's client name, a department the user did not
  work in, a tool they only touched once).

### Education Section
- Degree, School, Year
- Include relevant coursework or honors only if recent grad
- **Domain proof points:** if `profile.yml` has a proof point limited to
  certain fields (for example research involvement shown only on health
  care, clinical or research roles), add it as one brief line for those
  roles only. Leave it off everything else.

### Skills Section
- List JD keywords FIRST, then additional skills
- Group by category if 10+ skills (Technical, Tools, Methodologies, etc.)
- Include both acronym and full form: "Search Engine Optimization (SEO)"
- **Keyword-variant format**: when the JD uses a specific spelling or
  abbreviation for a real skill you have, write it the JD's way, then the
  common variant once in parentheses -- e.g. "Salesforce (CRM)" if the JD
  says "CRM." Name sub-skills of a tool (such as Excel pivot tables or
  VLOOKUP) only when the posting requires them, at the proficiency level
  the profile states; never inflate to "advanced" or "expert".
  This helps both literal ATS keyword search and a human skimming the
  section. Never stack more than one variant per skill (no
  "Salesforce, SFDC, Salesforce CRM" chains) -- that reads as keyword
  stuffing, not a real skill.

### Certifications Section (if applicable)
- From credentials in profile
- Include status, jurisdiction, number if relevant

### Projects / Portfolio (if applicable and relevant)
- Only include if the archetype values it (Creative, Technology)
- Brief description + link + key metric

## Step 3.5: Must-Have Verification (Ctrl+F Check)

Before generating the HTML, list the 4-6 real must-have requirements
identified from the JD (the ones already driving Block B of the
evaluation: items stated as required, appearing in both the "about the
role" text and the requirements list, or carrying a number like "5+
years"). For each one, confirm it appears somewhere concrete in the
draft resume content, either a skills-line entry or a proof bullet in
the experience section, not just implied.

- If a must-have has no home anywhere on the resume and it's something
  the candidate genuinely has, add it (a bullet or a skills entry).
- If a must-have has no home because the candidate genuinely doesn't
  have it, don't fabricate one -- this is a real, known gap that should
  already be reflected honestly in the evaluation, not papered over on
  the resume.
- A keyword that only lives in the skills list with no supporting
  bullet anywhere reads as "took a weekend course" to an experienced
  reader. Where practical, back a must-have skill with a proof bullet,
  not just a bare mention.

## Step 4: Generate HTML

Read the template from references/resume-template.html.

Fill all `{{PLACEHOLDER}}` slots with the generated content.

ATS compliance rules (from references/ats-rules.md):
- Single column ONLY
- Standard section headers exactly: "Experience", "Education", "Skills"
- No images, icons, or graphics
- All text selectable (no text-in-images)
- Standard fonts: Arial, Calibri, Georgia, or system sans-serif
- Font size: 10-12pt body, 14-16pt name
- Margins: 0.5-1 inch
- No headers/footers (ATS strips them)
- Max 2 pages

## Step 5: Output

Write the HTML to `data/resumes/{Company} ({Role}) - Resume {Initials}.html`
(e.g. `data/resumes/Acme (Operations Analyst) - Resume JD.html`).
Target-state resumes go in `data/resumes/Target State Resumes/` with the
same naming. **Always list the folder first and never overwrite an existing
file;** pick a more specific role label instead. `scripts/build_resume.py`
does the fill, the no-overwrite check, the PDF and the page count in one
step. Use the company's normal display
name (not a slug) and the candidate's initials from their profile name.
Deliberately plain and human-looking, not a machine-generated-looking
filename, since this file may be shared with employers directly.

Show the user a preview of the content (not the HTML code):

```
## Resume Preview: {Name} - {Target Role} at {Company}

**Summary:** {first 2 lines}

**Experience:**
- {Role 1} at {Company} ({dates}) - {first bullet}
- {Role 2} at {Company} ({dates}) - {first bullet}

**Skills:** {top 10}

**Keywords matched:** {n}/20 from the JD
```

## Step 6: Generate PDF

Automatically render the HTML to a PDF using headless Chrome or Edge. Create
`data/resumes/resumes (PDF)/` if it doesn't exist, then run:

```
<chrome-or-edge> --headless --disable-gpu --no-pdf-header-footer \
  --print-to-pdf="data/resumes/resumes (PDF)/{Company} - Resume {Initials}.pdf" \
  "file:///{absolute path to the html file}"
```

Use the same filename (minus extension) as the HTML file from Step 5.

Find a browser binary in this order and use the first one that exists:

1. `chrome`, `google-chrome`, `chromium`, or `msedge` on PATH
2. Common Windows install paths: `C:\Program Files\Google\Chrome\Application\chrome.exe`,
   `C:\Program Files (x86)\Google\Chrome\Application\chrome.exe`,
   `C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe`,
   `C:\Program Files\Microsoft\Edge\Application\msedge.exe`
3. Common macOS paths: `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`,
   `/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge`

The HTML's own `@page` CSS (Letter size, margins) is respected by headless
print-to-pdf, so no extra sizing flags are needed.

If no browser binary is found anywhere, fall back to manual instructions:

> "Your tailored resume is saved at `data/resumes/{filename}.html`. I
> couldn't find Chrome or Edge on this machine to generate the PDF
> automatically, so to save it yourself:
> 1. Open the file in your browser (double-click it)
> 2. Press **Cmd+P** (Mac) or **Ctrl+P** (Windows)
> 3. Select **Save as PDF**
> 4. Done!"

Otherwise, once the PDF is generated successfully, tell the user:

> "Your tailored resume is ready as both HTML (`data/resumes/{filename}.html`)
> and PDF (`data/resumes/resumes (PDF)/{filename}.pdf`)."

## Step 7: Update Tracker

Update the matching row in `data/applications.md`:
- Status: "Resume Ready" (if currently "Evaluated")
- Notes: append "Resume: {filename}"

## Step 8: Next Steps

> "Resume is ready! Next steps:
> - **Review it** by opening the HTML file
> - **Apply** by saying 'help me with the {company} application'
> - **Compare** this role with others: 'compare my options'"
