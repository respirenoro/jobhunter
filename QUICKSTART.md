# Career Ops: First-Time Quickstart

Career Ops is a Claude plugin that scans job boards, scores each posting against your background, builds a tailored one-page resume for the ones worth applying to, and logs them in a Google Sheet. You still submit every application yourself.

## 1. Install

```bash
claude --plugin-dir "<path to jobhunter>"
```

Your private files live in `data/`. Git ignores that folder, so never commit or upload it.

## 2. Feed it your background (one time, the more the better)

Paste each of these into Claude, in this order.

1. **Your resume.** Say: `Set up my profile. Here is my resume:` and paste it.
2. **Everything else you've done.** Say: `Here is my full work history. Use only these facts.` For every job, give:
   - dates, title, company, and what the company does
   - every duty, tool, system and process you touched, even small ones
   - real numbers you can defend (percentages, volumes, team sizes)
   - what you did NOT do, so Claude never claims it
   - how much phone, chat or email work each job had

   A resume holds maybe a third of your history. The rest is what Claude uses to match a posting's wording without inventing anything.
3. **Your targets.** Say: `My targets:` and give your minimum pay, remote/hybrid/on-site, states you can work in, kinds of work you'll take, kinds you won't (calls, sales, travel, clearances), and the job title format you want on resumes.
4. **Your voice.** Paste two or three things you wrote yourself, such as an old cover letter or answers to application questions. Say: `Match this voice in anything you write for me.`
5. **Form defaults.** Give your LinkedIn URL, work authorization, sponsorship answer, and willingness to travel. Claude fills these on application forms.

## 3. Decide your target-state ("hypothetical") rules

A target-state resume shows what you would look like with the skills a posting asks for. It's for spotting gaps, and it uses a second score marked with H, such as `4.2H`. Tell Claude your limits once:

```
Target-state rules: no certifications, classes or degrees. Only skills I could
pick up in a few days. One tool per category. Keep at least 2 bullets of my real
work. Never add coding, APIs or new languages.
```

Then set when each resume gets built:

```
Build a standard resume at 3.8+. Build only a target-state resume at 3.0-3.7.
Always build a target-state resume when the H score is 3.6+. No cover letter
unless the posting requires one.
```

## 4. Set up the Google Sheet

Create a sheet with these columns in row 1:

| A | B | C | D | E | F | G |
|---|---|---|---|---|---|---|
| Company | Title | Pay | Score | Posting age | Hypothetical score (H) | Date added |

Give Claude the sheet link and say: `Log every role I apply to here. Check it for duplicate companies before scoring anything.` If a posting lists no pay, Claude estimates it as `~$X-$Y/yr (est)`. Put `@ ` in front of a company name once you've applied, and Claude will skip that company.

## 5. Set up HiringCafe

1. Sign in at hiring.cafe in the browser Claude controls.
2. Create Talent Agent searches, one tab per job type, such as Ticket-Based, Operations, or Support. Set remote, pay and date filters in each one.
3. Leave that tab open and don't touch its filters. Claude never reloads it, because a reload can wipe your filters.

## 6. Run a scan

Say:

```
Scan HiringCafe. Work through every Talent Agent tab and every page.
```

On each tab, Claude does this:

1. It listens to the page's own job-list data, which holds the whole page of jobs (title, company, pay, location, apply link). It doesn't click each card.
2. It drops companies already in your sheet or tracker.
3. It pulls the full description of each remaining job and reads all of it.
4. It scores each job from 1.0 to 5.0, plus an H score. It skips on-site roles, call-heavy roles, clearance roles, and roles that rule out your state.
5. For a passing role, it confirms the posting is still open, builds the resume, adds a sheet row and a tracker row, and opens the application page for you.
6. When the page is done, it clicks **Next page** and repeats. When the tab is done, it moves to the next tab.
7. It reports what it found. It doesn't narrate every step.

If HiringCafe shows a CAPTCHA or security check, Claude stops at once and tells you. Clear it yourself, then say `continue`.

## 7. Other commands

| Say | What happens |
|---|---|
| `Evaluate this:` + pasted posting or link | Full A-F score report and a resume if it passes |
| `Tailor my resume for <company>` | One-page resume, saved as HTML and PDF |
| `Build a target-state resume for <company>` | Hypothetical resume and its gap list |
| `Answer these application questions:` + paste | Short first-person answers in your voice |
| `Interview prep for <company>` | Talking points, STAR stories from real facts, honest gap answers, questions to ask |
| `Show my applications` | Tracker summary |
| `continue` | Moves on after you finish an application |

## 8. What Claude will not do

- Submit applications, upload files, or fill disclosure sections (EEO, veteran, disability)
- Enter passwords, create accounts, or touch anything involving money
- Invent experience, tools, numbers or stories
- Overwrite an existing resume file
- Solve a CAPTCHA
