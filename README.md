🚀 NGROK TUNNEL MANAGER v5
O Ngrok Tunnel Manager é uma ferramenta avançada de automação de infraestrutura de rede, projetada para gerenciar múltiplos túneis TCP de forma simultânea e inteligente. O sistema otimiza a operação de múltiplos tokens, implementando um sistema de varredura de portas e monitoramento de tráfego em tempo real.

🛠️ Especificações Técnicas
Gestão Multitoken: Suporte a múltiplos tokens de autenticação com distribuição automática de slots.
Monitoramento Ativo: Interface de alta performance baseada em Rich, fornecendo status de conexão e métricas de tráfego por slot.
Inteligência de Rede:
Filtro de Endpoints: Detecção de endpoints duplicados e histórico de conexões.
Blacklist Dinâmica: Sistema de exclusão de endpoints indesejados via teclado em tempo real.
Estabilidade: Sistema de auto-recuperação que detecta a queda de túneis e reinicia o processo de spawn automaticamente.
⌨️ Comandos de Operação
O software opera através de gatilhos de teclado para máxima agilidade:

Letras Minúsculas (a-z): Libera e reinicia o slot associado à letra.
Letras Maiúsculas (A-Z): Adiciona o endpoint atual à blacklist e reinicia o slot.
Tecla =: Pausa ou retoma a operação de todos os slots.
Tecla ESC: Encerra a aplicação e limpa todos os processos do Ngrok.
⚙️ Pré-requisitos
Para a execução do sistema, é necessário:

Python 3.x instalado.
Dependências:
pip install colorama rich
Copy
Ngrok Executável: O binário ngrok.exe deve estar localizado em: C:\ngrok-v3-stable-windows-amd64\.
🚀 Como Iniciar
Execute o script via terminal ou IDE.
O sistema informará a porta local atual e as próximas portas programadas.
Configure seu serviço para a porta indicada.
Acompanhe o status dos slots:
🟢 Online: Slot ativo e buscando conexão.
⚡ Conectado: Túnel estabelecido e operante.
🔴 Offline: Slot inativo.
Desenvolvido por T H E
