from flask import Flask, render_template, request

from agent.controller import (
    handle_question,
    job_dashboard, get_dashboard_data, handle_library_question,
)

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():

    result = None
    sql = None
    error = None

    if request.method == "POST":
        question = request.form.get("question")

        try:
            sql, result = handle_question(question)
        except Exception as e:
            error = str(e)

    return render_template(
        "index.html",
        sql=sql,
        result=result,
        error=error,
    )

@app.route("/dashboard")
def dashboard():

    # data = get_dashboard_data()
    data = job_dashboard()

    return render_template(
        "dashboard.html",
        jobs=data["jobs"],
        ai_summary = data["ai_summary"]
    )

@app.route("/job_predictions")
def job_predictions():

    data = job_dashboard()

    return render_template(
        "job_predictions.html",
        ai=data["ai"],
    )

@app.route("/library", methods=["GET", "POST"])
def library():

    result = None
    error = None

    if request.method == "POST":
        question = request.form.get("question")

        try:
            result = handle_library_question(question)
            print("LIBRARY RESULT TYPE:", type(result))
            print("LIBRARY RESULT VALUE:", result)
        except Exception as e:
            error = str(e)

    return render_template(
        "library.html",
        result=result,
        error=error
    )

if __name__ == "__main__":
    app.run(debug=True)



# 1️⃣ job monitoring agent
# 2️⃣ MSGW predictor
# 3️⃣ failure detection
# 4️⃣ dashboards
# 5️⃣ alerting
# 6️⃣ scheduled scans