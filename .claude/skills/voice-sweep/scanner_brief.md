# Scanner brief — voice-pack conformance sweep (v2, 2026-07-17)

You are scanning ONE chapter of a statistics textbook for violations of the author's writing voice. This is a read-only review task: read the files below, then reply with findings as structured data. Your final message is consumed by another agent, not shown to a human — return only the findings in the specified format, with no preamble and no narration of what you did.

## Read first, in this order

1. `/Users/jm75583/Dropbox/voice-pack/voice/JARED_VOICE.md` — the voice rules (especially §2.2 non-negotiables incl. Rule 11, §2.4 vocabulary bans, and §2.6 editing calibration)
2. `/Users/jm75583/Dropbox/voice-pack/voice/JARED_CHECKLIST.md` — the QA checklist
3. `/Users/jm75583/Dropbox/voice-pack/voice/JARED_EXAMPLES.md` — the voice done RIGHT. **This file is the primary reference — calibrate on it, not on the chapter's own prose.** Much of the draft is machine-generated imitation of the voice; a phrasing is not acceptable just because the draft uses it elsewhere. Register drops ("that's real money!", "squinting away", "I won't bore you"), direct reader address, "we"/"I" narration, and colloquial moments are the author's own style — never flag those.
4. `/Users/jm75583/Dropbox/intro_notes_revision/.claude/skills/book-style/SKILL.md` — five book-specific rules, each with good/bad examples

Then read the ENTIRE target chapter file given to you, start to finish.

## North star

Academic, accessible teaching voice: a patient instructor reasoning out loud. The author's rule on emphasis: **if it's in the book, it's important** — prose must never rank its own importance, manage the reader's attitude, or perform. The failure modes to catch are LLM-speak, consultant-speak, and staged performance.

## What to flag — primary (the author's explicit targets)

- **LLM-isms / stock AI phrasing:** "load-bearing", "key insight", "the takeaway", "here's the powerful part", "at its core", "simply put", aphoristic or slogan-like sentences, flourishes that trade information for a turn of phrase.
- **"Not just X, but Y" — judge by the role it plays:** flag as `needs` when it persuades, sells, or emphasizes X's importance — the reframe where Y re-describes the same thing one rung grander and X is a foil to transcend ("not just a formula, but a way of seeing the data"). Do NOT flag uses that make something objective clearer or expand a point with real content (the author's examples: "The second portfolio is not just riskier, it has lower expected returns"; "not just which outcomes can happen, but how likely each one is"). Emphasis done additively, enhancing the original claim, is allowed. Same test for the variants ("isn't just," "not only … but (also)," "more than just"). Unsure of the role → `borderline`.
- **MBA / consultant-speak:** "an X-sigma event" used as vocabulary flair, "playbook", "unpack", "toolkit" as a frame, "close the loop", "best of both worlds", "feature not a bug", "earns its keep", "the X to reach for", pitching a method instead of teaching it, manufactured momentum ("let's dive in", "here's where it gets powerful").
- **Importance-ranking meta-commentary:** "worth memorizing / noting / remembering / internalizing / filing away / mentioning / stating", "it's important to remember", "keep in mind", "we must remember", "deserve(s) emphasis" — anything that tells the reader to rank the material instead of just teaching it. ("Worth" in a decision context is fine: "worth considering," "judged the risk not worth it.")
- **Telegraphing (book-style rule 2):** announcing a structural move before making it ("Let's connect this to…", "One word on…", "A caution here:", "One caution before moving on"); staging a reveal ("X is where things get interesting", "it turns out that…" as drumroll, "something remarkable happens"); billing an example before giving it ("The classic illustration is…", "makes a good worked example because…", "…is a good example." — the author's handoffs are "For example,", "As an example let's compute…", "Take the…", and "Here's an example…"); naming the lesson after the prose already made it ("the whole point is", "this shows that", "the lesson generalizes").
- **Post-figure narration that doesn't earn its ink:** prose after a figure that restates what is plain to see in it, or side-observations orthogonal to the section's through-line. The author sets a figure up beforehand and puts what-to-see in the caption; after-figure prose stays only when it points out something non-obvious or something the next step depends on. Flag plain-to-see walkthroughs as borderline; do not flag genuine interpretation or content that feeds what follows.
- **Emotion-rating of results:** "the surprise", "striking", "remarkable" applied to output. The author rates results by information or use ("more informative"), not reader reaction. Plain comparative "interesting" is NOT a flag — the author writes "more interesting" himself; the target is emotion-billing, not the word.
- **Forward-importance claims:** "an identity we will use constantly", "…will carry us through everything that follows". The author shows importance by linking backward to what the reader already has; short forward links ("We'll do that next") are fine.
- **Aphoristic closers:** a paragraph- or section-ending sentence that generalizes the lesson the example just made ("What it adds depends on what it's joining."). The author's closers state the case result or the decision it informs. Caption zingers count ("Nearly identical correlations, very different lines.").
- **Redundancy (the uniqueness test):** a sentence that restates the previous sentence, re-delivers a point the surrounding paragraphs just made, respends a metaphor already used for the same idea, or recites what a table or figure already shows. Closers that recap the section's own demonstration count, even when plainly worded — check what the preceding paragraphs already delivered before crediting a closer with content.
- **Performed enthusiasm / flourishes** in prose or figure captions. Chunk-option strings that render as prose (`#| fig-cap: "..."`) count as captions — check them.
- **Invented frameworks (book-style rule 4):** a bolded taxonomy or named multi-part breakdown that reads like imported structure rather than the book's own. Flag for verification rather than assuming.
- **Unresolved references / empty gestures:** a callback to a promise or frame that doesn't exist earlier in the book ("keeps that promise", "one more time" for a first occurrence), or a line that gestures at content without delivering it. Verify cross-references and antecedents before trusting a crafted line.

## What to flag — secondary (voice-pack non-negotiables, only when flagrant)

- Throat-clearing paragraph openers ("It is important to note", "There are several considerations").
- "Importantly," / "Interestingly," / "Notably" as sentence openers; "clearly" / "trivially" / "obviously" used to SKIP a reasoning step (fine when the reasoning is right there).
- Banned vocabulary: utilize, moreover, furthermore, additionally ("Further," as a connector counts), arguably, leverage, delve, multifaceted, foster, navigate, compelling, pivotal, transformative, "in order to", "significant" in a non-statistical sense.
- Passive voice with a known agent where it deadens the passage ("it is estimated" → "we estimate").
- A formula or new statistical quantity with no plain-English restatement in the same or next sentence.
- Degree adjectives with no number ("a substantial difference") where a number is available in context; stacked intensity rankings ("quite useful … immensely useful" — "quite" is the house level).
- Emphasis typography: whole clauses bolded (bold is for first-use key terms; emphasis takes italics), ALL-CAPS headings.

## Do NOT flag

- R code chunks, YAML front matter, or math — except chunk-option caption strings, and obvious typos anywhere.
- The author's own register: colloquial drops, direct reader address, "Note that…" openers, em-dash asides under ~10 words, short claims with justification attached even when emphatic ("Independence is important here! If the projects were dependent…"), purpose statements and short forward links.
- Cross-references themselves — only importance-ranking framing wrapped around them.
- **Text inside `<!-- -->` comment blocks** — report it under PARKED, not as a live flag. Map the comment blocks before you start flagging.

## Tiers

- `needs` — a clear violation.
- `borderline` — defensible, or you are unsure. **When in doubt, include as borderline rather than omit.** Missing a real violation is worse than over-flagging; the adjudicator filters.
- `parked` — a violation inside a commented-out block (give the block's line range).

## Output format — exactly this, one block per flag, ordered by line number

```
FLAG
lines: <start>-<end>
section: <nearest ## or ### heading>
tier: needs | borderline | parked
rule: <short label: meta-commentary | telegraphing | staged reveal | aphoristic closer | emotion-rating | forward-importance | consultant-speak | LLM-ism | flourish | banned vocab: <word> | throat-clearing | announcer opener | skip word | passive voice | no restatement | unquantified | emphasis typography | invented framework | unresolved reference>
quote: "<exact text copied verbatim from the file — the minimal offending sentence(s)>"
why: <one line>
```

After all flags:

```
TYPOS: <line>: "<misspelling>" → "<correction>"   (one per line, or "TYPOS: none")
NOTES: <≤3 lines — e.g. a dataset introduced in full here (name it and give the line, so cross-chapter duplication can be checked); a section that reads off-voice overall without one quotable line (give its line range); or "none">
```

If the chapter is clean, reply `NO FLAGS` followed by the TYPOS and NOTES sections.
