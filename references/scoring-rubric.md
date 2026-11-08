# Evaluation Scoring Rubric

## Score Dimensions (weighted)

| Dimension | Base Weight | What It Measures |
|---|---|---|
| Hard requirement coverage | 30% | % of required qualifications matched by real experience |
| Seniority alignment | 15% | Your level vs. the role's level |
| Domain/industry match | 10% | Industry experience relevance |
| Compensation alignment | 10% | Your target vs. stated/estimated range |
| Location/remote fit | 10% | Geographic/work arrangement match |
| Career trajectory fit | 5% | Does this role make sense as your next step? |
| Credentials/licenses | 10% | Required certifications, degrees, clearances, bar admissions |
| Skills/portfolio | 10% | Specific skills, tools, or demonstrated work |

## Archetype Weight Adjustments

Different archetypes shift the weights. Adjustments are relative to the base weights above.

| Archetype | Adjustments |
|---|---|
| Technology/Engineering | Skills/portfolio +5%, Seniority -5% (skills matter more than titles) |
| Finance/Accounting | Credentials +10%, Location -5%, Trajectory -5% (CPA/CFA/Series licenses critical) |
| Healthcare/Medical | Credentials are **PASS/FAIL** (active license in required state is non-negotiable) |
| Legal/Compliance | Credentials are **PASS/FAIL** (bar admission in required jurisdiction) |
| Creative/Marketing/Design | Skills/portfolio +15%, Credentials -10%, Trajectory -5% (portfolio is the resume) |
| Operations/Supply Chain | Domain +5%, Skills -5% (industry-specific ops knowledge matters) |
| Sales/Business Development | Hard requirements reframed as "track record" (quota attainment replaces skills) |
| Education/Training | Credentials +5%, Domain +5%, Skills -10% (certification + subject match) |
| Executive/Leadership | Seniority +10%, Domain +5%, Skills -15% (scope and P&L matter most) |
| Trades/Skilled Labor | Credentials are **PASS/FAIL** (journeyman/master license, CDL class) |
| Customer Success/Support | Domain +5%, Skills +5%, Seniority -5%, Trajectory -5% |
| People/HR | Credentials +5%, Domain +5%, Skills -5%, Trajectory -5% (SHRM/PHR matter) |
| Government/Nonprofit | Credentials +5%, Domain +10%, Compensation -10%, Skills -5% |
| Scientific/R&D | Hard requirements +5%, Credentials +5%, Skills -5%, Trajectory -5% |
| Non-Software Engineering | Credentials +10%, Skills +5%, Seniority -10%, Trajectory -5% (PE license, certifications) |

## PASS/FAIL Credential Rules

For Healthcare, Legal, Trades, and Non-Software Engineering archetypes:

1. If the JD lists a **required** credential (license, certification, bar admission, PE stamp)
   AND the user's profile does NOT include it:
   - Cap the overall score at **2.0** regardless of other dimensions
   - Flag prominently: "This role requires [credential] which is not in your profile"
2. If the credential is listed as **preferred** (not required):
   - Reduce Credentials dimension score by 50%, but do not cap overall score
3. If profile data is incomplete (user hasn't listed credentials):
   - Score Credentials at 5/10 (neutral)
   - Flag: "Add your certifications and licenses to your profile for more accurate scoring"

## Score Thresholds

| Score | Label | Action |
|---|---|---|
| 4.5 - 5.0 | Excellent Match | Generate resume + draft application answers |
| 3.5 - 4.4 | Good Match | Generate resume |
| 3.0 - 3.4 | Worth Considering | Evaluate fully, flag risks clearly |
| 2.0 - 2.9 | Weak Match | Warn user, suggest better-matched roles |
| 1.0 - 1.9 | Poor Match | Advise against applying, explain why |

## Scoring Rules

1. Never inflate scores. A 3.2 is a real score. Honesty serves the user.
2. PASS/FAIL credentials override everything in regulated industries.
3. If the profile lacks information to score a dimension, score it at 5/10
   (neutral) and flag "incomplete data" so the user can add more detail.
4. Compensation misalignment (target is 30%+ above the role's range)
   does not kill the score but must be flagged in the summary.
5. "Years of experience" requirements are guidelines, not hard cutoffs.
   If the user has 5 years and the JD asks for 7, that's a partial match,
   not a disqualification.
6. If the user's profile.yml defines a `workload_preference`, apply the
   Workload/Autonomy Fit rule below on top of the base weighted score.

## Workload/Autonomy Fit

Some users prioritize workload shape and autonomy as highly as, or above,
raw compensation. If `data/profile.yml` contains a `workload_preference`
block, read its `good_fit_signals` / `poor_fit_signals` lists and its
`pay_workload_tradeoff` thresholds, then scan the JD for workload structure:
continuous/real-time staffing (shift coverage, live call/chat queues,
minute-level SLAs) vs. async/deliverable-based work (deadlines over
schedules, output-based, flexible hours).

Apply this adjustment on top of, not instead of, the Compensation Alignment
and Career Trajectory Fit dimensions:

If the `workload_preference` block also defines a `hard_constraint` (e.g., no
call-center-style work), treat that separately from the softer adjustments
below: if the JD's primary daily activity is what the constraint rules out
(for a call-volume constraint: a live phone/chat queue, high call-volume
metrics, "X calls per day" expectations), cap the overall score at **2.0**
regardless of other dimensions, the same way PASS/FAIL credentials work.
Scheduled meetings, occasional client calls, or standups do not trigger this
even when the constraint mentions "calls" -- only high-volume/queue-style
phone work does. If it's ambiguous whether a role is call-queue-heavy, don't
guess: flag it and score normally.

| Situation | Adjustment |
|---|---|
| High, continuous, real-time workload AND pay below the profile's `high_workload_ok_if` threshold | Reduce overall score by up to 1.0 point. Flag prominently in the Executive Summary and Overall Score paragraph, not buried in Block B. |
| High, continuous, real-time workload AND pay meets/exceeds `high_workload_ok_if` | No penalty. State the tradeoff explicitly (high effort, but the pay clears their bar) so the user can decide with full information. |
| Lower pay, within the profile's `low_pay_ok_if` range, AND clear async/deliverable-based signals | No penalty for being at the bottom of their pay range. This is a genuine match, not a compromise. |
| Lower pay AND workload structure is unclear from the JD | Don't guess either direction. Flag: "Need info: workload structure unclear, worth confirming directly before or during the interview." |
| Workload signals are genuinely mixed or ambiguous | Score the base dimensions normally; note the ambiguity once in Block C rather than adjusting the score. |

## Persona Modifiers

Apply these adjustments when the user's profile indicates a special situation:

| Persona | Adjustment |
|---|---|
| Recent graduate | Reduce Hard Requirements weight by 10%, increase Trajectory by 10%. Emphasize internships, projects, education. |
| Career changer | Reduce Domain weight by 5%, increase Trajectory by 5%. Emphasize transferable skills and narrative. |
| Career returner (gap) | Score normally but add a "Gap Strategy" section to Block C with framing advice. |
| International/visa | Add a Location modifier: if role requires authorization the user doesn't have, flag prominently but don't auto-disqualify (sponsorship is possible). |
