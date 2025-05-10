import streamlit as st
import json
import gspread
from google.oauth2.service_account import Credentials
import secrets
import string

# --- Google Sheets認証 ---
service_account_info = {
    "type": st.secrets["GSHEET_TYPE"],
    "project_id": st.secrets["GSHEET_PROJECT_ID"],
    "private_key_id": st.secrets["GSHEET_PRIVATE_KEY_ID"],
    "private_key": st.secrets["GSHEET_PRIVATE_KEY"],
    "client_email": st.secrets["GSHEET_CLIENT_EMAIL"],
    "client_id": st.secrets["GSHEET_CLIENT_ID"],
    "auth_uri": st.secrets["GSHEET_AUTH_URI"],
    "token_uri": st.secrets["GSHEET_TOKEN_URI"],
    "auth_provider_x509_cert_url": st.secrets["GSHEET_AUTH_PROVIDER_X509_CERT_URL"],
    "client_x509_cert_url": st.secrets["GSHEET_CLIENT_X509_CERT_URL"]
}

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = Credentials.from_service_account_info(service_account_info, scopes=scope)
gc = gspread.authorize(credentials)
sheet = gc.open("streamlit_codes").worksheet("codes")  # シート名に合わせてください

# --- 認証コード生成 ---
def generate_code():
    return '-'.join(
        ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(4))
        for _ in range(2)
    )

# --- Webhook受信 ---
st.title("Stripe Webhook 受信アプリ")

payload = st.text_area("ここにStripeからのJSONを貼り付けてテストできます", height=200)
if st.button("コードを登録する"):
    try:
        data = json.loads(payload)
        # 実際の運用では data["type"] == "checkout.session.completed" を確認する
        code = generate_code()
        sheet.append_row([code, "FALSE"])
        st.success(f"コード {code} を登録しました。")
    except Exception as e:
        st.error(f"エラーが発生しました: {e}")
