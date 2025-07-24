import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_resume_data(resume_file):
    text = extract_text_from_pdf(resume_file)

    data = {
        "name": "Not detected",
        "email": "Not detected",
        "skills": [],
        "education": [],
        "experience": [],
    }

    import re
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize

    text_lower = text.lower()

    # Extract email
    email_match = re.search(r'\S+@\S+', text)
    if email_match:
        data['email'] = email_match.group(0)

    # Basic skill extraction (customize this list)
    skills = ['python', 'java', 'sql', 'excel', 'power bi', 'machine learning', 'data analysis']
    found_skills = [skill for skill in skills if skill in text_lower]
    data['skills'] = found_skills

    return data
