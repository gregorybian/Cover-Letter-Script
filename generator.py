# Variables to change
company = "Honeywell"
position = "Embedded Engineer"
employer = ""
address = "400 Maple Grove Road"
length = "8"
bs = "Redbrick’s mission to reimagine the modern browser through large-scale Chromium development and a thoughtful, user-focused design is particularly compelling to me, as it combines complex C++ engineering with real-world impact on how people work every day. As someone who values responsibility, collaboration, and mentorship, I am excited about the opportunity to contribute and grow within Redbrick's people-first culture."

#example bs
"""
LMI Technologies Inc’s work developing 3D machine vision sensors and manufacturing infrastructure is particularly
compelling to me, as it combines algorithmic software, calibration pipelines, and automated testing in a
multidisciplinary R&D environment. As someone who values responsibility and mentorship, I am excited about
the opportunity to work with LMI Technologies Inc. 

write this in a line for the following job posting, keep the sentence format and do NOT use em dashes or semicolons.
"""

# import operating system to rename files
import os
import shutil
import time

# String array to parse into tex file
lines_to_add = [
    r"\newcommand{\company}{%s}" %(company) + "\n",
    r"\newcommand{\position}{%s}" %(position) + "\n",
    r"\newcommand{\employer}{%s}" %(employer) + "\n",
    r"\newcommand{\address}{%s}" %(address) + "\n",
    r"\newcommand{\length}{%s}" %(length) + "\n",
    r"\newcommand{\bs}{%s}" %(bs) + "\n"
]

# Reads file returns string array with lines
def read_file():
    try:
        with open("template.tex", 'r') as file:
            text = file.readlines()
            return text
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Writes to file
def write_file(text):
    index = None
    index_end = None
    for i, line in enumerate(text):
        if line.strip() == "%variables%":
            index = i + 1
        if line.strip() == "%end%":
            index_end = i
            break

    if index is None:
        raise ValueError("%variables% not found in file")

    lines = text[:index] + lines_to_add + text[index_end:]
    with open("template.tex", "w") as file:
        file.writelines(lines)


def clear_files():
    new_name = "%s_CoverLetter.pdf" %(company)
    new_path = os.path.join("Summer_2026_Apps", new_name)

    if(os.path.exists(new_name)):
        os.remove(new_name)
    os.rename("template.pdf", new_name)
    if os.path.exists(new_path):
        os.remove(new_path)  
    shutil.move(new_name, "Summer_2026_Apps/")

    # Remove files
    os.remove("template.aux")
    os.remove("template.fdb_latexmk")
    os.remove("template.fls")
    os.remove("template.log")
    os.remove("template.out")
    os.remove("template.synctex.gz")


if (__name__ == "__main__"):
    # Read and Write the file
    text = read_file()
    write_file(text)

    # Wait to generate pdf, rename and clear
    time.sleep(15)
    clear_files()