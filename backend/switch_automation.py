from netmiko import ConnectHandler
import datetime
import os
import sys

# -----------------------------
# Conexão com o Switch
# -----------------------------
def connect_switch(host, username, password, secret=None):
    device = {
        "device_type": "cisco_ios",
        "host": host,
        "username": username,
        "password": password,
        "secret": secret
    }

    try:
        connection = ConnectHandler(**device)
        if secret:
            connection.enable()
        print(f"[OK] Conectado ao switch {host}")
        return connection
    except Exception as e:
        print(f"[ERRO] Falha ao conectar ao switch {host}: {e}")
        sys.exit(1)

# -----------------------------
# Configuração de VLANs
# -----------------------------
def configure_vlans(connection, vlans):
    commands = []
    for vlan in vlans:
        commands.append(f"vlan {vlan['id']}")
        commands.append(f"name {vlan['name']}")

    print("[INFO] Aplicando configuração de VLANs...")
    connection.send_config_set(commands)

# -----------------------------
# Configuração de Hostname
# -----------------------------
def configure_hostname(connection, hostname="SWITCH_AUTOMATIZADO"):
    print(f"[INFO] Configurando hostname para {hostname}...")
    connection.send_config_set([f"hostname {hostname}"])

# -----------------------------
# Salvando Configuração
# -----------------------------
def save_config(connection):
    print("[INFO] Salvando configuração...")
    try:
        connection.save_config()
    except Exception:
        connection.send_command("write memory")

# -----------------------------
# Backup da Configuração
# -----------------------------
from ftplib import FTP
import os
import datetime

def backup_config(connection, hostname="SWITCH_AUTOMATIZADO", backup_dir="backups"):
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    print("[INFO] Realizando backup da configuração...")
    output = connection.send_command("show running-config")

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{hostname}_{timestamp}.txt"
    filepath = os.path.join(backup_dir, filename)

    # Salva o backup localmente
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(output)

    print(f"[OK] Backup salvo em: {filepath}")

    try:
        print("[INFO] Conectando ao servidor FTP 10.10.10.1...")
        ftp = FTP("10.10.10.1")
        ftp.login("administrador", "P@ssw0rd")

        with open(filepath, "rb") as file:
            ftp.storbinary(f"STOR {filename}", file)

        ftp.quit()
        print(f"[OK] Backup enviado para o servidor FTP: {filename}")

    except Exception as e:
        print(f"[ERRO] Falha ao enviar backup para o FTP: {e}")

    return filepath


# -----------------------------
# Validação de Hostname
# -----------------------------
def get_current_hostname(connection):
    output = connection.send_command("show running-config | include hostname")
    parts = output.strip().split()
    if len(parts) == 2:
        return parts[1]
    return None

# -----------------------------
# Validação de VLANs
# -----------------------------
def validate_vlans(connection, vlans):
    print("[INFO] Validando VLANs...")
    output = connection.send_command("show vlan brief")

    errors = []
    for vlan in vlans:
        vlan_id = str(vlan["id"])
        vlan_name = vlan["name"]

        if vlan_id not in output:
            errors.append(f"[ERRO] VLAN {vlan_id} não encontrada.")
        if vlan_name not in output:
            errors.append(f"[ERRO] Nome da VLAN {vlan_name} não encontrado.")

    return errors

# -----------------------------
# Validação Geral
# -----------------------------
def validate_config(connection, vlans, expected_hostname="SWITCH_AUTOMATIZADO"):
    print("[INFO] Validando configurações aplicadas...")
    alerts = []

    current_hostname = get_current_hostname(connection)
    if current_hostname != expected_hostname:
        alerts.append(
            f"[ERRO] Hostname atual ({current_hostname}) diferente do esperado ({expected_hostname})."
        )

    vlan_errors = validate_vlans(connection, vlans)
    alerts.extend(vlan_errors)

    return alerts

# -----------------------------
# Função Principal
# -----------------------------
def main():
    host = "192.168.1.10"
    username = "admin"
    password = "cisco"
    secret = "enablepass"

    vlans = [
        {"id": 10, "name": "VLAN_DADOS"},
        {"id": 20, "name": "VLAN_VOZ"},
        {"id": 50, "name": "VLAN_SEGURANCA"}
    ]

    connection = connect_switch(host, username, password, secret)

    configure_hostname(connection)
    configure_vlans(connection, vlans)
    save_config(connection)
    backup_config(connection)

    alerts = validate_config(connection, vlans)

    if alerts:
        print("\n[ALERTAS] Problemas encontrados:")
        for alert in alerts:
            print(alert)
    else:
        print("\n[OK] Todas as configurações foram validadas com sucesso!")

    connection.disconnect()
    print("[OK] Conexão encerrada.")

# Executa o script
if __name__ == "__main__":
    main()