from flask import Flask, render_template, request
from model import compare_and_save 
from datetime import datetime

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        pickup = request.form["pickup"]
        drop = request.form["drop"]

        try:
            result = compare_and_save(pickup, drop)

            result["timestamp"] = result.get("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

            return render_template("result.html", result=result)

        except Exception as e:
     
            return render_template("index.html", error=str(e))

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
