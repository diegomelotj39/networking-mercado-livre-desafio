## Documentando o desafio de Automação proposto pela Mercado Livre ##

Este projeto implementa a automação de configuração de um switch Cisco utilizando Python, um frontend para entrada de dados (Tkinter, PyQt ou Flask) e bibliotecas de automação de rede (Netmiko, Paramiko ou Nornir).

Adicionalmente, o repositório público https://github.com/diegomelotj39/networking-mercado-livre-desafio contém um plano de automação para configuração de uma VPN IPSec entre firewalls Fortigate e Palo Alto.

## 1.0 Conectar no switch;
    ### 1.0.1 Conectar no switch fictício 192.168.1.10

## 1.1 Automatizar a configuração de switch Cisco;
    ### 1.1 Criar VLANs com IDs e names específicos;
        #### 1.1.1 VLAN ID 10, 20 e 50.
            ##### 1.1.1.1 Names "VLAN_DADOS", "VLAN_VOZ" e "VLAN_SEGURANÇA" respectivamente

### 1.2 Criar hostname;
    ### 1.2.1 hostname será "SWITCH_AUTOMATIZADO"

### 1.3 Salvar as configurações e gerar cópia de segurança 
    ### 1.3.1 Salvar a configuração na memória não volátio (NVRAM)
    ### 1.3.2 Gerar backup da running-config e enviar para servidor remoto

### 1.4 Validar as configurações
        1.4.1 Validar se foram alteradas as VLANs e hostname
        1.4.2 Exibir alertas no frontend
        1.4.3 Utilizar Git para versionamento

Instalação de LIBs

Deve-se instalar o netmiko (acesse o terminal do VS e digite "pip install netmiko")