# ZenithGuardAV

Um sistema avançado de detecção e proteção contra malware desenvolvido em Python, com interface gráfica intuitiva e capacidades de monitoramento em tempo real.

## 🛡️ Características

- **Monitoramento em Tempo Real**: Vigilância contínua de diretórios críticos do sistema
- **Detecção YARA**: Análise de arquivos usando regras YARA personalizadas
- **Sistema de Honeypots**: Armadilhas para detectar tentativas de acesso malicioso
- **Quarentena Automática**: Isolamento seguro de arquivos suspeitos
- **Interface Gráfica**: GUI intuitiva para gerenciamento e configuração
- **Whitelist Inteligente**: Sistema de lista branca para arquivos confiáveis
- **Logs Detalhados**: Registro completo de atividades e detecções

## 🚀 Instalação

### Pré-requisitos

- Python 3.7 ou superior
- Windows 10/11 (recomendado)
- Permissões de administrador (para funcionalidades avançadas)

### Dependências

```bash
pip install -r requirements.txt
```

### Instalação Manual

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/ZenithGuardAV.git
cd ZenithGuardAV
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute o programa:
```bash
python zenith_gui.py
```

## 📋 Uso

### Interface Gráfica

Execute o programa principal:
```bash
python zenith_gui.py
```

### Linha de Comando

Para monitoramento em background:
```bash
python zenith_monitor.py
```

## ⚙️ Configuração

### Arquivo de Configuração (`config.json`)

```json
{
  "monitor_paths": [
    "C:\\Users\\UsuarioADM/Documents",
    "C:\\Users\\UsuarioADM/Downloads",
    "C:/Users",
    "C:/Temp"
  ]
}
```

### Regras YARA (`zenith_rules.yar`)

O arquivo contém regras personalizadas para detecção de malware. Você pode adicionar suas próprias regras seguindo a sintaxe YARA.

### Whitelist (`whitelist.json`)

Arquivo para definir arquivos e processos confiáveis que devem ser ignorados pelo sistema.

## 📁 Estrutura do Projeto

```
ZenithGuardAV/
├── zenith_gui.py          # Interface gráfica principal
├── zenith_monitor.py      # Motor de monitoramento
├── zenith_rules.yar      # Regras de detecção YARA
├── config.json           # Configurações do sistema
├── whitelist.json        # Lista de arquivos confiáveis
├── baseline.json         # Baseline do sistema
├── honeypots/            # Diretório de honeypots
├── quarantine/           # Diretório de quarentena
├── icons/               # Ícones da interface
└── zenithguard.log      # Arquivo de log
```

## 🔧 Funcionalidades Avançadas

### Sistema de Honeypots

O ZenithGuardAV cria arquivos "isca" em locais estratégicos para detectar tentativas de acesso malicioso.

### Quarentena

Arquivos suspeitos são automaticamente movidos para o diretório de quarentena, onde podem ser analisados ou restaurados.

### Monitoramento de Processos

Capacidade de monitorar e interromper processos suspeitos em tempo real.

## 📊 Logs e Monitoramento

Todos os eventos são registrados no arquivo `zenithguard.log`, incluindo:
- Detecções de malware
- Tentativas de acesso a honeypots
- Ações de quarentena
- Erros do sistema

## 🛠️ Desenvolvimento

### Adicionando Novas Regras YARA

1. Edite o arquivo `zenith_rules.yar`
2. Adicione suas regras seguindo a sintaxe YARA
3. Reinicie o monitor para aplicar as mudanças

### Personalizando a Interface

A interface gráfica está em `zenith_gui.py` e pode ser customizada conforme necessário.

## ⚠️ Avisos Importantes

- Este software é para fins educacionais e de pesquisa
- Sempre faça backup de seus dados antes de usar
- O sistema requer permissões de administrador para funcionar completamente
- Teste em ambiente controlado antes de usar em produção

## 🤝 Contribuição

Contribuições são bem-vindas! Por favor:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 📞 Suporte

Para suporte e dúvidas:
- Abra uma issue no GitHub
- Consulte a documentação
- Verifique os logs para diagnóstico

## 🔄 Histórico de Versões

- **v1.0.0** - Versão inicial com funcionalidades básicas
- Interface gráfica completa
- Sistema de monitoramento em tempo real
- Detecção YARA
- Sistema de honeypots
- Quarentena automática

---

**ZenithGuardAV** - Proteção Avançada Contra Malware