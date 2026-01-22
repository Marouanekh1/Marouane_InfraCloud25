import json
import csv
import yaml
import xml.etree.ElementTree as ET

# ---------- 1. JSON INLEZEN ----------
with open("interfaces.json", "r", encoding="utf-8") as f:
    data = json.load(f)

interfaces = data["interfaces"]

# ---------- 2. JSON → YAML ----------
with open("interfaces.yaml", "w", encoding="utf-8") as f:
    yaml.dump(data, f, sort_keys=False)

# ---------- 3. JSON → CSV ----------
with open("interfaces.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["name", "ip", "status", "protocol"])

    for i in interfaces:
        writer.writerow([i["name"], i["ip"], i["status"], i["protocol"]])

# ---------- 4. JSON → TXT ----------
with open("interfaces.txt", "w", encoding="utf-8") as f:
    f.write(f"Device: {data['device']}\n")
    f.write("=" * 40 + "\n")

    for i in interfaces:
        f.write(
            f"{i['name']:20} "
            f"{i['ip']:15} "
            f"{i['status']:25} "
            f"{i['protocol']}\n"
        )

# ---------- 5. JSON → XML ----------
root = ET.Element("device", name=data["device"])

for i in interfaces:
    iface = ET.SubElement(root, "interface")
    for key, value in i.items():
        elem = ET.SubElement(iface, key)
        elem.text = value

tree = ET.ElementTree(root)
tree.write("interfaces.xml", encoding="utf-8", xml_declaration=True)

print("Conversie voltooid: YAML, CSV, TXT en XML aangemaakt.")
