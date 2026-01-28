# ibmi/job_monitor.py
from ibmi.connection import run_sql, run_cl
from utils.parser import parse_output, parse_wrkactjob


def get_active_jobs(library=None):
    """
    Returns all jobs in QSYS2.ACTIVE_JOB_INFO, not just RUNNING jobs
    """
    sql = """
    SELECT JOB_NAME, USER_NAME, JOB_STATUS, ELAPSED_TIME
    FROM QSYS2.ACTIVE_JOB_INFO
    """

    raw = run_sql(sql)
    return raw  # parse with your parser.py

# ==========================================================
# PUB400 COMPATIBLE JOB MONITOR (PRINT MODE)
# ==========================================================

def get_all_jobs():
    """
    Runs WRKACTJOB in PRINT mode and parses output.
    PUB400 only allows limited jobs.
    """

    raw = run_cl("WRKACTJOB OUTPUT(*PRINT)")

    return parse_wrkactjob(raw)


def get_msgw_jobs():
    """
    Filter MSGW jobs from available list
    """

    jobs = get_all_jobs()

    return [j for j in jobs if j.get("STATUS") == "MSGW"]