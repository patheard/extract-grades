import os
import re
import csv
from PyPDF2 import PdfReader

input_folder = "data/input"
output_csv = "data/output/grades.csv"

language_grades_pattern = re.compile(r"^IEP([ABCDRI][+-]?)Literacy Connections and Applications")
math_grades_pattern = re.compile(r"^French([ABCDRI][+-]?)")

def extract_grades_from_pdf(pdf_path):
    """
    Extracts Language and Mathematics grades from a PDF file.
    Args:
        pdf_path (str): Path to the PDF file.
    Returns:
        dict: A dictionary with Language and Mathematics grades.
    """
    reader = PdfReader(pdf_path)
    grades = {
        "Language": [],
        "Mathematics": []
    }

    for page_number, page in enumerate(reader.pages):
        text = page.extract_text()

        # Discard pages without the grades we need
        if "Language" not in text and "Mathematics" not in text:
            continue

        lines = text.splitlines()

        # Check for Language grades
        for line in lines:
            if language_grades_pattern.search(line):
                match = language_grades_pattern.search(line)
                if match:
                    grades["Language"].append(match.group(1))

        # Check for Mathematics grades
        for i in range(len(lines) - 3):
            if ("Mathematics" in lines[i] and
                "ESL/ELD" in lines[i + 1] and
                "IEP" in lines[i + 2]):

                # Check if the fourth line contains a valid grade
                match = math_grades_pattern.search(lines[i + 3])
                if match:
                    grades["Mathematics"].append(match.group(1))

    return grades

def main():
    """
    Main function to extract grades from all PDF files in the input folder
    and write the results to a CSV file.
    """
    grades = {"Mathematics": [], "Language": []}
    grade_headings = ["A", "B", "C", "D", "R", "I"]

    for filename in os.listdir(input_folder):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(input_folder, filename)
            grades = extract_grades_from_pdf(pdf_path)

    # Initialize counts for all grades to 0 per subject
    subject_grade_counts = {
        "Mathematics": {grade: 0 for grade in grade_headings},
        "Language": {grade: 0 for grade in grade_headings}
    }

    # Calculate total counts for each grade per subject (ignoring suffixes)
    for subject, grade_list in grades.items():
        for grade in grade_list:
            base_grade = grade[0]
            if base_grade in subject_grade_counts[subject]:
                subject_grade_counts[subject][base_grade] += 1

    print(f"Extracted grades, writing to {output_csv}...\n{grades}")

    # Write the extracted grades and totals to a CSV file
    with open(output_csv, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Subject"] + grade_headings)
        for subject, counts in subject_grade_counts.items():
            writer.writerow([subject] + [counts[grade] for grade in grade_headings])


if __name__ == "__main__":
    main()