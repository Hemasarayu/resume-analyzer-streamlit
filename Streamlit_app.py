import streamlit as st
import fitz  # PyMuPDF
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from wordcloud import WordCloud
import matplotlib.pyplot as plt

st.set_page_config(page_title="AI Resume Analyzer", layout="centered", page_icon="📄")

st.title("📄 AI Resume Analyzer")
st.write("Upload your resume and job description to see how well they match!")

# --------- PDF Reader ---------
def extract_text_from_pdf(pdf_file):
    text = ""
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    for page in doc:
        text += page.get_text()
    return text

# --------- Cosine Similarity ---------
def calculate_similarity(resume_text, jd_text):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([resume_text, jd_text])
    score = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
    return round(score * 100, 2), vectorizer.get_feature_names_out()

# --------- WordCloud ---------
def generate_wordcloud(text, title):
    wc = WordCloud(width=400, height=200, background_color='black', colormap='plasma').generate(text)
    fig, ax = plt.subplots()
    ax.imshow(wc, interpolation='bilinear')
    ax.axis("off")
    st.subheader(title)
    st.pyplot(fig)

# Upload Resume
resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
jd_file = st.file_uploader("Upload Job Description (TXT)", type=["txt"])

if resume_file and jd_file:
    resume_text = extract_text_from_pdf(resume_file)
    jd_text = jd_file.read().decode('utf-8')

    st.success("✅ Files uploaded successfully!")

    match_score, features = calculate_similarity(resume_text, jd_text)
    st.markdown(f"### 🔍 Match Score: `{match_score}%`")
    st.progress(int(match_score))

    # Extract keyword sets
    resume_words = set(resume_text.lower().split())
    jd_words = set(jd_text.lower().split())
    matched = resume_words & jd_words
    missing = jd_words - resume_words

    st.markdown("#### ✅ Skills Present in Resume:")
    st.write(", ".join(list(matched)[:20]))

    st.markdown("#### ❌ Skills Missing from Resume (Based on JD):")
    st.write(", ".join(list(missing)[:20]))

    # Wordclouds
    st.markdown("----")
    generate_wordcloud(" ".join(matched), "✅ WordCloud: Matched Terms")
    generate_wordcloud(" ".join(missing), "❌ WordCloud: Missing Terms")
