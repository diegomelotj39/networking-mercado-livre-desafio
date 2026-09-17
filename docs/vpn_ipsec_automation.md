# Plano de Automação da VPN IPSec entre Fortigate e Palo Alto

Este documento atende aos requisitos da Parte 2 do *Desafio de Automação Redes enviada pelo Mercado Livre*, descrevendo o plano para automatizar a configuração de uma VPN IPSec entre um dispositivo Fortigate e um firewall Palo Alto.

## 1. Definição de Parâmetros da VPN IPSec

### 1.1 Endereços IP WAN

- Fortigate (WAN): 200.200.200.1
- Palo Alto (WAN): 201.201.201.1

### 1.2 Redes locais

- Rede local Fortigate: 10.10.10.0/24
- Rede local Palo Alto: 10.20.20.0/24

### 1.3 Rede de túnel (link IPsec)

- Rede de túnel: 169.255.1.0/30
- IP do Fortigate no túnel: 169.255.1.1
- IP do Palo Alto no túnel: 169.255.1.2

### 1.4  Phase 1 (IKE)

- Modo: Main
- Autenticação: Pre-Shared Key
- Algoritmo de criptografia: AES-256
- Algoritmo de integridade: SHA256
- Grupo DH: 14
- Tempo de vida: 28800 segundos

### 1.5 Phase 2 (IPSec)

- Protocolo: ESP
- Algoritmo de criptografia: AES-256
- Algoritmo de integridade: SHA256
- PFS: grupo 14
- Tempo de vida: 3600 segundos
- Seletores de tráfego:
  - Origem: 10.10.10.0/24
  - Destino: 10.20.20.0/24
## 2. Ferramentas e APIs para Automação

### 2.1 Fortigate

- **API REST Fortinet**:
  - Utilizada para criar objetos de endereço, políticas, interfaces de túnel e configurações de IPSec.
  - Autenticação via token ou usuário/senha.
- **SSH (Netmiko/Paramiko)**:
  - Alternativa para enviar comandos CLI diretamente.
- **Ferramentas de gerenciamento centralizado**:
  - FortiManager (opcional, caso exista no ambiente).

### 2.2 Palo Alto

- **API REST Palo Alto (XML/REST)**:
  - Utilizada para criar objetos de endereço, regras de segurança, interfaces de túnel e configurações de IPSec.
  - Autenticação via API Key.
- **SSH (Netmiko/Paramiko)**:
  - Alternativa para enviar comandos CLI diretamente.
- **Ferramentas de gerenciamento centralizado**:
  - Panorama (opcional, caso exista no ambiente).

### 2.3 Linguagem e bibliotecas de automação

- Linguagem programação principal: Python
- Bibliotecas sugeridas:
  - `requests` para chamadas HTTP/HTTPS às APIs REST
  - `netmiko` para acesso SSH automatizado
  - `json` e `xml` para manipulação de payloads de API
  
## 3. Passos Lógicos da Automação da VPN IPSec

### 3.1 Passos gerais

1. Receber parâmetros de entrada (IPs WAN, redes locais, rede de túnel, propostas de Phase 1 e Phase 2).
2. Validar os parâmetros (formato de IP, máscaras, ranges).
3. Conectar ao Fortigate (API REST ou SSH).
4. Conectar ao Palo Alto (API REST ou SSH).
5. Aplicar configurações no Fortigate.
6. Aplicar configurações no Palo Alto.
7. Validar estado da VPN em ambos os lados.
8. Gerar logs e alertas em caso de falhas.

### 3.2 Passos específicos no Fortigate

1. Criar objetos de endereço para:
   - Rede local Fortigate (`10.10.10.0/24`)
   - Rede remota Palo Alto (`10.20.20.0/24`)
2. Criar interface de túnel IPSec com IP `169.255.1.1`.
3. Configurar Phase 1 (IKE) com os parâmetros definidos.
4. Configurar Phase 2 (IPSec) com seletores de tráfego.
5. Criar política de firewall permitindo tráfego entre rede local e rede remota via túnel.
6. Habilitar a VPN e aplicar configurações.

### 3.3 Passos específicos no Palo Alto

1. Criar objetos de endereço para:
   - Rede local Palo Alto (`10.20.20.0/24`)
   - Rede remota Fortigate (`10.10.10.0/24`)
2. Criar interface de túnel IPSec com IP `169.255.1.2`.
3. Configurar IKE Gateway (Phase 1) com os mesmos parâmetros.
4. Configurar IPSec Tunnel (Phase 2) com seletores de tráfego.
5. Criar regras de segurança permitindo tráfego entre as redes locais via túnel.
6. Habilitar a VPN e aplicar configurações.
## 4. Considerações Específicas e Desafios

1. **Diferenças de terminologia**:
   - Fortigate usa termos como *Phase 1*, *Phase 2*, *Policy*.
   - Palo Alto usa *IKE Gateway*, *IPSec Tunnel*, *Security Policy*.
2. **Diferenças de API**:
   - Fortigate: endpoints REST específicos, autenticação via token.
   - Palo Alto: API baseada em XML/REST com API Key.
3. **Ordem de aplicação**:
   - Em alguns dispositivos, é necessário criar objetos antes de políticas.
4. **Sincronização de parâmetros**:
   - Qualquer divergência em criptografia, integridade, PFS ou seletores de tráfego impede a formação do túnel.
5. **Ambiente heterogêneo**:
   - Logs e mensagens de erro são diferentes em cada fabricante, exigindo tratamento específico no script.
## 5. Estratégia de Validação da Configuração e Alertas

### 5.1 Validação no Fortigate

- Verificar estado da VPN:
  - Comando CLI: `get vpn ipsec tunnel summary`
  - Ou endpoint de API que retorna o status dos túneis.
- Verificar se o túnel está **UP**.
- Verificar contadores de tráfego (bytes enviados/recebidos).
- Verificar se as políticas de firewall estão permitindo tráfego entre as redes.

### 5.2 Validação no Palo Alto

- Verificar estado da VPN:
  - Comando CLI: `show vpn ipsec-sa`
  - Ou chamada à API para obter o status das SAs.
- Verificar se o túnel está **UP**.
- Verificar contadores de tráfego.
- Verificar se as regras de segurança estão permitindo tráfego entre as redes.

### 5.3 Geração de alertas

- Em caso de falha na formação do túnel:
  - Registrar log detalhado (lado Fortigate e lado Palo Alto).
  - Gerar alerta no sistema de automação (ex.: saída em console, frontend, arquivo de log).
- Em caso de divergência de parâmetros:
  - Listar quais parâmetros estão diferentes (ex.: criptografia, PFS, seletores).
- Em caso de ausência de tráfego:
  - Alertar que o túnel está UP, mas sem tráfego, sugerindo teste de conectividade.

## 6. Arquivos de Configuração de Exemplo 

- `docs/fortigate_example_config.txt`
- `docs/paloalto_example_config.txt`

