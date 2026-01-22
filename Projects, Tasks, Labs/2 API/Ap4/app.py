from flask import Flask, request, jsonify, render_template, redirect, url_for

app = Flask(__name__)

# In-memory "database"
tasks = [
    {"id": 1, "title": "Study REST APIs", "done": False},
    {"id": 2, "title": "Build Ap4 webforms app", "done": True},
]

def get_next_id():
    return max((t["id"] for t in tasks), default=0) + 1

def find_task(task_id: int):
    return next((t for t in tasks if t["id"] == task_id), None)

# -----------------------
# API (JSON) endpoints
# -----------------------
@app.get("/api/v1/tasks")
def api_list_tasks():
    return jsonify(tasks), 200

@app.post("/api/v1/tasks")
def api_create_task():
    if not request.is_json:
        return jsonify({"error": "Body must be JSON"}), 400

    data = request.get_json()
    title = data.get("title", "").strip()
    if not title:
        return jsonify({"error": "Field 'title' is required"}), 400

    new_task = {"id": get_next_id(), "title": title, "done": bool(data.get("done", False))}
    tasks.append(new_task)
    return jsonify(new_task), 201

@app.delete("/api/v1/tasks/<int:task_id>")
def api_delete_task(task_id):
    global tasks
    t = find_task(task_id)
    if t is None:
        return jsonify({"error": "Task not found"}), 404

    tasks = [x for x in tasks if x["id"] != task_id]
    return jsonify(t), 200

# -----------------------
# WEB (forms) routes
# -----------------------
@app.get("/")
def web_index():
    # Zoek/filter via query param ?q=
    q = request.args.get("q", "").strip().lower()

    if q:
        filtered = [t for t in tasks if q in t["title"].lower()]
    else:
        filtered = tasks

    return render_template("index.html", tasks=filtered, q=q)

@app.post("/add")
def web_add():
    title = request.form.get("title", "").strip()
    done = request.form.get("done") == "on"

    if title:
        tasks.append({"id": get_next_id(), "title": title, "done": done})

    return redirect(url_for("web_index"))

@app.post("/toggle/<int:task_id>")
def web_toggle(task_id):
    t = find_task(task_id)
    if t:
        t["done"] = not t["done"]
    return redirect(url_for("web_index"))

@app.post("/delete/<int:task_id>")
def web_delete(task_id):
    global tasks
    tasks = [t for t in tasks if t["id"] != task_id]
    return redirect(url_for("web_index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
