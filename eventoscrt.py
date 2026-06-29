import streamlit as st
from datetime import datetime, time

# Configuracao inicial da pagina com tema responsivo
st.set_page_config(page_title="CRT-ES - Sistema de Eventos", layout="wide")

# ---------------------------------------------------------
# IDENTIDADE VISUAL E ESTILIZAÇÃO CUSTOMIZADA (PADRÃO CRT-ES)
# ---------------------------------------------------------
st.markdown("""
    <style>
    /* Ajustes globais de fonte e containers */
    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    
    /* Customizacao de titulos da aplicacao */
    h1, h2, h3, h4 {
        color: #1B365D !important;
        font-weight: 700 !important;
    }
    
    /* Botoes Customizados - Padrao Azul Institucional com Hover em Dourado */
    div.stButton > button {
        background-color: #1B365D !important;
        color: #FFFFFF !important;
        border: 1px solid #1B365D !important;
        border-radius: 4px !important;
        padding: 0.6rem 2rem !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        font-size: 13px !important;
        letter-spacing: 0.5px;
        transition: all 0.3s ease-in-out !important;
        width: auto !important;
    }
    div.stButton > button:hover {
        background-color: #F2A900 !important;
        color: #1B365D !important;
        border: 1px solid #F2A900 !important;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.15) !important;
        transform: translateY(-1px);
    }
    
    /* Estilizacao de alertas, avisos e notas informativas */
    div[data-testid="stNotification"] {
        border-left: 6px solid #F2A900 !important;
        background-color: #F8F9FA !important;
        border-radius: 4px;
    }
    
    /* Customizacao visual de abas (Tabs) do painel */
    button[data-baseweb="tab"] {
        color: #666666 !important;
        font-weight: 600 !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #1B365D !important;
        border-bottom-color: #1B365D !important;
        font-weight: 700 !important;
    }
    
    /* Estilizacao do menu lateral (Sidebar) */
    section[data-testid="stSidebar"] {
        background-color: #F4F6F9 !important;
        border-right: 1px solid #E0E0E0;
    }
    </style>
""", unsafe_allow_html=True)

# Banner de Cabecalho Institucional (Idêntico à estrutura de topo do portal do CRT-ES)
st.markdown("""
    <div style="background-color: #1B365D; padding: 25px; border-bottom: 6px solid #F2A900; border-radius: 4px; margin-bottom: 30px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
        <h1 style="color: #FFFFFF !important; margin: 0; font-family: Arial, sans-serif; font-size: 24px; font-weight: 700; letter-spacing: 0.5px; line-height: 1.2;">
            CONSELHO REGIONAL DOS TÉCNICOS INDUSTRIAIS DO ESPÍRITO SANTO
        </h1>
        <p style="color: #F2A900; margin: 6px 0 0 0; font-family: Arial, sans-serif; font-size: 13px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;">
            Sistema Integrado de Gestão e Inscrição de Eventos • CRT-ES
        </p>
    </div>
""", unsafe_allow_html=True)

# Inicializacao do banco de dados temporario na memoria
if 'eventos' not in st.session_state:
    st.session_state.eventos = []

if 'inscricoes' not in st.session_state:
    st.session_state.inscricoes = []

if 'missing_fields' not in st.session_state:
    st.session_state.missing_fields = []

# Listas de Dados Consolidadas
escolas_tipo = [
    "Selecione...",
    "IFES - Instituto Federal do Espírito Santo",
    "CEETs - Centros Estaduais de Ensino Técnico",
    "SEDU - Escolas Estaduais Regulares",
    "Senai ES - Serviço Nacional de Aprendizagem Industrial",
    "Outra"
]

campi_ifes = [
    "Selecione o Campus...", "Alegre", "Aracruz", "Barra de São Francisco", 
    "Cachoeiro de Itapemirim", "Cariacica", "Centro-Serrano", "Colatina", 
    "Guarapari", "Ibatiba", "Itapina", "Linhares", "Montanha", "Nova Venécia", 
    "Piúma", "Santa Teresa", "São Mateus", "Serra", "Venda Nova do Imigrante", 
    "Viana", "Vila Velha", "Vitória"
]

centros_ceets = [
    "Selecione o Centro...", 
    "CEET Vasco Coutinho - Vila Velha", 
    "CEET Talmo Luiz Silva - João Neiva"
]

unidades_senai = [
    "Selecione a Unidade...", "Cachoeiro de Itapemirim", "Cariacica", 
    "Colatina", "Linhares", "Sivitec/Serra", "São Mateus", "Vila Velha", "Vitória"
]

escolas_sedu = [
    "Selecione a Escola...", "EEEFM Almirante Barroso", "EEEFM Gomes Cardim", 
    "EEEFM Marechal Mascarenhas de Moraes", "EEEFM Professor Fernando Duarte Rabelo",
    "EEEFM Arnulpho Mattos", "EEEFM Maria Ortiz", "EEEM Colégio Estadual"
]

cursos_tecnicos = [
    "Selecione o Curso...", "Automação Industrial", "Agrimensura", "Biomédica", 
    "Construção Naval", "Desenho de Construção Civil", "Edificações", 
    "Eletromecânica", "Eletrônica", "Eletrotécnica", "Estradas", "Geodésia e Cartografia", 
    "Geologia", "Informática", "Instrumentação Industrial", "Manutenção Automotiva", 
    "Mecânica", "Mecatrônica", "Metalurgia", "Mineração", "Petroquímica", "Plásticos", 
    "Portos", "Química", "Refrigeração e Climatização", "Saneamento", 
    "Segurança do Trabalho", "Sistemas de Energia Renovável", "Telecomunicações"
]

estados_brasil = [
    "Selecione...", "Acre", "Alagoas", "Amapá", "Amazonas", "Bahia", "Ceará", 
    "Distrito Federal", "Espírito Santo", "Goiás", "Maranhão", "Mato Grosso", 
    "Mato Grosso do Sul", "Minas Gerais", "Pará", "Paraíba", "Paraná", 
    "Pernambuco", "Piauí", "Rio de Janeiro", "Rio Grande do Norte", 
    "Rio Grande do Sul", "Rondônia", "Roraima", "Santa Catarina", 
    "São Paulo", "Sergipe", "Tocantins"
]

municipios_es = [
    "Selecione o Município...", "Afonso Cláudio", "Água Doce do Norte", "Águia Branca", 
    "Alegre", "Alfredo Chaves", "Alto Rio Novo", "Anchieta", "Apiacá", "Aracruz", 
    "Atílio Vivácqua", "Baixo Guandu", "Barra de São Francisco", "Boa Esperança", 
    "Bom Jesus do Norte", "Brejetuba", "Cachoeiro de Itapemirim", "Cariacica", 
    "Castelo", "Colatina", "Conceição da Barra", "Conceição do Castelo", 
    "Divino de São Lourenço", "Domingos Martins", "Dores do Rio Preto", "Ecoporanga", 
    "Fundão", "Governador Lindenberg", "Guaçuí", "Guarapari", "Ibatiba", "Ibiraçu", 
    "Ibitirama", "Iconha", "Irupi", "Itaguaçu", "Itapemirim", "Itarana", "Iúna", 
    "Jaguaré", "Jerônimo Monteiro", "João Neiva", "Laranja da Terra", "Linhares", 
    "Mantenópolis", "Marataízes", "Marechal Floriano", "Marilândia", "Mimoso do Sul", 
    "Montanha", "Mucurici", "Muniz Freire", "Muqui", "Nova Venécia", "Pancas", 
    "Pedro Canário", "Pinheiros", "Piúma", "Ponto Belo", "Presidente Kennedy", 
    "Rio Bananal", "Rio Novo do Sul", "Santa Leopoldina", "Santa Maria de Jetibá", 
    "Santa Teresa", "São Domingos do Norte", "São Gabriel da Palha", 
    "São José do Calçado", "São Mateus", "São Roque do Canaã", "Serra", 
    "Sooretama", "Vargem Alta", "Venda Nova do Imigrante", "Viana", "Vila Pavão", 
    "Vila Valério", "Vila Velha", "Vitória"
]

lista_conclusao = ["Selecione... ", "2026/02"]
for ano in range(2027, 2036):
    lista_conclusao.append(f"{ano}/01")
    lista_conclusao.append(f"{ano}/02")
lista_conclusao.append("2036/01")
lista_conclusao.append("2036/02")

locais_sistema = [
    "Selecione o local...", "CFT", "CRT-01", "CRT-02", "CRT-03", "CRT-05", 
    "CRT-06", "CRT-07", "CRT-08", "CRT-RN", "CRT-RS", "CRT-RJ", "CRT-SP", 
    "CRT-ES", "CRT-MG", "CRT-BA", "CRT-PR", "CRT-SC"
]

# Menu de navegacao lateral
st.sidebar.markdown("<h3 style='margin-top:0;'>Navegação</h3>", unsafe_allow_html=True)
area_selecionada = st.sidebar.radio(
    "Selecione o módulo de acesso:", 
    ["1. Criar Evento (Gestão)", "2. Área de Inscrição (Público)", "3. Painel do Organizador (Controle)"]
)

st.sidebar.markdown("---")
st.sidebar.caption("Suporte técnico corporativo: TI @ CRT-ES")

# ---------------------------------------------------------
# AREA 1: CRIACAO DO EVENTO (GESTAO)
# ---------------------------------------------------------
if area_selecionada == "1. Criar Evento (Gestão)":
    st.subheader("⚙️ Painel de Gestão: Cadastrar Novo Evento")
    st.write("Preencha as informações regulamentares e o período de vigência para disponibilização em portal.")
    
    with st.form("form_criacao_evento", clear_on_submit=True):
        nome_evento = st.text_input("Nome do Evento *")
        descricao_evento = st.text_area("Descrição detalhada do Evento")
        
        col1, col2 = st.columns(2)
        with col1:
            data_inicio = st.date_input("Início do Evento", value=datetime.now().date(), format="DD/MM/YYYY")
            horario_inicio = st.time_input("Horário de Início", value=time(9, 0))
        with col2:
            data_fim = st.date_input("Encerramento do Evento", value=datetime.now().date(), format="DD/MM/YYYY")
            horario_fim = st.time_input("Horário de Encerramento", value=time(18, 0))
        
        categoria_evento = st.selectbox(
            "Modalidade do Evento *",
            ["Selecione...", "CRT-ES na Escola", "Sistema CFT/CRTs", "Público Geral"]
        )
        
        st.markdown("### 📎 Arquivos e Mídias Complementares")
        capa_arquivo = st.file_uploader("Banner de Capa (Cabeçalho do Formulário)", type=["png", "jpg", "jpeg"])
        video_url = st.text_input("URL do Vídeo Institucional / Divulgação")
        
        submit_evento = st.form_submit_button("✅ Publicar Evento")
        
        if submit_evento:
            if categoria_evento == "Selecione..." or not nome_evento:
                st.error("O nome do evento e a respectiva modalidade são campos mandatórios.")
            else:
                imagem_bytes = capa_arquivo.getvalue() if capa_arquivo is not None else None
                
                novo_evento = {
                    "id": int(datetime.now().timestamp()),
                    "nome": nome_evento,
                    "descricao": descricao_evento,
                    "data_inicio": data_inicio.strftime("%d/%m/%Y"),
                    "data_fim": data_fim.strftime("%d/%m/%Y"),
                    "horario_inicio": horario_inicio.strftime("%H:%M"),
                    "horario_fim": horario_fim.strftime("%H:%M"),
                    "categoria": categoria_evento,
                    "imagem_capa": imagem_bytes,
                    "video_url": video_url
                }
                st.session_state.eventos.append(novo_evento)
                st.success(f"✅ Evento '{nome_evento}' registrado e publicado com sucesso.")

# ---------------------------------------------------------
# AREA 2: INSCRICAO (PUBLICO)
# ---------------------------------------------------------
elif area_selecionada == "2. Área de Inscrição (Público)":
    st.subheader("📝 Portal Público de Inscrições em Eventos")
    
    modo_organizador_view = st.toggle("🔐 Habilitar controle rápido de moderação (Apenas Organizadores)")
    
    if not st.session_state.eventos:
        st.warning("Não há eventos com inscrições vigentes abertas no presente momento.")
    else:
        opcoes_eventos = {f"{e['nome']} (Período: {e['data_inicio']} a {e['data_fim']})": e for e in st.session_state.eventos}
        evento_selecionado_str = st.selectbox("Selecione o evento de interesse para realizar sua inscrição:", list(opcoes_eventos.keys()))
        evento_atual = opcoes_eventos[evento_selecionado_str]
        
        st.markdown(f"## {evento_atual['nome']}")
        st.info(f"**Modalidade institucional:** {evento_atual['categoria']} | **Vigência:** {evento_atual['data_inicio']} às {evento_atual['horario_inicio']} até {evento_atual['data_fim']} às {evento_atual['horario_fim']}")
        
        if evento_atual['imagem_capa']:
            st.image(evento_atual['imagem_capa'], use_container_width=True)
            
        if evento_atual['descricao']:
            st.markdown(f"### 📄 Detalhes do Evento\n{evento_atual['descricao']}")
            
        if evento_atual['video_url']:
            st.markdown("### 🎬 Material em Vídeo")
            try:
                st.video(evento_atual['video_url'])
            except:
                st.warning("Falha na renderização do vídeo informado.")
        
        st.markdown("---")
        st.subheader("📋 Formulário de Inscrição Obrigatório")
        
        # Alinhamento estrito e tratamento de erros destacados em vermelho
        lbl_nome = "Nome Completo *" if "nome" not in st.session_state.missing_fields else ":red[Nome Completo * (Campo Obrigatório)]"
        lbl_telefone = "Telefone / Celular com DDD *" if "telefone" not in st.session_state.missing_fields else ":red[Telefone / Celular com DDD * (Campo Obrigatório)]"
        lbl_cpf = "CPF *" if "cpf" not in st.session_state.missing_fields else ":red[CPF * (Campo Obrigatório)]"
        lbl_email = "E-mail *" if "email" not in st.session_state.missing_fields else ":red[E-mail * (Campo Obrigatório)]"
        lbl_idade = "Idade *" if "idade" not in st.session_state.missing_fields else ":red[Idade * (Campo Obrigatório)]"
        lbl_termo = "Eu AUTORIZO o uso de minha imagem em materiais do CRT-ES *" if "termo" not in st.session_state.missing_fields else ":red[Eu AUTORIZO o uso de minha imagem em materiais do CRT-ES * (Aceite Obrigatório)]"
        
        lbl_escola_tipo = "Nome da Escola Técnica *" if "escola_tipo" not in st.session_state.missing_fields else ":red[Nome da Escola Técnica * (Campo Obrigatório)]"
        lbl_escola_detalhe = "Selecione ou Informe a Instituição *" if "escola_detalhe" not in st.session_state.missing_fields else ":red[Selecione ou Informe a Instituição * (Campo Obrigatório)]"
        lbl_curso = "Qual o seu Curso Técnico? *" if "curso" not in st.session_state.missing_fields else ":red[Qual o seu Curso Técnico? * (Campo Obrigatório)]"
        lbl_estado = "Qual Estado você mora? *" if "estado" not in st.session_state.missing_fields else ":red[Qual Estado você mora? * (Campo Obrigatório)]"
        lbl_cidade = "Qual cidade você mora? *" if "cidade" not in st.session_state.missing_fields else ":red[Qual cidade você mora? * (Campo Obrigatório)]"
        lbl_conclusao = "Ano de Conclusão do Curso *" if "conclusao" not in st.session_state.missing_fields else ":red[Ano de Conclusão do Curso * (Campo Obrigatório)]"
        lbl_trabalha = "Você trabalha e/ou estagia atualmente? *" if "trabalha" not in st.session_state.missing_fields else ":red[Você trabalha e/ou estagia atualmente? * (Campo Obrigatório)]"
        lbl_pretende = "Pretende trabalhar na área após se formar? *" if "pretende" not in st.session_state.missing_fields else ":red[Pretende trabalhar na área após se formar? * (Campo Obrigatório)]"
        lbl_expectativas = "Quais suas expectativas após se formar? *" if "expectativas" not in st.session_state.missing_fields else ":red[Quais suas expectativas após se formar? * (Campo Obrigatório)]"
        
        lbl_is_funcionario = "Você é funcionário do SISTEMA CFT/CRTs *" if "is_funcionario" not in st.session_state.missing_fields else ":red[Você é funcionário do SISTEMA CFT/CRTs * (Campo Obrigatório)]"
        lbl_origem_sistema = "De qual local do SISTEMA CFT/CRTs você veio? *" if "origem_sistema" not in st.session_state.missing_fields else ":red[De qual local do SISTEMA CFT/CRTs você veio? * (Campo Obrigatório)]"
        lbl_sabendo = "Como você ficou sabendo do evento? *" if "sabendo" not in st.session_state.missing_fields else ":red[Como você ficou sabendo do evento? * (Campo Obrigatório)]"

        # Coleta reativa para suportar a árvore de regras institucionais
        val_nome = st.text_input(lbl_nome, key="ins_nome")
        val_cpf = st.text_input(lbl_cpf, key="ins_cpf")
        val_email = st.text_input(lbl_email, key="ins_email")
        val_telefone = st.text_input(lbl_telefone, key="ins_telefone")
        val_idade = st.number_input(lbl_idade, min_value=0, max_value=120, value=0, key="ins_idade")
        
        sub_dados = {}
        
        if evento_atual["categoria"] == "CRT-ES na Escola":
            st.markdown("#### 🏫 Informações de Vínculo Acadêmico")
            
            sel_tipo = st.selectbox(lbl_escola_tipo, escolas_tipo, key="ins_escola_tipo")
            detalhe_escola = ""
            
            if sel_tipo == "IFES - Instituto Federal do Espírito Santo":
                detalhe_escola = st.selectbox(lbl_escola_detalhe, campi_ifes, key="ins_escola_detalhe")
            elif sel_tipo == "CEETs - Centros Estaduais de Ensino Técnico":
                detalhe_escola = st.selectbox(lbl_escola_detalhe, centros_ceets, key="ins_escola_detalhe")
            elif sel_tipo == "SEDU - Escolas Estaduais Regulares":
                detalhe_escola = st.selectbox(lbl_escola_detalhe, escolas_sedu, key="ins_escola_detalhe")
            elif sel_tipo == "Senai ES - Serviço Nacional de Aprendizagem Industrial":
                detalhe_escola = st.selectbox(lbl_escola_detalhe, unidades_senai, key="ins_escola_detalhe")
            elif sel_tipo == "Outra":
                detalhe_escola = st.text_input(lbl_escola_detalhe, key="ins_escola_detalhe")
                
            sub_dados["escola_tipo"] = sel_tipo
            sub_dados["escola_detalhe"] = detalhe_escola
            
            sub_dados["curso"] = st.selectbox(lbl_curso, cursos_tecnicos, key="ins_curso")
            
            sel_estado = st.selectbox(lbl_estado, estados_brasil, key="ins_estado")
            sub_dados["estado"] = sel_estado
            
            if sel_estado == "Espírito Santo":
                sub_dados["cidade"] = st.selectbox(lbl_cidade, municipios_es, key="ins_cidade")
            elif sel_estado != "Selecione...":
                sub_dados["cidade"] = st.text_input(lbl_cidade, key="ins_cidade")
            else:
                sub_dados["cidade"] = "Selecione..."
                
            sub_dados["conclusao"] = st.selectbox(lbl_conclusao, lista_conclusao, key="ins_conclusao")
            sub_dados["trabalha"] = st.radio(lbl_trabalha, ["Selecione...", "Sim", "Não"], key="ins_trabalha")
            
            sel_pretende = st.radio(lbl_pretende, ["Selecione...", "Sim", "Não"], key="ins_pretende")
            sub_dados["pretende"] = sel_pretende
            
            if sel_pretende == "Sim":
                sub_dados["expectativas"] = st.text_area(lbl_expectativas, key="ins_expectativas")
            else:
                sub_dados["expectativas"] = "Não se aplica"
                
            st.checkbox("Desejo receber informações do CRT-ES após a conclusão do curso para fins de registro profissional.", key="ins_contato_futuro")

        elif evento_atual["categoria"] == "Sistema CFT/CRTs":
            st.markdown("#### 🏢 Declaração Corporativa")
            is_func = st.radio(lbl_is_funcionario, ["Selecione...", "Sim", "Não"], key="ins_is_funcionario")
            sub_dados["is_funcionario"] = is_func
            
            if is_func == "Sim":
                sub_dados["origem_sistema"] = st.selectbox(lbl_origem_sistema, locais_sistema, key="ins_origem_sistema")
                sub_dados["sabendo"] = "Integrante do Sistema Corporativo"
            elif is_func == "Não":
                sub_dados["sabendo"] = st.text_input(lbl_sabendo, key="ins_sabendo")
                sub_dados["origem_sistema"] = "Público Externo ao Sistema"

        elif evento_atual["categoria"] == "Público Geral":
            st.markdown("#### 💼 Identificação de Atividade Profissional")
            sub_dados["profissao"] = st.text_input("Profissão / Cargo *", key="ins_profissao")
            sub_dados["empresa"] = st.text_input("Empresa ou Instituição de Vínculo *", key="ins_empresa")

        st.markdown("---")
        val_termo = st.checkbox(lbl_termo, key="ins_termo")
        
        submit_inscricao = st.button("✅ Confirmar Minha Inscrição")
        
        if submit_inscricao:
            erros = []
            if not st.session_state.ins_nome.strip(): erros.append("nome")
            if not st.session_state.ins_telefone.strip(): erros.append("telefone")
            if not st.session_state.ins_cpf.strip(): erros.append("cpf")
            if not st.session_state.ins_email.strip(): erros.append("email")
            if st.session_state.ins_idade == 0: erros.append("idade")
            if not st.session_state.ins_termo: erros.append("termo")
            
            if evento_atual["categoria"] == "CRT-ES na Escola":
                if sub_dados["escola_tipo"] == "Selecione...": erros.append("escola_tipo")
                if not sub_dados["escola_detalhe"] or sub_dados["escola_detalhe"] in ["Selecione o Campus...", "Selecione o Centro...", "Selecione a Unidade...", "Selecione a Escola..."]: erros.append("escola_detalhe")
                if sub_dados["curso"] == "Selecione o Curso...": erros.append("curso")
                if sub_dados["estado"] == "Selecione...": erros.append("estado")
                if sub_dados["cidade"] in ["Selecione...", "Selecione o Município...", ""]: erros.append("cidade")
                if sub_dados["conclusao"] == "Selecione... ": erros.append("conclusao")
                if sub_dados["trabalha"] == "Selecione...": erros.append("trabalha")
                if sub_dados["pretende"] == "Selecione...": erros.append("pretende")
                if sub_dados["pretende"] == "Sim" and not st.session_state.ins_expectativas.strip(): erros.append("expectativas")
                
            elif evento_atual["categoria"] == "Sistema CFT/CRTs":
                if sub_dados["is_funcionario"] == "Selecione...": erros.append("is_funcionario")
                if sub_dados["is_funcionario"] == "Sim" and sub_dados["origem_sistema"] == "Selecione o local...": erros.append("origem_sistema")
                if sub_dados["is_funcionario"] == "Não" and not st.session_state.ins_sabendo.strip(): erros.append("sabendo")
                
            elif evento_atual["categoria"] == "Público Geral":
                if not sub_dados["profissao"].strip(): erros.append("profissao")
                if not sub_dados["empresa"].strip(): erros.append("empresa")
            
            if erros:
                st.session_state.missing_fields = erros
                st.error("❌ Não foi possível processar a requisição. Certifique-se de preencher todos os campos assinalados como obrigatórios.")
                st.scroll_to_top()
            else:
                st.session_state.missing_fields = []
                timestamp_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                
                nova_inscricao = {
                    "id": int(datetime.now().timestamp()),
                    "evento_id": evento_atual["id"],
                    "nome": st.session_state.ins_nome,
                    "cpf": st.session_state.ins_cpf,
                    "email": st.session_state.ins_email,
                    "telefone": st.session_state.ins_telefone,
                    "idade": st.session_state.ins_idade,
                    "log_data_hora": timestamp_atual,
                    "detalhes_adicionais": sub_dados
                }
                st.session_state.inscricoes.append(nova_inscricao)
                st.success("✅ Sua inscrição foi confirmada e registrada no sistema do CRT-ES.")
                st.balloons()
                    
        if modo_organizador_view:
            st.markdown("---")
            st.subheader("🛠️ Auditoria Rápida (Exclusivo da Organização)")
            inscritos_deste_evento = [i for i in st.session_state.inscricoes if i["evento_id"] == evento_atual["id"]]
            
            if not inscritos_deste_evento:
                st.info("Nenhum registro de inscrição associado a este evento até o momento.")
            else:
                for inscrito in inscritos_deste_evento:
                    col_info, col_acao = st.columns([4, 1])
                    with col_info:
                        st.write(f"📅 Data/Hora Log: {inscrito['log_data_hora']} | 👤 Beneficiário: {inscrito['nome']} | 🆔 CPF: {inscrito['cpf']}")
                    with col_acao:
                        if st.button("🗑️ Excluir", key=f"del_fast_{inscrito['id']}", type="primary"):
                            st.session_state.inscricoes.remove(inscrito)
                            st.toast(f"Inscrição de {inscrito['nome']} removida!")
                            st.rerun()

# ---------------------------------------------------------
# AREA 3: PAINEL DO ORGANIZADOR (CONTROLE TOTAL)
# ---------------------------------------------------------
elif area_selecionada == "3. Painel do Organizador (Controle)":
    st.subheader("📊 Painel Administrativo, Auditoria e Relatórios")
    st.write("Gerencie eventos ativos, edite informações ou remova registros do sistema.")
    
    if not st.session_state.eventos:
        st.warning("O sistema não possui eventos homologados na base ativa.")
    else:
        opcoes_gerenciamento = {f"{e['nome']} [{e['categoria']}]": e for e in st.session_state.eventos}
        selecionado_str = st.selectbox("Selecione a ação sobre o respectivo evento institucional:", list(opcoes_gerenciamento.keys()))
        ev_gerenciar = opcoes_gerenciamento[selecionado_str]
        
        tab1, tab2, tab3 = st.tabs(["👥 Lista de Inscritos Homologados", "✏️ Editar Propriedades do Evento", "🚨 Gerenciamento Avançado / Zona Crítica"])
        
        # ABA 1: LISTA DE INSCRITOS COM LOGS
        with tab1:
            inscritos = [i for i in st.session_state.inscricoes if i["evento_id"] == ev_gerenciar["id"]]
            st.subheader(f"📋 Lista Geral de Participantes: {ev_gerenciar['nome']}")
            st.metric(label="Total de Inscrições Confirmadas na Base", value=len(inscritos))
            
            if not inscritos:
                st.info("Nenhum cidadão ou profissional efetuou inscrição para este evento.")
            else:
                st.markdown("---")
                for idx, ins in enumerate(inscritos):
                    c1, c2, c3, c4 = st.columns([3, 2, 3, 1])
                    with c1:
                        st.write(f"**Nome:** {ins['nome']} (Idade: {ins['idade']})")
                        st.caption(f"📝 Registro eletrônico: {ins['log_data_hora']}")
                    with c2:
                        st.write(f"**CPF:** {ins['cpf']}")
                    with c3:
                        st.write(f"**Contato:** {ins['email']} / {ins['telefone']}")
                        with st.expander("📄 Ficha Complementar (JSON)"):
                            st.json(ins['detalhes_adicionais'])
                    with c4:
                        if st.button("❌ Remover Registro", key=f"panel_del_{ins['id']}", type="secondary"):
                            st.session_state.inscricoes.remove(ins)
                            st.success(f"✅ Inscrição de {ins['nome']} removida com sucesso.")
                            st.rerun()
                            
        # ABA 2: EDITAR EVENTO
        with tab2:
            st.subheader("✏️ Editar Propriedades Cronológicas e Textuais")
            with st.form(f"form_edit_{ev_gerenciar['id']}"):
                novo_nome = st.text_input("Alterar Nome do Evento", value=ev_gerenciar["nome"])
                nova_desc = st.text_area("Alterar Descrição", value=ev_gerenciar["descricao"])
                nova_data_in = st.text_input("Alterar Data de Início", value=ev_gerenciar["data_inicio"])
                nova_data_fi = st.text_input("Alterar Data de Fim", value=ev_gerenciar["data_fim"])
                novo_hr_in = st.text_input("Alterar Horário Inicial", value=ev_gerenciar["horario_inicio"])
                novo_hr_fi = st.text_input("Alterar Horário Final", value=ev_gerenciar["horario_fim"])
                nova_cat = st.selectbox("Mudar Modalidade", ["CRT-ES na Escola", "Sistema CFT/CRTs", "Público Geral"], index=["CRT-ES na Escola", "Sistema CFT/CRTs", "Público Geral"].index(ev_gerenciar["categoria"]))
                novo_video = st.text_input("Alterar Link do Vídeo", value=ev_gerenciar["video_url"])
                
                salvar_edicao = st.form_submit_button("✅ Confirmar Atualizações")
                if salvar_edicao:
                    ev_gerenciar["nome"] = novo_nome
                    ev_gerenciar["descricao"] = nova_desc
                    ev_gerenciar["data_inicio"] = nova_data_in
                    ev_gerenciar["data_fim"] = nova_data_fi
                    ev_gerenciar["horario_inicio"] = novo_hr_in
                    ev_gerenciar["horario_fim"] = novo_hr_fi
                    ev_gerenciar["categoria"] = nova_cat
                    ev_gerenciar["video_url"] = novo_video
                    st.success("✅ Modificações salvas na sessão corrente.")
                    st.rerun()
                    
        # ABA 3: APAGAR EVENTO COMPLETO
        with tab3:
            st.subheader("🚨 Remoção e Exclusão de Registros")
            st.warning("⚠️ Atenção: A deleção deste evento expurgará de forma permanente o registro e o histórico de inscrições associado.")
            
            confirmar_exclusao = st.checkbox(f"Estou ciente e concordo em remover permanentemente o evento '{ev_gerenciar['nome']}'")
            btn_deletar_tudo = st.button("🗑️ Eliminar Registro Definitivamente", type="primary", disabled=not confirmar_exclusao)
            
            if btn_deletar_tudo:
                st.session_state.inscricoes = [i for i in st.session_state.inscricoes if i["evento_id"] != ev_gerenciar["id"]]
                st.session_state.eventos.remove(ev_gerenciar)
                st.error("🗑️ O evento e os dados correlatos foram expurgados da memória.")
                st.rerun()
