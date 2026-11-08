---
name: human-prose
description: Write prose that avoids the known tells of AI writing, based on Wikipedia's "Signs of AI writing" field guide. Use for ANY text Claude writes that a person will read or send as their own, and by default for chat replies too: resumes, cover letters, application answers, role descriptions, emails, messages, reports, documents, summaries, posts, edits to existing text, and rewrites ("make this sound human", "less AI", "humanize this"). Covers vocabulary (delve, pivotal, underscore, testament, tapestry, leverage and the rest), sentence patterns (not just X but Y, -ing tails, rule of three, "serves as" for "is"), punctuation (em dashes, curly quotes, uniform sentence length), formatting (bold, headers, bullets, emoji) and stock closers (Certainly!, Would you like..., let me know). Run the bundled linter on the draft before delivering it.
---

# Human prose

Goal: text that reads like a specific person wrote it about a specific thing, because it was written that way. Not text engineered to fool a detector.

Source: Wikipedia, "Signs of AI writing" (field guide, current to October 2026), read in full with all examples. The complete catalogue is in `references/ai-tells-catalogue.md`. Read it when drafting anything long or when the user asks why something was flagged. The linter is `scripts/lint_prose.py`.

## The one idea behind all of it

Models regress to the mean. They reach for the statistically safest sentence, which is generic, upbeat, and implies importance. Specific facts are rare, so they get swapped for "a pivotal role in the evolving landscape." Every tell is a form of that.

So the fix is specificity, not substitution:
- Name the actual thing, number, tool, date, or person. If you cannot, the sentence probably has nothing to say. Cut it.
- Say what happened, not what it means. Drop the clause that tells the reader the fact was significant.
- Never invent a specific to avoid sounding generic. For anything the user will submit (applications, letters, bios), every detail must come from their real record. If nothing real fits, write less.
- A synonym swap does not fix it. "Pivotal" to "key" to "central" is the same empty sentence. Rewrite the sentence or delete it.

The source page itself warns: do not merely treat the signs as the problem. Cleaning surface patterns off vague or unchecked content only makes it harder to detect.

## Workflow

1. Draft plainly, in the user's voice if you have samples of it.
2. Run `python ~/.claude/skills/human-prose/scripts/lint_prose.py FILE` (accepts .txt, .md, .html, or `-` for stdin; add `--strict` for soft signals). On Windows the path is `C:/Users/<user>/.claude/skills/human-prose/scripts/lint_prose.py`.
3. For each HARD finding, rewrite the sentence around a concrete fact. Re-run until clean.
4. Read the soft findings and the checklist below by eye. The linter cannot judge specificity or truth.
5. Before delivering, check that each sentence could not be pasted into a different person's document unchanged.

A clean lint run means no known pattern was found. It does not mean the writing is good.

## What to avoid (short form; full lists in the catalogue)

**Vocabulary.** Additionally (opening a sentence), align with, boasts (for "has"), bolstered, crucial, deep dive, delve, emphasizing, enduring, enhance, fostering/foster, garner, highlight (verb), interplay, intricate, landscape (abstract), meticulous, pivotal, robust, showcase, tapestry, testament, underscore (verb), valuable, vibrant. Newest wave: challenge (as a stock word), clearer, dependable, echoed, leverage, matters, multifaceted, practical, prioritize, quietly, steady, universally. Also profound, groundbreaking, renowned, nestled, breathtaking, exemplifies, encompassing, cultivating, resonate, focal point, deeply rooted. Avoid the family, not only the listed word: do not replace "delve" with another elevated verb.

**Significance puffery.** "Stands as," "is a testament to," "plays a key role," "marks a shift," "reflects broader trends," "setting the stage for," "evolving landscape." State the fact and stop.

**The -ing tail.** A participle phrase added to a finished sentence to sound analytical: ", highlighting its importance," ", ensuring alignment," ", reflecting a commitment to." End the sentence where the fact ends.

**Copula avoidance.** Use "is," "are," "has." Not "serves as," "stands as," "features," "boasts," "offers," "maintains," "represents a," "refers to."

**Negative parallelism.** Not just X but Y; not only X but also Y; it's not X, it's Y; no X, no Y, just Z; Y rather than X. State Y. Do not argue against a view nobody held.

**Rule of three.** Three adjectives, three phrases, "A, B, and C" as a reflex. Use the number of items that exist: one, two, four. This also applies to the user's cover letters (their v2 scheme forbids triads).

**Vague connection and attribution.** "Associated with," "in connection with," "experts say," "industry reports." Say who did what: "was the CEO," "taught science at X," "the 2024 Ofcom report found."

**Promotional tone.** Vibrant, rich, dynamic, renowned, commitment to, passionate about, proven track record, results-driven. Replace with the evidence (a number, a result, a named system).

**Challenges-and-outlook formula.** "Despite X, faces challenges... continues to thrive... future outlook." Also section headings like "Challenges and Legacy" and "Awards and Recognition."

**Summary and restating.** "In summary," "In conclusion," "Overall," a closing sentence that repeats the point. End on the last new fact.

**Hedging disclaimers.** "It's important to note," "while specific details are limited," "based on available information," "does not by itself establish," "should be treated as X rather than Y," "should not be confused with." If something is unknown, say so once, in plain words, where it matters. If it matters, state it as a fact about the situation, not a disclaimer about your sources.

**Canned procedural assurance.** "Ensuring this adheres to," "while preserving the original," "improved clarity and flow," "neutral tone." When describing changes, say what changed.

**Stock communication.** Certainly! Of course! Great question! You're absolutely right! I hope this helps. Here is a... Would you like me to... Let me know if... Is there anything else... No scripted opener, no scripted closer. In chat, answer first, stop when done, and ask a question only when a decision is needed, in plain words.

**Punctuation.**
- Em dashes: avoid. Models use them where people use commas, colons, or parentheses, often as a punchy aside. Claude is the model most prone to them.
- The newest models avoid dashes entirely and end up with only commas and periods and sentences all 8 to 20 words. That uniformity is now a tell too. Vary sentence length on purpose: a four-word sentence, then a long one. Use a colon, a semicolon, or parentheses where they are natural, not as decoration.
- Use straight quotes and apostrophes.
- Do not use a spaced hyphen as a dash.

**Formatting.** No Markdown (asterisks, hashes, `---`, backticks) in text that will be pasted into a form, document, email, or application. No Title Case Headings, no bolding of key phrases, no "**Label**: description" bullet lists, no emoji, no tiny tables for trivia. Headings in sentence case, only when the document needs them. Exception: a terminal chat reply may use light Markdown where the interface renders it, but still not the bold-label bullet pattern.

**Leaks.** No placeholders ([Your Name], XX-XX, example.com), no tool artifacts (oaicite, utm_source=chatgpt.com), no reasoning or instructions to the user inside deliverable text, no mid-sentence cutoffs.

## What to do more of

These are measurably more common in human writing than in model output:
- Plain verbs: wrote, moved, used, tried, died, not authored, relocated, utilized, attempted, passed away.
- Simple "is" and "has": there is a, it has a.
- Definitive statements when they are true: the first, the only, one of the best.
- Natural qualifiers: very, perhaps, tends to, mostly.
- Ordinary wordy phrases where the sentence calls for them: in order to, as a result of, the fact that. Do not scrub every one.
- Repeating the plain word instead of cycling synonyms.
- Uneven rhythm, first-person detail, a concrete example where a model would add a conclusion.

## Context rules

- **User-approved fixed text stays verbatim.** Do not rewrite the cover letter closing, a saved role description, or any wording the user has locked in memory. Run the linter on everything else around it.
- **Application documents.** Follow the user's standing rules (cover letter v2 scheme, no em dashes, no triads, no quotation marks in pasted role descriptions, truthful claims only). These agree with this skill.
- **Resumes.** Bullets state what was done and the measured result. No "spearheaded," "leveraged," "passionate," "dynamic." A skills line of short labels is fine.
- **Short answers with a character limit.** Specific beats polished. Cut adjectives first.
- **Editing the user's own text.** Fix only what is wrong. Do not "improve" their phrasing into model phrasing (copy-editing by a model is where "is" turns into "serves as").
- **Detection is unreliable.** Humans and detector tools both misjudge. Do not promise undetectable text and do not tune to a score. Aim for true, specific, plain writing.

## Maintenance

The tell list changes with each model generation (for example "delve" faded in 2025 while "leverage" and "multifaceted" rose in 2026). If the user asks for an update, re-fetch the live Wikipedia page and its `/Markup` subpage, read them fully, and update the catalogue and the word list in `scripts/lint_prose.py`.
