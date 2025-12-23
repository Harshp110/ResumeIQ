from django.shortcuts import render
import fitz  # PyMuPDF

ROLE_KEYWORDS = {
    "backend": ["python", "django", "api", "sql", "git"],
    "frontend": ["html", "css", "javascript", "react", "ui"],
    "data": ["python", "pandas", "numpy", "sql", "analysis"],
}

def extract_text(pdf):
    text = ""
    doc = fitz.open(stream=pdf.read(), filetype="pdf")
    for page in doc:
        text += page.get_text()
    return text.lower()

def dashboard_home(request):
    return render(request, "index.html")

def comprehensive_analysis(request):
    if request.method == "POST":
        pdf = request.FILES["resume"]
        role = request.POST.get("role", "backend")

        text = extract_text(pdf)
        keywords = ROLE_KEYWORDS[role]

        matched = [k for k in keywords if k in text]
        score = int((len(matched) / len(keywords)) * 100)

        return render(request, "comprehensive_dashboard.html", {
            "ats_score": f"{score}%",
            "matched": matched,
            "missing": list(set(keywords) - set(matched)),
        })

    return render(request, "index.html")
