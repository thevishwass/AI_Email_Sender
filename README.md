# 🧠 AI Email Sender

An **AI-powered email automation tool** built with **Next.js** (frontend) and **FastAPI** (backend).  
It helps users **apply for jobs automatically** by generating personalized, professional emails — with plans to add deeper customization soon.

<hr>



## 🚀 Features

- 🤖 **AI Email Generation** – Auto-create subject & body based on job details  
- ✉️ **Send Emails Instantly** – Integrated email sending via backend  
- 🔐 **JWT Authentication** – Secure user login and token-based auth  
- 🌐 **Next.js Frontend** – Fast, responsive UI with modern design  
- ⚡ **FastAPI Backend** – Lightweight, efficient API server  
- 🗄️ **MongoDB Integration** – Store user and email data (optional)  
- 🧩 **Future Plans** – Add job-specific personalization and templates  

<hr>


## 🛠️ Tech Stack

| Layer | Technology |
|--------|-------------|
| Frontend | Next.js, React, TailwindCSS |
| Backend | FastAPI, Python |
| Database | MongoDB |
| Auth | JWT |
| Email | SMTP / Custom Provider |

<hr>


## ⚙️ Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/thevishwass/AI_Email_Sender.git
   cd AI_Email_Sender
   ```

2. **Install backend dependencies**
   ```bash
    cd ../backend
    pip install -r requirements.txt
   ```
   
3. **Install frontend dependencies**
   ```bash
    cd frontend
    npm install
   ```

4. **Configure environment variables**
   ```bash
    Create .env files for both frontend & backend
    Add your email credentials, JWT secret, and other keys
   ```

5. **Run the app**

### Backend
   ```bash
cd ../backend
uvicorn main:app --reload
```
### Frontend
   ```bash
    cd frontend
    npm run dev
   ```

6. **Visit**
   ```bash
   http://localhost:3000
   ```

<hr>


## 📁 Folder Structure

```bash
AI_Email_Sender/
│
├── frontend/              # Next.js frontend
│   ├── components/
│   ├── pages/
│   └── ...
│
├── backend/               # FastAPI backend
│   ├── main.py
│   ├── routes/
│   ├── requirements.txt
│   └── ...
│
├── .gitignore
└── README.md

```
<hr>


## 🧭 Roadmap
- **Job-specific personalization**
- **Resume & cover letter integration**
- **Analytics dashboard**
- **Multiple email templates**

<hr>


## 👨‍💻 Author

***Vishwas Singh***  


