# ibmi/failure_detection.py
from ibmi.connection import run_sql

def detect_failures():
    sql = """
    SELECT JOB_NAME, JOB_USER, JOB_STATUS, MSG_TEXT
    FROM QSYS2.JOB_LOG_INFO
    WHERE MSG_TEXT LIKE '%FAIL%' OR JOB_STATUS = 'ENDED ABNORMALLY'
    """
    raw = run_sql(sql)
    return raw
