from dataset_trainer import train_dataset
from dataset_bot import dataset_answer

# Load and train the dataset when the module is imported
print("Loading dataset...")
questions, answers, vectorizer, question_vectors = train_dataset(
    "dataset.json",
    "intents.json"
)
print("Dataset loaded successfully!")

def get_response(user_input):
    """
    Get response from the chatbot for the given user input
    """
    if not user_input.strip():
        return "Please ask me something!"
    
    # Try smart assistant first
    try:
        from smart_assistant import get_smart_response
        
        # Check if input needs smart features
        smart_keywords = [
            'schedule', 'reminder', 'expense', 'money', 'study', 'padhai',
            'weather', 'mausam', 'today', 'aaj', 'kal', 'tomorrow',
            'add', 'log', 'kharcha', 'paisa'
        ]
        
        if any(keyword in user_input.lower() for keyword in smart_keywords):
            return get_smart_response(user_input)
    
    except ImportError:
        pass
    
    # Fallback to original chatbot
    response = dataset_answer(
        user_input.lower(),
        questions,
        answers,
        vectorizer,
        question_vectors
    )
    
    return response