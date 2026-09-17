## Documentando o desafio de Automação proposto pela Mercado Livre ##

Este projeto implementa a automação de configuração de um switch Cisco utilizando Python, um frontend para entrada de dados (Tkinter, PyQt ou Flask) e as bibliotecas para automação de rede (Netmiko, Paramiko ou Nornir).

Adicionalmente, o repositório público https://github.com/diegomelotj39/networking-mercado-livre-desafio contém um plano de automação para configuração de uma VPN IPSec entre firewalls Fortigate e Palo Alto.

Também traz informações sobre como interagir com o frontend ## 2.0

## 1.0 Instalar LIBs & Automatizar tarefas via Python;
    ### 1.0.1 Instalar as dependências netmiko, paramiko e flask;
    ### 1.1.1 Conectar no switch fictício 192.168.1.10;
    ### 1.2.1 Criar VLANs com IDs e names específicos;
        #### 1.2.1.1 VLAN ID 10, 20 e 50.
            ##### 1.2.1.2 Names "VLAN_DADOS", "VLAN_VOZ" e "VLAN_SEGURANÇA" respectivamente;
    ### 1.3.1 O hostname será "SWITCH_AUTOMATIZADO";
    ### 1.4.1 Salvar a configuração na memória não volátio (NVRAM);
    ### 1.4.2 Gerar backup da running-config e enviar para servidor remoto;
    ### 1.5.1 Validar se foram alteradas as VLANs e hostname;
    ### 1.5.2 Exibir alertas no frontend;
    ### 1.5.3 Utilizar Git para versionamento;

## 2.0 Interagindo com o FrontEnd
    ### 2.0.1 Administrador deve abrir o frontend
    ### 2.0.2 Inserir:
        #### ID da VLAN
        #### Nome da VLAN
        #### Hostname do switch

    ### 2.0.3 O script vai:
        #### Conectar no switch via SSH
        #### Alterar as VLANs existentes no switch
        #### Alterar o hostname conforme necessidade
        #### Salvar as configurações (wr)
        #### Realizar o backup (show run)
        #### Validar se as VLANs e hostname estão corretos
        #### Exibir alertas caso haja divergências.

## 3.0 Evidências
    ### 3.0.1 Não possuo licença para usar imagens dos vendor a nível pessoal e por isso não foi possivel fazer uso de simuladores GNS3 ou EVE-NG para executar a tarefa, uma vez que não é permitido por lei o uso de imagens fora do appliance dedicado do fabricante ou em ambiente que não esteja licenciado (VIRL/CML). 
    
    A licença custa U$199 (equivalente a R$1.000) e no momento não há recursos financeiros reservados para este fim. O Cisco packet tracert não possui os recursos técnicos necessários (não que eu tenha conseguido) para atingir o alvo desejado.

    Em meus estudos pessoais faço uso do devnet cisco modem labs, mas este está em período de manutenção pela cisco
