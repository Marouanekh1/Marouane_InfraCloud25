from netmiko import ConnectHandler

device = {
    "device_type": "cisco_ios",
    "host": "sandbox-iosxe-latest-1.cisco.com",
    "username": "admin",
    "password": "C1sco12345",
    "secret": "C1sco12345",
    "port": 22,
}

print("Verbinden met device...")

connection = ConnectHandler(**device)

print("Succesvol verbonden!\n")

commands = [
    "show version",
    "show ip interface brief",
    "show running-config | section interface",
]

for cmd in commands:
    print("=" * 60)
    print(f"COMMAND: {cmd}")
    print("=" * 60)
    output = connection.send_command(cmd)
    print(output)
    print()

connection.disconnect()
print("Verbinding gesloten.")
