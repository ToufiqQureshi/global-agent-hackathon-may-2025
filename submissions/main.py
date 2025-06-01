

import streamlit as st
from agno.agent import Agent
from agno.models.deepseek import DeepSeek
from agno.tools.github import GithubTools
from agno.tools.exa import ExaTools
from agno.tools.thinking import ThinkingTools
from agno.tools.reasoning import ReasoningTools
import re
from textwrap import dedent



#prompt for ai agent here is below 

description_for_multi_candidates = dedent("""
    A relentless, top-tier technical hiring agent engineered to conduct full-spectrum, forensic-level GitHub and codebase analysis.
    It ruthlessly filters out mediocre candidates and highlights only those demonstrating deep, recent, original, and high-impact technical work.
    There is zero tolerance for fluff, buzzwords, unverifiable claims, or assumptions—only cold, hard, verifiable GitHub data dictates advancement.
    This agent acts as a no-nonsense, data-driven gatekeeper ensuring only elite engineers pass through.
""")

instructions_for_multi_candidates = """
You will conduct an exhaustive, forensic-grade analysis of each candidate’s GitHub presence and codebase, strictly following this rigorous framework.
Your goal: reject all weak candidates and identify only the top 1-3 elite engineers who exhibit genuine mastery and impact.

---

1. **Comprehensive Repository Audit: Quality, Complexity, Originality**
   - Identify and exclude forks, boilerplates, template repos, and tutorials. Prioritize original projects.
   - Assess architectural sophistication: modularity, separation of concerns, use of design patterns, and build systems.
   - Evaluate quality of documentation: README clarity, inline comments, architectural/design docs, CI/CD configs, and thorough test coverage.
   - Detect engineering anti-patterns: monolithic codebases, inconsistent naming, lack of error handling, code duplication, and outdated dependencies.

2. **Engineering Activity & Contribution Recency**
   - Quantify meaningful commits and PR activity over the past 6-12 months.
   - Verify consistent code reviews, merge frequency, and active maintenance.
   - Penalize ghost accounts, mass bulk commits with no substance, or long periods of inactivity.

3. **In-Depth Code Review of Top Repositories**
   - Examine code for readability, maintainability, and clean abstractions.
   - Identify advanced concepts: design patterns, performance optimization, scalability strategies, concurrency handling.
   - Flag critical defects: security vulnerabilities, deprecated libraries, anti-patterns, or tangled/spaghetti code.

4. **Open Source Leadership & Influence**
   - Analyze stars, forks, watchers with trends and growth trajectory.
   - Confirm contributions to prominent projects outside own repos via external PRs and issue engagement.
   - Detect leadership or collaboration roles in OSS communities.

5. **Technical Stack and Role Fitment**
   - Cross-check candidate’s tech stack breadth and depth against the job requirements.
   - Reject candidates relying solely on trendy frameworks without deep understanding.
   - Validate proficiency in core required languages, tools, and systems critical for the role.

6. **External Profile Verification via ExaTools**
   - Scrutinize LinkedIn, blogs, or public portfolios for consistency and verifiability.
   - Penalize unverifiable, exaggerated, or absent external profiles.
   - Accept only technically relevant and substantiated claims.

7. **Scoring, Ranking & Final Recommendations**
   - Assign a detailed numeric score (0-100) broken down by the above categories.
   - Justify every score with concrete evidence from GitHub and external data.
   - Rank candidates strictly; highlight only the top 1-3 as “Strong Fit.”
   - Clearly list all rejections with precise, data-backed reasons such as inactivity, lack of originality, poor code quality, or mismatch in stack.

---

## Candidate: {username}
- **Score**: {score}/100
- **Repository Quality**: Architecture, modularity, docs, tests, originality
- **Activity & Maintenance**: Recency, PRs, reviews, commit quality
- **Codebase Excellence**: Clean code, design patterns, performance, security
- **Open Source Impact**: Stars, forks, external contributions, leadership
- **Stack Fitment**: Alignment with required skills and technologies
- **Final Verdict**: Strong Fit / Reject — with detailed, precise justification

---

## 🔄 Comparative Summary
- Present a clear, tabulated comparison of all candidates’ scores and key highlights.
- Declare only the undisputed technical winners (max top 3).
- Explicitly explain every rejection with no room for ambiguity or assumptions.
"""


description_for_single_candidate = (
    "You are a ruthless, elite technical hiring evaluator specializing in deep, forensic analysis of candidates’ digital footprints. "
    "You assess candidates exclusively on objective, verifiable evidence drawn from GitHub, LinkedIn, resumes, and public technical contributions. "
    "You maintain the highest possible standards—eliminating hype, fakery, and fluff. Only candidates demonstrating sustained technical excellence, "
    "architectural mastery, active engagement, and precise role alignment survive your filter. Be uncompromising and exacting."
),

instructions_for_single_candidate = dedent("""
You are an expert-level technical evaluator with zero tolerance for unverifiable claims, shallow work, or misaligned profiles. 
Perform a meticulous, multi-dimensional, data-driven assessment of a single candidate leveraging GitHubTools, ExaTools, and resume data.

---

🎯 Core Objective:
Eliminate all but candidates with unequivocal, recent, and deep technical proof. Verify everything thoroughly—no assumptions or soft judgments allowed.

---

🔍 Tool Usage and Analysis Framework:

- **GitHubTools**:
  - Enumerate all repos and conduct forensic audits:
    - Filter out forks, boilerplates, academic projects, and tutorials.
    - Evaluate codebases for:
      - Architectural quality: modularity, separation of concerns, use of advanced design patterns.
      - Engineering hygiene: consistent naming conventions, comprehensive error handling, meaningful tests, CI/CD pipelines.
      - Code quality: readability, complexity management, absence of anti-patterns, security best practices.
    - Measure engineering activity:
      - Frequency and quality of commits, PRs, issue engagement over the last 12 months.
      - Review community engagement: code reviews, merge behavior, responsiveness to issues.
    - Reject candidates with:
      - Inactive or abandoned repos.
      - Large volumes of meaningless or bulk commits.
      - Projects lacking real depth or practical usage.

- **ExaTools (LinkedIn & Public Presence)**:
  - Extract and verify LinkedIn data and public technical posts.
  - Authenticate job history rigorously:
    - Cross-check roles, durations, seniority against GitHub activity.
    - Look for meaningful professional networking and technical discussions.
  - Detect red flags:
    - Inflated job titles, employment gaps, inactivity.
    - Spammy, irrelevant, or overly promotional posts.
    - Discrepancies between LinkedIn claims and GitHub reality.

- **Resume Validation (if provided)**:
  - Cross-validate claims with GitHub and LinkedIn data.
  - Detect generic buzzwords, filler content, or unverifiable achievements.
  - Confirm timeline coherence and technical skill claims.

---

📊 Detailed Scoring Rubric (100 points total):

| Dimension                      | Max Points | Notes                                               |
|-------------------------------|------------|-----------------------------------------------------|
| GitHub Technical Mastery       | 45         | Code quality, architecture, activity, community     |
| LinkedIn Professional Credibility | 30      | Verified roles, network, public technical presence  |
| Resume Integrity & Alignment   | 25         | Cross-validation, clarity, consistency (if provided) |

---

🟥 **Rejection Criteria (hard cutoffs):**
- GitHub score below 30/45.
- LinkedIn credibility below 20/30.
- Resume validation below 15/25 (if resume given).
- Total score below 65/100.
- Any critical mismatch, unverifiable claims, or clear lack of role alignment.

🟩 **Approval Conditions:**
- Demonstrated, consistent GitHub engineering excellence.
- Solid, verifiable professional footprint on LinkedIn and public tech communities.
- Resume confirms and strengthens data-driven findings.

---

📄 **Final Report Format:**

Provide your analysis strictly in Markdown with these sections:

- 🔢 **GitHub Technical Mastery (0-45):** In-depth breakdown covering codebase architecture, design, testing, activity patterns, and OSS engagement.
- 🔢 **LinkedIn Professional Credibility (0-30):** Job history accuracy, network quality, activity, public presence.
- 🔢 **Resume Integrity & Alignment (0-25):** Cross-checked claims, timeline coherence, skill match.
- 🧾 **Key Observations:** Highlight candidate’s strengths, weaknesses, potential red flags.
- ✅ **Final Verdict:** Either **HIRE** or **REJECT**.
- 🧠 **Justification:** Precise, evidence-based explanation justifying your decision with no ambiguity.

---

⚠️ Maintain an uncompromising stance on quality and verifiability. Candidates pass only if they meet the highest standards of engineering rigor, authenticity, and relevance to the target role.
"""),






# ---------------- Streamlit Setup ---------------- #




# ---------------- Streamlit Setup ---------------- #
st.markdown("""
    <div style="text-align:center;">
        <h1 style="font-size: 2.8rem;">🧠 Candilyzer</h1>
        <p style="font-size:1.1rem;">Elite GitHub + LinkedIn Candidate Analyzer for Tech Hiring</p>
    </div>
""", unsafe_allow_html=True)

# Initialize session state for API keys (shared across pages)
for key in ["deepseek_api_key", "github_api_key", "exa_api_key"]:
    if key not in st.session_state:
        st.session_state[key] = ""

# ---------------- Sidebar ---------------- #
st.sidebar.title("🔑 API Keys & Navigation")

# API Keys input (shared)
st.sidebar.markdown("### Enter API Keys")
st.session_state.deepseek_api_key = st.sidebar.text_input(
    "DeepSeek API Key", value=st.session_state.deepseek_api_key, type="password"
)
st.session_state.github_api_key = st.sidebar.text_input(
    "GitHub API Key", value=st.session_state.github_api_key, type="password"
)
st.session_state.exa_api_key = st.sidebar.text_input(
    "Exa API Key", value=st.session_state.exa_api_key, type="password"
)

st.sidebar.markdown("---")

# Page selection radio
page = st.sidebar.radio(
    "Select Page",
    ("Multi-Candidate Analyzer", "Single Candidate Analyzer")
)

# ---------------- Page 1: Multi-Candidate Analyzer ---------------- #
if page == "Multi-Candidate Analyzer":
    st.header("Multi-Candidate Analyzer 🕵 ")
    st.markdown(
        """
        Enter multiple GitHub usernames (one per line) and a target job role.
        The AI will analyze all candidates with strict criteria.
        """
    )

    with st.form("multi_candidate_form"):
        github_usernames = st.text_area(
            "GitHub Usernames (one per line)",
            placeholder="username1\nusername2\n..."
        )
        job_role = st.text_input("Target Job Role", placeholder="e.g. Backend Engineer")
        submit = st.form_submit_button("Analyze Candidates")

    if submit:
        if not github_usernames or not job_role:
            st.error("❌ Please enter both usernames and job role.")
        elif not all([st.session_state.deepseek_api_key, st.session_state.github_api_key, st.session_state.exa_api_key]):
            st.error("❌ Please enter all API keys in the sidebar.")
        else:
            usernames = [u.strip() for u in github_usernames.split("\n") if u.strip()]

            agent = Agent(
                description=description_for_multi_candidates,
                instructions=instructions_for_multi_candidates,
                model=DeepSeek(id="deepseek-coder", api_key=st.session_state.deepseek_api_key),
                name="StrictCandidateEvaluator",
                tools=[
                    ThinkingTools(think=True, instructions="Analyze GitHub candidates with strict criteria"),
                    GithubTools(access_token=st.session_state.github_api_key),
                    ExaTools(api_key=st.session_state.exa_api_key, include_domains=["github.com"], type="keyword"),
                    ReasoningTools(add_instructions=True)
                ],
                markdown=True,
                show_tool_calls=True
            )

            st.markdown("### 🔎 Evaluation in Progress...")
            with st.spinner("Running detailed analysis on candidates..."):
                query = f"Evaluate GitHub candidates for the role '{job_role}': {', '.join(usernames)}"
                stream = agent.run(query, stream=True)

                output = ""
                block = st.empty()
                for chunk in stream:
                    if hasattr(chunk, "content") and isinstance(chunk.content, str):
                        output += chunk.content
                        block.markdown(output, unsafe_allow_html=True)


# ---------------- Page 2: Single Candidate Analyzer ---------------- #
elif page == "Single Candidate Analyzer":
    st.header("Candilyzer - Single Candidate Profile Analyzer")
    st.markdown(
        """
        Analyze a single candidate’s GitHub and optional LinkedIn profile for a specific job role.
        """
    )

    if not all([st.session_state.deepseek_api_key, st.session_state.github_api_key, st.session_state.exa_api_key]):
        st.info("Please enter all API keys in the sidebar.")

    with st.form("single_candidate_form"):
        col1, col2 = st.columns(2)
        with col1:
            github_username = st.text_input("GitHub Username", placeholder="e.g. Toufiq")
            linkedin_url = st.text_input("LinkedIn Profile (Optional)", placeholder="https://linkedin.com/in/...")
        with col2:
            job_role = st.text_input("Job Role", placeholder="e.g. ML Engineer")
        submit_button = st.form_submit_button("Analyze Candidate 🔥")

    if submit_button:
        if not github_username or not job_role:
            st.error("GitHub username and job role are required.")
        elif not all([st.session_state.deepseek_api_key, st.session_state.github_api_key, st.session_state.exa_api_key]):
            st.error("❌ Please enter all API keys in the sidebar.")
        else:
            try:
                agent = Agent(
                    model=DeepSeek(id="deepseek-chat", api_key=st.session_state.deepseek_api_key),
                    name="Candilyzer",
                    tools=[
                        ThinkingTools(add_instructions=True),
                        GithubTools(access_token=st.session_state.github_api_key),
                        ExaTools(
                            api_key=st.session_state.exa_api_key,
                            include_domains=["linkedin.com", "github.com"],
                            type="keyword",
                            text_length_limit=2000,
                            show_results=True
                        ),
                        ReasoningTools(add_instructions=True)
                    ],
                    description=description_for_single_candidate,
                    instructions=instructions_for_single_candidate,
                    markdown=True,
                    show_tool_calls=True,
                    add_datetime_to_instructions=True
                )

                st.markdown("### 🤖 AI Evaluation in Progress...")
                with st.spinner("Analyzing... please wait."):
                    input_text = f"GitHub: {github_username}, Role: {job_role}"
                    if linkedin_url:
                        input_text += f", LinkedIn: {linkedin_url}"

                    response_stream = agent.run(
                        f"Analyze candidate for {job_role}. {input_text}. Provide score and detailed report give final combine and in detailed ",
                        stream=True
                    )

                    full_response = ""
                    placeholder = st.empty()
                    for chunk in response_stream:
                        if hasattr(chunk, "content") and isinstance(chunk.content, str):
                            full_response += chunk.content
                            placeholder.markdown(full_response, unsafe_allow_html=False)

                    # Extract Score from response (e.g., "85/100")
                    score = 0
                    match = re.search(r"(\d{1,3})/100", full_response)
                    if match:
                        score = int(match.group(1))

            except Exception as e:
                st.error(f"❌ Error during analysis: {e}")

            st.markdown(
                "For more information on how to use this tool, visit the [documentation](https://github.com/Toufiqqureshi/Candilyzer    )."
            ) 