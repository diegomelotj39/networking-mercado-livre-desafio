import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import tkinter as tk
from tkinter import messagebox

from backend.switch_automation import (
    connect_switch,
    configure_vlans,
    configure_hostname,
    save_config,
    backup_config,
    validate_config
)

# -----------------------------
# Função principal de aplicação
# -----------------------------
def aplicar_configuracoes():
    try:
        # Coleta das VLANs inseridas pelo usuário
        vlans = []

        try:
            vlans.append({"id": int(vlan1_id.get()), "name": vlan1_name.get()})
            vlans.append({"id": int(vlan2_id.get()), "name": vlan2_name.get()})
            vlans.append({"id": int(vlan3_id.get()), "name": vlan3_name.get()})
        except ValueError:
            messagebox.showerror("Erro", "IDs das VLANs devem ser números inteiros.")
            return

        hostname = hostname_entry.get()

        # Conectar ao switch
        conn = connect_switch("192.168.1.10", "admin", "cisco123")

        # Aplicar configurações
        configure_vlans(conn, vlans)
        configure_hostname(conn, hostname)
        save_config(conn)

        # Backup
        backup_config(conn, hostname)

        # Validação
        alerts = validate_config(conn, vlans, hostname)

        if alerts:
            messagebox.showwarning("Alertas encontrados", "\n".join(alerts))
        else:
            messagebox.showinfo("Sucesso", "Configuração aplicada sem divergências!")

        conn.disconnect()

    except Exception as e:
        messagebox.showerror("Erro", str(e))


# -----------------------------
# Interface Tkinter
# -----------------------------
root = tk.Tk()
root.title("Automação de Switch Cisco")
root.geometry("450x450")

tk.Label