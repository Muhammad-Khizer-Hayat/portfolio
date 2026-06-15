# My Portfolio

A production-ready personal portfolio built with **FastAPI** (backend) and vanilla **HTML/CSS/JS** (frontend).

## Quick start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Copy and fill in your secrets
cp .env.example .env

# 3. Run the dev server
python -m backend.main
# Visit http://localhost:8000
```

## With Docker

```bash
docker build -t portfolio .
docker run -p 8000:8000 --env-file .env portfolio
```

## Project structure

```
portfolio/
├── backend/
│   ├── main.py       # App entry point
│   ├── routes.py     # API endpoints
│   ├── models.py     # Pydantic schemas
│   └── config.py     # Settings from .env
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
├── projects/         # JSON files for each project
├── static/           # resume.pdf, images
├── requirements.txt
├── Dockerfile
└── .env
```

## API endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/projects | List all projects |
| GET | /api/projects/{id} | Single project |
| GET | /api/skills | List skills |
| POST | /api/contact | Send contact message |
| GET | /api/resume | Download resume PDF |
