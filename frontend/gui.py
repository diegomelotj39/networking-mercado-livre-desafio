from flask import Flask, render_template, request
import webbrowser
import threading
import sys
import os

# Permite importar o backend sem alterar estrutura
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from backend.switch_automation import configure_vlans, configure_hostname

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/aplicar', methods=['POST'])
def aplicar():
    vlan10 = request.form['vlan10']
    vlan20 = request.form['vlan20']
    vlan50 = request.form['vlan50']
    hostname = request.form['hostname']

    connection = None

    vlans = [
        {'id': vlan10, 'name': 'VLAN_DADOS'},
        {'id': vlan20, 'name': 'VLAN_VOZ'},
        {'id': vlan50, 'name': 'VLAN_SEGURANCA'}
    ]

    configure_vlans(connection, vlans)
    configure_hostname(connection, hostname)

    return "Configuração aplicada com sucesso!"

def abrir_navegador():
    webbrowser.open("http://127.0.0.1:5000")

if __name__ == '__main__':
    threading.Timer(1.5, abrir_navegador).start()
    app.run(debug=True)