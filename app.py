import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
from google.cloud import firestore
from google.oauth2 import service_account
import json

# 1. Configuração da Página
st.set_page_config(page_title="Report Operacional SPA1", page_icon="📋", layout="wide")

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
        # Pega o documento atual do banco
        doc = db.collection("reports").document("atual").get()
        return doc.to_dict() if doc.exists else {}
    except: return {}

# 3. Estilo e Nome
st.markdown("<style>#MainMenu, footer, header {visibility: hidden;} .stDeployButton {display:none;}</style>", unsafe_allow_html=True)
st.markdown('<div style="text-align: right; color: grey; font-weight: bold;">Ezequiel Miranda</div>', unsafe_allow_html=True)

# 4. Inicialização de Estado e Função de Update
if 'form_data' not in st.session_state:
    st.session_state.form_data = carregar()

def update(key):
    # Atualiza o estado local com o valor do input e salva no banco
    st.session_state.form_data[key] = st.session_state[f"in_{key}"]
    salvar(st.session_state.form_data)

# --- CABEÇALHO E SINCRONIZAÇÃO ---
col_t, col_s = st.columns([3, 1])
with col_t:
    st.title("📋 Report Operacional SPA1")
    st.write(f"Analista: **Ezequiel Miranda**")
with col_s:
    st.write("##")
    # Botão Sincronizar: Recarrega do banco e reinicia a página para atualizar textos
    if st.button("🔄 Sincronizar", use_container_width=True, type="primary"):
        st.session_state.form_data = carregar()
        st.toast("Dados atualizados com sucesso!", icon="✅")
        st.rerun()

# 5. Variáveis Globais
data_hoje = datetime.now().strftime("%d/%m/%Y")
status_opts = ["🔴", "🟡", "🟢"]
f = st.session_state.form_data # Atalho para facilitar leitura

tab1, tab2, tab3 = st.tabs(["🏭 Layout", "👷 Operacional", "📝 Presença"])

# --- ABA 1: LAYOUT ---
with tab1:
    def area(label, k):
        st.markdown(f"**{label}**")
        c1, c2 = st.columns(2)
        # O index busca o valor atual no form_data. Se não achar, usa padrão.
        c1.selectbox("Org. Ruas", status_opts, key=f"in_{k}_o", index=status_opts.index(f.get(f"{k}_o", "🟡")), on_change=update, args=(f"{k}_o",))
        c2.selectbox("Etiq. QRs", status_opts, key=f"in_{k}_q", index=status_opts.index(f.get(f"{k}_q", "🟡")), on_change=update, args=(f"{k}_q",))
    
    area("Gaiolas XPT", "gx")
    area("Volumoso XPT", "vx")
    area("Gaiolas SVC", "gs")
    area("Volumoso SVC", "vs")
    area("Goleiro", "go")

# --- ABA 2: OPERACIONAL ---
with tab2:
    st.subheader("Responsáveis e Status")
    
    def resp_row(label, k, d_n):
        c_nome, c_status = st.columns([3, 1]) # Layout 75% / 25%
        with c_nome:
            st.text_input(label, key=f"in_{k}_n", value=f.get(f"{k}_n", d_n), on_change=update, args=(f"{k}_n",))
        with c_status:
            st.selectbox(f"Status {label}", status_opts, key=f"in_{k}_s", index=status_opts.index(f.get(f"{k}_s", "🟡")), on_change=update, args=(f"{k}_s",), label_visibility="visible")
        st.markdown("---")

    resp_row("Devolução XPT", "d", "Luis Felipe")
    resp_row("Sem Identificação", "s", "Dharlyson")
    resp_row("Avarias", "a", "Ney")
    resp_row("Backlog Volumoso", "b", "Ney")
    resp_row("Retorno Estação", "r", "Ney / Rauan")
    resp_row("Recebimento", "p", "Oliverrah / Robert")
    
    c_inv_l, c_inv_s = st.columns([3, 1])
    with c_inv_l: st.write("**Inventário**")
    with c_inv_s: st.selectbox("Status Inventário", status_opts, key="in_inv", index=status_opts.index(f.get("inv", "🔴")), on_change=update, args=("inv",), label_visibility="collapsed")

# --- ABA 3: PRESENÇA ---
with tab3:
    st.markdown("### Dados de PSs")
    c_ps1, c_ps2 = st.columns(2)
    with c_ps1:
        st.number_input("✅ PSs Presentes", key="in_pss_p", value=int(f.get("pss_p", 0)), on_change=update, args=("pss_p",))
    with c_ps2:
        st.number_input("✅ PSs de Folga", key="in_pss_f", value=int(f.get("pss_f", 0)), on_change=update, args=("pss_f",))
    
    st.markdown("---")
    st.markdown("### Dados Gerais")
    c1, c2, c3 = st.columns(3)
    p_campos = [("Presentes (Log)", "p1", 50), ("Diaristas Sol.", "p2", 12), ("Diaristas Pres.", "p3", 12),
                ("Atestados", "p4", 1), ("Faltas", "p5", 8), ("Pulmão", "p6", 1),
                ("Folgas", "p7", 8), ("Suspensões", "p8", 0)]
    for i, (l, k, d) in enumerate(p_campos):
        [c1, c2, c3][i%3].number_input(l, key=f"in_{k}", value=int(f.get(k, d)), on_change=update, args=(k,))

# --- GERAÇÃO DE TEXTO E CÓPIA ---
txt_layout = f"""Status Layout 
🔴 Não iniciado | 🟡 Em andamento | 🟢 Finalizado 

Gaiolas XPT: {f.get('gx_o','🟡')} Org. Ruas | {f.get('gx_q','🟡')} QRs
Volumoso XPT: {f.get('vx_o','🟡')} Org. Ruas | {f.get('vx_q','🟡')} QRs
Gaiolas SVC: {f.get('gs_o','🟡')} Org. Ruas | {f.get('gs_q','🟡')} QRs
Volumoso SVC: {f.get('vs_o','🟡')} Org. Ruas | {f.get('vs_q','🟡')} QRs
Goleiro: {f.get('go_o','🟡')} Org. Ruas | {f.get('go_q','🟡')} QRs"""

txt_operacional = f"""REPORT OPERACIONAL DE PSs T2 - Demandas
📅 Data: {data_hoje}
🔹 Devolução: {f.get('d_n','Luis Felipe')} {f.get('d_s','🟡')}
🔹 Avarias: {f.get('a_n','Ney')} {f.get('a_s','🟡')}
🔹 Retorno: {f.get('r_n','Ney/Rauan')} {f.get('r_s','🟡')}
🔹 Sem ID: {f.get('s_n','Dharlyson')} {f.get('s_s','🟡')}
🔹 Backlog: {f.get('b_n','Ney')} {f.get('b_s','🟢')}
🔹 Recebimento: {f.get('p_n','Oliverrah')} {f.get('p_s','🟡')}
🔹 Inventário: {f.get('p_n','Oliverrah')} {f.get('inv','🔴')}"""

# CORREÇÃO AQUI: Adicionado o campo Suspensões (p8)
txt_presenca = f"""*RESUMO DE PRESENÇA*
✅ PSs Presentes: {f.get('pss_p', 0)}
✅ PSs de Folga: {f.get('pss_f', 0)}
✅ Log: {f.get('p1',50)} | ✅ Diaristas: {f.get('p3',12)}/{f.get('p2',12)}
📄 Atestados: {f.get('p4',1)} | ❌ Faltas: {f.get('p5',8)}
🫁 Pulmão: {f.get('p6',1)} | 🛌 Folgas: {int(f.get('p7',8))}
⚠ Suspensões: {f.get('p8',0)}"""

txt_completo = f"{txt_layout}\n\n{txt_operacional}\n\n{txt_presenca}"

st.divider()
st.subheader("🚀 Relatório Final")
st.text_area("Confira o texto:", txt_completo, height=700)

# Tratamento para JavaScript
txt_js = txt_completo.replace("\n", "\\n").replace("'", "\\'")
js_code = f"""
<script>
function cp(){{
    const text = `{txt_js}`;
    navigator.clipboard.writeText(text).then(() => alert('Copiado! ✅'));
}}
</script>
<button style='width:100%; background:#25D366; color:white; border:none; padding:18px; border-radius:10px; font-weight:bold; font-size:18px; cursor:pointer;' onclick='cp()'>
    COPIAR PARA WHATSAPP 📲
</button>
"""
components.html(js_code, height=100)
