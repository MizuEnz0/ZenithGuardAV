# Guia de Contribuição para ZenithGuardAV

Obrigado por considerar contribuir para o ZenithGuardAV! Este documento fornece diretrizes para contribuições.

## 🚀 Como Contribuir

### 1. Fork e Clone

1. Faça um fork do repositório
2. Clone seu fork:
```bash
git clone https://github.com/seu-usuario/ZenithGuardAV.git
cd ZenithGuardAV
```

### 2. Configurar Ambiente de Desenvolvimento

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
pip install -r requirements-dev.txt  # se existir
```

### 3. Criar Branch

```bash
git checkout -b feature/nova-funcionalidade
# ou
git checkout -b bugfix/correcao-bug
```

### 4. Fazer Mudanças

- Siga o estilo de código existente
- Adicione testes para novas funcionalidades
- Atualize a documentação conforme necessário
- Certifique-se de que todos os testes passam

### 5. Testes

```bash
# Executar testes
pytest

# Executar com cobertura
pytest --cov=.

# Verificar estilo de código
flake8 .

# Formatar código
black .
```

### 6. Commit

```bash
git add .
git commit -m "feat: adiciona nova funcionalidade de detecção"
```

**Convenção de Commits:**
- `feat:` nova funcionalidade
- `fix:` correção de bug
- `docs:` mudanças na documentação
- `style:` formatação, ponto e vírgula, etc.
- `refactor:` refatoração de código
- `test:` adição de testes
- `chore:` mudanças em ferramentas, configurações, etc.

### 7. Push e Pull Request

```bash
git push origin feature/nova-funcionalidade
```

Depois, abra um Pull Request no GitHub.

## 📋 Checklist para Pull Requests

- [ ] Código segue o estilo do projeto
- [ ] Testes foram adicionados/atualizados
- [ ] Documentação foi atualizada
- [ ] Todos os testes passam
- [ ] Não há conflitos de merge
- [ ] Commit messages seguem a convenção

## 🐛 Reportando Bugs

Use o template de issue para bugs:

1. **Descrição clara** do problema
2. **Passos para reproduzir**
3. **Comportamento esperado**
4. **Comportamento atual**
5. **Ambiente** (OS, Python version, etc.)
6. **Logs relevantes**

## 💡 Sugerindo Funcionalidades

Use o template de issue para funcionalidades:

1. **Descrição clara** da funcionalidade
2. **Justificativa** - por que seria útil?
3. **Casos de uso** específicos
4. **Considerações de implementação**

## 🏗️ Arquitetura do Projeto

### Estrutura Principal

```
ZenithGuardAV/
├── zenith_gui.py          # Interface gráfica
├── zenith_monitor.py      # Motor de monitoramento
├── zenith_rules.yar      # Regras YARA
├── config.json           # Configurações
├── whitelist.json        # Lista branca
└── quarantine/           # Quarentena
```

### Padrões de Código

- **Python 3.7+** obrigatório
- **PEP 8** para estilo de código
- **Docstrings** para funções públicas
- **Type hints** quando possível
- **Logging** para debug e monitoramento

### Testes

- **Unit tests** para funções individuais
- **Integration tests** para fluxos completos
- **Mocking** para dependências externas
- **Coverage** mínimo de 80%

## 🔒 Segurança

- **NUNCA** commite credenciais ou chaves
- **SEMPRE** valide entrada do usuário
- **CUIDADO** com operações de sistema
- **TESTE** em ambiente isolado

## 📚 Documentação

- Atualize o README.md para mudanças significativas
- Adicione docstrings para novas funções
- Documente APIs públicas
- Mantenha exemplos atualizados

## 🎯 Roadmap

### Próximas Funcionalidades

- [ ] Suporte a mais sistemas operacionais
- [ ] Interface web
- [ ] API REST
- [ ] Machine Learning para detecção
- [ ] Integração com SIEM
- [ ] Relatórios avançados

### Melhorias Técnicas

- [ ] Performance otimizada
- [ ] Testes automatizados
- [ ] CI/CD pipeline
- [ ] Containerização
- [ ] Monitoramento de saúde

## 🤝 Código de Conduta

### Nossos Compromissos

- Ambiente acolhedor e inclusivo
- Respeito mútuo
- Foco no que é melhor para a comunidade
- Aceitação de críticas construtivas

### Comportamento Esperado

- Linguagem inclusiva
- Respeito a diferentes pontos de vista
- Aceitação de feedback
- Foco na colaboração

### Comportamento Inaceitável

- Linguagem ou imagens sexualizadas
- Trolling, insultos ou comentários depreciativos
- Assédio público ou privado
- Publicação de informações privadas

## 📞 Contato

- **Issues**: Use o sistema de issues do GitHub
- **Discussões**: Use as GitHub Discussions
- **Email**: zenithguardav@example.com

## 📄 Licença

Contribuindo, você concorda que suas contribuições serão licenciadas sob a mesma licença MIT do projeto.

---

**Obrigado por contribuir para o ZenithGuardAV!** 🛡️