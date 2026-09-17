import re

# -----------------------------
# EXTRAÇÃO DE CONFIG FORTIGATE
# -----------------------------
def parse_fortigate(config):
    data = {}

    # Phase 1
    data["peer"] = re.search(r"set remote-gw (\S+)", config).group(1)
    data["psk"] = re.search(r"set psksecret \"(.+?)\"", config).group(1)
    data["ike_proposal"] = re.search(r"set proposal (\S+)", config).group(1)
    data["ike_dh"] = re.search(r"set dhgrp (\d+)", config).group(1)

    # Phase 2
    data["ipsec_proposal"] = re.search(r"set proposal (\S+)", config).group(1)
    data["ipsec_dh"] = re.search(r"set dhgrp (\d+)", config).group(1)
    data["pfs"] = "enable" in config

    data["src_subnet"] = re.search(r"set src-subnet (\S+ \S+)", config).group(1)
    data["dst_subnet"] = re.search(r"set dst-subnet (\S+ \S+)", config).group(1)

    # Tunnel interface
    tun_ip = re.search(r"set ip (\S+) (\S+)", config)
    data["tun_ip"] = tun_ip.group(1)
    data["tun_mask"] = tun_ip.group(2)

    remote_ip = re.search(r"set remote-ip (\S+)", config)
    data["tun_remote"] = remote_ip.group(1)

    return data


# -----------------------------
# EXTRAÇÃO DE CONFIG PALO ALTO
# -----------------------------
def parse_paloalto(config):
    data = {}

    # Phase 1
    data["peer"] = re.search(r"gateway .* address (\S+)", config).group(1)
    data["psk"] = re.search(r"pre-shared-key \"(.+?)\"", config).group(1)
    data["ike_proposal"] = re.search(r"proposal (\S+)", config).group(1)
    data["ike_dh"] = re.search(r"dh-group (\S+)", config).group(1)

    # Phase 2
    data["ipsec_proposal"] = re.search(r"ipsec-crypto-profile (\S+)", config).group(1)
    data["pfs"] = "group14" in config or "pfs" in config

    # Proxy IDs
    local = re.search(r"proxy-id .* remote (\S+)", config)
    remote = re.findall(r"proxy-id .* remote (\S+)", config)

    data["src_subnet"] = remote[0]
    data["dst_subnet"] = remote[1]

    # Tunnel interface
    tun_ip = re.search(r"interface tunnel\.1 ip (\S+)", config)
    data["tun_ip"] = tun_ip.group(1)
    data["tun_mask"] = "255.255.255.252"  # /30 fixo
    data["tun_remote"] = None  # Palo Alto não define remote-ip

    return data


# -----------------------------
# COMPARAÇÃO
# -----------------------------
def compare_configs(fgt, pa):
    results = []

    def check(label, a, b):
        if a == b:
            results.append(f"✔ {label}: OK ({a})")
        else:
            results.append(f"❌ {label}: Fortigate={a} | Palo Alto={b}")

    check("Peer IP", fgt["peer"], pa["peer"])
    check("PSK", fgt["psk"], pa["psk"])
    check("IKE Proposal", fgt["ike_proposal"], pa["ike_proposal"])
    check("IKE DH Group", fgt["ike_dh"], pa["ike_dh"])
    check("IPSec Proposal", fgt["ipsec_proposal"], pa["ipsec_proposal"])
    check("PFS", fgt["pfs"], pa["pfs"])
    check("SRC Subnet", fgt["src_subnet"], pa["src_subnet"])
    check("DST Subnet", fgt["dst_subnet"], pa["dst_subnet"])
    check("Tunnel IP", fgt["tun_ip"], pa["tun_ip"])

    return results


# -----------------------------
# VALIDAÇÃO FINAL
# -----------------------------
def validate_vpn(fgt_config, pa_config):
    fgt = parse_fortigate(fgt_config)
    pa = parse_paloalto(pa_config)

    comparison = compare_configs(fgt, pa)

    print("\n=== RESULTADO DA COMPARAÇÃO ===\n")
    for item in comparison:
        print(item)

    # Veredito
    errors = [x for x in comparison if x.startswith("❌")]

    print("\n=== VEREDITO FINAL ===")
    if errors:
        print("❌ A VPN NÃO VAI SUBIR.")
        print("Motivos:")
        for e in errors:
            print(" - " + e)
    else:
        print("✔ A VPN VAI SUBIR SEM PROBLEMAS.")


# -----------------------------
# EXEMPLO DE USO
# -----------------------------
if __name__ == "__main__":
    with open("fortigate.txt") as f:
        fgt_config = f.read()

    with open("paloalto.txt") as f:
        pa_config = f.read()

    validate_vpn(fgt_config, pa_config)