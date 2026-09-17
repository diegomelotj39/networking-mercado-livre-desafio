from netmiko import ConnectHandler
import datetime
import os
import sys
from ftplib import FTP


# -----------------------------
# Conexão com o Switch
# -----------------------------
def conectar_switch(
    ip="192.168.1.200",
    usuario="administrador",
    senha="P@ssw0rd",
    secret=None,
    porta_ssh=22,
    tipo_dispositivo="cisco_ios"
):
    device = {
        "device_type": tipo_dispositivo,
        "host": ip,
        "username": usuario,
        "password": senha,
        "port": porta_ssh,
    }

    if secret:
        device["secret"] = secret

    try:
        print(f"[INFO] Conectando ao switch {ip} via SSH...")

        connection = ConnectHandler(**device)

        if secret:
            connection.enable()

        print("[OK] Conexão estabelecida com sucesso!")

        return connection

    except Exception as e:
        print(f"[ERROR] Falha ao conectar ao switch {ip}: {e}")
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

    print("[OK] VLANs configuradas com sucesso!")


# -----------------------------
# Configuração de Hostname
# -----------------------------
def configure_hostname(
    connection,
    hostname="SWITCH_AUTOMATIZADO"
):
    print(f"[INFO] Configurando hostname para {hostname}...")

    connection.send_config_set(
        [f"hostname {hostname}"]
    )

    print("[OK] Hostname configurado!")


# -----------------------------
# Salvando Configuração
# -----------------------------
def save_config(connection):
    print("[INFO] Salvando configuração...")

    try:
        connection.save_config()
        print("[OK] Configuração salva!")

    except Exception:
        connection.send_command("write memory")
        print("[OK] Configuração salva com write memory!")


# -----------------------------
# Backup da Configuração
# -----------------------------
def backup_config(
    connection,
    hostname="SWITCH_AUTOMATIZADO",
    backup_dir="backups"
):

    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    print("[INFO] Realizando backup da configuração...")

    output = connection.send_command(
        "show running-config"
    )

    timestamp = datetime.datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    filename = f"{hostname}_{timestamp}.txt"

    filepath = os.path.join(
        backup_dir,
        filename
    )

    with open(
        filepath,
        "w",
        encoding="utf-8"
    ) as f:
        f.write(output)

    print(f"[OK] Backup salvo em: {filepath}")

    try:
        print(
            "[INFO] Conectando ao servidor FTP 10.10.10.1..."
        )

        ftp = FTP("10.10.10.1")

        ftp.login(
            "administrador",
            "P@ssw0rd"
        )

        with open(filepath, "rb") as file:
            ftp.storbinary(
                f"STOR {filename}",
                file
            )

        ftp.quit()

        print(
            f"[OK] Backup enviado para o servidor FTP: {filename}"
        )

    except Exception as e:
        print(
            f"[ERRO] Falha ao enviar backup para o FTP: {e}"
        )

    return filepath


# -----------------------------
# Validação de Hostname
# -----------------------------
def get_current_hostname(connection):

    output = connection.send_command(
        "show running-config | include hostname"
    )

    parts = output.strip().split()

    if len(parts) == 2:
        return parts[1]

    return None


# -----------------------------
# Validação de VLANs
# -----------------------------
def validate_vlans(connection, vlans):

    print("[INFO] Validando VLANs...")

    output = connection.send_command(
        "show vlan brief"
    )

    errors = []

    for vlan in vlans:

        vlan_id = str(vlan["id"])
        vlan_name = vlan["name"]

        if vlan_id not in output:
            errors.append(
                f"[ERRO] VLAN {vlan_id} não encontrada."
            )

        if vlan_name not in output:
            errors.append(
                f"[ERRO] Nome da VLAN {vlan_name} não encontrado."
            )

    return errors


# -----------------------------
# Validação Geral
# -----------------------------
def validate_config(
    connection,
    vlans,
    expected_hostname="SWITCH_AUTOMATIZADO"
):

    print("[INFO] Validando configurações aplicadas...")

    alerts = []

    current_hostname = get_current_hostname(
        connection
    )

    if current_hostname != expected_hostname:

        alerts.append(
            f"[ERRO] Hostname atual "
            f"({current_hostname}) "
            f"diferente do esperado "
            f"({expected_hostname})."
        )

    vlan_errors = validate_vlans(
        connection,
        vlans
    )

    alerts.extend(vlan_errors)

    return alerts