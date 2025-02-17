# 📸 InstaConnect

A powerful and easy-to-use Instagram integration tool designed to connect, manage, and analyze your Instagram account with ease. Built to help creators, photographers, and businesses streamline their Instagram workflow.

## 🚀 Features
- 📊 **Analytics Dashboard**: Track your followers, engagement, and post performance.  
- 🤝 **Auto Engagement**: Like, comment, and follow based on hashtags or profiles.  
- 🗓️ **Post Scheduler**: Plan and schedule posts ahead of time.  
- 🔑 **Secure Authentication**: Connect your Instagram account safely using OAuth.  
- 📝 **Hashtag Generator**: Get the best hashtags for your posts using AI.  
- 💬 **Auto DM**: Automatically send welcome messages to new followers.  

---

## 🛠️ Tech Stack
- **Frontend:** React, Tailwind CSS  
- **Backend:** FastAPI, PostgreSQL  
- **Authentication:** OAuth 2.0  
- **Storage:** AWS S3  
- **Deployment:** Vercel (Frontend), Heroku (Backend)  

---

## 🚀 Getting Started
### 1. Clone the Repository
```bash
git clone https://github.com/eddieir/InstaConnect.git
cd InstaConnect
```
### 2. Backend Setup (FastAPI)
1. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Set environment variables (.env):**
   ```
   DATABASE_URL=postgresql://user:password@localhost/instaconnect
   INSTAGRAM_CLIENT_ID=your_client_id
   INSTAGRAM_CLIENT_SECRET=your_client_secret
   ```
4. **Run the backend server:**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

---
### 3. Frontend Setup (React)
1. **Navigate to the frontend directory:**
   ```bash
   cd frontend
   ```
2. **Install dependencies:**
   ```bash
   npm install
   ```
3. **Set environment variables (.env):**
   ```
   REACT_APP_API_URL=http://localhost:8000
   ```
4. **Run the frontend server:**
   ```bash
   npm start
   ```

---
## 🧪 Running Tests
Tests are written using **Playwright**. You can find them [here](https://github.com/eddieir/InstaConnect/tree/main/tests).
- **Run Tests (Playwright):**
  ```bash
  npx playwright test
  ```

---
## 🚀 Deployment
### Frontend (Vercel)
1. Connect your GitHub repository to Vercel.  
2. Add environment variables.  
3. Deploy with one click!

### Backend (Heroku)
1. Create a Heroku app.  
2. Add environment variables using the Heroku dashboard.  
3. Deploy via Heroku CLI:
   ```bash
   git push heroku main
   ```

---
## 🤝 Contributing
Contributions are welcome! Please follow these steps:
1. **Fork the repository**  
2. **Create a new branch:** `git checkout -b feature-name`  
3. **Commit your changes:** `git commit -m 'Add new feature'`  
4. **Push to your fork:** `git push origin feature-name`  
5. **Submit a pull request**  

---
## 🛡️ License
This project is licensed under the [MIT License](LICENSE).

---
## 💡 Acknowledgments
- Built with ❤️ by [Eddie](https://github.com/eddieir)  
- Inspired by creators and businesses who thrive on Instagram.
