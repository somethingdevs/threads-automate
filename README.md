# 🧵 Threads Automation API – FastAPI + Render

This project allows you to post to [Meta Threads](https://www.threads.net) programmatically via the **Threads API**,
using a secure backend powered by **FastAPI** and deployed on **Render**.

---

## 🚀 Features

- Full OAuth2 flow (via Meta Threads)
- Post new Threads (with or without image)
- Publish Threads after creation
- Combined route to post and publish in one go
- Designed to work perfectly with **Postman**

---

## 🛠️ Setup & Deployment

### 1. 🧰 Environment Variables (`.env`)

Create a `.env` file locally or configure these in your Render dashboard:

```env
APP_ID=your_meta_app_id
APP_SECRET=your_meta_app_secret
REDIRECT_URI=https://your-app-name.onrender.com/auth/callback
```

### 2. 📦 Install dependencies (if running locally)

```bash
pip install -r requirements.txt
```

## 🌐 API Endpoints (Postman-friendly)

Use in browser only

Initiates the OAuth login flow:

```python
https: // your - app - name.onrender.com / login
```

## 🔄 GET /auth/callback

```python
{
    "access_token": "EAABsbCS1iHg...",
    ...
}
```

## 🔁 POST /post-and-publish-thread

```python
{
    "access_token": "your_access_token_here",
    "text": "This one goes straight to Threads 🚀",
    "image_url": "https://your-image-url.com/image.jpg" // optional
}
```
