"""
AI-Enhanced Website Health Checker (Smart Version)
--------------------------------------------------
Checks one URL, generates Markdown + HTML reports.
AI summary is only generated for WARN or FAIL statuses.
"""

import os
import requests
import markdown
from datetime import datetime
from dotenv import load_dotenv  # Load .env variables for API key

# Load environment variables from .env
load_dotenv()

# Optional AI import
try:
    from openai import OpenAI
    AI_ENABLED = True
except ImportError:
    AI_ENABLED = False

# --- CONFIG ---
URL = "https://openai.com/"  # Example: change to any URL to check
TIMEOUT = 5  # Seconds to wait for the website to respond
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Optional for AI summary

# --- CHECK URL FUNCTION ---
def check_url(url):
    """
    Check a website's health.
    Returns: status string and HTTP code
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",  # Avoid 403 errors
        "Accept": "text/html",
    }
    try:
        response = requests.get(url, headers=headers, timeout=TIMEOUT)
        status = "OK" if response.status_code == 200 else "WARN"
        code = response.status_code
    except requests.exceptions.RequestException:
        status = "FAIL"
        code = "-"
    return status, code

# --- AI SUMMARY FUNCTION (only for WARN/FAIL) ---
def ai_summary(url, status, code):
    """
    Generate an AI summary if the status is WARN or FAIL.
    Returns a string summary or fallback message.
    """
    # Skip AI for OK status
    if status == "OK":
        return "_No AI summary needed for healthy site._"

    # Skip if AI not enabled or API key missing
    if not (AI_ENABLED and OPENAI_API_KEY):
        return "_AI summary disabled (no API key found)_"

    client = OpenAI(api_key=OPENAI_API_KEY)
    prompt = f"The website {url} returned status '{status}' with HTTP code {code}. Write a short, clear summary explaining what this means."

    try:
        response = client.chat.completions.create(
            model="gpt-5",
            messages=[{"role": "user", "content": prompt}],
            max_completion_tokens=60  # Updated param for GPT-5
        )

        # Robust extraction to handle different SDK responses
        content = None
        if hasattr(response.choices[0], "message") and hasattr(response.choices[0].message, "content"):
            content = response.choices[0].message.content
        elif hasattr(response.choices[0], "delta") and hasattr(response.choices[0].delta, "content"):
            content = response.choices[0].delta.content

        if content and content.strip():
            return content.strip()
        else:
            return "_AI did not return any summary text._"

    except Exception as e:
        return f"_AI summary error: {e}_"

# --- GENERATE REPORT FUNCTION ---
def generate_report(url, status, code, summary):
    """
    Generate Markdown and HTML reports from the results.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Markdown content
    md = f"# Website Health Report\n\nGenerated: {timestamp}\n\n"
    md += f"- URL: {url}\n- Status: {status}\n- HTTP Code: {code}\n\n"
    md += f"## AI Summary\n{summary}\n"

    # Save Markdown file
    with open("report.md", "w", encoding="utf-8") as f:
        f.write(md)

    # Convert Markdown → HTML
    html = markdown.markdown(md)
    with open("report.html", "w", encoding="utf-8") as f:
        f.write(html)

    print("✅ Report generated: report.md + report.html")

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    # 1️⃣ Check the website
    status, code = check_url(URL)

    # 2️⃣ Generate AI summary only for WARN or FAIL
    summary = ai_summary(URL, status, code)

    # 3️⃣ Generate Markdown + HTML reports
    generate_report(URL, status, code, summary)
