from fastapi import FastAPI, UploadFile, File
from typing import List
import os
import shutil
import uuid
from fastapi.middleware.cors import CORSMiddleware

from ocr.ocr_engine import extract_text
from evaluation.answer_similarity import (
    calculate_similarity,
    calculate_marks,
    generate_feedback,
    extract_keywords,
    analyze_concepts
)
from plagiarism.plagiarism_checker import check_plagiarism

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.post("/evaluate-with-teacher")
async def evaluate_with_teacher(
    teacher_file: UploadFile = File(...),
    student_files: List[UploadFile] = File(...)
):
    try:
        # Teacher file
        teacher_filename = f"{uuid.uuid4()}_{teacher_file.filename}"
        teacher_path = os.path.join(UPLOAD_FOLDER, teacher_filename)

        with open(teacher_path, "wb") as buffer:
            shutil.copyfileobj(teacher_file.file, buffer)

        teacher_answer = extract_text(teacher_path)

        if not teacher_answer.strip():
            return {"error": "Teacher answer extraction failed"}

        teacher_keywords = extract_keywords(teacher_answer)

        # Students
        answers = []
        filenames = []

        for file in student_files:
            unique_name = f"{uuid.uuid4()}_{file.filename}"
            file_path = os.path.join(UPLOAD_FOLDER, unique_name)

            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            text = extract_text(file_path)

            if not text.strip():
                text = " "

            answers.append(text)
            filenames.append(file.filename)

        # Evaluation
        evaluation_results = []

        for i, ans in enumerate(answers):
            sim = calculate_similarity(ans, teacher_answer)
            marks = calculate_marks(sim)
            feedback = generate_feedback(ans, teacher_answer, sim)

            concept_analysis = analyze_concepts(ans, teacher_answer)

            evaluation_results.append({
                "file": filenames[i],
                "similarity": round(sim, 2),
                "marks": marks,
                "feedback": feedback,
                "present_concepts": concept_analysis["present_concepts"],
                "missing_concepts": concept_analysis["missing_concepts"],
                "coverage_score": concept_analysis["coverage_score"]
            })

        # Plagiarism 
        plagiarism_results = check_plagiarism(answers)

        return {
            "teacher_answer_preview": teacher_answer[:200],
            "evaluations": evaluation_results,
            "plagiarism_cases": plagiarism_results
        }

    except Exception as e:
        return {"error": str(e)}