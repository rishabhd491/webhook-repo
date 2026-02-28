# GitHub Webhook Receiver Dashboard

A real-time dashboard that receives and displays GitHub webhook events for **PUSH**, **PULL REQUEST**, and **MERGE** actions.

## 🚀 Live Demo
- **Live Dashboard**: [https://webhook-receiver-q6r8.onrender.com/](https://webhook-receiver-q6r8.onrender.com/)

## 🛠️ Features
- **Real-time Updates**: Frontend polls the backend every 15 seconds to fetch latest activities.
- **Webhook Integration**: Handles multiple GitHub event types (push, pull_request).
- **Cloud Storage**: Stores all events in a MongoDB Atlas cloud database.
- **Production Ready**: Served using Gunicorn on Render.com.

## 📁 Repository Links
- **Webhook Receiver (this repo)**: [https://github.com/rishabhd491/webhook-repo](https://github.com/rishabhd491/webhook-repo)
- **Source/Action Repo**: [https://github.com/rishabhd491/action-repo](https://github.com/rishabhd491/action-repo)

## 💻 Tech Stack
- **Backend**: Python, Flask, PyMongo
- **Database**: MongoDB Atlas
- **Frontend**: HTML5, CSS3, JavaScript
- **Hosting**: Render.com
- **Web Server**: Gunicorn

## 🔧 Installation & Local Setup

### Prerequisites
- Python 3.11+
- MongoDB (local or Atlas)

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/rishabhd491/webhook-repo.git
   cd webhook-repo
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Configure environment variables in `.env`:
   ```text
   MONGO_URI=your_mongodb_connection_string
   ```

4. Run the application:
   ```bash
   python run.py
   ```

## 🧪 Testing
Run the unit tests to verify the webhook receiver logic:
```bash
pytest
```

---
Built as part of a Technical Assessment.
