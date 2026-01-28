import re


def parse_output(output):
    lines = [l.strip() for l in output.splitlines() if l.strip()]
    if len(lines) < 2:
        return []

    headers = lines[0].split()
    data_lines = lines[1:]

    records = []

    for line in data_lines:
        # skip footer like "(62 ROWS)"
        if line.startswith("(") and "ROWS" in line.upper():
            continue

        values = line.split()
        if len(values) < len(headers):
            values += [''] * (len(headers) - len(values))

        row = {headers[i]: values[i] for i in range(len(headers))}
        records.append(row)

    return records
def parse_wrkactjob(text):

    jobs = []

    for line in text.splitlines():

        line = line.rstrip()

        # match common WRKACTJOB print format
        m = re.match(
            r"\s*(\d+)\s+(\S+)\s+(\S+)\s+(\S+)\s+([\d.,]+)\s+(.+?)\s+(\S+)$",
            line
        )

        if not m:
            continue

        jobs.append({
            "JOBNO": m.group(1),
            "USER": m.group(2),
            "JOB": m.group(3),
            "TYPE": m.group(4),
            "CPU": m.group(5),
            "FUNCTION": m.group(6),
            "STATUS": m.group(7)
        })

    return jobs