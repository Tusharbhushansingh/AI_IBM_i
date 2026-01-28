# ibmi/msgw_predictor.py
from ibmi.connection import run_sql

def get_message_queue(queue_name):
    if queue_name != ' ':
        sql = f"""
        SELECT MSG_ID, MSG_TYPE, MSG_TEXT, MSG_TIME
        FROM QSYS2.MESSAGE_QUEUE_ENTRIES
        WHERE MSGQ_NAME = '{queue_name.upper()}'
        """
        raw = run_sql(sql)
        return raw
