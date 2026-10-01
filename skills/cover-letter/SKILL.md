---
name: cover-letter
description: Generate a tailored cover letter PDF for a specific company and job posting, using this repo's LaTeX template. Use when the user asks to write, generate, or draft a cover letter, or names a company plus a job posting.
---

# Cover Letter Generator

Produces a cover letter PDF via `scripts/build_cover_letter.py`, which fills
in `template.tex` and builds it with `latexmk`. Your job is the part the
script can't do: research the company and write the opening paragraph.

## 1. Gather inputs

Required: company name, and the job posting (pasted text, or a URL to fetch
with WebFetch).

From the posting, extract:
- Position title
- Employer/hiring manager name and company address, if listed

If the position title is missing from the posting, ask the user for it.
Address and term length may be left at their defaults (script fills in the
usual office address and an 8-month term) unless the user or posting says
otherwise.

## 2. Confirm before proceeding

Before doing any research, show the user what you extracted and STOP to get
explicit confirmation:

- Company
- Position title
- Location (city/region from the posting, e.g. "Langley, British Columbia")

Do not continue to research or build until the user confirms these are
correct, or corrects them. This catches wrong extractions (e.g. a job board
listing the recruiting agency instead of the actual employer) before a PDF
gets built on bad info.

## 3. Research the company

Use WebSearch (and WebFetch on the company's own site if useful) to learn
what the company actually builds and any recent, specific work — products,
projects, news. Generic descriptions ("a leading provider of solutions") are
not enough; the paragraph needs one or two concrete details a generic
cover letter wouldn't have.

## 4. Draft the opening paragraph (the `--bs` argument)

Write exactly 2 sentences, no more than ~60 words total:
- Name something specific and real about the company's work (from step 2)
- Tie it to Gregory's interest in embedded systems, robotics, or hardware/software integration
- Read as one continuous voice — do not use em dashes or semicolons
- Match the tone AND length of past examples, e.g. (58 words):

  > LMI Technologies Inc's work developing 3D machine vision sensors and
  > manufacturing infrastructure is particularly compelling to me, as it
  > combines algorithmic software, calibration pipelines, and automated
  > testing in a multidisciplinary R&D environment. As someone who values
  > responsibility and mentorship, I am excited about the opportunity to
  > work with LMI Technologies Inc.

`copypaste.txt` has reference phrasing for Gregory's experience if useful
context, but the opening paragraph itself must be freshly written for this
company, not reused boilerplate.

## 5. Build the PDF

Run from the repo root:

```bash
python3 scripts/build_cover_letter.py \
  --company "Company Name" \
  --position "Position Title" \
  --bs "The researched opening paragraph." \
  [--employer "Hiring Manager Name"] \
  [--address "123 Street, City, Province Postal"] \
  [--length "8"]
```

The script escapes LaTeX special characters itself — pass plain text.

If it exits non-zero, it printed the `latexmk` log tail to stderr: report
the error to the user rather than retrying blindly (a LaTeX syntax issue in
`template.tex` itself needs a human look).

## 6. Report

On success the script prints the path to the new PDF
(`Fall_2026_Apps/Cover_Letters/{Company}_CoverLetter.pdf`). Tell the user
that path. Any cover letter that was already sitting in
`Fall_2026_Apps/Cover_Letters/` gets moved into
`Fall_2026_Apps/Cover_Letters/Archive/` automatically before the new one
is saved.
