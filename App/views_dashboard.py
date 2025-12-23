from django.shortcuts import render
from django.http import JsonResponse
import fitz  # PyMuPDF
import re

# ---- ROLE-BASED SKILL MAP (REALISTIC) ----
ROLE_SKILLS = {
    "backend": [
        "python", "java", "django", "flask", "sql",
        "api", "rest", "docker", "git", "linux"
    ],
    "frontend": [
        "html", "css", "javascript", "react", "typescript",
        "ui", "ux", "responsive", "tailwind"
    ],
    "data": [
        "python", "pandas", "numpy", "sql",
        "machine learning", "statistics", "analysis"
    ]
}

SECTION_KEYWORDS = {
    "skills": ["skills", "technical skills", "technologies"],
    "experience": ["experience", "work experience", "internship"],
    "education": ["education", "academic"]
}


# ----------------- HELPERS -----------------

def extract_text_from_pdf(file):
    text = ""
    doc = fitz.open(stream=file.read(), filetype="pdf")
    for page in doc:
        text += page.get_text()
    return text.lower()


def detect_sections(text):
    detected = {}
    for section, keywords in SECTION_KEYWORDS.items():
        detected[section] = any(k in text for k in keywords)
    return detected


def keyword_coverage(text, keywords):
    found = [k for k in keywords if k in text]
    coverage = len(found) / len(keywords)
    return found, coverage


def compute_ats_score(section_presence, keyword_coverage):
    """
    Realistic ATS scoring:
    - Structure: 40%
    - Keyword coverage: 60%
    """
    structure_score = sum(section_presence.values()) / len(section_presence)
    ats = (0.4 * structure_score + 0.6 * keyword_coverage) * 100
    return round(ats)


# ----------------- VIEWS -----------------

def dashboard_home(request):
    return render(request, "index.html")


def comprehensive_analysis(request):
    if request.method == "POST" and request.FILES.get("resume"):
        role = request.POST.get("role", "backend")
        pdf = request.FILES["resume"]

        text = extract_text_from_pdf(pdf)
        sections = detect_sections(text)

        role_keywords = ROLE_SKILLS.get(role, [])
        found_skills, coverage = keyword_coverage(text, role_keywords)

        ats_score = compute_ats_score(sections, coverage)

        missing_skills = list(set(role_keywords) - set(found_skills))

        suggestions = []
        if not sections["experience"]:
            suggestions.append("Add a clearly labeled Experience section")
        if not sections["skills"]:
            suggestions.append("Add a dedicated Skills section")
        if coverage < 0.5:
            suggestions.append("Include more role-relevant technical keywords")
        if len(text.split()) < 300:
            suggestions.append("Resume content is too short for ATS systems")

        context = {
            "ats_score": f"{ats_score}%",
            "skill_match": "Strong" if coverage > 0.7 else "Average" if coverage > 0.4 else "Weak",
            "resume_quality": "Well Structured" if all(sections.values()) else "Needs Improvement",
            "missing_skills": missing_skills[:6],
            "suggestions": suggestions
        }

        return render(request, "comprehensive_dashboard.html", context)

    return render(request, "index.html")


def get_dashboard_api(request):
    return JsonResponse({"status": "ok"})
