from flask import Flask, render_template, request
import json

app = Flask(__name__)

def load_data():
    """Leest het JSON-bestand en geeft Python-data terug (dict)."""
    with open("devices.json", "r", encoding="utf-8") as f:
        return json.load(f)

def filter_interfaces(interfaces, status=None, if_type=None, name_contains=None):
    """
    Filtert een lijst van interfaces op:
    - status: 'up' of 'down'
    - if_type: 'ethernet', 'loopback', ...
    - name_contains: stukje tekst dat in de naam voorkomt
    """
    results = []

    for iface in interfaces:
        # 1) status filter (optioneel)
        if status and iface.get("oper_status") != status:
            continue

        # 2) type filter (optioneel)
        if if_type and iface.get("type") != if_type:
            continue

        # 3) name filter (optioneel)
        if name_contains and name_contains.lower() not in iface.get("name", "").lower():
            continue

        results.append(iface)

    return results

@app.route("/", methods=["GET"])
def index():
    # Startpagina met invulvelden
    return render_template("index.html")

@app.route("/results", methods=["POST"])
def results():
    # 1) Lees input uit het formulier
    status = request.form.get("status") or None
    if_type = request.form.get("type") or None
    name_contains = request.form.get("name_contains") or None

    # 2) Laad JSON
    data = load_data()
    interfaces = data["device"]["interfaces"]

    # 3) Filter
    filtered = filter_interfaces(
        interfaces,
        status=status,
        if_type=if_type,
        name_contains=name_contains
    )

    # 4) Toon in HTML
    return render_template(
        "results.html",
        hostname=data["device"]["hostname"],
        filters={"status": status, "type": if_type, "name_contains": name_contains},
        interfaces=filtered
    )

if __name__ == "__main__":
    app.run(debug=True)
