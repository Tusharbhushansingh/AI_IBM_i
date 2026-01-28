import re

from ibmi.connection import run_sql
from config import LIBRARY


def list_tables():
    sql = f"""
    SELECT TABLE_NAME
    FROM QSYS2.SYSTABLES
    WHERE TABLE_SCHEMA = '{LIBRARY}'
      AND TABLE_TYPE IN ('T', 'P', 'L', 'V')
    ORDER BY TABLE_NAME
    """
    raw = run_sql(sql)

    tables = []

    for line in raw.splitlines():
        line = line.strip()

        # skip empty lines
        if not line:
            continue

        # skip headers
        if line.upper() == "TABLE_NAME":
            continue

        # skip separator lines (----)
        if all(c in "- " for c in line):
            continue

        # skip footer like (62 ROWS)
        if line.startswith("(") and "ROWS" in line.upper():
            continue

        # take first token as table name
        table_name = line.split()[0].upper()
        tables.append(table_name)

    print("DEBUG: Tables loaded:", tables)  # 🔹 Debug output
    return tables

def detect_table(question):

    q = question.upper()

    tables = list_tables()

    # Sort by length descending
    tables_sorted = sorted(tables, key=len, reverse=True)

    for t in tables_sorted:
        # Match whole word (STUDENT01, not part of STUDENTNAME)
        if re.search(rf"\b{t}\b", q):
            return t

def get_table_schema(table):

    sql = f"""
    SELECT COLUMN_NAME, DATA_TYPE
    FROM QSYS2.SYSCOLUMNS
    WHERE TABLE_SCHEMA = '{LIBRARY}'
      AND TABLE_NAME = '{table}'
    ORDER BY ORDINAL_POSITION
    """

    raw = run_sql(sql)

    lines = [l.strip() for l in raw.splitlines() if l.strip()]

    cols = []

    for line in lines:
        if line.upper().startswith("COLUMN_NAME"):
            continue
        if set(line) <= {"-"}:
            continue

        parts = line.split()
        if len(parts) >= 2:
            cols.append(f"{parts[0]} ({parts[1]})")

    return cols

# ---------------- JOB MONITORING ----------------
def get_all_jobs():

    sql = """
    SELECT JOB_NAME,
           AUTHORIZATION_NAME,
           JOB_STATUS,
           SUBSYSTEM,
           ELAPSED_TOTAL_TIME
    FROM QSYS2.ACTIVE_JOB_INFO
    """

    return run_sql(sql)

def get_msgw_jobs():

    sql = """
    SELECT JOB_NAME,
           AUTHORIZATION_NAME,
           JOB_STATUS,
           SUBSYSTEM
    FROM QSYS2.ACTIVE_JOB_INFO
    WHERE JOB_STATUS = 'MSGW'
    """

    return run_sql(sql)

# ---------------- FILE ANALYSIS -----------------
def count_physical_files():

    sql = f"""
    SELECT TABLE_NAME
    FROM QSYS2.SYSTABLES
    WHERE TABLE_SCHEMA = '{LIBRARY}'
      AND TABLE_TYPE = 'T'
    """

    raw = run_sql(sql)

    lines = [l.strip() for l in raw.splitlines() if l.strip()]

    files = []

    for line in lines:
        if line.upper() == "TABLE_NAME":
            continue
        if set(line) <= {"-"}:
            continue
        files.append(line)

    return len(files), files

def count_logical_files():

    sql = f"""
        SELECT TABLE_NAME
        FROM QSYS2.SYSTABLES
        WHERE TABLE_SCHEMA = '{LIBRARY}'
          AND TABLE_TYPE = 'L'
    """

    raw = run_sql(sql)

    lines = [l.strip() for l in raw.splitlines() if l.strip()]

    files = []

    for line in lines:
        if line.upper() == "TABLE_NAME":
            continue
        if set(line) <= {"-"}:
            continue

        files.append(line)

    return len(files), files

def logical_for_physical(pf):

    sql = f"""
    SELECT TABLE_NAME
    FROM QSYS2.SYSTABLES
    WHERE BASE_TABLE_SCHEMA = '{LIBRARY}'
      AND BASE_TABLE_NAME = '{pf.upper()}'
    """

    raw = run_sql(sql)

    lines = [l.strip() for l in raw.splitlines() if l.strip()]

    files = []

    for line in lines:
        if line.upper() == "TABLE_NAME":
            continue
        if set(line) <= {"-"}:
            continue

        files.append(line)

    return len(files), files

def list_physical_files():

    sql = f"""
    SELECT TABLE_NAME
    FROM QSYS2.SYSTABLES
    WHERE TABLE_SCHEMA = '{LIBRARY}'
      AND TABLE_TYPE = 'T'
    ORDER BY TABLE_NAME
    """

    raw = run_sql(sql)

    lines = [l.strip() for l in raw.splitlines() if l.strip()]

    files = []

    for line in lines:
        if line.upper() == "TABLE_NAME":
            continue
        if set(line) <= {"-"}:
            continue
        files.append(line)

    return files

def list_all_files(object_type=None):

    cond = ""

    if object_type == "PF":
        cond = "AND TABLE_TYPE = 'T'"

    elif object_type == "LF":
        cond = "AND TABLE_TYPE = 'L'"

    sql = f"""
        SELECT TABLE_NAME
        FROM QSYS2.SYSTABLES
        WHERE TABLE_SCHEMA = '{LIBRARY}'
        {cond}
    """

    raw = run_sql(sql)

    lines = [l.strip() for l in raw.splitlines() if l.strip()]

    files = []

    for l in lines:
        if l.upper() == "TABLE_NAME":
            continue
        if set(l) <= {"-"}:
            continue

        files.append(l.upper())

    return files


