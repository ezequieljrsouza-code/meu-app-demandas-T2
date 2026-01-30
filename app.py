import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime

# Configuração da Página
st.set_page_config(page_title="Report Operacional SPA1", page_icon="📦", layout="wide")

# --- 1. ESTILIZAÇÃO CSS (Esconder Menus) ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} 
    footer {visibility: hidden;} 
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    div.stButton > button:first-child[kind="primary"] {
        background-color: #007bff !important; border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. NOME NO TOPO ---
st.markdown('<div style="text-align: right; color: grey; font-weight: bold;">Ezequiel Miranda</div>', unsafe_allow_html=True)

# Título
st.title("📦 Report Operacional - SPA1 T2")

# --- DADOS AUTOMÁTICOS ---
data_hoje = datetime.now().strftime("%d/%m/%Y")

# --- OPÇÕES DE STATUS ---
status_opts = ["🔴", "🟡", "🟢"]

# --- FUNÇÃO AJUDANTE PARA LAYOUT (SEM PORCENTAGEM) ---
def area_section(titulo, key_prefix):
    st.markdown(f"**{titulo}**")
    c1, c2 = st.columns(2)
    with c1:
        s_org = st.selectbox("Org. Ruas", status_opts, key=f"{key_prefix}_org_status", index=1)
    with c2:
        s_qr = st.selectbox("Etiq. QRs", status_opts, key=f"{key_prefix}_qr_status", index=1)
    return s_org, s_qr

# ==========================================
# FORMULÁRIO
# ==========================================

# Usamos abas para organizar melhor visualmente
tab1, tab2, tab3 = st.tabs(["🏭 Layout", "👷 Operacional", "📝 Presença"])

with tab1:
    st.markdown("### Status Layout / Áreas")
    gxpt_s_org, gxpt_s_qr = area_section("Gaiolas XPT", "gxpt")
    st.divider()
    vxpt_s_org, vxpt_s_qr = area_section("Volumoso XPT", "vxpt")
    st.divider()
    gsvc_s_org, gsvc_s_qr = area_section("Gaiolas SVC", "gsvc")
    st.divider()
    vsvc_s_org, vsvc_s_qr = area_section("Volumoso SVC", "vsvc")
    st.divider()
    gol_s_org, gol_s_qr = area_section("Goleiro", "gol")

with tab2:
    st.markdown("### Report Operacional - PSs")
    c_resp1, c_resp2 = st.columns(2)
    
    with c_resp1:
        dev_xpt_nome = st.text_input("Devolução de XPT", "Luis Felipe")
        dev_xpt_status = st.selectbox("Status ", status_opts, key="dev_xpt_st", index=1)
        
        avarias_nome = st.text_input("Avarias", "Ney")
        avarias_status = st.selectbox("Status ", status_opts, key="avarias_st", index=1)
        
        retorno_nome = st.text_input("Retorno a Estação", "Ney / Rauan")
        retorno_status = st.selectbox("Status ", status_opts, key="retorno_st", index=1)
        
        sem_id_nome = st.text_input("Sem Identificação", "Dharlyson")
        sem_id_status = st.selectbox("Status ", status_opts, key="sem_id_st", index=1)

    with c_resp2:
        backlog_nome = st.text_input("Backlog Volumoso", "Ney")
        backlog_status = st.selectbox("Status ", status_opts, key="backlog_st", index=2) # Verde
        
        receb_nome = st.text_input("Recebimento Pacotes", "Oliverrah / Robert")
        receb_status = st.selectbox("Status ", status_opts, key="receb_st", index=1)
        
        st.write("Inventário")
        inv_status = st.selectbox("Status Inventário", status_opts, key="inv_st", index=0) # Vermelho

with tab3:
    st.markdown("### Resumo de Presença")
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

st.markdown("---")

# ==========================================
# BOTÃO DE GERAR E COPIAR
# ==========================================

# Montagem do Texto (F-String)
texto_final = f"""Status Layout 
🔴 Não iniciado
🟡 Em andamento 
🟢 Finalizado 

"{data_hoje}" - SPA1 - T2 - Demandas

Gaiolas XPT
{gxpt_s_org} Organização das ruas
{gxpt_s_qr} Etiquetas de Qrs

Volumoso XPT 
{vxpt_s_org} Organização das ruas
{vxpt_s_qr} Etiquetas de Qrs

Gaiolas SVC 
{gsvc_s_org} Organização das ruas
{gsvc_s_qr} Etiquetas de Qrs

Volumoso SVC 
{vsvc_s_org} Organização das ruas
{vsvc_s_qr} Etiquetas de Qrs

Goleiro
{gol_s_org}  Organização das ruas
{gol_s_qr} Etiquetas de Qrs

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

# Exibição do texto gerado
st.text_area("Pré-visualização (Copie usando o botão verde abaixo)", texto_final, height=300)

# --- JAVASCRIPT PARA COPIAR ---
# Tratamento para quebras de linha no JavaScript
texto_js = texto_final.replace("\n", "\\n").replace('"', '\\"')

js_code = f"""
<script>
function copiarTexto() {{
    const textToCopy = `{texto_final}`;
    navigator.clipboard.writeText(textToCopy).then(() => {{
        // Feedback visual simples pode ser adicionado aqui
    }});
}}
</script>
<button 
    style="width:100%; background:#25D366; color:white; border:none; padding:15px; border-radius:10px; font-weight:bold; font-size:16px; cursor:pointer;" 
    onclick="copiarTexto()">
    COPIAR PARA WHATSAPP 📲
</button>
"""
components.html(js_code, height=80)
