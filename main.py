from flask import Flask, render_template, request


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
def index():
    appname = ""
    ip_filter = ""
    if request.method == "POST":
        appname = request.form["appname"]
        ip_filter = request.form["ip_filter"]
    return render_template("app1.html", appname=appname, ip_filter=ip_filter)


if __name__ == "__main__":
    app.run(debug=True)
