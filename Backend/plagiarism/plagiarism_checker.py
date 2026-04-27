from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def clean_text(text):
    """Basic text cleaning"""
    return text.strip().lower()


def check_plagiarism(answers, threshold=0.5):
    """
    Compare multiple answers and detect plagiarism
    """

    # 🔒 Handle edge case
    if len(answers) < 2:
        return []

    # 🧹 Clean answers
    cleaned_answers = [clean_text(ans) for ans in answers if ans.strip()]

    # 🔒 If all answers are empty
    if len(cleaned_answers) < 2:
        return []

    # Vectorization
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(cleaned_answers)

    similarity_matrix = cosine_similarity(vectors)

    results = []
    n = len(cleaned_answers)

    # Compare pairs
    for i in range(n):
        for j in range(i + 1, n):

            score = similarity_matrix[i][j]

            if score >= threshold:
                results.append({
                    "student_1": i + 1,
                    "student_2": j + 1,
                    "similarity": round(float(score), 2),
                    "message": f"Answer {i+1} is {round(score*100)}% similar to Answer {j+1} → Possible plagiarism"
                })

    return results