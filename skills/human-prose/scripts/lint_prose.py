#!/usr/bin/env python3
"""Flag AI-writing tells in a draft (Wikipedia "Signs of AI writing", Oct 2026).

Usage:
    python lint_prose.py FILE            # file may be .txt, .md or .html (tags are stripped)
    python lint_prose.py -               # read stdin
    python lint_prose.py FILE --strict   # also report soft signals

Exit code 1 when any HARD finding exists, else 0. This is an aid, not a detector:
it finds known patterns; it cannot judge whether the text is specific and true.
Fix the cause (be concrete), not just the flagged word, and do not swap in a synonym.
"""
import re
import statistics
import sys

# ---- hard findings: rewrite these ------------------------------------------------

WORDS = [
    # vocabulary lists, all eras
    "additionally", "align with", "aligns with", "aligned with", "boasts", "bolstered", "bolster",
    "crucial", "deep dive", "delve", "delves", "delving", "emphasizing", "emphasising", "enduring",
    "enhance", "enhances", "enhancing", "fostering", "foster", "fosters", "garner", "garners",
    "highlighting", "highlights", "interplay", "intricate", "intricacies", "landscape",
    "meticulous", "meticulously", "pivotal", "robust", "showcase", "showcases", "showcasing",
    "tapestry", "testament", "underscore", "underscores", "underscoring", "valuable",
    "vibrant", "profound", "groundbreaking", "renowned", "nestled", "breathtaking",
    "exemplifies", "encompassing", "cultivating", "resonate", "resonates", "multifaceted",
    "leverage", "leveraging", "leverages", "prioritize", "prioritizing", "dependable",
    "echoed", "universally", "quietly", "steady", "clearer", "focal point", "indelible",
    "deeply rooted", "causal", "empirical",
]

PHRASES = [
    (r"\b(stands|serves|functions|operates|acts) as (a|an|the)\b", "copula avoidance: use 'is'"),
    (r"\b(is|are|was|were) (a )?(testament|reminder) to\b", "significance puffery"),
    (r"\bplays? an? (crucial|vital|key|pivotal|significant|important) role\b", "significance puffery"),
    (r"\b(a|the) (pivotal|key|defining|turning) (moment|point)\b", "significance puffery"),
    (r"\b(underscore|highlight|emphasi[sz]e)s? (its|their|the) (importance|significance)\b", "significance puffery"),
    (r"\bsetting the stage for\b", "significance puffery"),
    (r"\bevolving landscape\b", "significance puffery"),
    (r"\bin the heart of\b", "promotional"),
    (r"\bdiverse array\b|\brich (cultural )?(heritage|tapestry|history)\b", "promotional"),
    (r"\bcommitment to\b", "promotional / canned assurance"),
    (r"\bvaluable insights?\b", "superficial analysis"),
    (r"\b(is|are|was|were|been|being) (closely |widely |broadly )?(associated|connected) with\b", "vague association: state the relationship"),
    (r"\b(in connection with|in association with|connected to)\b", "vague association: state the relationship"),
    (r"\b(industry reports?|observers (have )?(note|cite|say)|experts (argue|say|agree)|some critics|several (sources|publications))\b", "vague attribution"),
    (r"\bdespite (its|these|the|their) [^.]{0,60}(faces?|face|facing) [^.]{0,40}challenges?\b", "'despite challenges' formula"),
    (r"\bnot (only|just|merely|simply) [^.;:!?]{2,80}[,;]? (but|it'?s|it is)\b", "negative parallelism: not just X but Y"),
    (r"\b(it'?s|it is|this is|that'?s|that is|isn'?t|is not|wasn'?t|was not|doesn'?t|does not) (not|just|merely)? ?[^.;:!?]{0,60}[,;] ?(it'?s|it is|but)\b", "negative parallelism"),
    (r"\b[A-Za-z' ]{3,60} rather than [A-Za-z' ]{3,60}\b", "'Y rather than X' contrast"),
    (r"\bno [a-z]+, no [a-z]+,? (just|only)\b", "negative parallelism"),
    (r"\b(it'?s|it is) (important|crucial|worth|essential|vital) (to )?(note|noting|remember|recognize|mention)\b", "didactic hedge"),
    (r"\b(should|must) not be confused with\b|\bdoes not (by itself )?establish\b|\bshould be (treated|viewed|read|understood) as\b", "corrective-framing disclaimer"),
    (r"\b(based on|from) (the )?(available|provided|public(ly available)?) (information|sources|search results)\b", "source-availability hedge"),
    (r"\b(not|isn'?t|aren'?t) (widely|publicly) (documented|available|disclosed)\b|\bwhile specific details\b", "source-availability hedge"),
    (r"^\s*(in summary|in conclusion|overall|to summarize|to sum up)\b[,:]?", "summary closer"),
    (r"\b(certainly|absolutely)!|\bof course!|\bgreat question\b|\byou'?re absolutely right\b|\bI hope this (helps|finds)\b", "collaborative filler"),
    (r"\blet me know\b|\bis there anything else\b|\bwould you like me to\b|\bfeel free to\b", "stock closer"),
    (r"\b(as an ai|as a large language model|knowledge (cutoff|update))\b", "AI self-reference"),
    (r"\bhere(?:'s| is| are) (a|an|the|your|some) ", "'here is a...' lead-in"),
    (r"\b(ensur(ed|ing) (that )?[^.]{0,40}(adher|compl)|in compliance with|neutral tone|while preserving|preserved the|retain(ed|ing) the)\b", "canned procedural assurance"),
    (r"\bmaintains an? (active|strong) (social media|digital) presence\b|\bindependent coverage\b|\bfeatured in\b", "canned notability"),
    (r"\b(passionate about|results[- ]driven|proven track record|dynamic|self-starter|go-getter|rockstar|synerg\w+)\b", "résumé-speak filler (soft in applications)"),
]

# participial tail: ", highlighting ...", ", ensuring ..."
ING_TAIL = re.compile(
    r",\s+(?:thereby |thus |further |also )?(highlighting|underscoring|emphasi[sz]ing|ensuring|reflecting|symbolizing|"
    r"contributing|cultivating|fostering|showcasing|enhancing|encompassing|demonstrating|illustrating|"
    r"facilitating|reinforcing|solidifying|shaping|creating a|offering a|providing a)\b[^.;!?]{0,80}",
    re.I,
)

PLACEHOLDER = re.compile(r"\[[A-Z][A-Za-z0-9 _/'-]{2,40}\]|INSERT_|PASTE_|\(Add [^)]+\)|XX-XX|example\.com|utm_source=|oaicite|turn\d+search\d+|contentReference")
MARKDOWN = re.compile(r"(\*\*[^*\n]+\*\*)|(^#{1,6}\s)|(^\s*[-*]\s+\*\*)|(\[[^\]]+\]\(https?://)|(^```)|(^\s*---+\s*$)", re.M)
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿⭐✅❌]")
EM_DASH = re.compile("—|―| -- ")
CURLY = re.compile("[‘’“”]")
SPACED_HYPHEN = re.compile(r"\s-\s")

# ---- soft signals (--strict) -----------------------------------------------------

TRIAD = re.compile(
    r"\b([A-Za-z-]+(?: [A-Za-z-]+){0,3}), ([A-Za-z-]+(?: [A-Za-z-]+){0,3}),? (?:and|or) ([A-Za-z-]+(?: [A-Za-z-]+){0,3})\b"
)
SENT_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z\"'(])")


def strip_html(text):
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.S)
    text = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", text, flags=re.S | re.I)
    text = re.sub(r"</(p|div|li|h\d|tr|br)>", "\n", text, flags=re.I)
    text = re.sub(r"<br\s*/?>", "\n", text, flags=re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    text = text.replace("&nbsp;", " ").replace("&amp;", "&").replace("&#39;", "'").replace("&middot;", "-")
    return text


def main(argv):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    if len(argv) < 2:
        print(__doc__)
        return 2
    strict = "--strict" in argv
    src = argv[1]
    raw = sys.stdin.read() if src == "-" else open(src, encoding="utf-8", errors="replace").read()
    text = strip_html(raw) if (src.lower().endswith((".html", ".htm")) or "<html" in raw[:500].lower()) else raw

    hard, soft = [], []
    lines = text.splitlines()

    word_re = re.compile(r"\b(" + "|".join(re.escape(w) for w in sorted(WORDS, key=len, reverse=True)) + r")\b", re.I)
    for n, line in enumerate(lines, 1):
        for m in word_re.finditer(line):
            hard.append((n, "ai-vocabulary", m.group(0), line.strip()))
        for pat, label in PHRASES:
            for m in re.finditer(pat, line, re.I):
                hard.append((n, label, m.group(0).strip(), line.strip()))
        for m in ING_TAIL.finditer(line):
            hard.append((n, "-ing tail (superficial analysis)", m.group(0).strip(), line.strip()))
        for m in PLACEHOLDER.finditer(line):
            hard.append((n, "placeholder / artifact", m.group(0), line.strip()))
        for m in MARKDOWN.finditer(line):
            hard.append((n, "markdown in plain text", m.group(0).strip(), line.strip()))
        for m in EMOJI.finditer(line):
            hard.append((n, "emoji", m.group(0), line.strip()))
        for m in EM_DASH.finditer(line):
            hard.append((n, "em dash", m.group(0).strip() or "--", line.strip()))
        for m in CURLY.finditer(line):
            hard.append((n, "curly quote/apostrophe (use straight)", m.group(0), line.strip()))
        for m in SPACED_HYPHEN.finditer(line):
            soft.append((n, "spaced hyphen used as a dash", "-", line.strip()))
        for m in TRIAD.finditer(line):
            soft.append((n, "rule of three", m.group(0), line.strip()))

    # sentence-length uniformity (GPT-6-era tell: everything 8-20 words, commas and periods only)
    body = " ".join(l for l in lines if l.strip())
    sents = [s for s in SENT_SPLIT.split(body) if len(s.split()) >= 3]
    if len(sents) >= 8:
        lens = [len(s.split()) for s in sents]
        in_band = sum(1 for x in lens if 8 <= x <= 20) / len(lens)
        sd = statistics.pstdev(lens)
        if in_band >= 0.85 and sd < 4.5:
            soft.append((0, "uniform sentence length",
                         f"{in_band:.0%} of {len(lens)} sentences are 8-20 words (sd {sd:.1f})",
                         "vary length: mix a very short sentence with a longer one"))
        punct_variety = sum(body.count(c) for c in ":;()")
        if len(sents) >= 8 and punct_variety == 0:
            soft.append((0, "punctuation variety", "no colons, semicolons or parentheses",
                         "only commas and periods can read as machine-regular; use others only where natural"))
    starts = {}
    for s in sents:
        w = s.split()[0].lower().strip(",")
        starts[w] = starts.get(w, 0) + 1
    for w, c in starts.items():
        if c >= 4 and len(sents) >= 8 and w not in ("i", "the", "and"):
            soft.append((0, "repeated sentence opener", f"'{w}' x{c}", ""))

    def show(items, tag):
        for n, label, hit, line in items:
            where = f"line {n}" if n else "whole text"
            ctx = (line[:110] + "...") if len(line) > 110 else line
            print(f"[{tag}] {where}: {label}: '{hit}'" + (f"\n        {ctx}" if ctx else ""))

    show(hard, "HARD")
    if strict:
        show(soft, "soft")
    print(f"\n{len(hard)} hard finding(s)" + (f", {len(soft)} soft" if strict else f" ({len(soft)} soft hidden; use --strict)"))
    if not hard:
        print("No known tells found. That does not make the text good: check that every sentence says something specific and true.")
    return 1 if hard else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
