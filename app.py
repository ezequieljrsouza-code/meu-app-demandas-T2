import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
from google.cloud import firestore
from google.oauth2 import service_account
import json

# Configuração da Página
st.set_page_config(page_title="Report Operacional SPA1", page_icon="📦", layout="wide")

# --- CONEXÃO FIREBASE ---
@st.cache_resource
def get_db():
    key_dict = json.loads(st.secrets["firestore_key"])
    creds = service_account.Credentials.from_service_account_info(key_dict)
    return firestore.Client(credentials=creds, project=key_dict['project_id'])

db = get_db()

def salvar_dados(dados):
    db.collection("reports").document("atual").set(dados)

def carregar_dados():
    doc = db.collection("reports").document("atual").get()
    return doc.to_dict() if doc.exists else {}

# --- CSS E NOME ---
st.markdown("<style>#MainMenu, footer, header {visibility: hidden;} .stDeployButton {display:none;}</style>", unsafe_allow_html=True)
st.markdown('<div style="text-align: right; color: grey; font-weight: bold;">Ezequiel Miranda</div>', unsafe_allow_html=True)

# --- INICIALIZAÇÃO DE ESTADO ---
if 'form_data' not in st.session_state:
    dados_nuvem = carregar_dados()
    st.session_state.form_data = dados_nuvem if dados_nuvem else {}

# Interface
st.title("📦 Report Operacional - Cloud")
data_hoje = datetime.now().strftime("%d/%m/%Y")
status_opts = ["🔴", "🟡", "🟢"]

# Exemplo de campo conectado ao Firebase
def input_sync(label, key, default_val="", is_select=False):
    val_atual = st.session_state.form_data.get(key, default_val)
    if is_select:
        idx = status_opts.index(val_atual) if val_atual in status_opts else 0
        res = st.selectbox(label, status_opts, index=idx, key=f"input_{key}")
    else:
        res = st.text_input(label, val_atual, key=f"input_{key}")
    
    if res != val_atual:
        st.session_state.form_data[key] = res
        salvar_dados(st.session_state.form_data)
    return res

# --- FORMULÁRIO (Simplificado para o exemplo) ---
tab1, tab2 = st.tabs(["🏭 Layout", "👷 Operacional"])

with tab1:
    st.subheader("Gaiolas XPT")
    g_org = input_sync("Org. Ruas", "gxpt_org", is_select=True)
    g_qr = input_sync("Etiq. QRs", "gxpt_qr", is_select=True)

with tab2:
    resp_dev = input_sync("Responsável Devolução", "resp_dev", "Luis Felipe")
    status_dev = input_sync("Status Devolução", "status_dev", "🟡", is_select=True)

# --- BOTÃO COPIAR ---
# (Aqui você usaria a mesma lógica de montagem da string 'texto_final' anterior)
texto_final = f"Report SPA1 - {data_hoje}\n\nGaiolas XPT:\n{g_org} Org. Ruas\n{g_qr} QRs\n\nResp: {resp_dev} {status_dev}"

st.divider()
js_code = f"""
<script>
function copiar() {{ navigator.clipboard.writeText(`{texto_final}`); }}
</script>
<button style="width:100%; background:#25D366; color:white; border:none; padding:15px; border-radius:10px; cursor:pointer;" onclick="copiar()">COPIAR WHATSAPP</button>
"""
components.html(js_code, height=80)

if st.button("🔄 Forçar Sincronização"):
    st.rerun()
