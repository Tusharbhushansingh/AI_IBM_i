import subprocess
from config import LIBRARY, OLLAMA_MODEL


def generate_sql(question, table, columns):
    col_text = "\n".join(f"- {c}" for c in columns)

    prompt = f"""
You MUST generate a SELECT statement for table {LIBRARY}.{table}.
Do NOT use any other table.
Do NOT add explanations or extra text.
Do NOT hallucinate.
Return SQL only, starting with SELECT.

Columns available in the table:
{col_text}

Question:
{question}
"""

    result = subprocess.run(
        ["ollama", "run", OLLAMA_MODEL],
        input=prompt,
        text=True,
        capture_output=True
    )

    return result.stdout.strip()

# ---------- AI JOB ANALYSIS ----------
def analyze_jobs_for_risk(job_text):

    prompt = f"""
You are an IBM i operations expert.

Analyze these jobs and identify:

- Jobs likely to hang
- MSGW risks
- Failures
- Performance problems

Job list:
{job_text}

Respond in plain English bullet points.
"""

    result = subprocess.run(
        ["ollama", "run", OLLAMA_MODEL],
        input=prompt,
        text=True,
        capture_output=True,
    )

    return result.stdout.strip()

# ---------- AI FILE ANALYSIS ---------
#def summarize_library_result(question, data):

    prompt = f"""
You are IBM i expert.

Explain result in simple way.

Question:
{question}

Raw Data:
{data}
"""

    result = subprocess.run(
        ["ollama", "run", OLLAMA_MODEL],
        input=prompt,
        text=True,
        capture_output=True
    )

    return result.stdout.strip()