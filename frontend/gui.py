from flask import Flask, render_template, request
import webbrowser
import threading
import sys
import os

# --------------------------------------------------
# Importa o backend
# --------------------------------------------------
sys.path.append(
    os.path.join(
        os.path.dirname(__file__),
        '..'
    )
)

from backend.switch_automation import (
    conectar_switch,
    configure_vlans,
    configure_hostname
)


# --------------------------------------------------
# Inicialização do Flask
# --------------------------------------------------
app = Flask(__name__)


# --------------------------------------------------
# Página principal
# --------------------------------------------------
@app.route('/')
def index():
    return render_template('index.html')


# --------------------------------------------------
# Aplicar configuração
# --------------------------------------------------
@app.route('/aplicar', methods=['POST'])
def aplicar():

    # Recebe os dados enviados pelo formulário
    vlan10 = request.form['vlan10']
    vlan20 = request.form['vlan20']
    vlan50 = request.form['vlan50']
    hostname = request.form['hostname']

    # Lista de VLANs
    vlans = [
        {
            'id': vlan10,
            'name': 'VLAN_DADOS'
        },
        {
            'id': vlan20,
            'name': 'VLAN_VOZ'
        },
        {
            'id': vlan50,
            'name': 'VLAN_SEGURANCA'
        }
    ]

    connection = None

    try:

        # --------------------------------------------------
        # Dados de acesso ao switch
        # --------------------------------------------------
        print("[INFO] Iniciando conexão com o switch...")

        connection = conectar_switch(
            ip="192.168.1.10",
            usuario="admin",
            senha="cisco",
            secret="enablepass"
        )

        # --------------------------------------------------
        # Configuração das VLANs
        # --------------------------------------------------
        print("[INFO] Aplicando VLANs...")

        configure_vlans(
            connection,
            vlans
        )

        # --------------------------------------------------
        # Configuração do hostname
        # --------------------------------------------------
        print(
            f"[INFO] Configurando hostname: {hostname}"
        )

        configure_hostname(
            connection,
            hostname
        )

        # --------------------------------------------------
        # Resultado
        # --------------------------------------------------
        print(
            "[OK] Configuração aplicada com sucesso!"
        )

        return """
        <!DOCTYPE html>
        <html lang="pt-br">
        <head>
            <meta charset="UTF-8">
            <title>Sucesso</title>
        </head>

        <body>

            <h1>Configuração aplicada com sucesso!</h1>

            <p>
                O switch foi configurado corretamente.
            </p>

            <p>
                <strong>Hostname:</strong>
                SWITCH_AUTOMATIZADO
            </p>

            <p>
                <strong>VLAN 10:</strong>
                VLAN_DADOS
            </p>

            <p>
                <strong>VLAN 20:</strong>
                VLAN_VOZ
            </p>

            <p>
                <strong>VLAN 50:</strong>
                VLAN_SEGURANCA
            </p>

            <br>

            <a href="/">
                Voltar
            </a>

        </body>
        </html>
        """

    except Exception as e:

        # --------------------------------------------------
        # Tratamento de erro
        # --------------------------------------------------
        print(
            f"[ERRO] Falha ao aplicar configuração: {e}"
        )

        return f"""
        <!DOCTYPE html>
        <html lang="pt-br">
        <head>
            <meta charset="UTF-8">
            <title>Erro</title>
        </head>

        <body>

            <h1>Erro ao aplicar configuração</h1>

            <p>
                Não foi possível configurar o switch.
            </p>

            <pre>{e}</pre>

            <br>

            <a href="/">
                Voltar
            </a>

        </body>
        </html>
        """, 500

    finally:

        # --------------------------------------------------
        # Encerra conexão com o switch
        # --------------------------------------------------
        if connection:

            try:
                connection.disconnect()

                print(
                    "[INFO] Conexão com o switch encerrada."
                )

            except Exception as e:

                print(
                    f"[AVISO] Erro ao encerrar conexão: {e}"
                )


# --------------------------------------------------
# Abre o navegador automaticamente
# --------------------------------------------------
def abrir_navegador():

    webbrowser.open(
        "http://127.0.0.1:5000"
    )


# --------------------------------------------------
# Inicialização
# --------------------------------------------------
if __name__ == '__main__':

    print("")
    print("=" * 60)
    print("  SISTEMA DE AUTOMAÇÃO DE SWITCH")
    print("=" * 60)
    print("")
    print(
        "[INFO] Iniciando servidor Flask..."
    )
    print(
        "[INFO] Endereço: http://127.0.0.1:5000"
    )
    print("")

    # Abre o navegador após 1,5 segundos
    threading.Timer(
        1.5,
        abrir_navegador
    ).start()

    # Inicia o Flask
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,
        use_reloader=False
    )