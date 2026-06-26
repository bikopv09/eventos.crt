# 📅 Eventos.CRT - Sistema de Gestão de Eventos

App de Gestão de Eventos do CRT-ES (protótipo) desenvolvido com **Streamlit**.

Um sistema completo para criação, gerenciamento e inscrição em eventos, com suporte a diferentes modalidades e painel administrativo.

---

## 🎯 Funcionalidades

### 1️⃣ **Criar Evento (Gestão)**
- ✅ Criar novos eventos com nome, descrição e data/horário
- ✅ Definir modalidade (CRT-ES na Escola, Sistema CFT/CRTs, Público Geral)
- ✅ Upload de imagem de capa
- ✅ Adicionar link de vídeo de divulgação

### 2️⃣ **Portal de Inscrições (Público)**
- ✅ Visualizar eventos disponíveis
- ✅ Preencher formulário com validação de campos obrigatórios
- ✅ Campos específicos conforme a modalidade do evento
- ✅ Modo organizador integrado para moderação rápida
- ✅ Visualização de mídias (imagem e vídeo)

### 3️⃣ **Painel do Organizador (Controle)**
- ✅ Lista completa de inscritos por evento
- ✅ Editar informações do evento
- ✅ Remover inscrições
- ✅ Deletar evento completo (com confirmação)

---

## 🛠️ Requisitos

- Python 3.8+
- Streamlit >= 1.28.0

---

## 📦 Instalação

1. **Clone o repositório:**
```bash
git clone https://github.com/bikopv09/eventos.crt.git
cd eventos.crt
```

2. **Crie um ambiente virtual (recomendado):**
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

3. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

---

## 🚀 Como Executar

```bash
streamlit run eventoscrt.py
```

A aplicação abrirá automaticamente em seu navegador no endereço `http://localhost:8501`

---

## 📋 Estrutura do Projeto

```
eventos.crt/
├── eventoscrt.py          # Arquivo principal da aplicação
├── requirements.txt       # Dependências Python
├── .gitignore            # Arquivos ignorados pelo Git
└── README.md             # Este arquivo
```

---

## 🔑 Campos do Formulário

### Campos Obrigatórios (Global)
- Nome Completo
- CPF
- E-mail
- Telefone / Celular com DDD
- Idade
- Autorização de uso de imagem (checkbox)

### Campos Específicos por Modalidade

#### 🏫 CRT-ES na Escola
- Nome da escola técnica
- Curso técnico
- Cidade
- Ano de conclusão
- Situação profissional
- Expectativas após formação
- Interesse em contato para registro profissional

#### 🏢 Sistema CFT/CRTs
- Local do SISTEMA CFT/CRTs
- Confirmação de presença

#### 👥 Público Geral
- Profissão
- Empresa/Escola

---

## 💾 Armazenamento de Dados

Atualmente, os dados são armazenados **em memória** durante a sessão usando `st.session_state`. Isso significa que:

⚠️ **Os dados são perdidos quando a aplicação é reiniciada**

Para um ambiente de produção, considere:
- Integrar um banco de dados (SQLite, PostgreSQL, etc.)
- Exportar dados para CSV/Excel
- Usar a API do Streamlit Community Cloud

---

## 🎨 Interface

- **Design responsivo** com layout em colunas
- **Ícones e emojis** para melhor UX
- **Validação em tempo real** com destaque em vermelho para campos obrigatórios
- **Modais de confirmação** para ações críticas (deleção)
- **Tabs para organização** do painel administrativo

---

## 🔐 Segurança

⚠️ **Versão de Protótipo**: Este é um protótipo educacional. Para produção, considere:
- Implementar autenticação e autorização
- Validar e sanitizar inputs
- Usar HTTPS
- Implementar controle de acesso
- Adicionar logs de auditoria

---

## 📝 Próximas Melhorias Sugeridas

- [ ] Integrar banco de dados persistente
- [ ] Adicionar autenticação de usuários
- [ ] Exportar relatórios (PDF/Excel)
- [ ] Sistema de email para confirmação
- [ ] Dashboard com gráficos e estatísticas
- [ ] Upload de documentos anexos
- [ ] Sistema de pagamento (se necessário)
- [ ] Integração com calendário

---

## 📧 Contato

Para dúvidas ou sugestões sobre este projeto, entre em contato com o desenvolvedor.

---

## 📄 Licença

Este projeto é fornecido como protótipo para fins educacionais e de desenvolvimento.

---

**Desenvolvido com ❤️ usando Streamlit**
