#!/usr/bin/env python3
"""CLI: build the tailored resume.tex working copy at repo root into a PDF, archive it."""
import argparse
import os
import shutil
import subprocess
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKING_TEX = os.path.join(REPO_ROOT, "resume.tex")
OUTPUT_DIR = os.path.join(REPO_ROOT, "Fall_2026_Apps", "Resume")
ARCHIVE_DIR = os.path.join(OUTPUT_DIR, "Archive")

BUILD_ARTIFACTS = [
    "resume.aux",
    "resume.fdb_latexmk",
    "resume.fls",
    "resume.log",
    "resume.out",
    "resume.synctex.gz",
]


def parse_args():
    parser = argparse.ArgumentParser(
        description="Build the tailored resume.tex working copy into a PDF"
    )
    parser.add_argument("--company", required=True)
    return parser.parse_args()


def build_pdf():
    if not os.path.exists(WORKING_TEX):
        raise RuntimeError(
            "resume.tex not found at repo root - copy Fall_2026_Apps/Resume/"
            "resume_master.tex there and tailor it before running this script."
        )

    # Same flaky-exit-code caveat as build_cover_letter.py: trust the PDF +
    # log over latexmk's own return code.
    result = subprocess.run(
        ["latexmk", "-pdf", "-interaction=nonstopmode", "resume.tex"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    pdf_path = os.path.join(REPO_ROOT, "resume.pdf")
    log_path = os.path.join(REPO_ROOT, "resume.log")
    fatal_error = False
    if os.path.exists(log_path):
        with open(log_path, "r", errors="replace") as f:
            fatal_error = any(line.startswith("!") for line in f)

    if fatal_error or not os.path.exists(pdf_path):
        log_tail = "\n".join(result.stdout.splitlines()[-40:])
        raise RuntimeError(f"latexmk failed (exit {result.returncode}):\n{log_tail}")


def archive_previous_resumes():
    os.makedirs(ARCHIVE_DIR, exist_ok=True)
    for name in os.listdir(OUTPUT_DIR):
        if not name.endswith("_Resume.pdf"):
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
    archive_previous_resumes()
    new_path = os.path.join(OUTPUT_DIR, f"{company}_Resume.pdf")
    shutil.move(os.path.join(REPO_ROOT, "resume.pdf"), new_path)
    return new_path


def clean_artifacts():
    for name in BUILD_ARTIFACTS:
        path = os.path.join(REPO_ROOT, name)
        if os.path.exists(path):
            os.remove(path)
    if os.path.exists(WORKING_TEX):
        os.remove(WORKING_TEX)


def main():
    args = parse_args()

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
