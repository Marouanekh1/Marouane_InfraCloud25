from netmiko import ConnectHandler
import json

def parse_show_ip_int_brief(output: str):
    """
    Zet 'show ip interface brief' output om naar een lijst van dictionaries.
    Werkt voor typische Cisco IOS/IOS-XE tabellen.

    Verwachte kolommen (ongeveer):
    Interface  IP-Address  OK?  Method  Status  Protocol
    """
    lines = [ln.strip() for ln in output.splitlines() if ln.strip()]

    # Zoek header lijn (bevat meestal 'Interface' en 'IP-Address')
    header_index = None
    for i, ln in enumerate(lines):
        if "Interface" in ln and "IP-Address" in ln:
            header_index = i
            break

    if header_index is None:
        raise ValueError("Kon header van 'show ip interface brief' niet vinden. Output onverwacht.")

    data_lines = lines[header_index + 1:]

    interfaces = []
    for ln in data_lines:
        # Split op whitespace
        parts = ln.split()

        # Minimale check: we verwachten minstens 6 velden
        # Interface, IP, OK?, Method, Status..., Protocol
        if len(parts) < 6:
            continue

        interface = parts[0]
        ip_address = parts[1]
        ok = parts[2]
        method = parts[3]

        # Status kan 1 of meerdere woorden zijn (bv. "administratively down")
        protocol = parts[-1]
        status = " ".join(parts[4:-1])

        interfaces.append({
            "interface": interface,
            "ip_address": ip_address,
            "ok": ok,
            "method": method,
            "status": status,
            "protocol": protocol
        })

    return interfaces

def filter_interfaces(interfaces, status_contains=None, protocol=None, has_ip=None):
    """
    Filtert interfaces op:
    - status_contains: bv. 'up' of 'administratively'
    - protocol: 'up' of 'down'
    - has_ip: True => IP != 'unassigned'
    """
    results = []

    for i in interfaces:
        if status_contains and status_contains.lower() not in i["status"].lower():
            continue

        if protocol and i["protocol"].lower() != protocol.lower():
            continue

        if has_ip is True and i["ip_address"].lower() == "unassigned":
            continue

        if has_ip is False and i["ip_address"].lower() != "unassigned":
            continue

        results.append(i)

    return results

def main():
    # 1) Device info (pas dit aan naar jullie lab/sandbox!)
    device = {
        "device_type": "cisco_ios",
        "host": "192.168.56.101",
        "username": "admin",
        "password": "cisco",
        "secret": "cisco"
    }

    # 2) Connect + enable
    conn = ConnectHandler(**device)
    conn.enable()

    # 3) Show command
    cmd = "show ip interface brief"
    raw = conn.send_command(cmd)

    conn.disconnect()

    # 4) Parse naar JSON-achtige data
    interfaces = parse_show_ip_int_brief(raw)

    # 5) Opslaan als JSON (handig voor portfolio bewijs)
    with open("interfaces.json", "w", encoding="utf-8") as f:
        json.dump({"command": cmd, "interfaces": interfaces}, f, indent=2)

    # 6) Filter voorbeelden
    up_up = filter_interfaces(interfaces, status_contains="up", protocol="up")
    only_with_ip = filter_interfaces(interfaces, has_ip=True)

    # 7) Print resultaat (duidelijk)
    print("\n=== Alle interfaces (parsed) ===")
    for i in interfaces:
        print(f'{i["interface"]:20} {i["ip_address"]:15} {i["status"]:25} {i["protocol"]}')

    print("\n=== Filter: status bevat 'up' EN protocol = up ===")
    for i in up_up:
        print(f'{i["interface"]:20} {i["ip_address"]:15} {i["status"]:25} {i["protocol"]}')

    print("\n=== Filter: interfaces met een IP (niet unassigned) ===")
    for i in only_with_ip:
        print(f'{i["interface"]:20} {i["ip_address"]:15} {i["status"]:25} {i["protocol"]}')

if __name__ == "__main__":
    main()
