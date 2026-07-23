from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from .models import ContactForm, Project, Skill
from .config import settings
from .autoreply import send_auto_reply
import json, os
import resend

router = APIRouter(prefix="/api")

# ---------- Projects ----------

def load_projects():
    projects = []
    folder = "projects"
    if not os.path.exists(folder):
        return projects
    for file in sorted(os.listdir(folder)):
        if file.endswith(".json"):
            with open(os.path.join(folder, file)) as f:
                projects.append(json.load(f))
    return projects

@router.get("/projects", response_model=list[Project])
def get_projects():
    return load_projects()

@router.get("/projects/{project_id}", response_model=Project)
def get_project(project_id: int):
    for p in load_projects():
        if p["id"] == project_id:
            return p
    raise HTTPException(status_code=404, detail="Project not found")

# ---------- Skills ----------

@router.get("/skills", response_model=list[Skill])
def get_skills():
    return [
        {"name": "Python",      "level": 90, "category": "Backend"},
        {"name": "FastAPI",     "level": 85, "category": "Backend"},
        {"name": "LangChain",   "level": 80, "category": "AI/ML"},
        {"name": "FAISS",       "level": 75, "category": "AI/ML"},
        # {"name": "Docker",      "level": 70, "category": "DevOps"},
        {"name": "MySQL",       "level": 75, "category": "Database"},
        {"name": "JavaScript",  "level": 65, "category": "Frontend"},
        {"name": "HTML/CSS",    "level": 80, "category": "Frontend"},
    ]

# ---------- Contact ----------

@router.post("/contact")
def send_contact(form: ContactForm):
    if not form.name or not form.message:
        raise HTTPException(status_code=400, detail="Name and message are required")

    if not settings.RESEND_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="Email is not configured on the server. Set RESEND_API_KEY environment variable.",
        )

    resend.api_key = settings.RESEND_API_KEY

    try:
        resend.Emails.send({
            "from": "onboarding@resend.dev",
            "to": settings.OWNER_EMAIL,
            "reply_to": form.email,
            "subject": f"Portfolio contact from {form.name}",
            "html": (
                f"<p><strong>Name:</strong> {form.name}</p>"
                f"<p><strong>Email:</strong> {form.email}</p>"
                f"<p><strong>Message:</strong><br>{form.message}</p>"
            ),
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Email error: {str(e)}")

    # Auto-reply to the visitor. Never blocks or fails the main response -
    # if it fails for any reason, the contact form still succeeds normally.
    send_auto_reply(name=form.name, to_email=form.email, message=form.message)

    return {"success": True, "message": "Message received! I'll get back to you soon."}

# ---------- Resume download ----------

@router.get("/resume")
def download_resume():
    path = "static/resume.pdf"
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Resume not found")
    return FileResponse(path, media_type="application/pdf", filename="resume.pdf")