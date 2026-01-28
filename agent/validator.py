import re
from config import LIBRARY

def validate_sql(sql, table):

    s = sql.upper()

    if not s.startswith("SELECT"):
        raise Exception("Only SELECT allowed")

    if f"{LIBRARY}.{table}" not in s:
        raise Exception("Wrong table reference")

    banned = ["DELETE", "UPDATE", "DROP", "ALTER", "INSERT"]

    for word in banned:
        if word in s:
            raise Exception("Dangerous SQL detected")


def extract_sql(text):
    # Look for ```sql ... ``` block
    match = re.search(r"```sql\s*(.*?)```", text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    # Otherwise take first line starting with SELECT
    for line in text.splitlines():
        line = line.strip()
        if line.upper().startswith("SELECT"):
            return line
    raise Exception("No valid SQL found")

