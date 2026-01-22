from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoAuthenticationException, NetmikoTimeoutException

device = {
    "device_type": "cisco_ios",
    "host": "sandbox-iosxe-latest-1.cisco.com",
    # VUL HIER JOUW JUISTE CREDS IN (van DevNet Sandbox / Quick Access)
    "username": "admin",
    "password": "C1sco12345",
    "secret": "C1sco12345",
    "port": 22,

    # Extra stabiliteit
    "banner_timeout": 60,
    "auth_timeout": 30,
    "conn_timeout": 30,
    "fast_cli": False,
}

# Config die we gaan pushen (veilig)
config_commands = [
    "hostname MAROUANE-N2",
    "banner motd ^AUTHORIZED ACCESS ONLY^",
    "interface Loopback123",
    " description Netmiko N2 test",
    " ip address 10.123.123.123 255.255.255.255",
    " no shutdown",
    "exit",
]

show_verification = [
    "show run | include hostname",
    "show run | include banner motd",
    "show ip interface brief | include Loopback123",
    "show run interface Loopback123",
]

try:
    print("Verbinden met device...")
    conn = ConnectHandler(**device)

    # Enable mode (privileged EXEC)
    conn.enable()
    print("Succesvol verbonden + enable mode!\n")

    print("CONFIG PUSHEN...")
    output = conn.send_config_set(config_commands)
    print(output)
    print("\nCONFIG GEDAAN.\n")

    # (Optioneel) config opslaan
    # Bij sommige sandboxes heeft dit geen nut of is het beperkt, maar dit is wel “correct” in N2:
    print("CONFIG OPSLAAN (write memory)...")
    save_out = conn.save_config()
    print(save_out)
    print()

    print("VERIFICATIE (show commands):")
    for cmd in show_verification:
        print("=" * 70)
        print(f"SHOW: {cmd}")
        print("=" * 70)
        print(conn.send_command(cmd))
        print()

    conn.disconnect()
    print("Verbinding gesloten.")

except NetmikoAuthenticationException:
    print("AUTH ERROR: username/password/secret klopt niet voor dit device.")
    print("Tip: haal de credentials uit DevNet Sandbox 'Quick Access / Credentials'.")

except NetmikoTimeoutException:
    print("TIMEOUT: device onbereikbaar via netwerk/poort 22.")
    print("Tip: Test-NetConnection <host> -Port 22")

except Exception as e:
    print(f"Onverwachte fout: {e}")
