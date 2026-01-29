import streamlit as st
from datetime import datetime

# Configuração da Página
st.set_page_config(page_title="Report Operacional SPA1", page_icon="📋", layout="wide")

# Título
st.title("📋 Gerador de Report - SPA1 T2")
st.markdown("Preencha os dados abaixo para gerar a mensagem padrão.")

# --- DADOS AUTOMÁTICOS ---
data_hoje = datetime.now().strftime("%d/%m/%Y")

# --- OPÇÕES DE STATUS ---
status_opts = ["🔴", "🟡", "🟢"]
status_legenda = {"🔴": "Não iniciado/Pendente", "🟡": "Em andamento", "🟢": "Finalizado"}

# --- FUNÇÃO AJUDANTE PARA LAYOUT ---
def area_section(titulo, key_prefix):
    st.subheader(titulo)
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown("**Organização das ruas**")
        s_org = st.selectbox("Status", status_opts, key=f"{key_prefix}_org_status", index=1) # Default Amarelo
        p_org = st.number_input("% Conclusão", 0, 100, 100, key=f"{key_prefix}_org_pct")
    
    with c2:
        st.markdown("**Etiquetas de Qrs**")
        s_qr = st.selectbox("Status", status_opts, key=f"{key_prefix}_qr_status", index=1)
        p_qr = st.number_input("% Conclusão", 0, 100, 100, key=f"{key_prefix}_qr_pct")
        
    return s_org, p_org, s_qr, p_qr

# ==========================================
# FORMULÁRIO DE PREENCHIMENTO
# ==========================================

with st.form("report_form"):
    
    # --- SEÇÃO 1: ÁREAS ---
    st.markdown("### 📦 Status Layout / Áreas")
    
    # Gaiolas XPT
    gxpt_org_s, gxpt_org_p, gxpt_qr_s, gxpt_qr_p = area_section("Gaiolas XPT", "gxpt")
    st.divider()
    
    # Volumoso XPT
    vxpt_org_s, vxpt_org_p, vxpt_qr_s, vxpt_qr_p = area_section("Volumoso XPT", "vxpt")
    st.divider()
    
    # Gaiolas SVC
    gsvc_org_s, gsvc_org_p, gsvc_qr_s, gsvc_qr_p = area_section("Gaiolas SVC", "gsvc")
    st.divider()

    # Volumoso SVC
    vsvc_org_s, vsvc_org_p, vsvc_qr_s, vsvc_qr_p = area_section("Volumoso SVC", "vsvc")
    st.divider()
    
    # Goleiro
    gol_org_s, gol_org_p, gol_qr_s, gol_qr_p = area_section("Goleiro", "gol")
    st.divider()

    # --- SEÇÃO 2: RESPONSÁVEIS (REPORT OPERACIONAL) ---
    st.markdown("### 👷 Report Operacional - PSs")
    
    c_resp1, c_resp2 = st.columns(2)
    
    with c_resp1:
        dev_xpt_nome = st.text_input("Devolução de XPT (Nome)", "Luis Felipe")
        dev_xpt_status = st.selectbox("Status", status_opts, key="dev_xpt_st", index=1)
        
        avarias_nome = st.text_input("Avarias (Nome)", "Ney")
        avarias_status = st.selectbox("Status", status_opts, key="avarias_st", index=1)
        
        retorno_nome = st.text_input("Retorno a Estação", "Ney / Rauan")
        retorno_status = st.selectbox("Status", status_opts, key="retorno_st", index=1)
        
        sem_id_nome = st.text_input("Sem Identificação", "Dharlyson")
        sem_id_status = st.selectbox("Status", status_opts, key="sem_id_st", index=1)

    with c_resp2:
        backlog_nome = st.text_input("Backlog Volumoso", "Ney")
        backlog_status = st.selectbox("Status", status_opts, key="backlog_st", index=2) # Default Verde
        
        receb_nome = st.text_input("Recebimento Pacotes", "Oliverrah / Robert")
        receb_status = st.selectbox("Status", status_opts, key="receb_st", index=1)
        
        inv_status = st.selectbox("Inventário (Status)", status_opts, key="inv_st", index=0) # Default Vermelho

    st.divider()

    # --- SEÇÃO 3: RESUMO DE PRESENÇA ---
    st.markdown("### 📝 Resumo de Presença")
    
    col_p1, col_p2, col_p3 = st.columns(3)
    with col_p1:
        pres_log = st.number_input("✅ Presentes Log/PT", value=50)
        diarista_sol = st.number_input("✅ Diaristas Solicitados", value=12)
        diarista_pres = st.number_input("✅ Diaristas Presentes", value=12)
    with col_p2:
        atestados = st.number_input("📄 Atestados", value=1)
        faltas = st.number_input("❌ Faltas", value=8)
        pulmao = st.number_input("🫁 Pulmão", value=1)
    with col_p3:
        folgas = st.number_input("🛌 Folgas", value=8)
        suspensoes = st.number_input("⚠ Suspensões", value=0)

    # Botão de Gerar
    submit_button = st.form_submit_button(label='✨ Gerar Relatório')

# ==========================================
# GERAÇÃO DO TEXTO FINAL
# ==========================================

if submit_button:
    # Montagem do Texto
    texto_final = f"""Status Layout 
🔴 Não iniciado
🟡 Em andamento 
🟢 finalizado 

"{data_hoje}" - SPA1 - T2 - Demandas

Gaiolas XPT
{gxpt_org_s} Organização das ruas {gxpt_org_p}%
{gxpt_qr_s} Etiquetas de Qrs {gxpt_qr_p}%

Volumoso XPT 
{vxpt_org_s} Organização das ruas {vxpt_org_p}%
{vxpt_qr_s} Etiquetas de Qrs {vxpt_qr_p}%

Gaiolas SVC 
{gsvc_org_s} Organização das ruas {gsvc_org_p}%
{gsvc_qr_s} Etiquetas de Qrs {gsvc_qr_p}%

Volumoso SVC 
{vsvc_org_s} Organização das ruas {vsvc_org_p}%
{vsvc_qr_s} Etiquetas de Qrs {vsvc_qr_p}%

Goleiro-
{gol_org_s}  Organização das ruas {gol_org_p}%
{gol_qr_s} Etiquetas de Qrs {gol_qr_p}%

REPORT OPERACIONAL - PSs
Legenda: 🟢 Finalizado | 🟡 Em andamento | 🔴 Pendente
📅 Data: {data_hoje}
Responsáveis por categoria hoje:
🔹 Devolução de XPT: {dev_xpt_nome} {dev_xpt_status}
🔹 Avarias: {avarias_nome} {avarias_status}
🔹 Retorno a Estação: {retorno_nome} {retorno_status}
🔹 Sem Identificação: {sem_id_nome} {sem_id_status}
🔹Backlog volumoso : {backlog_nome} {backlog_status}
🔹Recebimento de Pacotes : {receb_nome} {receb_status}
🔹Inventário: {inv_status}

*RESUMO DE PRESENÇA*
"{data_hoje}" - SPA1 - T2

✅ Presentes Log/PT: {pres_log}
✅ Diaristas Solicitados: {diarista_sol}
✅ Diaristas Presentes: {diarista_pres}
📄 Atestados: {atestados}
❌ Faltas: {faltas}
🫁 Pulmão: {pulmao}
🛌 Folgas: {folgas:02d}
⚠ Suspensões: {suspensoes}
"""
    
    st.success("Relatório gerado com sucesso! Copie abaixo:")
    st.code(texto_final, language="text")
