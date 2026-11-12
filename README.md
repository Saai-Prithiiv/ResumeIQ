# ResumeIQ — AI-Powered Resume Analysis & Job Matching System

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.36+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
[![Plotly](https://img.shields.io/badge/Plotly-5.22+-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com)
[![Privacy](https://img.shields.io/badge/Privacy-100%25%20Local-22C55E?style=for-the-badge)](https://github.com)

**ResumeIQ** is an enterprise-inspired AI resume analysis and job matching dashboard built with Python, Streamlit, Scikit-learn, and Plotly. It empowers job seekers to evaluate their resume directly against target job descriptions, discover missing industry keywords, and optimize their applications before submission.

Designed with a modern dark-mode SaaS UI, ResumeIQ operates **100% locally and confidentially** inside Docker without sending documents or data to external cloud APIs.

---

## ⚡ Key Highlights & Capabilities

- **🎯 Intelligent Keyword & Term Extraction:** Normalized parsing of PDF, DOCX, and TXT resumes with technical token preservation (`C++`, `C#`, `Node.js`, `.NET`).
- **📊 Interactive Visual Telemetry:**
  - Modern Plotly circular progress gauge with dynamic threshold coloration.
  - Term distribution comparison bar charts (Matched vs. Missing).
  - Green and orange responsive pill badges with smooth hover feedback.
- **🔍 Gap Analysis & Actionable Checklist:** Highlights missing requirements and provides practical, prioritized next steps.
- **🕒 Session-Based History:** Review and revisit past analyses conducted during your active session.
- **📥 Downloadable Reports:** Export a structured Markdown report summarizing executive scores, keywords, and recommendations.
- **🛡️ 100% Offline & Private:** Zero third-party LLM calls, zero tracking cookies, zero external telemetry.

---

## 🎨 Design System

| Element | Specification / Hex |
| :--- | :--- |
| **Main Background** | `#0B1020` (Deep Midnight Obsidian) |
| **Sidebar Surface** | `#111827` (Dark Slate) |
| **Cards & Containers** | `#1E293B` (Elevated Navy Slate) |
| **Primary Brand Purple** | `#8B5CF6` (Vibrant Violet) |
| **Secondary Brand Blue** | `#6366F1` (Indigo Glow) |
| **Success Indicator** | `#22C55E` (Emerald Green) |
| **Warning Indicator** | `#F59E0B` (Amber Orange) |
| **Primary Typography** | Plus Jakarta Sans / Inter |
| **Monospace / Code** | JetBrains Mono |

---

## 📂 Project Architecture

```
ResumeIQ/
├── app.py                 # Core Streamlit application & routing logic
├── resume_analyzer.py     # Document text extraction & NLP matching engine
├── ui_components.py       # Custom dark SaaS CSS, Plotly gauges & UI widgets
├── requirements.txt       # Production dependencies
├── Dockerfile             # Multi-stage security-hardened container spec
├── .dockerignore          # Docker build ignore rules
└── README.md              # Project documentation
```

---

## 🚀 Running with Docker (Recommended)

ResumeIQ is fully containerized and production-ready.

### 1. Build the Docker Image
```bash
docker build -t resumeiq .
```

### 2. Run the Container
```bash
docker run --rm -p 8501:8501 resumeiq
```

### 3. Access the Dashboard
Open your browser and navigate to:
```
http://localhost:8501
```

---

## 💻 Running Locally (Development)

Requires **Python 3.11** or newer.

```powershell
# 1. Create and activate a virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1   # On Windows
# source .venv/bin/activate    # On Linux/macOS

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch ResumeIQ
streamlit run app.py
```

---

## 🧠 Algorithmic Matching Methodology

1. **Document Parsing:** PyPDF and python-docx convert file byte streams into normalized text.
2. **Tokenization:** Regex patterns extract alpha-numeric and programming tokens (`[a-zA-Z][a-zA-Z0-9+#.-]*`).
3. **Stopword Elimination:** Common English prepositions, conjunctions, and auxiliary verbs are suppressed.
4. **Frequency Ranking:** The top 40 high-frequency terms in the job description are extracted as primary requirements.
5. **Set Overlap Calculation:** `Match Score = (Matched Keywords / Total Job Keywords) * 100`.
6. **Heuristic Evaluation:** Detects quantifiable achievement bullets (`%`, numerical impact) and generates contextual recommendations.

> **Note on Transparency:** The match score reflects algorithmic keyword and text overlap against the employer's posting. It serves as an informative optimization guideline and is not an official ATS rating or hiring prediction.

---

## 🔒 Security & Privacy

- Runs non-root (`appuser`) inside Docker.
- Bound strictly to container host `0.0.0.0:8501`.
- Healthcheck monitored via `/_stcore/health`.
- No sensitive user documents leave the local environment.
