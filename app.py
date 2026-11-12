"""ResumeIQ — AI-Powered Resume Analysis and Job Matching System.

A modern, dark-mode SaaS-style recruitment intelligence dashboard built
with Streamlit, Scikit-learn, Plotly, PyPDF, and python-docx.
"""

from __future__ import annotations

import html
from datetime import datetime
from typing import Any

import streamlit as st

from resume_analyzer import (
    AnalysisResult,
    analyze_resume,
    extract_resume_text,
    generate_markdown_report,
)
from ui_components import (
    create_keyword_breakdown_chart,
    create_match_gauge_chart,
    inject_custom_css,
    render_badge_cloud,
    render_sidebar_branding,
    render_sidebar_footer,
    render_stat_card,
)

# -----------------------------------------------------------------------------
# Streamlit Configuration & Initialization
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="ResumeIQ — AI Resume Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inject modern dark-theme SaaS stylesheet
inject_custom_css()

# Initialize session state variables
if "active_page" not in st.session_state:
    st.session_state["active_page"] = "dashboard"
if "history" not in st.session_state:
    st.session_state["history"] = []
if "current_analysis" not in st.session_state:
    st.session_state["current_analysis"] = None
if "uploaded_file_cache" not in st.session_state:
    st.session_state["uploaded_file_cache"] = None
if "job_desc_cache" not in st.session_state:
    st.session_state["job_desc_cache"] = ""


def navigate_to(page: str) -> None:
    """Safely update active navigation page and trigger a rerun."""
    st.session_state["active_page"] = page
    st.rerun()


# -----------------------------------------------------------------------------
# Sidebar Navigation
# -----------------------------------------------------------------------------
with st.sidebar:
    render_sidebar_branding()

    st.markdown(
        '<div style="font-size:0.75rem; font-weight:700; color:#64748B; text-transform:uppercase; letter-spacing:0.08em; margin:0.8rem 0 0.4rem 4px;">Navigation</div>',
        unsafe_allow_html=True,
    )

    current_page = st.session_state["active_page"]
    history_count = len(st.session_state["history"])

    # Navigation items
    nav_dash_label = "📊  Dashboard"
    nav_analyze_label = "⚡  Analyze Resume"
    nav_history_label = f"🕒  Analysis History ({history_count})" if history_count > 0 else "🕒  Analysis History"
    nav_about_label = "ℹ️  About ResumeIQ"

    if st.button(
        nav_dash_label,
        key="nav_btn_dash",
        use_container_width=True,
        type="primary" if current_page == "dashboard" else "secondary",
    ):
        navigate_to("dashboard")

    if st.button(
        nav_analyze_label,
        key="nav_btn_analyze",
        use_container_width=True,
        type="primary" if current_page == "analyze" else "secondary",
    ):
        navigate_to("analyze")

    if st.button(
        nav_history_label,
        key="nav_btn_history",
        use_container_width=True,
        type="primary" if current_page == "history" else "secondary",
    ):
        navigate_to("history")

    if st.button(
        nav_about_label,
        key="nav_btn_about",
        use_container_width=True,
        type="primary" if current_page == "about" else "secondary",
    ):
        navigate_to("about")

    st.markdown("<hr style='border-color:#1F2937; margin:1.2rem 0 0.8rem 0;'>", unsafe_allow_html=True)
    render_sidebar_footer()


# -----------------------------------------------------------------------------
# PAGE 1: DASHBOARD
# -----------------------------------------------------------------------------
def render_dashboard() -> None:
    """Render the main overview dashboard."""
    # Hero Section
    st.markdown(
        """
        <div class="riq-hero">
            <span class="riq-badge-pill riq-badge-purple">⚡ AI-Powered Resume Intelligence</span>
            <h1 style="font-size: 2.2rem; font-weight: 800; margin: 0.4rem 0 0.8rem 0; color: #FFFFFF; letter-spacing: -0.02em;">
                Supercharge Your Job Applications with <span style="background: linear-gradient(135deg, #A78BFA 0%, #818CF8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Targeted Keyword Matching</span>
            </h1>
            <p style="font-size: 1.05rem; line-height: 1.6; color: #94A3B8; max-width: 780px; margin-bottom: 1.4rem;">
                ResumeIQ evaluates your resume against target job postings using offline natural language processing. 
                Discover critical missing technical skills, evaluate keyword density, and optimize your application — 
                all running 100% locally with zero cloud telemetry.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Action Banner Row
    c1, c2, c3 = st.columns([1.8, 1.8, 3.4])
    with c1:
        if st.button("🚀 Start New Analysis", use_container_width=True, type="primary"):
            navigate_to("analyze")
    with c2:
        if st.button("📖 Read Documentation", use_container_width=True, type="secondary"):
            navigate_to("about")

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    # Session Analytics Cards
    st.markdown("### 📈 Session Overview")
    history = st.session_state["history"]
    total_analyses = len(history)

    if total_analyses > 0:
        avg_score = round(sum(item["match_score"] for item in history) / total_analyses)
        best_score = max(item["match_score"] for item in history)
        avg_score_display = f"{avg_score}%"
        best_score_display = f"{best_score}%"
    else:
        avg_score_display = "—"
        best_score_display = "—"

    col_s1, col_s2, col_s3, col_s4 = st.columns(4)
    with col_s1:
        st.markdown(
            render_stat_card("Analyses in Session", total_analyses, "Active memory", "Session Metric"),
            unsafe_allow_html=True,
        )
    with col_s2:
        st.markdown(
            render_stat_card("Average Match", avg_score_display, "Mean keyword overlap", "Quality Score"),
            unsafe_allow_html=True,
        )
    with col_s3:
        st.markdown(
            render_stat_card("Highest Alignment", best_score_display, "Best recorded match", "Benchmark"),
            unsafe_allow_html=True,
        )
    with col_s4:
        st.markdown(
            render_stat_card("Data Security", "100%", "Zero cloud leakage", "Privacy Level"),
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

    # Core Features Section
    st.markdown("### 💎 Key Platform Capabilities")
    f1, f2 = st.columns(2)
    with f1:
        st.markdown(
            """
            <div class="riq-card" style="margin-bottom: 1rem;">
                <div style="font-size: 1.6rem; margin-bottom: 0.6rem;">🎯</div>
                <h4 style="margin: 0 0 0.5rem 0; color: #FFFFFF; font-size: 1.15rem;">Automated Keyword & Skill Extraction</h4>
                <p style="color: #94A3B8; font-size: 0.92rem; line-height: 1.5; margin: 0;">
                    Parses PDF, DOCX, and TXT resumes with full formatting normalization. Identifies modern programming languages, 
                    frameworks, cloud platforms, and specialized domain terms.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <div class="riq-card">
                <div style="font-size: 1.6rem; margin-bottom: 0.6rem;">🔍</div>
                <h4 style="margin: 0 0 0.5rem 0; color: #FFFFFF; font-size: 1.15rem;">Accurate Gap Analysis</h4>
                <p style="color: #94A3B8; font-size: 0.92rem; line-height: 1.5; margin: 0;">
                    Instantly highlights which critical requirements from the employer's posting are missing in your resume, 
                    providing clear signals before you submit your application.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with f2:
        st.markdown(
            """
            <div class="riq-card" style="margin-bottom: 1rem;">
                <div style="font-size: 1.6rem; margin-bottom: 0.6rem;">📊</div>
                <h4 style="margin: 0 0 0.5rem 0; color: #FFFFFF; font-size: 1.15rem;">Interactive Visual Telemetry</h4>
                <p style="color: #94A3B8; font-size: 0.92rem; line-height: 1.5; margin: 0;">
                    Visual circular gauges, frequency breakdown charts, and categorized color badges deliver immediate 
                    at-a-glance comprehension of candidate qualifications.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <div class="riq-card">
                <div style="font-size: 1.6rem; margin-bottom: 0.6rem;">🛡️</div>
                <h4 style="margin: 0 0 0.5rem 0; color: #FFFFFF; font-size: 1.15rem;">100% Confidential Docker Execution</h4>
                <p style="color: #94A3B8; font-size: 0.92rem; line-height: 1.5; margin: 0;">
                    Built on containerized local Python NLP. No documents, personal identifying data, or text snippets 
                    are ever sent to commercial LLMs or remote tracking servers.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

    # How It Works Pipeline
    st.markdown("### ⚙️ How ResumeIQ Works")
    p1, p2 = st.columns(2)
    with p1:
        st.markdown(
            """
            <div class="riq-step-box">
                <div class="riq-step-number">1</div>
                <div>
                    <div style="font-weight: 700; color: #FFFFFF; margin-bottom: 3px;">Upload Resume Document</div>
                    <div style="color: #94A3B8; font-size: 0.88rem; line-height: 1.4;">
                        Select your PDF, DOCX, or TXT document. ResumeIQ extracts raw text, stripping away formatting artifacts.
                    </div>
                </div>
            </div>
            <div class="riq-step-box">
                <div class="riq-step-number">2</div>
                <div>
                    <div style="font-weight: 700; color: #FFFFFF; margin-bottom: 3px;">Paste Job Description</div>
                    <div style="color: #94A3B8; font-size: 0.88rem; line-height: 1.4;">
                        Provide the job posting details including responsibilities, requirements, technical qualifications, and certifications.
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with p2:
        st.markdown(
            """
            <div class="riq-step-box">
                <div class="riq-step-number">3</div>
                <div>
                    <div style="font-weight: 700; color: #FFFFFF; margin-bottom: 3px;">Algorithmic Keyword Cross-Reference</div>
                    <div style="color: #94A3B8; font-size: 0.88rem; line-height: 1.4;">
                        Our engine eliminates domain stopwords, extracts key technical tokens, and calculates frequency-weighted set overlap.
                    </div>
                </div>
            </div>
            <div class="riq-step-box">
                <div class="riq-step-number">4</div>
                <div>
                    <div style="font-weight: 700; color: #FFFFFF; margin-bottom: 3px;">Review Insights & Download Report</div>
                    <div style="color: #94A3B8; font-size: 0.88rem; line-height: 1.4;">
                        Examine matched terms, missing keywords, quantifiable bullet recommendations, and export a ready-to-share Markdown report.
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# -----------------------------------------------------------------------------
# PAGE 2: ANALYZE RESUME
# -----------------------------------------------------------------------------
def render_analyze_page() -> None:
    """Render the resume upload and analysis page."""
    st.markdown(
        """
        <div style="margin-bottom: 1.5rem;">
            <span class="riq-badge-pill riq-badge-purple">⚡ Analyzer Studio</span>
            <h1 style="font-size: 2rem; font-weight: 800; color: #FFFFFF; margin: 0.3rem 0; letter-spacing: -0.02em;">
                Resume & Job Description Matcher
            </h1>
            <p style="color: #94A3B8; font-size: 0.95rem; margin: 0;">
                Compare your resume with a specific job posting to uncover keyword alignment, gaps, and targeted improvements.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Two-Column Input Workspace
    col_left, col_right = st.columns([1, 1], gap="large")

    with col_left:
        st.markdown(
            """
            <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:0.5rem;">
                <span style="font-weight:700; font-size:1rem; color:#F8FAFC;">📄 1. Upload Resume</span>
                <span style="font-size:0.75rem; color:#94A3B8;">PDF, DOCX, TXT</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        uploaded_file = st.file_uploader(
            "Choose a resume file",
            type=["pdf", "docx", "txt"],
            help="Supported formats: PDF, DOCX, or plain text. Documents are analyzed locally in container memory.",
            label_visibility="collapsed",
        )

        extracted_text = ""
        file_stats_html = ""

        if uploaded_file is not None:
            file_bytes = uploaded_file.getvalue()
            file_size_kb = len(file_bytes) / 1024
            file_size_str = f"{file_size_kb:.1f} KB" if file_size_kb < 1024 else f"{(file_size_kb/1024):.2f} MB"

            try:
                extracted_text = extract_resume_text(file_bytes, uploaded_file.name)
                word_count = len(extracted_text.split())
                file_stats_html = f"""
                <div style="background:#162032; border:1px solid #232D3F; border-radius:10px; padding:0.9rem; margin-top:0.8rem;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
                        <span style="font-weight:600; color:#F8FAFC; font-size:0.9rem;">{html.escape(uploaded_file.name)}</span>
                        <span class="riq-badge-pill riq-badge-green" style="font-size:0.65rem; margin:0;">Verified</span>
                    </div>
                    <div style="font-size:0.78rem; color:#94A3B8; display:flex; gap:12px;">
                        <span>📦 Size: {file_size_str}</span>
                        <span>📝 Extracted: ~{word_count} words</span>
                        <span>📑 Format: {html.escape(uploaded_file.type or 'Document')}</span>
                    </div>
                </div>
                """
            except Exception as err:
                st.error(f"⚠️ Extraction issue: {err}")
        else:
            file_stats_html = """
            <div style="background:#162032; border:1px dashed #283548; border-radius:10px; padding:1.2rem; text-align:center; margin-top:0.8rem;">
                <div style="color:#64748B; font-size:0.85rem;">No file loaded yet. Drag & drop your resume above.</div>
            </div>
            """

        st.markdown(file_stats_html, unsafe_allow_html=True)

    with col_right:
        st.markdown(
            """
            <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:0.5rem;">
                <span style="font-weight:700; font-size:1rem; color:#F8FAFC;">💼 2. Target Job Description</span>
                <span style="font-size:0.75rem; color:#94A3B8;">Paste Posting</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        job_desc_input = st.text_area(
            "Job Description",
            height=250,
            value=st.session_state.get("job_desc_cache", ""),
            placeholder="Paste the target job description here...\n\nInclude:\n• Required technical skills and tools\n• Key responsibilities\n• Qualifications, degrees, or certifications\n• Preferred experience",
            label_visibility="collapsed",
        )

        # Live counters
        char_count = len(job_desc_input)
        word_count = len(job_desc_input.split())
        st.markdown(
            f"""
            <div style="display:flex; justify-content:space-between; color:#64748B; font-size:0.78rem; margin-top:0.4rem; padding:0 4px;">
                <span>Character Count: <strong style="color:#CBD5E1;">{char_count:,}</strong></span>
                <span>Estimated Words: <strong style="color:#CBD5E1;">{word_count:,}</strong></span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height: 1.2rem;'></div>", unsafe_allow_html=True)

    # Action Buttons
    action_col1, action_col2 = st.columns([3, 1])
    with action_col1:
        analyze_clicked = st.button("⚡ Analyze My Resume", use_container_width=True, type="primary")
    with action_col2:
        clear_clicked = st.button("🔄 Clear Inputs", use_container_width=True, type="secondary")

    if clear_clicked:
        st.session_state["job_desc_cache"] = ""
        st.session_state["current_analysis"] = None
        st.rerun()

    # Process Analysis
    if analyze_clicked:
        if uploaded_file is None:
            st.error("Please upload a resume file (PDF, DOCX, or TXT) before starting.")
        elif not job_desc_input.strip():
            st.error("Please paste a target job description to match against.")
        else:
            with st.spinner("Extracting text and computing keyword match telemetry..."):
                try:
                    if not extracted_text:
                        extracted_text = extract_resume_text(uploaded_file.getvalue(), uploaded_file.name)
                    
                    analysis_result = analyze_resume(extracted_text, job_desc_input)
                    
                    # Store current analysis
                    timestamp_str = datetime.now().strftime("%b %d, %Y • %I:%M %p")
                    record = {
                        "timestamp": timestamp_str,
                        "filename": uploaded_file.name,
                        "match_score": analysis_result["match_score"],
                        "matched_keywords": analysis_result["matched_keywords"],
                        "missing_keywords": analysis_result["missing_keywords"],
                        "suggestions": analysis_result["suggestions"],
                        "resume_text": analysis_result["resume_text"],
                        "total_keywords": analysis_result.get("total_keywords", len(analysis_result["matched_keywords"]) + len(analysis_result["missing_keywords"])),
                        "has_quantifiable_metrics": analysis_result.get("has_quantifiable_metrics", False),
                        "job_description_snippet": job_desc_input[:200] + ("..." if len(job_desc_input) > 200 else ""),
                    }
                    
                    st.session_state["current_analysis"] = record
                    # Save to history list
                    st.session_state["history"].insert(0, record)
                    st.session_state["job_desc_cache"] = job_desc_input
                    st.success("✅ Analysis successfully completed! Explore your detailed results below.")
                except Exception as error:
                    st.error(f"Analysis failed: {error}")

    # Render Results Section if available
    current = st.session_state.get("current_analysis")
    if current:
        st.markdown("<hr style='border-color:#1F2937; margin:2.2rem 0 1.5rem 0;'>", unsafe_allow_html=True)
        render_results_dashboard(current)


# -----------------------------------------------------------------------------
# PAGE 2 SUB-COMPONENT: RESULTS DASHBOARD
# -----------------------------------------------------------------------------
def render_results_dashboard(data: dict[str, Any]) -> None:
    """Render the full SaaS results dashboard for an analyzed resume."""
    score = data["match_score"]
    matched = data.get("matched_keywords", [])
    missing = data.get("missing_keywords", [])
    total_target = len(matched) + len(missing)
    filename = data.get("filename", "Resume")
    timestamp = data.get("timestamp", "")
    suggestions = data.get("suggestions", [])
    resume_text = data.get("resume_text", "")

    # Header with Disclaimer
    st.markdown(
        f"""
        <div style="display:flex; justify-content:space-between; align-items:flex-end; flex-wrap:wrap; margin-bottom:1rem;">
            <div>
                <span class="riq-badge-pill riq-badge-green">Live Analysis Report</span>
                <h2 style="font-size:1.8rem; font-weight:800; color:#FFFFFF; margin:0.2rem 0; letter-spacing:-0.01em;">
                    Results for <span style="color:#C4B5FD;">{html.escape(filename)}</span>
                </h2>
                <div style="font-size:0.8rem; color:#94A3B8;">Generated: {html.escape(timestamp)}</div>
            </div>
        </div>
        <div class="riq-disclaimer-box">
            <strong>Estimated Keyword Alignment:</strong> This score reflects the algorithmic text and keyword overlap 
            between your uploaded resume and the provided job description. It serves as an informative optimization guideline 
            and is not an official ATS rating or hiring guarantee.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Metric Cards Row
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(
            render_stat_card("Keyword Match", f"{score}%", f"{len(matched)} of {total_target} terms", "Overall"),
            unsafe_allow_html=True,
        )
    with m2:
        st.markdown(
            render_stat_card("Matched Terms", len(matched), "Present in your resume", "Found"),
            unsafe_allow_html=True,
        )
    with m3:
        st.markdown(
            render_stat_card("Missing Terms", len(missing), "To consider adding", "Gaps"),
            unsafe_allow_html=True,
        )
    with m4:
        st.markdown(
            render_stat_card("Total Evaluated", total_target, "Key job requirements", "Target Base"),
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    # Visualizations Row
    chart_col1, chart_col2 = st.columns([1, 1])
    with chart_col1:
        st.markdown(
            """
            <div class="riq-card">
                <div style="font-weight:700; color:#F8FAFC; margin-bottom:0.2rem; font-size:1rem;">🎯 Match Alignment Gauge</div>
                <div style="color:#94A3B8; font-size:0.8rem; margin-bottom:0.5rem;">Visual indicator of target keyword frequency coverage</div>
            """,
            unsafe_allow_html=True,
        )
        gauge_fig = create_match_gauge_chart(score)
        st.plotly_chart(gauge_fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    with chart_col2:
        st.markdown(
            """
            <div class="riq-card">
                <div style="font-weight:700; color:#F8FAFC; margin-bottom:0.2rem; font-size:1rem;">📊 Term Distribution Breakdown</div>
                <div style="color:#94A3B8; font-size:0.8rem; margin-bottom:0.5rem;">Ratio of detected requirements versus identified gaps</div>
            """,
            unsafe_allow_html=True,
        )
        bar_fig = create_keyword_breakdown_chart(len(matched), len(missing))
        st.plotly_chart(bar_fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    # Detailed Tabs
    tab_matched, tab_missing, tab_recommendations, tab_preview = st.tabs(
        [
            f"✅ Matched Keywords ({len(matched)})",
            f"⚠️ Missing Keywords ({len(missing)})",
            "💡 Strategic Recommendations",
            "📄 Extracted Resume Text",
        ]
    )

    with tab_matched:
        st.markdown(
            """
            <div style="margin: 0.8rem 0;">
                <div style="font-weight:600; color:#F8FAFC; margin-bottom:4px;">Directly Identified Skills & Keywords</div>
                <div style="color:#94A3B8; font-size:0.85rem; margin-bottom:1rem;">
                    These high-frequency terms from the job posting were found in your resume text:
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(render_badge_cloud(matched, badge_type="match"), unsafe_allow_html=True)

    with tab_missing:
        st.markdown(
            """
            <div style="margin: 0.8rem 0;">
                <div style="font-weight:600; color:#F8FAFC; margin-bottom:4px;">Target Keywords Not Detected</div>
                <div style="color:#94A3B8; font-size:0.85rem; margin-bottom:1rem;">
                    The following important terms appear in the job description but are missing from your resume. 
                    Include them naturally in your experience bullets if you possess relevant background:
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(render_badge_cloud(missing, badge_type="missing"), unsafe_allow_html=True)

    with tab_recommendations:
        st.markdown("<div style='margin-top:0.8rem;'></div>", unsafe_allow_html=True)
        for i, tip in enumerate(suggestions, 1):
            st.markdown(
                f"""
                <div class="riq-step-box" style="margin-bottom:0.7rem;">
                    <div class="riq-step-number" style="background:#6366F1; font-size:0.8rem;">{i}</div>
                    <div style="color:#E2E8F0; font-size:0.92rem; line-height:1.5;">
                        {html.escape(tip)}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Interactive Resume Improvement Checklist
        st.markdown("#### 📝 Candidate Action Checklist")
        st.checkbox("Integrate missing technical terms into relevant role descriptions", key="chk_missing")
        st.checkbox("Quantify key achievements with metrics, percentages, or scale", key="chk_metrics")
        st.checkbox("Align your summary statement with the employer's core focus areas", key="chk_summary")
        st.checkbox("Verify spelling of industry frameworks and certifications", key="chk_proofread")

    with tab_preview:
        st.markdown(
            """
            <div style="margin: 0.8rem 0;">
                <div style="font-weight:600; color:#F8FAFC; margin-bottom:4px;">Verified Text Extraction Output</div>
                <div style="color:#94A3B8; font-size:0.85rem; margin-bottom:0.8rem;">
                    Review the exact text parsed by the local PDF/DOCX extractor to confirm no sections were skipped:
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="riq-code-preview">{html.escape(resume_text)}</div>',
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    # Export & Download Report Section
    st.markdown("### 📥 Export Analysis")
    report_md = generate_markdown_report(filename, data)  # type: ignore[arg-type]
    
    rep_col1, rep_col2 = st.columns([1.5, 3])
    with rep_col1:
        st.download_button(
            label="📄 Download Markdown Report",
            data=report_md,
            file_name=f"ResumeIQ_Report_{filename.split('.')[0]}.md",
            mime="text/markdown",
            use_container_width=True,
        )


# -----------------------------------------------------------------------------
# PAGE 3: ANALYSIS HISTORY
# -----------------------------------------------------------------------------
def render_history_page() -> None:
    """Render the session history page."""
    st.markdown(
        """
        <div style="margin-bottom: 1.5rem;">
            <span class="riq-badge-pill riq-badge-purple">🕒 Session Activity</span>
            <h1 style="font-size: 2rem; font-weight: 800; color: #FFFFFF; margin: 0.3rem 0; letter-spacing: -0.02em;">
                Analysis History
            </h1>
            <p style="color: #94A3B8; font-size: 0.95rem; margin: 0;">
                Review analyses conducted during your current active session. Data is kept in secure in-memory session state.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    history = st.session_state["history"]

    if not history:
        st.markdown(
            """
            <div class="riq-card" style="text-align:center; padding:3rem 1.5rem; margin-top:1.5rem;">
                <div style="font-size:3rem; margin-bottom:0.8rem;">📋</div>
                <h3 style="color:#F8FAFC; margin-bottom:0.5rem;">No Analyses Recorded Yet</h3>
                <p style="color:#94A3B8; max-width:480px; margin:0 auto 1.5rem auto; font-size:0.92rem; line-height:1.5;">
                    Run your first resume analysis to compare keywords and view insights here during your session.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("⚡ Go to Resume Analyzer", type="primary"):
            navigate_to("analyze")
        return

    # Top summary & Clear button
    top_col1, top_col2 = st.columns([3, 1])
    with top_col1:
        st.markdown(
            f"<div style='font-size:0.95rem; color:#CBD5E1;'>Total saved session analyses: <strong>{len(history)}</strong></div>",
            unsafe_allow_html=True,
        )
    with top_col2:
        if st.button("🗑️ Clear History", use_container_width=True, type="secondary"):
            st.session_state["history"] = []
            st.rerun()

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

    # Render History Cards
    for idx, entry in enumerate(history):
        score = entry["match_score"]
        score_color = "#22C55E" if score >= 75 else ("#8B5CF6" if score >= 50 else "#F59E0B")
        matched_cnt = len(entry.get("matched_keywords", []))
        missing_cnt = len(entry.get("missing_keywords", []))

        with st.container():
            col_info, col_btn = st.columns([4, 1.2])
            with col_info:
                st.markdown(
                    f"""
                    <div style="background:#162032; border:1px solid #232D3F; border-radius:12px; padding:1.1rem; margin-bottom:0.8rem;">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                            <span style="font-weight:700; color:#F8FAFC; font-size:1.05rem;">
                                📄 {html.escape(entry['filename'])}
                            </span>
                            <span style="font-size:1.2rem; font-weight:800; color:{score_color};">
                                {score}% Match
                            </span>
                        </div>
                        <div style="font-size:0.82rem; color:#94A3B8; display:flex; gap:16px; margin-bottom:6px;">
                            <span>🕒 {html.escape(entry['timestamp'])}</span>
                            <span>✅ Matched: {matched_cnt}</span>
                            <span>⚠️ Missing: {missing_cnt}</span>
                        </div>
                        <div style="font-size:0.8rem; color:#64748B; font-style:italic;">
                            Target: {html.escape(entry.get('job_description_snippet', ''))}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with col_btn:
                st.markdown("<div style='height: 0.6rem;'></div>", unsafe_allow_html=True)
                if st.button("🔍 View Results", key=f"hist_btn_{idx}", use_container_width=True):
                    st.session_state["current_analysis"] = entry
                    navigate_to("analyze")


# -----------------------------------------------------------------------------
# PAGE 4: ABOUT RESUMEIQ
# -----------------------------------------------------------------------------
def render_about_page() -> None:
    """Render the comprehensive technical and architecture documentation."""
    st.markdown(
        """
        <div style="margin-bottom: 1.5rem;">
            <span class="riq-badge-pill riq-badge-purple">ℹ️ System Architecture</span>
            <h1 style="font-size: 2rem; font-weight: 800; color: #FFFFFF; margin: 0.3rem 0; letter-spacing: -0.02em;">
                About ResumeIQ
            </h1>
            <p style="color: #94A3B8; font-size: 0.95rem; margin: 0;">
                AI-Powered Resume Analysis and Job Matching System designed for modern career optimization.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Mission & Overview
    st.markdown("### 🎯 Project Overview")
    st.markdown(
        """
        <div class="riq-card" style="margin-bottom:1.5rem;">
            <p style="color:#CBD5E1; font-size:0.95rem; line-height:1.6; margin:0 0 1rem 0;">
                <strong>ResumeIQ</strong> is an enterprise-inspired recruitment intelligence platform designed to eliminate the 
                "black box" of applicant tracking systems (ATS). By providing instant, deterministic keyword and requirement 
                cross-referencing, candidates can identify missing technical qualifications and strengthen their resumes before applying.
            </p>
            <p style="color:#CBD5E1; font-size:0.95rem; line-height:1.6; margin:0;">
                Unlike third-party cloud tools that upload personal resumes to external proprietary APIs, ResumeIQ runs entirely 
                within a localized, secure Docker container. All tokenization, parsing, and scoring algorithms execute client-side.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Technology Stack
    st.markdown("### 💻 Technology Stack")
    t1, t2, t3 = st.columns(3)
    with t1:
        st.markdown(
            """
            <div class="riq-card" style="height:100%;">
                <h4 style="color:#C4B5FD; margin-top:0;">Frontend & Presentation</h4>
                <ul style="color:#94A3B8; font-size:0.88rem; line-height:1.7; padding-left:1.2rem;">
                    <li><strong>Streamlit 1.36+</strong> (Reactive Web UI)</li>
                    <li><strong>Custom CSS3</strong> (Dark SaaS Design System)</li>
                    <li><strong>Plotly 5.22+</strong> (Interactive Vector Visuals)</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with t2:
        st.markdown(
            """
            <div class="riq-card" style="height:100%;">
                <h4 style="color:#C4B5FD; margin-top:0;">Document Processing & NLP</h4>
                <ul style="color:#94A3B8; font-size:0.88rem; line-height:1.7; padding-left:1.2rem;">
                    <li><strong>pypdf 4.2+</strong> (PDF Stream Text Extraction)</li>
                    <li><strong>python-docx 1.1+</strong> (XML Paragraph & Table Parsing)</li>
                    <li><strong>Scikit-learn & Python re</strong> (Tokenization & Frequency)</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with t3:
        st.markdown(
            """
            <div class="riq-card" style="height:100%;">
                <h4 style="color:#C4B5FD; margin-top:0;">DevOps & Security</h4>
                <ul style="color:#94A3B8; font-size:0.88rem; line-height:1.7; padding-left:1.2rem;">
                    <li><strong>Docker & Python 3.11-slim</strong></li>
                    <li><strong>Non-root execution</strong> (<code>appuser</code>)</li>
                    <li><strong>Automated Healthcheck</strong> (<code>/_stcore/health</code>)</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    # Matching Engine Details
    st.markdown("### 🧠 How the Matching Algorithm Works")
    st.markdown(
        """
        <div class="riq-card" style="margin-bottom:1.5rem;">
            <ol style="color:#CBD5E1; font-size:0.92rem; line-height:1.7; padding-left:1.3rem;">
                <li><strong>Document Ingestion:</strong> The uploaded document (PDF, DOCX, or TXT) is decoded into a normalized Unicode text stream.</li>
                <li><strong>Regex Token Extraction:</strong> Tokens matching <code>[a-zA-Z][a-zA-Z0-9+#.-]*</code> are extracted, preserving special technical terms like <em>C++</em>, <em>C#</em>, <em>Node.js</em>, and <em>.NET</em>.</li>
                <li><strong>Domain Stopword Suppression:</strong> High-frequency English conjunctions, prepositions, and pronouns are filtered using an internal stopword collection.</li>
                <li><strong>Frequency Ranking:</strong> Terms are ranked by occurrence frequency within the target job description to pinpoint the employer's top priorities (up to 40 primary terms).</li>
                <li><strong>Set Overlap Scoring:</strong> The formula <code>Score = (Matched Keywords / Total Job Keywords) × 100</code> determines the keyword overlap percentage.</li>
                <li><strong>Heuristic Suggestions:</strong> Suggestions evaluate missing qualifications, overall alignment threshold, and detect whether quantifiable numerical impacts (e.g., percentages, scale metrics) are present.</li>
            </ol>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Containerization & Deployment
    st.markdown("### 🐳 Docker Containerization Architecture")
    st.code(
        """
# Docker Architecture Snapshot
FROM python:3.11-slim
WORKDIR /app
# Dependencies layer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && useradd -m appuser
# Application files
COPY --chown=appuser:appuser app.py resume_analyzer.py ui_components.py ./
USER appuser
EXPOSE 8501
HEALTHCHECK --interval=30s --timeout=5s CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8501/_stcore/health', timeout=3)"
CMD ["streamlit", "run", "app.py", "--server.headless=true"]
        """.strip(),
        language="dockerfile",
    )


# -----------------------------------------------------------------------------
# Main Application Router
# -----------------------------------------------------------------------------
def main() -> None:
    page = st.session_state["active_page"]
    if page == "dashboard":
        render_dashboard()
    elif page == "analyze":
        render_analyze_page()
    elif page == "history":
        render_history_page()
    elif page == "about":
        render_about_page()
    else:
        render_dashboard()


if __name__ == "__main__":
    main()
