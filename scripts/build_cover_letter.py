#!/usr/bin/env python3
"""CLI: splice cover letter variables into template.tex, build the PDF, archive it."""
import argparse
import os
import re
import shutil
import subprocess
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE = os.path.join(REPO_ROOT, "template.tex")
OUTPUT_DIR = os.path.join(REPO_ROOT, "Fall_2026_Apps", "Cover_Letters")
ARCHIVE_DIR = os.path.join(OUTPUT_DIR, "Archive")
DEFAULT_ADDRESS = "999 West Broadway, Suite 720, Vancouver, BC V5Z 1K5"

BUILD_ARTIFACTS = [
    "template.aux",
    "template.fdb_latexmk",
    "template.fls",
    "template.log",
    "template.out",
    "template.synctex.gz",
]

# Order matters: backslash must be escaped first so later replacements don't
# double-escape the backslashes they introduce.
LATEX_ESCAPES = [
    ("\\", r"\textbackslash{}"),
    ("&", r"\&"),
    ("%", r"\%"),
    ("$", r"\$"),
    ("#", r"\#"),
    ("_", r"\_"),
    ("{", r"\{"),
    ("}", r"\}"),
    ("~", r"\textasciitilde{}"),
    ("^", r"\textasciicircum{}"),
]


def escape_latex(text):
    for char, escaped in LATEX_ESCAPES:
        text = text.replace(char, escaped)
    return text


def parse_args():
    parser = argparse.ArgumentParser(description="Build a cover letter PDF from template.tex")
    parser.add_argument("--company", required=True)
    parser.add_argument("--position", required=True)
    parser.add_argument("--bs", required=True, help="Company-specific opening paragraph")
    parser.add_argument("--employer", default="")
    parser.add_argument("--address", default=DEFAULT_ADDRESS)
    parser.add_argument("--length", default="8")
    return parser.parse_args()


def read_template():
    with open(TEMPLATE, "r") as f:
        return f.readlines()


def write_template(lines_to_add):
    text = read_template()
    index = None
    index_end = None
    for i, line in enumerate(text):
        if line.strip() == "%variables%":
            index = i + 1
        if line.strip() == "%end%":
            index_end = i
            break

    if index is None or index_end is None:
        raise ValueError("%variables% / %end% markers not found in template.tex")

    lines = text[:index] + lines_to_add + text[index_end:]
    with open(TEMPLATE, "w") as f:
        f.writelines(lines)


def build_pdf():
    # No -halt-on-error: it made latexmk's own rerun-for-bookmarks pass
    # (triggered by rerunfilecheck/hyperref) flake between 1 and 2 runs,
    # sometimes reporting exit 12 even though template.pdf built fine.
    # Trust the PDF + log instead of latexmk's exit code.
    result = subprocess.run(
        ["latexmk", "-pdf", "-interaction=nonstopmode", "template.tex"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    pdf_path = os.path.join(REPO_ROOT, "template.pdf")
    log_path = os.path.join(REPO_ROOT, "template.log")
    fatal_error = False
    if os.path.exists(log_path):
        with open(log_path, "r", errors="replace") as f:
            fatal_error = any(line.startswith("!") for line in f)

    if fatal_error or not os.path.exists(pdf_path):
        log_tail = "\n".join(result.stdout.splitlines()[-40:])
        raise RuntimeError(f"latexmk failed (exit {result.returncode}):\n{log_tail}")


def archive_previous_cover_letters():
    os.makedirs(ARCHIVE_DIR, exist_ok=True)
    for name in os.listdir(OUTPUT_DIR):
        if not name.endswith("_CoverLetter.pdf"):
            continue
        old_path = os.path.join(OUTPUT_DIR, name)
        if not os.path.isfile(old_path):
            continue
        archived_path = os.path.join(ARCHIVE_DIR, name)
        if os.path.exists(archived_path):
            os.remove(archived_path)
        shutil.move(old_path, archived_path)


def save_pdf(company):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    archive_previous_cover_letters()
    new_path = os.path.join(OUTPUT_DIR, f"{company}_CoverLetter.pdf")
    shutil.move(os.path.join(REPO_ROOT, "template.pdf"), new_path)
    return new_path


def clean_artifacts():
    for name in BUILD_ARTIFACTS:
        path = os.path.join(REPO_ROOT, name)
        if os.path.exists(path):
            os.remove(path)


def main():
    args = parse_args()

    lines_to_add = [
        r"\newcommand{\company}{%s}" % escape_latex(args.company) + "\n",
        r"\newcommand{\position}{%s}" % escape_latex(args.position) + "\n",
        r"\newcommand{\employer}{%s}" % escape_latex(args.employer) + "\n",
        r"\newcommand{\address}{%s}" % escape_latex(args.address) + "\n",
        r"\newcommand{\length}{%s}" % escape_latex(args.length) + "\n",
        r"\newcommand{\bs}{%s}" % escape_latex(args.bs) + "\n",
    ]

    write_template(lines_to_add)

    try:
        build_pdf()
    except RuntimeError as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)

    output_path = save_pdf(args.company)
    clean_artifacts()
    print(output_path)


if __name__ == "__main__":
    main()
