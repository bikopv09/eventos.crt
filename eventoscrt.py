import streamlit as st
from datetime import datetime, time

# Configuração inicial da página
st.set_page_config(page_title="Eventos.CRT - Sistema de Gestão", layout="wide")

# Inicialização do banco de dados temporário (na memória)
if 'eventos' not in st.session_state:
    st.session_state.eventos = []

if 'inscricoes' not in st.session_state:
    st.session_state.inscricoes = []

if 'missing_fields' not in st.session_state:
    st.session_state.missing_fields = []

# Menu de navegação lateral
st.sidebar.title("Navegação Sistema")
area_selecionada = st.sidebar.radio(
    "Escolha a área:", 
    ["1. Criar Evento (Gestão)", "2. Área de Inscrição (Público)", "3. Painel do Organizador (Controle)"]
)

st.sidebar.markdown("---")
st.sidebar.info("Eventos.CRT - Versão Atualizada")

# ---------------------------------------------------------
# ÁREA 1: CRIAÇÃO DO EVENTO (GESTÃO)
# ---------------------------------------------------------
if area_selecionada == "1. Criar Evento (Gestão)":
    st.header("⚙️ Área de Gestão: Criar Novo Evento")
    st.write("Preencha os detalhes do evento e defina o público-alvo.")
    
    with st.form("form_criacao_evento", clear_on_submit=True):
        nome_evento = st.text_input("Nome do Evento *")
        descricao_evento = st.text_area("Descrição detalhada do Evento")
        
        col1, col2 = st.columns(2)
        with col1:
            data_evento = st.date_input("Data do Evento", value=datetime.now().date())
        with col2:
            horario_evento = st.time_input("Horário do Evento", value=time(19, 0))
        
        categoria_evento = st.selectbox(
            "Modalidade do Evento *",
            ["Selecione...", "CRT-ES na Escola", "Sistema CFT/CRTs", "Público Geral"]
        )
        
        st.markdown("### Mídias de Divulgação")
        capa_arquivo = st.file_uploader("Imagem de Capa (Cabeçalho da Inscrição)", type=["png", "jpg", "jpeg"])
        video_url = st.text_input("Link do Vídeo de Divulgação (YouTube, Vimeo ou link direto)")
        
        submit_evento = st.form_submit_button("Publicar Evento")
        
        if submit_evento:
            if categoria_evento == "Selecione..." or not nome_evento:
                st.error("Nome do Evento e Modalidade são campos obrigatórios!")
            else:
                # Ler bytes da imagem se houver upload
                imagem_bytes = capa_arquivo.getvalue() if capa_arquivo is not None else None
                
                novo_evento = {
                    "id": int(datetime.now().timestamp()), # ID Único baseado no tempo
                    "nome": nome_evento,
                    "descricao": descricao_evento,
                    "data": data_evento.strftime("%d/%m/%Y"),
                    "horario": horario_evento.strftime("%H:%M"),
                    "categoria": categoria_evento,
                    "imagem_capa": imagem_bytes,
                    "video_url": video_url
                }
                st.session_state.eventos.append(novo_evento)
                st.success(f"Evento '{nome_evento}' publicado com sucesso!")

# ---------------------------------------------------------
# ÁREA 2: INSCRIÇÃO (PÚBLICO)
# ---------------------------------------------------------
elif area_selecionada == "2. Área de Inscrição (Público)":
    st.header("📝 Portal de Inscrições em Eventos")
    
    # Toggle para modo organizador na própria página de inscrição
    modo_organizador_view = st.toggle("👁️ Visualizar como ORGANIZADOR (Permite apagar inscrições nesta tela)")
    
    if not st.session_state.eventos:
        st.warning("Nenhum evento com inscrições abertas no momento.")
    else:
        opcoes_eventos = {f"{e['nome']} ({e['data']} às {e['horario']})": e for e in st.session_state.eventos}
        evento_selecionado_str = st.selectbox("Selecione o evento que deseja se inscrever:", list(opcoes_eventos.keys()))
        evento_atual = opcoes_eventos[evento_selecionado_str]
        
        # EXIBIÇÃO DO EVENTO (Layout e Mídias)
        st.markdown(f"## {evento_atual['nome']}")
        st.info(f"**Modalidade:** {evento_atual['categoria']} | **Data:** {evento_atual['data']} às {evento_atual['horario']}")
        
        if evento_atual['imagem_capa']:
            st.image(evento_atual['imagem_capa'], use_container_width=True)
            
        if evento_atual['descricao']:
            st.markdown(f"### Sobre o Evento\n{evento_atual['descricao']}")
            
        if evento_atual['video_url']:
            st.markdown("### Vídeo de Divulgação")
            try:
                st.video(evento_atual['video_url'])
            except:
                st.warning("Não foi possível carregar o vídeo. Verifique se a URL está correta.")
        
        st.markdown("---")
        st.subheader("Formulário de Inscrição")
        
        # Lógica de coloração vermelha para campos obrigatórios não preenchidos
        lbl_nome = "Nome Completo *" if "nome" not in st.session_state.missing_fields else ":red[Nome Completo * (Campo Obrigatório)]"
        lbl_telefone = "Telefone / Celular com DDD *" if "telefone" not in st.session_state.missing_fields else ":red[Telefone / Celular com DDD * (Campo Obrigatório)]"
        lbl_cpf = "CPF *" if "cpf" not in st.session_state.missing_fields else ":red[CPF * (Campo Obrigatório)]"
        lbl_email = "E-mail *" if "email" not in st.session_state.missing_fields else ":red[E-mail * (Campo Obrigatório)]"
        lbl_idade = "Idade *" if "idade" not in st.session_state.missing_fields else ":red[Idade * (Campo Obrigatório)]"
        lbl_termo = "Eu AUTORIZO o uso de minha imagem em materiais do CRT-ES *" if "termo" not in st.session_state.missing_fields else ":red[Eu AUTORIZO o uso de minha imagem em materiais do CRT-ES * (Aceite Obrigatório)]"

        # FORMULÁRIO DE INSCRIÇÃO
        with st.form("form_inscricao"):
            # Campos Obrigatórios Globais
            val_nome = st.text_input(lbl_nome, key="ins_nome")
            val_cpf = st.text_input(lbl_cpf, key="ins_cpf")
            val_email = st.text_input(lbl_email, key="ins_email")
            val_telefone = st.text_input(lbl_telefone, key="ins_telefone")
            val_idade = st.number_input(lbl_idade, min_value=0, max_value=120, value=0, key="ins_idade")
            
            # CAMPOS ESPECÍFICOS POR MODALIDADE
            if evento_atual["categoria"] == "CRT-ES na Escola":
                st.markdown("#### Informações Escolares Adicionais")
                escola = st.text_input("Nome da escola técnica:")
                curso = st.text_input("Qual o seu Curso Técnico?")
                cidade = st.text_input("Qual cidade você mora?")
                ano_conclusao = st.text_input("Ano de Conclusão do Curso")
                st.radio("Você trabalha atualmente?", ["Sim", "Não"], key="ins_trabalha")
                st.text_area("Quais suas expectativas após se formar? Pretende trabalhar na área?")
                st.checkbox("Deseja receber contato do CRT-ES após concluir o curso para registro profissional?")
            
            elif evento_atual["categoria"] == "Sistema CFT/CRTs":
                st.markdown("#### Informações Corporativas")
                locais = ["CFT", "CRT-01", "CRT-02", "CRT-03", "CRT-05", "CRT-06", "CRT-07", "CRT-08", "CRT-RN", "CRT-RS", "CRT-RJ", "CRT-SP", "CRT-ES", "CRT-MG", "CRT-BA", "CRT-PR", "CRT-SC"]
                st.selectbox("De qual local do SISTEMA CFT/CRTs você veio?", locais)
                st.checkbox("Confirmo minha presença no evento institucional.")
            
            elif evento_atual["categoria"] == "Público Geral":
                st.markdown("#### Informações Profissionais")
                st.text_input("Profissão")
                st.text_input("Empresa/Escola")
            
            st.markdown("---")
            val_termo = st.checkbox(lbl_termo, key="ins_termo")
            
            submit_inscricao = st.form_submit_button("Confirmar Minha Inscrição")
            
            if submit_inscricao:
                # Validação estrita dos campos requeridos
                erros = []
                if not st.session_state.ins_nome.strip(): erros.append("nome")
                if not st.session_state.ins_telefone.strip(): erros.append("telefone")
                if not st.session_state.ins_cpf.strip(): erros.append("cpf")
                if not st.session_state.ins_email.strip(): erros.append("email")
                if st.session_state.ins_idade == 0: erros.append("idade")
                if not st.session_state.ins_termo: erros.append("termo")
                
                if erros:
                    st.session_state.missing_fields = erros
                    st.error("🚨 Não foi possível confirmar a inscrição. Faltam campos obrigatórios!")
                    st.rerun()
                else:
                    st.session_state.missing_fields = [] # Limpa erros
                    nova_inscricao = {
                        "id": int(datetime.now().timestamp()),
                        "evento_id": evento_atual["id"],
                        "nome": st.session_state.ins_nome,
                        "cpf": st.session_state.ins_cpf,
                        "email": st.session_state.ins_email,
                        "telefone": st.session_state.ins_telefone,
                        "idade": st.session_state.ins_idade
                    }
                    st.session_state.inscricoes.append(nova_inscricao)
                    st.success("🎉 Inscrição confirmada com sucesso!")
                    st.balloons()
                    
        # VISÃO DE MODERAÇÃO DO ORGANIZADOR NA ÁREA DE INSCRIÇÃO
        if modo_organizador_view:
            st.markdown("---")
            st.subheader("🛠️ Moderação Rápida de Inscritos (Visão do Organizador)")
            inscritos_deste_evento = [i for i in st.session_state.inscricoes if i["evento_id"] == evento_atual["id"]]
            
            if not inscritos_deste_evento:
                st.info("Nenhuma inscrição realizada neste evento ainda.")
            else:
                for inscrito in inscritos_deste_evento:
                    col_info, col_acao = st.columns([4, 1])
                    with col_info:
                        st.write(f"👤 **{inscrito['nome']}** | CPF: {inscrito['cpf']} | Tel: {inscrito['telefone']}")
                    with col_acao:
                        if st.button("Apagar Inscrição", key=f"del_fast_{inscrito['id']}", type="primary"):
                            st.session_state.inscricoes.remove(inscrito)
                            st.toast(f"Inscrição de {inscrito['nome']} removida!")
                            st.rerun()

# ---------------------------------------------------------
# ÁREA 3: PAINEL DO ORGANIZADOR (CONTROLE TOTAL)
# ---------------------------------------------------------
elif area_selecionada == "3. Painel do Organizador (Controle)":
    st.header("📊 Painel de Controle e Auditoria")
    st.write("Gerencie eventos ativos, edite informações ou remova registros do sistema.")
    
    if not st.session_state.eventos:
        st.warning("Não há eventos cadastrados no sistema para gerenciamento.")
    else:
        opcoes_gerenciamento = {f"{e['nome']} [{e['categoria']}]": e for e in st.session_state.eventos}
        selecionado_str = st.selectbox("Selecione o evento que deseja gerenciar:", list(opcoes_gerenciamento.keys()))
        ev_gerenciar = opcoes_gerenciamento[selecionado_str]
        
        tab1, tab2, tab3 = st.tabs(["👥 Lista de Inscritos", "✏️ Editar Evento", "🚨 Zona de Perigo"])
        
        # ABA 1: LISTA DE INSCRITOS
        with tab1:
            inscritos = [i for i in st.session_state.inscricoes if i["evento_id"] == ev_gerenciar["id"]]
            st.subheader(f"Inscritos para: {ev_gerenciar['nome']}")
            st.metric(label="Total de Inscrições Confirmadas", value=len(inscritos))
            
            if not inscritos:
                st.info("Nenhum participante se inscreveu neste evento até o momento.")
            else:
                st.markdown("---")
                for idx, ins in enumerate(inscritos):
                    c1, c2, c3, c4 = st.columns([2, 2, 2, 1])
                    with c1:
                        st.write(f"**Nome:** {ins['nome']} (Idade: {ins['idade']})")
                    with c2:
                        st.write(f"**CPF:** {ins['cpf']}")
                    with c3:
                        st.write(f"**Contato:** {ins['email']} / {ins['telefone']}")
                    with c4:
                        if st.button("Remover", key=f"panel_del_{ins['id']}", type="secondary"):
                            st.session_state.inscricoes.remove(ins)
                            st.success(f"Inscrição de {ins['nome']} removida.")
                            st.rerun()
                            
        # ABA 2: EDITAR EVENTO
        with tab2:
            st.subheader("Editar Propriedades do Evento")
            with st.form(f"form_edit_{ev_gerenciar['id']}"):
                novo_nome = st.text_input("Alterar Nome do Evento", value=ev_gerenciar["nome"])
                nova_desc = st.text_area("Alterar Descrição", value=ev_gerenciar["descricao"])
                nova_data = st.text_input("Alterar Data (Texto)", value=ev_gerenciar["data"])
                novo_horario = st.text_input("Alterar Horário (Texto)", value=ev_gerenciar["horario"])
                nova_cat = st.selectbox("Mudar Modalidade", ["CRT-ES na Escola", "Sistema CFT/CRTs", "Público Geral"], index=["CRT-ES na Escola", "Sistema CFT/CRTs", "Público Geral"].index(ev_gerenciar["categoria"]))
                novo_video = st.text_input("Alterar Link do Vídeo", value=ev_gerenciar["video_url"])
                
                salvar_edicao = st.form_submit_button("Salvar Alterações")
                if salvar_edicao:
                    ev_gerenciar["nome"] = novo_nome
                    ev_gerenciar["descricao"] = nova_desc
                    ev_gerenciar["data"] = nova_data
                    ev_gerenciar["horario"] = novo_horario
                    ev_gerenciar["categoria"] = nova_cat
                    ev_gerenciar["video_url"] = novo_video
                    st.success("Modificações salvas com sucesso!")
                    st.rerun()
                    
        # ABA 3: APAGAR EVENTO COMPLETO
        with tab3:
            st.subheader("Exclusão Permanente")
            st.warning("⚠️ Atenção: Apagar o evento removerá permanentemente o registro e TODAS as inscrições de pessoas associadas a ele.")
            
            confirmar_exclusao = st.checkbox(f"Estou ciente e quero deletar permanentemente o evento '{ev_gerenciar['nome']}'")
            btn_deletar_tudo = st.button("Apagar Evento por Completo", type="primary", disabled=not confirmar_exclusao)
            
            if btn_deletar_tudo:
                # Remove todas as inscrições ligadas ao evento
                st.session_state.inscricoes = [i for i in st.session_state.inscricoes if i["evento_id"] != ev_gerenciar["id"]]
                # Remove o evento da lista
                st.session_state.eventos.remove(ev_gerenciar)
                st.error(f"O evento e todos os seus inscritos foram eliminados do sistema.")
                st.rerun()
