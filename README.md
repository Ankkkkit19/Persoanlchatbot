# Ankit's Personal Chatbot 🤖

A personal chatbot project with both GUI and web interfaces that can answer questions about Ankit and provide college information.

## Features

- **Dual Interface**: Both Tkinter GUI (`app.py`) and Flask web app (`app_web.py`)
- **Smart Responses**: Uses TF-IDF vectorization and cosine similarity for intelligent responses
- **Voice Input**: Web interface supports voice input (browser dependent)
- **Responsive Design**: Mobile-friendly web interface
- **Comprehensive Dataset**: Includes personal information and college-related Q&A

## Project Structure

```
├── app.py                 # Tkinter GUI application
├── app_web.py            # Flask web application
├── chatbot.py            # Core chatbot logic
├── dataset_trainer.py    # Dataset training and vectorization
├── dataset_bot.py        # Response generation logic
├── intent_to_dataset.py  # Intent processing utilities
├── dataset.json          # Personal Q&A dataset
├── intents.json          # Intent-based responses
├── requirements.txt      # Python dependencies
├── templates/
│   └── index.html       # Web interface template
└── static/
    ├── style.css        # Web interface styling
    └── script.js        # Web interface JavaScript
```

## Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Web Interface (Recommended)
```bash
python app_web.py
```
Then open http://localhost:5000 in your browser.

### GUI Interface
```bash
python app.py
```

## Dataset

The chatbot uses two data sources:

1. **dataset.json**: Personal information about Ankit including education, skills, projects, and interests
2. **intents.json**: General conversational intents like greetings, college information, and common queries

## How It Works

1. **Training**: The system loads both datasets and creates TF-IDF vectors for all questions
2. **Query Processing**: User input is vectorized using the same TF-IDF model
3. **Similarity Matching**: Cosine similarity finds the best matching question
4. **Response**: Returns the corresponding answer if similarity exceeds threshold (0.3)

## Customization

- **Add new Q&A**: Edit `dataset.json` to add personal information
- **Modify intents**: Update `intents.json` for general conversational patterns
- **Adjust similarity threshold**: Modify the threshold in `dataset_bot.py`
- **Styling**: Customize the web interface via `static/style.css`

## Technologies Used

- **Backend**: Python, Flask, scikit-learn, NumPy
- **Frontend**: HTML5, CSS3, JavaScript
- **GUI**: Tkinter
- **ML**: TF-IDF Vectorization, Cosine Similarity
- **Voice**: Web Speech API

## Deployment

Ready to deploy? Check out [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions on deploying to:

- **Heroku** (Beginner-friendly)
- **Render** (Free tier available) 
- **Railway** (Modern platform)
- **Vercel** (Serverless)
- **PythonAnywhere** (Simple hosting)

### Quick Deploy Options:

**Render (Recommended):**
1. Push code to GitHub
2. Connect repository at [render.com](https://render.com)
3. Deploy automatically

**Heroku:**
```bash
git init
git add .
git commit -m "Deploy chatbot"
heroku create your-app-name
git push heroku main
```

### Test Locally First:
```bash
python deploy_local.py
```

## Author

Created by Ankit Kumar Pandit - B.Tech CSE (AI/ML) student at Dev Bhoomi Uttarakhand University, Dehradun.