import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
from google.cloud import firestore
from google.oauth2 import service_account
import json

# 1. Configuração da Página
st.set_page_config(page_title="Report Operacional SPA1", page_icon="📋", layout="wide")
st.write(f"Autor: **Ezequiel Miranda**")

# 2. Conexão Firestore
@st.cache_resource
def get_db():
    try:
        key_dict = json.loads(st.secrets["firestore_key"])
        creds = service_account.Credentials.from_service_account_info(key_dict)
        return firestore.Client(credentials=creds, project=key_dict['project_id'])
    except Exception as e:
        st.error(f"Erro de conexão: {e}")
        return None

db = get_db()

def salvar(dados):
    db.collection("reports").document("atual").set(dados)

def carregar():
    try:
        # Forçamos a leitura sem cache para garantir dados novos
        doc = db.collection("reports").document("atual").get()
        return doc.to_dict() if doc.exists else {}
    except: return {}

# 3. CSS e Nome
st.markdown("<style>#MainMenu, footer, header {visibility: hidden;} .stDeployButton {display:none;}</style>", unsafe_allow_html=True)
st.markdown('<div style="text-align: right; color: grey; font-weight: bold;">Ezequiel Miranda</div>', unsafe_allow_html=True)

# 4. Inicialização e Lógica de Sincronia
if 'form_data' not in st.session_state:
    st.session_state.form_data = carregar()

def atualizar_pagina():
    # Limpa o cache e recarrega do banco
    st.session_state.form_data = carregar()
    st.toast("Dados atualizados em tempo real! 🔄", icon="✅")

def update(key):
    st.session_state.form_data[key] = st.session_state[f"in_{key}"]
    salvar(st.session_state.form_data)

# --- TOPO COM BOTÃO DE SINCRONISMO ---
col_tit, col_sync = st.columns([3, 1])
with col_tit:
    st.title("📋 Report Operacional SPA1")
with col_sync:
    st.write("") # Alinhamento
    if st.button("🔄 Sincronizar Agora", use_container_width=True, type="primary"):
        atualizar_pagina()

# 5. Variáveis Globais
data_hoje = datetime.now().strftime("%d/%m/%Y")
status_opts = ["🔴", "🟡", "🟢"]
f = st.session_state.form_data

# 6. Interface por Abas
tab1, tab2, tab3 = st.tabs(["🏭 Layout", "👷 Operacional", "📝 Presença"])

# --- ABA 1: LAYOUT ---
with tab1:
    def area(label, k):
        st.markdown(f"**{label}**")
        c1, c2 = st.columns(2)
        c1.selectbox("Org. Ruas", status_opts, key=f"in_{k}_o", index=status_opts.index(f.get(f"{k}_o", "🟡")), on_change=update, args=(f"{k}_o",))
        c2.selectbox("Etiq. QRs", status_opts, key=f"in_{k}_q", index=status_opts.index(f.get(f"{k}_q", "🟡")), on_change=update, args=(f"{k}_q",))

    area("Gaiolas XPT", "gx")
    area("Volumoso XPT", "vx")
    area("Gaiolas SVC", "gs")
    area("Volumoso SVC", "vs")
    area("Goleiro", "go")

    txt_layout = f"""Status Layout 
🔴 Não iniciado | 🟡 Em andamento | 🟢 finalizado 

"{data_hoje}" - SPA1 - T2 - Demandas

Gaiolas XPT: {f.get('gx_o','🟡')} Org. Ruas | {f.get('gx_q','🟡')} QRs
Volumoso XPT: {f.get('vx_o','🟡')} Org. Ruas | {f.get('vx_q','🟡')} QRs
Gaiolas SVC: {f.get('gs_o','🟡')} Org. Ruas | {f.get('gs_q','🟡')} QRs
Volumoso SVC: {f.get('vs_o','🟡')} Org. Ruas | {f.get('vs_q','🟡')} QRs
Goleiro: {f.get('go_o','🟡')} Org. Ruas | {f.get('go_q','🟡')} QRs"""
    
    st.divider()
    st.text_area("Cópia Parcial Layout", txt_layout, height=150, key="txt_lay")

# --- ABA 2: OPERACIONAL ---
with tab2:
    def resp(label, k, d_n, col):
        with col:
            st.text_input(label, key=f"in_{k}_n", value=f.get(f"{k}_n", d_n), on_change=update, args=(f"{k}_n",))
            st.selectbox(f"Status {label}", status_opts, key=f"in_{k}_s", index=status_opts.index(f.get(f"{k}_s", "🟡")), on_change=update, args=(f"{k}_s",))

    c1, c2 = st.columns(2)
    resp("Devolução XPT", "d", "Luis Felipe", c1)
    resp("Avarias", "a", "Ney", c1)
    resp("Retorno Estação", "r", "Ney / Rauan", c1)
    resp("Sem Identificação", "s", "Dharlyson", c2)
    resp("Backlog Volumoso", "b", "Ney", c2)
    resp("Recebimento", "p", "Oliverrah / Robert", c2)
    c2.selectbox("Inventário", status_opts, key="in_inv", index=status_opts.index(f.get("inv", "🔴")), on_change=update, args=("inv",))

    txt_operacional = f"""REPORT OPERACIONAL
📅 Data: {data_hoje}
🔹 Devolução: {f.get('d_n','Luis Felipe')} {f.get('d_s','🟡')}
🔹 Avarias: {f.get('a_n','Ney')} {f.get('a_s','🟡')}
🔹 Retorno: {f.get('r_n','Ney/Rauan')} {f.get('r_s','🟡')}
🔹 Sem ID: {f.get('s_n','Dharlyson')} {f.get('s_s','🟡')}
🔹 Backlog: {f.get('b_n','Ney')} {f.get('b_s','🟢')}
🔹 Recebimento: {f.get('p_n','Oliverrah')} {f.get('p_s','🟡')}
🔹 Inventário: {f.get('inv','🔴')}"""

    st.divider()
    st.text_area("Cópia Parcial Operacional", txt_operacional, height=150, key="txt_ope")

# --- ABA 3: PRESENÇA ---
with tab3:
    c1, c2, c3 = st.columns(3)
    p_campos = [("Presentes", "p1", 50), ("Diaristas Sol.", "p2", 12), ("Diaristas Pres.", "p3", 12),
                ("Atestados", "p4", 1), ("Faltas", "p5", 8), ("Pulmão", "p6", 1),
                ("Folgas", "p7", 8), ("Suspensões", "p8", 0)]
    for i, (l, k, d) in enumerate(p_campos):
        [c1, c2, c3][i%3].number_input(l, key=f"in_{k}", value=int(f.get(k, d)), on_change=update, args=(k,))

    txt_presenca = f"""*RESUMO DE PRESENÇA*
✅ Log: {f.get('p1',50)} | ✅ Diaristas: {f.get('p3',12)}/{f.get('p2',12)}
📄 Atestados: {f.get('p4',1)} | ❌ Faltas: {f.get('p5',8)}
🫁 Pulmão: {f.get('p6',1)} | 🛌 Folgas: {int(f.get('p7',8)):02d}"""

    st.divider()
    st.text_area("Cópia Parcial Presença", txt_presenca, height=120, key="txt_pre")

# --- RESUMO TOTAL E BOTÃO FINAL ---
st.markdown("---")
st.subheader("🚀 Relatório Completo")
txt_completo = f"{txt_layout}\n\n{txt_operacional}\n\n{txt_presenca}"
st.text_area("Texto final:", txt_completo, height=250)

js_code = f"""
<script>
function cp(){{
    const text = `{txt_completo}`;
    navigator.clipboard.writeText(text).then(() => {{
        alert('Relatório completo copiado! ✅');
    }});
}}
</script>
<button style='width:100%; background:#25D366; color:white; border:none; padding:18px; border-radius:10px; font-weight:bold; font-size:18px; cursor:pointer;' onclick='cp()'>
    COPIAR TUDO PARA WHATSAPP 📲
</button>
"""
components.html(js_code, height=100)
