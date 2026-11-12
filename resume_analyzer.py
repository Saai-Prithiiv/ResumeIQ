from __future__ import annotations

import io
import re
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import TypedDict

from docx import Document
from pypdf import PdfReader


class AnalysisResult(TypedDict, total=False):
    match_score: int
    matched_keywords: list[str]
    missing_keywords: list[str]
    suggestions: list[str]
    resume_text: str
    total_keywords: int
    word_count: int
    has_quantifiable_metrics: bool


STOP_WORDS = {
    "a", "about", "above", "after", "again", "against", "all", "also", "am",
    "an", "and", "any", "are", "as", "at", "be", "because", "been", "before",
    "being", "below", "between", "both", "but", "by", "can", "could", "did",
    "do", "does", "during", "each", "few", "for", "from", "further", "had",
    "has", "have", "having", "he", "her", "here", "hers", "him", "his", "how",
    "i", "if", "in", "into", "is", "it", "its", "itself", "just", "me", "more",
    "most", "my", "no", "nor", "not", "of", "off", "on", "once", "only", "or",
    "other", "our", "out", "over", "own", "same", "she", "should", "so", "some",
    "such", "than", "that", "the", "their", "them", "then", "there", "these",
    "they", "this", "those", "through", "to", "too", "under", "until", "up",
    "very", "was", "we", "were", "what", "when", "where", "which", "while",
    "who", "whom", "why", "will", "with", "you", "your",
}
MIN_KEYWORD_LENGTH = 2
MAX_KEYWORDS = 40


def extract_resume_text(file_bytes: bytes, filename: str) -> str:
    """Extract text from a supported resume file."""
    extension = Path(filename).suffix.lower()
    try:
        if extension == ".pdf":
            reader = PdfReader(io.BytesIO(file_bytes))
            text = "\n".join(page.extract_text() or "" for page in reader.pages)
        elif extension == ".docx":
            document = Document(io.BytesIO(file_bytes))
            text = "\n".join(paragraph.text for paragraph in document.paragraphs)
            for table in document.tables:
                text += "\n" + "\n".join(
                    " ".join(cell.text for cell in row.cells) for row in table.rows
                )
        elif extension == ".txt":
            text = file_bytes.decode("utf-8-sig")
        else:
            raise ValueError("Unsupported file type. Upload a PDF, DOCX, or TXT file.")
    except (UnicodeDecodeError, OSError, ValueError) as error:
        if isinstance(error, ValueError) and str(error).startswith("Unsupported"):
            raise
        raise ValueError("The uploaded file could not be read. Try another file.") from error
    except Exception as error:
        raise ValueError("The uploaded file could not be read. Try another file.") from error

    cleaned_text = text.strip()
    if not cleaned_text:
        raise ValueError(
            "No text could be extracted from this resume. For scanned PDFs, "
            "use an OCR-enabled tool to create a text-searchable PDF first."
        )
    return cleaned_text


def _keywords(text: str) -> list[str]:
    words = re.findall(r"[a-zA-Z][a-zA-Z0-9+#.-]*", text.lower())
    counts = Counter(
        word for word in words
        if len(word) >= MIN_KEYWORD_LENGTH and word not in STOP_WORDS
    )
    return [word for word, _ in counts.most_common(MAX_KEYWORDS)]


def analyze_resume(resume_text: str, job_description: str) -> AnalysisResult:
    """Compare resume terms with job-description terms and suggest next steps."""
    if not resume_text.strip():
        raise ValueError("The resume does not contain any text to analyze.")
    if not job_description.strip():
        raise ValueError("The job description does not contain any text to analyze.")

    job_keywords = _keywords(job_description)
    resume_words = set(re.findall(r"[a-zA-Z][a-zA-Z0-9+#.-]*", resume_text.lower()))
    matched = [word for word in job_keywords if word in resume_words]
    missing = [word for word in job_keywords if word not in resume_words]
    score = round(100 * len(matched) / len(job_keywords)) if job_keywords else 0

    has_metrics = bool(re.search(r"\b\d+(?:\.\d+)?%?\b", resume_text))
    word_count = len(resume_text.split())

    suggestions: list[str] = []
    if missing:
        suggestions.append(
            "Review the missing terms and include any that accurately reflect your "
            "experience, using them naturally in relevant sections."
        )
    if score < 50:
        suggestions.append(
            "Tailor your summary and experience bullets to emphasize the most "
            "relevant qualifications from the job description."
        )
    if not has_metrics:
        suggestions.append(
            "Where possible, quantify accomplishments with outcomes such as time "
            "saved, revenue supported, or users served."
        )
    if not suggestions:
        suggestions.append(
            "The detected terms overlap well. Review the resume for clear, specific "
            "examples that support the listed qualifications."
        )

    return {
        "match_score": score,
        "matched_keywords": matched,
        "missing_keywords": missing,
        "suggestions": suggestions,
        "resume_text": resume_text,
        "total_keywords": len(job_keywords),
        "word_count": word_count,
        "has_quantifiable_metrics": has_metrics,
    }


def generate_markdown_report(filename: str, result: AnalysisResult) -> str:
    """Generate a clean, downloadable markdown analysis report."""
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    score = result.get("match_score", 0)
    matched = result.get("matched_keywords", [])
    missing = result.get("missing_keywords", [])
    suggestions = result.get("suggestions", [])
    word_count = result.get("word_count", 0)
    has_metrics = "Yes" if result.get("has_quantifiable_metrics") else "No (Recommended to add)"

    matched_list = "\n".join(f"- `{k}`" for k in matched) if matched else "- None"
    missing_list = "\n".join(f"- `{k}`" for k in missing) if missing else "- None"
    suggestions_list = "\n".join(f"1. {s}" for s in suggestions) if suggestions else "1. No specific suggestions."

    report = f"""# ResumeIQ — Analysis & Match Report
**Generated:** {now_str}
**Resume File:** `{filename}`

---

## 1. Executive Summary
- **Keyword Match Score:** {score}%
- **Matching Keywords Detected:** {len(matched)}
- **Keywords to Consider:** {len(missing)}
- **Total Key Terms Evaluated:** {len(matched) + len(missing)}
- **Resume Word Count:** {word_count}
- **Quantified Accomplishments Found:** {has_metrics}

> **Notice:** This score is an estimated keyword and text overlap metric generated locally by ResumeIQ. It reflects textual alignment with the provided job description and is not an official ATS score or hiring prediction.

---

## 2. Matched Keywords ({len(matched)})
These terms from the job posting were identified in your resume:

{matched_list}

---

## 3. Keywords to Consider Adding ({len(missing)})
These high-frequency terms from the job posting are missing from your resume. Incorporate only those that accurately represent your real background:

{missing_list}

---

## 4. Strategic Recommendations
{suggestions_list}

---
*Generated privately by ResumeIQ — AI Resume Intelligence System*
"""
    return report
