from pydantic import BaseModel, EmailStr
from typing import List, Optional

class ContactForm(BaseModel):
    name: str
    email: str
    message: str

class Project(BaseModel):
    id: int
    title: str
    description: str
    tech_stack: List[str]
    github_url: Optional[str] = None
    live_url: Optional[str] = None
    image: Optional[str] = None

class Skill(BaseModel):
    name: str
    level: int  # 1-100
    category: str
