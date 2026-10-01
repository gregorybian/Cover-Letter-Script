---
name: resume
description: Generate a tailored resume PDF for a specific company and job posting, based on this repo's master LaTeX resume. Use when the user asks to tailor, generate, or update a resume, or names a company plus a job posting for a resume.
---

# Resume Tailoring

Produces a resume PDF via `scripts/build_resume.py`, which builds a working
`resume.tex` copy with `latexmk`. Your job is the part the script can't do:
decide which existing content to emphasize, reorder, or cut to match the
posting.

## 1. Gather inputs

Required: company name, and the job posting (pasted text, or a URL to fetch
with WebFetch).

From the posting, extract the position title. If it's missing, ask the user
for it.

## 2. Confirm before proceeding

Before editing anything, show the user what you extracted and STOP to get
explicit confirmation:

- Company
- Position title

Do not continue until the user confirms these are correct, or corrects them.

## 3. Read the master resume

Read `Fall_2026_Apps/Resume/resume_master.tex` in full alongside the job
posting.

## 4. Decide tailoring

Compare the posting's requirements/keywords against the master's bullets
and projects. Decide:
- Which bullets to reorder or lead with (most relevant to this posting
  first within each section)
- Which wording to tighten toward the posting's own terms (e.g. if the
  posting says "test automation," prefer that phrasing where truthful)
- Which currently-commented-out projects (if any better match the posting)
  to swap in, and which included ones to drop, to stay on one page

This is content selection and rewording only — never fabricate experience,
skills, or metrics that aren't already true of Gregory's background per the
master file.

## 5. Build the working copy

Copy the master to a scratch file, then edit the scratch copy:

```bash
cp Fall_2026_Apps/Resume/resume_master.tex resume.tex
```

Edit `resume.tex` (repo root) with the tailored changes from step 4. Leave
`resume_master.tex` untouched — it's the permanent source.

## 6. Build the PDF

Run from the repo root:

```bash
python3 scripts/build_resume.py --company "Company Name"
```

If it exits non-zero, it printed the `latexmk` log tail to stderr: report
the error to the user rather than retrying blindly.

## 7. Report

On success the script prints the path to the new PDF
(`Fall_2026_Apps/Resume/{Company}_Resume.pdf`). Tell the user that path. Any
resume that was already sitting in `Fall_2026_Apps/Resume/` gets moved into
`Fall_2026_Apps/Resume/Archive/` automatically before the new one is saved.
