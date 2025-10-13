# Variables to change
company = "Tesla"
position = "Software Developer"
employername = "John Doe"
address = "123 hello street"
city = "Vancouver"
state = "BC"
postal = "V7E465"
length = "4"

# import operating system to rename files
import os
import time

# String array to parse into tex file
lines_to_add = [
    r"\newcommand{\company}{%s}" %(company) + "\n",
    r"\newcommand{\position}{%s}" %(position) + "\n",
    r"\newcommand{\employer}{%s}" %(employername) + "\n",
    r"\newcommand{\address}{%s}" %(address) + "\n",
    r"\newcommand{\city}{%s}" %(city) + "\n",
    r"\newcommand{\state}{%s}" %(state) + "\n",
    r"\newcommand{\postal}{%s}" %(postal) + "\n",
    r"\newcommand{\length}{%s}" %(length) + "\n",
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
    lines = text[:58] + lines_to_add + text[66:]
    with open("template.tex", "w") as file:
        file.writelines(lines)

def clear_files():
    new_name = "%s_CoverLetter.pdf" %(company)
    if(os.path.exists(new_name)):
        os.remove(new_name)
    os.rename("template.pdf", new_name)

    # Remove files
    os.remove("template.aux")
    os.remove("template.fdb_latexmk")
    os.remove("template.fls")
    os.remove("template.log")
    os.remove("template.out")
    os.remove("template.synctex.gz")

# Read and Write the file
text = read_file()
write_file(text)

# Wait to generate pdf, rename and clear
time.sleep(5)
clear_files()