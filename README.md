# Article Summarizer

A web application that summarizes articles from given URLs in multiple languages using AI. 

## 🌟 Features

- Submit any article URL for summarization
- Choose the language of summarization result
- Real-time progress tracking during summarization
- View previous summaries in history
- Copy summaries to clipboard
- Responsive and clean UI

## 🛠️ Tech Stack

**Frontend:**
- React

**Backend:**
- FastAPI
- Celery
- Redis
- MongoDB (database)
- OpenRouter AI API

## 📋 Prerequisites
- Docker
- Node.js (for local frontend development)
- Python (for local backend development)

## 🚀 Installation
1. Clone the repository
```bash
   git clone https://github.com/your-username/article-summarizer.git
   cd article-summarizer
```

2. Create .env file in the backend directory with your [OpenRouter API key](https://openrouter.ai/deepseek/deepseek-r1-0528:free/api)
```bash
MONGO_URI=mongodb://mongo:27017
CELERY_BROKER_URL=redis://redis:6379/0
OPENAI_API_KEY=your_api_key
```

3. Run the application
```bash
docker-compose up --build
```

## 🔌 API Endpoints
- POST /submit: Submit a URL for summarization
Parameters in body: url, language

- GET /result/{link_id}: Get summarization status and result

## 📸 Application Screenshots
![1](https://github.com/Hikkaruu/Article-Summarizer/blob/main/readme_resources/1.png)
![2](https://github.com/Hikkaruu/Article-Summarizer/blob/main/readme_resources/2.png)
![3](https://github.com/Hikkaruu/Article-Summarizer/blob/main/readme_resources/3.png)
