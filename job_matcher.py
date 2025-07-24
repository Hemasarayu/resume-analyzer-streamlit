from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def match_resume_to_job(resume_data, job_description):
    resume_text = " ".join(resume_data["skills"])

    texts = [resume_text, job_description]

    vectorizer = CountVectorizer().fit_transform(texts)
    vectors = vectorizer.toarray()

    similarity = cosine_similarity([vectors[0]], [vectors[1]])[0][0]
    match_score = round(similarity * 100, 2)

    # Detect missing keywords (simple match)
    job_keywords = job_description.lower().split()
    missing = [word for word in job_keywords if word not in resume_text.lower()]

    return match_score, missing[:10]  # return top 10 missing keywords
