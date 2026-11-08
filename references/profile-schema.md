# Profile Schema Reference

This documents every field in `data/profile.yml`. Users can edit this file
directly or use the `/career-ops:setup` command to fill it conversationally.

## Fields

```yaml
# === Identity ===
name: "Your Name"
email: "your@email.com"           # Optional. Used in resume header.
phone: ""                          # Optional. Used in resume header.
linkedin_url: ""                   # Optional. Used in resume + outreach.
portfolio_url: ""                  # Optional. Used in creative/tech resumes.
location: "City, State/Country"
work_preference: "remote"          # remote | hybrid | onsite | flexible
visa_status: ""                    # Optional. "US Citizen", "H-1B", "Green Card", etc.

# === Current State ===
current:
  title: "Current Job Title"
  company: "Current Company"
  years_experience: 8              # Total years of professional experience

# === Target ===
target:
  primary_role: "Senior Product Manager"
  secondary_roles:
    - "Director of Product"
    - "Head of Product"
  industries:
    - "SaaS"
    - "Healthcare Tech"
  seniority: "senior"              # entry | mid | senior | lead | director | vp | c-suite
  exclude_keywords:                # Optional. Roles to skip in scanning.
    - "Junior"
    - "Intern"

# === Skills ===
skills:
  - "Product Strategy"
  - "SQL"
  - "User Research"
  # List your top 10-15 skills

# === Credentials (for regulated industries) ===
credentials:                       # Optional. Critical for Healthcare, Legal, Trades, Engineering.
  - type: "PMP"                    # Certification/license type
    status: "Active"               # Active | Expired | In Progress
    state: ""                      # Jurisdiction if applicable
    number: ""                     # Optional. License number.
    expiry: ""                     # Optional. Expiration date.

# === Narrative ===
narrative:
  headline: "Product leader who turns user research into revenue"
  story: "Transitioned from engineering to product after building internal tools that became the company's main product line."
  superpowers: "Data-driven decisions, cross-functional leadership, 0-to-1 product launches"

# === Work History (parsed from resume) ===
work_history:
  - title: "Senior Product Manager"
    company: "Acme Corp"
    dates: "Jan 2022 - Present"
    highlights:
      - "Launched 3 products generating $4M ARR"
      - "Led cross-functional team of 12"
      - "Reduced churn 25% through data-driven feature prioritization"
  - title: "Product Manager"
    company: "StartupCo"
    dates: "Mar 2019 - Dec 2021"
    highlights:
      - "Built product from 0 to 10K users in 8 months"
      - "Defined and executed product roadmap for Series A pitch"

# === Education ===
education:
  - degree: "BS Computer Science"
    school: "State University"
    year: 2018
  - degree: "MBA"                  # Optional additional degrees
    school: "Business School"
    year: 2022

# === Compensation ===
compensation:
  target: "$160,000"
  minimum: "$140,000"
  currency: "USD"

# === Proof Points ===
proof_points:
  - "Launched 3 products totaling $4M ARR at Acme Corp"
  - "Grew user base from 0 to 10K in 8 months at StartupCo"
  - "PMP certified, 2023"

# === Portfolio / Projects ===
portfolio:
  - url: "https://yoursite.com/case-study"
    description: "Product case study: Acme onboarding redesign"

# === Persona Modifiers ===
persona:                           # Optional. Triggers special scoring adjustments.
  recent_graduate: false
  career_changer: false
  career_returner: false
  international: false
  gap_explanation: ""              # If career_returner, brief explanation

# === Full history (more than the resume holds) ===
# Setup collects these. They are the material for tailoring without inventing.
work_history_detail:               # One entry per job, same order as work_history
  - company: "Acme Corp"
    what_company_does: "Scheduling software for clinics"
    duties: []                     # Every duty, even small ones
    tools: []                      # Every tool touched, with real proficiency
    numbers: []                    # Only numbers the user can defend
    did_not_do: []                 # So Claude never claims them
    channels: "email and tickets, no phone"
pinned_bullets: []                 # Bullets that go on every resume verbatim
never_say: []                      # Client names, departments, tools never to mention
domain_proof_points:               # Shown only on matching roles
  - text: "Research assistant on a published clinical study"
    only_for: ["health care", "clinical", "research"]

# === Career Ops settings (defaults in references/standing-rules.md) ===
settings:
  pay_floor: "$42,000/yr or $20/hr"
  home_state: "Ohio"               # Used to skip postings whose state list leaves it out
  avoid: ["phone-heavy", "sales", "security clearance"]
  simple_no_calls_bonus: true      # +0.5 for very simple, call-free work
  hard_skills_are_gaps: true       # Coding, Git, APIs count as gaps
  resume_title_format: "Project Manager ({subsection})"
  pass_score: 3.0
  standard_resume_at: 3.8
  target_state_at_h: 3.6
  target_state_limits: "No certs, classes or degrees. Days-to-learn only. One tool per category. Keep 2+ real bullets."
  reapply_after_rows: 150
  google_sheet_url: ""
  form_defaults:
    source: "Company careers page"
    work_authorization: "Yes"
    sponsorship: "No"
    travel: ""
```

## Notes

- `work_history` is the most important field for accurate evaluations.
  It's populated automatically when you paste your resume during setup.
- `credentials` only matter for regulated industries (Healthcare, Legal,
  Trades, Non-Software Engineering, Finance, Education, Government).
  If your industry doesn't require licenses, leave it empty.
- `persona` modifiers adjust scoring weights. See scoring-rubric.md.
