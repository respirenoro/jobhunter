"""Build a one-page resume from a JSON spec.

Usage:
    python scripts/build_resume.py spec.json [--target-state] [--max-pages 1]

Fills references/resume-template.html, writes the HTML to
data/resumes/ (or data/resumes/Target State Resumes/ with --target-state),
prints a PDF with headless Chrome or Edge into the matching "(PDF)" folder,
and reports the page count. It refuses to overwrite an existing file.

spec.json:
{
  "company": "Acme", "role": "Operations Analyst",
  "name": "Jane Doe", "initials": "JD",
  "contact": "City, ST | jane@example.org | (555) 555-0100 | linkedin.com/in/jane",
  "title": "Project Manager (Operations)",           # optional headline under the name
  "page_size": "letter",
  "summary": "Two or three plain sentences.",
  "experience": [
    {"title": "...", "company": "...", "location": "Remote", "dates": "Jan 2025 - Present",
     "bullets": ["...", "..."]}
  ],
  "education": [{"degree": "BA Biology", "school": "State University", "year": "2019"}],
  "extra_education_lines": ["Research: one line, only for roles where it belongs"],
  "skills": {"Skills": ["...", "..."], "Technologies": ["...", "..."], "Languages": ["English (Fluent)"]},
  "certifications": [], "projects": []
}
"""
import html
import json
import os
import re
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE = os.path.join(ROOT, "references", "resume-template.html")


def esc(s):
    return html.escape(str(s), quote=False)


def find_browser():
    for name in ("chrome", "google-chrome", "chromium", "msedge"):
        p = shutil.which(name)
        if p:
            return p
    for p in (
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    ):
        if os.path.exists(p):
            return p
    return None


def render(spec):
    t = open(TEMPLATE, encoding="utf-8").read()
    exp = []
    for e in spec.get("experience", []):
        lis = "\n".join("      <li>%s</li>" % esc(b) for b in e.get("bullets", []))
        where = esc(e["company"]) + (" | " + esc(e["location"]) if e.get("location") else "")
        exp.append(
            '<div class="entry">\n    <div class="entry-header">\n'
            '      <span class="title">%s</span>\n      <span class="dates">%s</span>\n    </div>\n'
            '    <div class="company">%s</div>\n    <ul>\n%s\n    </ul>\n  </div>'
            % (esc(e["title"]), esc(e.get("dates", "")), where, lis)
        )
    edu = [
        '<div class="edu-entry">\n    <span class="degree">%s</span> | %s%s\n  </div>'
        % (esc(d["degree"]), esc(d["school"]), (", " + esc(d["year"])) if d.get("year") else "")
        for d in spec.get("education", [])
    ]
    edu += ['<div class="edu-entry">%s</div>' % esc(x) for x in spec.get("extra_education_lines", [])]
    skills = [
        '<div class="category"><span class="category-name">%s:</span> %s</div>'
        % (esc(k), " &middot; ".join(esc(v) for v in vals))
        for k, vals in spec.get("skills", {}).items() if vals
    ]
    certs = ""
    if spec.get("certifications"):
        certs = "<h2>Certifications</h2>\n" + "\n".join(
            '<div class="edu-entry">%s</div>' % esc(c) for c in spec["certifications"])
    projects = ""
    if spec.get("projects"):
        projects = "<h2>Projects</h2>\n" + "\n".join(
            '<div class="edu-entry">%s</div>' % esc(p) for p in spec["projects"])
    contact = esc(spec.get("contact", ""))
    if spec.get("title"):
        contact = '<div class="headline">%s</div>%s' % (esc(spec["title"]), contact)
    fills = {
        "NAME": esc(spec["name"]),
        "PAGE_SIZE": spec.get("page_size", "letter"),
        "CONTACT_LINE": contact,
        "SUMMARY": esc(spec.get("summary", "")),
        "EXPERIENCE": "\n  ".join(exp),
        "EDUCATION": "\n  ".join(edu),
        "SKILLS": "\n    ".join(skills),
        "CERTIFICATIONS": certs,
        "PROJECTS": projects,
    }
    for k, v in fills.items():
        t = t.replace("{{%s}}" % k, v)
    left = re.findall(r"\{\{[A-Z_]+\}\}", t)
    if left:
        sys.exit("unfilled placeholders: %s" % left)
    return t


def main(argv):
    if len(argv) < 2:
        sys.exit(__doc__)
    spec = json.load(open(argv[1], encoding="utf-8"))
    target = "--target-state" in argv
    max_pages = int(argv[argv.index("--max-pages") + 1]) if "--max-pages" in argv else 1

    base = os.path.join(ROOT, "data", "resumes")
    html_dir = os.path.join(base, "Target State Resumes") if target else base
    pdf_dir = os.path.join(base, "Target State Resumes (PDF)" if target else "resumes (PDF)")
    os.makedirs(html_dir, exist_ok=True)
    os.makedirs(pdf_dir, exist_ok=True)

    stem = "%s (%s) - Resume %s" % (spec["company"], spec["role"], spec["initials"])
    html_path = os.path.join(html_dir, stem + ".html")
    pdf_path = os.path.join(pdf_dir, stem + ".pdf")
    for p in (html_path, pdf_path):
        if os.path.exists(p):
            sys.exit("REFUSING TO OVERWRITE: %s\nPick a more specific role label." % p)

    open(html_path, "w", encoding="utf-8").write(render(spec))
    print("HTML:", html_path)

    browser = find_browser()
    if not browser:
        print("No Chrome or Edge found. Open the HTML and print it to PDF by hand.")
        return
    url = "file:///" + html_path.replace("\\", "/")
    subprocess.call(
        [browser, "--headless", "--disable-gpu", "--no-pdf-header-footer", "--print-to-pdf=" + pdf_path, url],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    if not os.path.exists(pdf_path):
        sys.exit("PDF was not created.")
    pages = len(re.findall(rb"/Type\s*/Page[^s]", open(pdf_path, "rb").read()))
    print("PDF:", pdf_path, "| pages:", pages)
    if pages > max_pages:
        print("TOO LONG: %d pages, limit %d. Cut a bullet or tighten wording, then rebuild "
              "(delete both files first)." % (pages, max_pages))


if __name__ == "__main__":
    main(sys.argv)
