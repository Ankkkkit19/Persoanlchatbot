import json
from sklearn.feature_extraction.text import TfidfVectorizer
from intent_to_dataset import load_intents_as_qa

def train_dataset(dataset_path, intents_path):
    # ---------- LOAD dataset.json ----------
    with open(dataset_path, encoding="utf-8") as f:
        data = json.load(f)

    questions = [item["question"].lower() for item in data]
    answers = [item["answer"] for item in data]

    # ---------- LOAD intents.json ----------
    intent_q, intent_a = load_intents_as_qa(intents_path)

    questions.extend(intent_q)
    answers.extend(intent_a)

    # ---------- TF-IDF ----------
    vectorizer = TfidfVectorizer()
    question_vectors = vectorizer.fit_transform(questions)

    return questions, answers, vectorizer, question_vectors



# import json
# from sentence_transformers import SentenceTransformer

# model = SentenceTransformer("all-MiniLM-L6-v2")

# def train_dataset(path):
#     with open(path, encoding="utf-8") as f:
#         data = json.load(f)

#     questions = [item["question"] for item in data]
#     answers = [item["answer"] for item in data]

#     embeddings = model.encode(questions)
#     return questions, answers, embeddings
