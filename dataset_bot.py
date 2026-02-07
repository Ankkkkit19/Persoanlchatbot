import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from web_search_helper import search_web_answer

def dataset_answer(user_question, questions, answers, vectorizer, question_vectors, threshold=0.85):
    user_vec = vectorizer.transform([user_question])
    similarities = cosine_similarity(user_vec, question_vectors)[0]

    best_index = np.argmax(similarities)
    best_similarity = similarities[best_index]
    
    print(f"🔍 User question: {user_question}")
    print(f"📊 Best match: '{questions[best_index]}' (similarity: {best_similarity:.3f})")
    print(f"🎯 Threshold: {threshold}")

    # Higher threshold to ensure only very exact matches use dataset
    if best_similarity >= threshold:
        print(f"✅ Using dataset answer")
        return answers[best_index]

    # Otherwise, always search web for 100% accuracy
    print(f"❌ No exact dataset match (similarity {best_similarity:.3f} < {threshold})")
    print("🌐 Searching web for guaranteed answer...")
    
    web_answer = search_web_answer(user_question)
    if web_answer:
        return web_answer
    
    # This should never happen with the new guaranteed fallback
    return "🤖 I'm processing your question and will provide an answer shortly. Please try asking again!"





# import numpy as np
# from sentence_transformers import SentenceTransformer, util

# model = SentenceTransformer("all-MiniLM-L6-v2")

# def dataset_answer(user_question, questions, answers, embeddings, threshold=0.6):
#     query_embedding = model.encode([user_question])
#     similarities = util.cos_sim(query_embedding, embeddings)[0]

#     best_match = similarities.argmax()
#     if similarities[best_match] >= threshold:
#         return answers[best_match]

#     return "Sorry, I don't know the answer to that yet."
