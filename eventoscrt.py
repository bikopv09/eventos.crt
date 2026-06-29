import streamlit as st
import psycopg2
import psycopg2.extras
import json
from datetime import datetime, time

# Configuracao inicial da pagina com tema responsivo
st.set_page_config(page_title="CRT-ES - Sistema de Eventos", layout="wide")

# Seletor de Tema Fixo posicionado no Canto Superior Direito (Sem permissao para digitar)
col_vazia, col_seletor = st.columns([5.2, 1.8])
with col_seletor:
    tema_selecionado = st.radio(
        "Visualização",
        options=["Modo Claro", "Modo Escuro"],
        index=0,
        horizontal=True,
        label_visibility="collapsed"
    )

# Definicao dinamica de variaveis de estilo baseadas no tema
if tema_selecionado == "Modo Claro":
    bg_principal = "#FFFFFF"
    texto_principal = "#333333"
    bg_sidebar = "#F4F6F9"
    texto_sidebar = "#1B365D"
    borda_sidebar = "#E0E0E0"
    card_bg = "#F8F9FA"
    titulo_cor = "#1B365D"
else:
    bg_principal = "#0E1117"
    texto_principal = "#E0E0E0"
    bg_sidebar = "#1E222B"
    texto_sidebar = "#E0E0E0"
    borda_sidebar = "#2D3139"
    card_bg = "#1A1C23"
    titulo_cor = "#4A90E2"

# Parametros de conexao com o banco de dados PostgreSQL
DB_CONFIG = {
    "host": "seu_host_do_banco",
    "database": "seu_nome_do_banco",
    "user": "seu_usuario",
    "password": "sua_senha",
    "port": 5432
}

def executar_query(sql, params=None, is_write=False, role="publico"):
    """
    Executa comandos no PostgreSQL definindo o papel (role) do usuario
    corrente para validacao das diretrizes de RLS.
    """
    conn = psycopg2.connect(**DB_CONFIG)
    try:
        with conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("SET LOCAL app.usuario_role = %s;", (role,))
                cursor.execute(sql, params)
                if is_write:
                    conn.commit()
                    return True
                else:
                    return cursor.fetchall()
    except Exception as e:
        st.error(f"Erro operacional na base de dados: {e}")
        return None
    finally:
        conn.close()

# Identidade Visual e Estilizacao Customizada Dinamica
st.markdown(f"""
    <style>
    .main {{
        background-color: {bg_principal} !important;
        color: {texto_principal} !important;
    }}
    .main .block-container {{
        padding-top: 0.5rem;
        padding-bottom: 3rem;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }}
    .main p, .main span, .main label, .main [data-testid="stMarkdownContainer"] p {{
        color: {texto_principal} !important;
    }}
    h1, h2, h3, h4 {{
        color: {titulo_cor} !important;
        font-weight: 700 !important;
    }}
    
    /* BLOQUEIO CRÍTICO: Impede totalmente a digitacao dentro de qualquer lista do sistema */
    div[data-baseweb="select"] input {{
        display: none !important;
    }}
    div[data-baseweb="select"] {{
        cursor: pointer !important;
    }}
    
    /* Correcao de Contraste e Legibilidade do Sidebar */
    section[data-testid="stSidebar"] {{
        background-color: {bg_sidebar} !important;
        border-right: 1px solid {borda_sidebar} !important;
    }}
    section[data-testid="stSidebar"] .stText,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] h3 {{
        color: {texto_sidebar} !important;
    }}
    
    /* Estilizacao Padrao dos Botoes Institucionais */
    div.stButton > button {{
        background-color: #1B365D !important;
        border: 1px solid #1B365D !important;
        border-radius: 4px !important;
        padding: 0.6rem 2rem !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        font-size: 13px !important;
        letter-spacing: 0.5px;
        transition: all 0.3s ease-in-out !important;
        width: auto !important;
    }}
    div.stButton > button, div.stButton > button span {{
        color: #FFFFFF !important;
    }}
    div.stButton > button:hover {{
        background-color: #F2A900 !important;
        border: 1px solid #F2A900 !important;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.15) !important;
        transform: translateY(-1px);
    }}
    div.stButton > button:hover span {{
        color: #1B365D !important;
    }}
    
    div[data-testid="stNotification"] {{
        border-left: 6px solid #F2A900 !important;
        background-color: {card_bg} !important;
        border-radius: 4px;
    }}
    button[data-baseweb="tab"] {{
        color: #666666 !important;
        font-weight: 600 !important;
    }}
    button[data-baseweb="tab"][aria-selected="true"] {{
        color: #1B365D !important;
        border-bottom-color: #1B365D !important;
        font-weight: 700 !important;
    }}
    </style>
""", unsafe_allow_html=True)

# Banner de Cabecalho Institucional
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

if 'missing_fields' not in st.session_state:
    st.session_state.missing_fields = []

# Listas de Dados do Formulario
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

lista_conclusao = ["Selecione... "]
for ano in range(2026, 2036):
    lista_conclusao.append(f"{ano}/01")
    lista_conclusao.append(f"{ano}/02")

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

# Definicao do papel para o RLS com base na navegacao
role_contexto = "organizador" if "3. Painel do Organizador" in area_selecionada or "1. Criar Evento" in area_selecionada else "publico"

# ---------------------------------------------------------
# AREA 1: CRIACAO DO EVENTO (GESTAO)
# ---------------------------------------------------------
if area_selecionada == "1. Criar Evento (Gestão)":
    st.subheader("Painel de Gestão: Cadastrar Novo Evento")
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
        
        st.markdown("### Arquivos e Mídias Complementares")
        capa_arquivo = st.file_uploader("Banner de Capa (Cabeçalho do Formulário)", type=["png", "jpg", "jpeg"])
        video_url = st.text_input("URL do Vídeo Institucional / Divulgação")
        
        submit_evento = st.form_submit_button("Publicar Evento")
        
        if submit_evento:
            if categoria_evento == "Selecione..." or not nome_evento:
                st.error("O nome do evento e a respectiva modalidade são campos mandatórios.")
            else:
                imagem_bytes = capa_arquivo.getvalue() if capa_arquivo is not None else None
                
                sql_inserir = """
                    INSERT INTO eventos (nome, descricao, data_inicio, data_fim, horario_inicio, horario_fim, categoria, imagem_capa, video_url)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
                """
                valores = (nome_evento, descricao_evento, data_inicio, data_fim, horario_inicio, horario_fim, categoria_evento, imagem_bytes, video_url)
                
                if executar_query(sql_inserir, valores, is_write=True, role=role_contexto):
                    st.success(f"Evento '{nome_evento}' registrado e publicado com sucesso no banco de dados.")

# ---------------------------------------------------------
# AREA 2: INSCRICAO (PUBLICO)
# ---------------------------------------------------------
elif area_selecionada == "2. Área de Inscrição (Público)":
    st.subheader("Portal Público de Inscrições em Eventos")
    
    sql_buscar_eventos = """
        SELECT id, nome, descricao, categoria, imagem_capa, video_url,
               TO_CHAR(data_inicio, 'DD/MM/YYYY') as data_inicio,
               TO_CHAR(data_fim, 'DD/MM/YYYY') as data_fim,
               TO_CHAR(horario_inicio, 'HH24:MI') as horario_inicio,
               TO_CHAR(horario_fim, 'HH24:MI') as horario_fim
        FROM eventos ORDER BY id DESC;
    """
    lista_eventos_db = executar_query(sql_buscar_eventos, role=role_contexto)
    
    if not lista_eventos_db:
        st.warning("Não há eventos com inscrições vigentes abertas no presente momento.")
    else:
        opcoes_eventos = {f"{e['nome']} (Período: {e['data_inicio']} a {e['data_fim']})": e for e in lista_eventos_db}
        evento_selecionado_str = st.selectbox("Selecione o evento de interesse para realizar sua inscrição:", list(opcoes_eventos.keys()))
        evento_atual = opcoes_eventos[evento_selecionado_str]
        
        st.markdown(f"## {evento_atual['nome']}")
        st.info(f"**Modalidade institucional:** {evento_atual['categoria']} | **Vigência:** {evento_atual['data_inicio']} às {evento_atual['horario_inicio']} até {evento_atual['data_fim']} às {evento_atual['horario_fim']}")
        
        if evento_atual['imagem_capa']:
            st.image(bytes(evento_atual['imagem_capa']), use_container_width=True)
            
        if evento_atual['descricao']:
            st.markdown(f"### Detalhes do Evento\n{evento_atual['descricao']}")
            
        if evento_atual['video_url']:
            st.markdown("### Material em Vídeo")
            try:
                st.video(evento_atual['video_url'])
            except:
                st.warning("Falha na renderização do vídeo informado.")
        
        st.markdown("---")
        st.subheader("Formulário de Inscrição Obrigatório")
        
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

        val_nome = st.text_input(lbl_nome, key="ins_nome")
        val_cpf = st.text_input(lbl_cpf, key="ins_cpf")
        val_email = st.text_input(lbl_email, key="ins_email")
        val_telefone = st.text_input(lbl_telefone, key="ins_telefone")
        val_idade = st.number_input(lbl_idade, min_value=0, max_value=120, value=0, key="ins_idade")
        
        sub_dados = {}
        
        if evento_atual["categoria"] == "CRT-ES na Escola":
            st.markdown("#### Informações de Vínculo Acadêmico")
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

        elif evento_atual["categoria"] == "Sistema CFT/CRTs":
            st.markdown("#### Declaração Corporativa")
            is_func = st.radio(lbl_is_funcionario, ["Selecione...", "Sim", "Não"], key="ins_is_funcionario")
            sub_dados["is_funcionario"] = is_func
            
            if is_func == "Sim":
                sub_dados["origem_sistema"] = st.selectbox(lbl_origem_sistema, locais_sistema, key="ins_origem_sistema")
                sub_dados["sabendo"] = "Integrante do Sistema Corporativo"
            elif is_func == "Não":
                sub_dados["sabendo"] = st.text_input(lbl_sabendo, key="ins_sabendo")
                sub_dados["origem_sistema"] = "Público Externo ao Sistema"

        elif evento_atual["categoria"] == "Público Geral":
            st.markdown("#### Identificação de Atividade Profissional")
            sub_dados["profissao"] = st.text_input("Profissão / Cargo *", key="ins_profissao")
            sub_dados["empresa"] = st.text_input("Empresa ou Instituição de Vínculo *", key="ins_empresa")

        st.markdown("---")
        val_termo = st.checkbox(lbl_termo, key="ins_termo")
        
        submit_inscricao = st.button("Confirmar Minha Inscrição")
        
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
                st.error("Não foi possível processar a requisição. Certifique-se de preencher todos os campos assinalados como obrigatórios.")
            else:
                st.session_state.missing_fields = []
                
                sql_gravar_inscricao = """
                    INSERT INTO inscricoes (evento_id, nome, cpf, email, telefone, idade, detalhes_adicionais)
                    VALUES (%s, %s, %s, %s, %s, %s, %s);
                """
                valores_inscricao = (
                    evento_atual["id"], 
                    st.session_state.ins_nome, 
                    st.session_state.ins_cpf, 
                    st.session_state.ins_email, 
                    st.session_state.ins_telefone, 
                    st.session_state.ins_idade, 
                    json.dumps(sub_dados)
                )
                
                if executar_query(sql_gravar_inscricao, valores_inscricao, is_write=True, role=role_contexto):
                    st.success("Sua inscrição foi confirmada e registrada no sistema do CRT-ES.")

# ---------------------------------------------------------
# AREA 3: PAINEL DO ORGANIZADOR (CONTROLE TOTAL)
# ---------------------------------------------------------
elif area_selecionada == "3. Painel do Organizador (Controle)":
    st.subheader("Painel Administrativo, Auditoria e Relatórios")
    
    sql_buscar_todos_eventos = "SELECT id, nome, categoria, descricao, data_inicio, data_fim, horario_inicio, horario_fim, video_url FROM eventos ORDER BY id DESC;"
    todos_eventos = executar_query(sql_buscar_todos_eventos, role=role_contexto)
    
    if not todos_eventos:
        st.warning("O sistema não possui eventos homologados na base ativa.")
    else:
        opcoes_gerenciamento = {f"{e['nome']} [{e['categoria']}]": e for e in todos_eventos}
        selecionado_str = st.selectbox("Selecione a ação sobre o respectivo evento institucional:", list(opcoes_gerenciamento.keys()))
        ev_gerenciar = opcoes_gerenciamento[selecionado_str]
        
        tab1, tab2, tab3 = st.tabs(["Lista de Inscritos Homologados", "Editar Propriedades do Evento", "Gerenciamento Avançado / Zona Crítica"])
        
        with tab1:
            sql_buscar_inscritos = """
                SELECT id, nome, cpf, email, telefone, idade,
                       TO_CHAR(log_data_hora, 'DD/MM/YYYY HH24:MI:SS') as log_data_hora,
                       detalhes_adicionais
                FROM inscricoes WHERE evento_id = %s ORDER BY id DESC;
            """
            inscritos = executar_query(sql_buscar_inscritos, (ev_gerenciar["id"],), role=role_contexto)
            
            st.subheader(f"Lista Geral de Participantes: {ev_gerenciar['nome']}")
            st.metric(label="Total de Inscrições Confirmadas na Base", value=len(inscritos) if inscritos else 0)
            
            if not inscritos:
                st.info("Nenhum cidadão ou profissional efetuou inscrição para este evento.")
            else:
                st.markdown("---")
                for ins in inscritos:
                    c1, c2, c3, c4 = st.columns([3, 2, 3, 1])
                    with c1:
                        st.write(f"**Nome:** {ins['nome']} (Idade: {ins['idade']})")
                        st.caption(f"Registro eletrônico: {ins['log_data_hora']}")
                    with c2:
                        st.write(f"**CPF:** {ins['cpf']}")
                    with c3:
                        st.write(f"**Contato:** {ins['email']} / {ins['telefone']}")
                        with st.expander("Ficha Complementar"):
                            st.json(ins['detalhes_adicionais'])
                    with c4:
                        if st.button("Remover Registro", key=f"panel_del_{ins['id']}", type="secondary"):
                            sql_deletar_ins = "DELETE FROM inscricoes WHERE id = %s;"
                            if executar_query(sql_deletar_ins, (ins['id'],), is_write=True, role=role_contexto):
                                st.success("Registro removido.")
                                st.rerun()
                            
        with tab2:
            st.subheader("Editar Propriedades Cronológicas e Textuais")
            with st.form(f"form_edit_{ev_gerenciar['id']}"):
                novo_nome = st.text_input("Alterar Nome do Evento", value=ev_gerenciar["nome"])
                nova_desc = st.text_area("Alterar Descrição", value=ev_gerenciar["descricao"])
                nova_data_in = st.text_input("Alterar Data de Início (AAAA-MM-DD)", value=str(ev_gerenciar["data_inicio"]))
                nova_data_fi = st.text_input("Alterar Data de Fim (AAAA-MM-DD)", value=str(ev_gerenciar["data_fim"]))
                novo_hr_in = st.text_input("Alterar Horário Inicial", value=str(ev_gerenciar["horario_inicio"]))
                novo_hr_fi = st.text_input("Alterar Horário Final", value=str(ev_gerenciar["horario_fim"]))
                novo_video = st.text_input("Alterar Link do Vídeo", value=ev_gerenciar["video_url"])
                
                salvar_edicao = st.form_submit_button("Confirmar Atualizações")
                if salvar_edicao:
                    sql_update = """
                        UPDATE eventos 
                        SET nome = %s, descricao = %s, data_inicio = %s, data_fim = %s, horario_inicio = %s, horario_fim = %s, video_url = %s
                        WHERE id = %s;
                    """
                    params_update = (novo_nome, nova_desc, nova_data_in, nova_data_fi, novo_hr_in, novo_hr_fi, novo_video, ev_gerenciar["id"])
                    if executar_query(sql_update, params_update, is_write=True, role=role_contexto):
                        st.success("Modificações salvas com sucesso.")
                        st.rerun()
                    
        with tab3:
            st.subheader("Remoção e Exclusão de Registros")
            st.warning("Atenção: A deleção deste evento expurgará de forma permanente o registro e o histórico de inscrições associado.")
            
            confirmar_exclusao = st.checkbox(f"Estou ciente e concordo em remover permanentemente o evento '{ev_gerenciar['nome']}'")
            btn_deletar_tudo = st.button("Eliminar Registro Definitivamente", type="primary", disabled=not confirmar_exclusao)
            
            if btn_deletar_tudo:
                sql_deletar_evento = "DELETE FROM eventos WHERE id = %s;"
                if executar_query(sql_deletar_evento, (ev_gerenciar["id"],), is_write=True, role=role_contexto):
                    st.error("O evento e os dados correlatos foram expurgados da base de dados.")
                    st.rerun()
