from pypdf import PdfReader # type: ignore
import keywords


def has_keyword(keyword, resume_text):
    keyword = keyword.lower().strip()
    if keyword == "":
        return False

    if keyword in resume_text:
        return True

    words = keyword.split()
    for word in words:
        if word not in resume_text:
            return False

    return True


def analyze_once():
    file_path = input("\nEnter PDF file path:\n").strip().strip('"')
    if file_path.startswith("file:///"):
        file_path = file_path.replace("file:///", "")
    file_path = file_path.replace("%20", " ")

    pdf_text = ""
    try:
        reader = PdfReader(file_path)
        for page in reader.pages:
            text = page.extract_text()
            if text:
                pdf_text = pdf_text + text + "\n"
        print("\nPDF read successfully!")
    except FileNotFoundError:
        print("File not found! Check your PDF path.")
        return
    except Exception as e:
        print("Error:", e)
        print("Invalid PDF file. Please check the file path and try again.")
        return

    pdf_text = pdf_text.lower()

    prof_input = input("\n............ Please enter your profession: ............\n").strip().lower()

    matched_key = None
    input_words = prof_input.split()

    for key in keywords.professions.keys():
        if key == prof_input or prof_input in key or key in prof_input:
            matched_key = key
            break

    if matched_key is None:
        for key in keywords.professions.keys():
            for word in input_words:
                if word in key:
                    matched_key = key
                    break
            if matched_key is not None:
                break

    if matched_key is not None:
        print(f"\nMatched profession category: '{matched_key}'")

        target_keywords = keywords.professions[matched_key]
        matched_skills = []
        missing_skills = []

        for kw in target_keywords:
            if has_keyword(kw, pdf_text):
                matched_skills.append(kw)
            else:
                missing_skills.append(kw)

        total_count = len(target_keywords)
        matched_count = len(matched_skills)
        if total_count > 0:
            score_percentage = (matched_count / total_count) * 100
        else:
            score_percentage = 0

        print(f"\nMatch Score: {score_percentage:.1f}% ({matched_count}/{total_count})")

        if len(matched_skills) > 0:
            print("Matched Keywords:", ", ".join(matched_skills))
        else:
            print("Matched Keywords: None")

        if len(missing_skills) > 0:
            print("Missing Keywords:", ", ".join(missing_skills))
        else:
            print("Missing Keywords: None")
    else:
        print(f"Profession '{prof_input}' is not recognized.")


def main():
    print("..................Welcome to the AI Resume Analyzer!..................")
    print("This tool will help you analyze your resume against a specific profession's required skills.")
    print("Please ensure your resume is in PDF format and contains text (not just images).\n")

    while True:
        print("Please choose an option:")
        print("1. Analyze a Resume")
        print("2. Quit")
        choice = input("Enter option (1 or 2): ").strip()

        if choice == "1":
            analyze_once()
            print("\n--------------------------------------------------\n")
        elif choice == "2":
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice! Please enter 1 or 2.\n")


if __name__ == "__main__":
    main()