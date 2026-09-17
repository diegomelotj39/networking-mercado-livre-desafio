## Documentando o desafio de Automação proposto pela Mercado Livre ##

Este projeto implementa a automação de configuração de um switch Cisco utilizando Python, um frontend para entrada de dados (Tkinter, PyQt ou Flask) e as bibliotecas para automação de rede (Netmiko, Paramiko ou Nornir).

Adicionalmente, o repositório público https://github.com/diegomelotj39/networking-mercado-livre-desafio contém um plano de automação para configuração de uma VPN IPSec entre firewalls Fortigate e Palo Alto.

Também traz informações sobre como interagir com o frontend ## 2.0

## 1.0 Instalar LIBs & Automatizar tarefas via Python;
    ### 1.0.1 Instale as dependências netmiko, paramiko e flask.

## 1.1 Conectar no switch;
    ### 1.1.1 Conectar no switch fictício 192.168.1.10

## 1.2 Automatizar a configuração do switch;
    ### 1.2.1 Criar VLANs com IDs e names específicos;
        #### 1.2.1.1 VLAN ID 10, 20 e 50.
            ##### 1.2.1.2 Names "VLAN_DADOS", "VLAN_VOZ" e "VLAN_SEGURANÇA" respectivamente

### 1.3 Criar hostname;
    ### 1.3.1 hostname será "SWITCH_AUTOMATIZADO"

### 1.4 Salvar as configurações e gerar cópia de segurança;
    ### 1.4.1 Salvar a configuração na memória não volátio (NVRAM)
    ### 1.4.2 Gerar backup da running-config e enviar para servidor remoto

### 1.5 Validar as configurações;
        1.5.1 Validar se foram alteradas as VLANs e hostname
        1.5.2 Exibir alertas no frontend
        1.5.3 Utilizar Git para versionamento

### 2.0 Interagindo com o FrontEnd