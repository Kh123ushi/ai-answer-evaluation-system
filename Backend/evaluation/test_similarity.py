from answer_similarity import calculate_similarity, calculate_marks

student= "The capital of France is Paris."
teacher= "Paris is the capital of France."


similarity= calculate_similarity(student, teacher)
marks= calculate_marks(similarity)

print(f"Similarity Score: {similarity}")
print(f"Marks Awarded: {marks}")

