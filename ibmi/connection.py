import paramiko
from config import IBM_HOST, IBM_PORT, IBM_USER, IBM_PASS


def run_sql(sql):

    sql_clean = sql.strip().rstrip(";")

    if not sql_clean.upper().startswith("SELECT"):
        raise Exception("Only SELECT statements allowed")

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ssh.connect(
        hostname=IBM_HOST,
        port=IBM_PORT,
        username=IBM_USER,
        password=IBM_PASS
    )

    cmd = f'qsh -c "db2 \\"{sql_clean}\\""'

    stdin, stdout, stderr = ssh.exec_command(cmd)

    out = stdout.read().decode()
    err = stderr.read().decode()

    ssh.close()

    if err.strip():
        raise Exception(err)

    return out

def run_cl(cmd):

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ssh.connect(
        hostname=IBM_HOST,
        port=IBM_PORT,
        username=IBM_USER,
        password=IBM_PASS
    )

    full_cmd = f'qsh -c \'system "{cmd}"\''

    stdin, stdout, stderr = ssh.exec_command(full_cmd)

    out = stdout.read().decode()
    err = stderr.read().decode()

    ssh.close()

    if err.strip():
        raise Exception(err)

    return out
