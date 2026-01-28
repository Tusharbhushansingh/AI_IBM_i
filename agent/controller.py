import re

from config import LIBRARY
from ibmi.failure_detection import detect_failures
from ibmi.job_monitor import get_active_jobs, get_all_jobs, get_msgw_jobs
from ibmi.metadata import detect_table, get_table_schema, count_physical_files, count_logical_files, \
    logical_for_physical, list_all_files
from agent.ai_engine import generate_sql, analyze_jobs_for_risk
from agent.validator import validate_sql, extract_sql
from ibmi.connection import run_sql
from ibmi.msgw_predictor import get_message_queue
from utils.parser import parse_output, parse_wrkactjob


def handle_question(question):
    # 1️⃣ Detect the correct table from the question
    table = detect_table(question)  # e.g., "STUDENT01"
    print("INITIAL TABLE DETECTED-----------:", table)

    # 2️⃣ Get columns for that table
    columns = get_table_schema(table)

    # 3️⃣ Generate AI SQL (AI only decides which columns to select)
    ai_output = generate_sql(question, table, columns)

    # 4️⃣ Extract only the SQL part from AI output
    sql_extracted = extract_sql(ai_output)

    # 5️⃣ Force the correct table name (ignore whatever AI wrote)
    #sql_clean = re.sub(r"FROM\s+\S+", f"FROM {table}", sql_extracted, flags=re.IGNORECASE)

    # 6️⃣ Validate SQL (safe checks)
    validate_sql(sql_extracted, table)
    print("TABLE DETECTED---------------:", table)

    # 7️⃣ Execute SQL on IBM i
    raw_result = run_sql(sql_extracted)

    # 8️⃣ Parse output for rendering in UI
    result = parse_output(raw_result)

    # Return the cleaned SQL and parsed result
    return sql_extracted, result


# ---------------- DASHBOARD ----------------

def job_dashboard():

    raw_jobs = get_all_jobs()
    #jobs = parse_wrkactjob(raw_jobs)

    # raw_msgw = get_msgw_jobs()
    # msgw = parse_output(raw_msgw)

    ai_summary = analyze_jobs_for_risk(raw_jobs)
    print('AI Summary:' + ai_summary)

    return {
        "jobs": raw_jobs,
        #"msgw": msgw,
        "ai_summary": ai_summary,
    }

def get_dashboard_data():

    jobs = get_all_jobs()

    return {
        "jobs": jobs
    }

# ------------------FILE ANALYSIS --------------------
def handle_library_question(question):

    q = question.lower()

    # 🔴 MOST SPECIFIC FIRST

    # logical for physical file
    if "logical" in q and "physical file" in q:
        pf = extract_file_name(question)
        data = logical_for_physical(pf)

    # count physical files
    elif "physical" in q and "how many" in q:
        data = count_physical_files()

    # count logical files
    elif "logical" in q and "how many" in q:
        data = count_logical_files()

    else:
        raise Exception("Unsupported library question yet")

    return data

# ---------------- SAFE FILE DETECTOR ----------------

def extract_file_name(text):

    text = text.upper()

    # match IBM i style names like E304_PF or CUSTOMER
    matches = re.findall(r"\b[A-Z0-9_]{2,10}\b", text)

    stop_words = {"HOW", "MANY", "LOGICAL", "PHYSICAL", "FILES", "FILE", "ARE", "THERE", "IN"}

    for m in matches:
        if m not in stop_words:
            return m

    raise Exception("Could not detect file name")