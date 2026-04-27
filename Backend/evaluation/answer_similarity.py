from sentence_transformers import SentenceTransformer, util

# Load model once (global)
model = SentenceTransformer('all-MiniLM-L6-v2')


# 🔹 Clean text
def clean_text(text):
    return text.strip().lower()


# 🔹 Similarity calculation
def calculate_similarity(answer1, answer2):

    answer1 = clean_text(answer1)
    answer2 = clean_text(answer2)

    if not answer1 or not answer2:
        return 0.0

    embeddings = model.encode([answer1, answer2], convert_to_tensor=True)

    similarity = util.cos_sim(embeddings[0], embeddings[1])

    return float(similarity)


# 🔹 Marks calculation (improved scaling)
def calculate_marks(similarity_score, max_marks=10):

    # Better grading curve
    if similarity_score > 0.85:
        marks = max_marks
    elif similarity_score > 0.7:
        marks = similarity_score * max_marks
    elif similarity_score > 0.5:
        marks = similarity_score * (max_marks - 1)
    else:
        marks = similarity_score * (max_marks - 2)

    return round(marks, 2)


# 🔹 Keyword extraction (basic)
def extract_keywords(text):
    words = text.lower().split()
    return set(words)


# 🔹 Feedback generation (SMART)
def generate_feedback(student_answer, teacher_answer, similarity):

    feedback = []

    student_answer = clean_text(student_answer)
    teacher_answer = clean_text(teacher_answer)

    # 1️⃣ Similarity-based feedback
    if similarity > 0.85:
        feedback.append("Excellent answer, very close to expected answer.")
    elif similarity > 0.7:
        feedback.append("Good answer but lacks some depth.")
    elif similarity > 0.5:
        feedback.append("Average answer, missing key points.")
    else:
        feedback.append("Poor answer, needs major improvement.")

    # 2️⃣ Length check
    word_count = len(student_answer.split())

    if word_count < 20:
        feedback.append("Answer is too short, add more explanation.")
    elif word_count > 120:
        feedback.append("Answer is lengthy, try to be more concise.")

    # 3️⃣ Keyword comparison
    teacher_keywords = extract_keywords(teacher_answer)
    student_keywords = extract_keywords(student_answer)

    missing_keywords = teacher_keywords - student_keywords

    if len(missing_keywords) > 5:
        feedback.append("Important concepts are missing from the answer.")

    # 4️⃣ Coverage score (bonus intelligence)
    coverage = len(student_keywords & teacher_keywords) / (len(teacher_keywords) + 1)

    if coverage < 0.5:
        feedback.append("Low concept coverage detected.")

    return " ".join(feedback)


# 🔹 Concept extraction (phrases)
def extract_key_phrases(text):
    words = text.lower().split()
    phrases = []

    for i in range(len(words) - 1):
        phrases.append(words[i] + " " + words[i + 1])

    return set(phrases)


# 🔹 Concept analysis
def analyze_concepts(student_answer, teacher_answer):
    teacher_phrases = extract_key_phrases(teacher_answer)
    student_phrases = extract_key_phrases(student_answer)

    present = teacher_phrases & student_phrases
    missing = teacher_phrases - student_phrases

    coverage = len(present) / len(teacher_phrases) if teacher_phrases else 0

    return {
        "present_concepts": list(present)[:10],
        "missing_concepts": list(missing)[:10],
        "coverage_score": round(coverage, 2)
    }