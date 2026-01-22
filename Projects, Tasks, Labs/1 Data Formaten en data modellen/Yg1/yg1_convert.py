import yaml
import json
import csv
import xml.etree.ElementTree as ET

# ---------- 1. YAML INLEZEN ----------
with open("interfaces.yaml", "r", encoding="utf-8") as f:
    data = yaml.safe_load(f)

interfaces = data["interfaces"]

# ---------- 2. YAML → JSON ----------
with open("interfaces.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

# ---------- 3. YAML → CSV ----------
with open("interfaces.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["name", "ip", "status", "protocol"])

    for i in interfaces:
        writer.writerow([i["name"], i["ip"], i["status"], i["protocol"]])

# ---------- 4. YAML → TXT ----------
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

# ---------- 5. YAML → XML ----------
root = ET.Element("device", name=data["device"])

for i in interfaces:
    iface = ET.SubElement(root, "interface")
    for key, value in i.items():
        elem = ET.SubElement(iface, key)
        elem.text = value

tree = ET.ElementTree(root)
tree.write("interfaces.xml", encoding="utf-8", xml_declaration=True)

print("YAML conversie voltooid (JSON, CSV, TXT, XML).")
