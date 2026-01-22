from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def home():
    user_ip = request.remote_addr or "Unknown"
    return render_template("index.html", user_ip=user_ip)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
