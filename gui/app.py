import os
import time
import json
import requests
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------------
# Page Configuration & Light Maximalism Styling
# ---------------------------------------------------------
st.set_page_config(
    page_title="Payment Gateway Console | DevOps",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Light Maximalism CSS Injection
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700;800;900&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    /* Global Body & Light Background */
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #FAF8F5 !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: #0F172A !important;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #FFF9F2 0%, #F5EFE6 100%) !important;
        border-right: 3px solid #0F172A !important;
    }

    /* Headings */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 800 !important;
        color: #0F172A !important;
        letter-spacing: -0.5px;
    }

    /* Hero Header Banner */
    .hero-banner {
        background: linear-gradient(135deg, #FF5A5F 0%, #6366F1 50%, #4F46E5 100%);
        padding: 2.2rem 2rem;
        border-radius: 20px;
        border: 3px solid #0F172A;
        box-shadow: 8px 8px 0px #0F172A;
        margin-bottom: 2rem;
        color: #FFFFFF;
        position: relative;
        overflow: hidden;
    }
    .hero-banner h1 {
        color: #FFFFFF !important;
        font-size: 2.6rem !important;
        margin: 0 0 0.4rem 0 !important;
        text-shadow: 2px 2px 0px rgba(0,0,0,0.2);
    }
    .hero-banner p {
        color: #F1F5F9 !important;
        font-size: 1.15rem;
        font-weight: 600;
        margin: 0;
    }

    /* Status Badges */
    .badge-online {
        background: #10B981;
        color: #FFFFFF;
        border: 2px solid #0F172A;
        box-shadow: 3px 3px 0px #0F172A;
        padding: 0.4rem 1rem;
        border-radius: 50px;
        font-weight: 800;
        font-size: 0.9rem;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }
    .badge-offline {
        background: #EF4444;
        color: #FFFFFF;
        border: 2px solid #0F172A;
        box-shadow: 3px 3px 0px #0F172A;
        padding: 0.4rem 1rem;
        border-radius: 50px;
        font-weight: 800;
        font-size: 0.9rem;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }

    /* Maximalist Cards */
    .max-card {
        background: #FFFFFF;
        border: 3px solid #0F172A;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 6px 6px 0px #0F172A;
        margin-bottom: 1.5rem;
        transition: transform 0.15s ease-in-out;
    }
    .max-card:hover {
        transform: translate(-2px, -2px);
        box-shadow: 8px 8px 0px #0F172A;
    }

    .max-card-indigo {
        border-top: 8px solid #4F46E5;
    }
    .max-card-coral {
        border-top: 8px solid #FF5A5F;
    }
    .max-card-emerald {
        border-top: 8px solid #10B981;
    }
    .max-card-amber {
        border-top: 8px solid #F59E0B;
    }

    /* Metric Display */
    .metric-title {
        font-size: 0.85rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #64748B;
        margin-bottom: 0.3rem;
    }
    .metric-number {
        font-family: 'Outfit', sans-serif;
        font-size: 2.2rem;
        font-weight: 900;
        color: #0F172A;
        margin: 0;
    }

    /* Custom Receipt Styling */
    .receipt-container {
        background: #FFFBEB;
        border: 3px dashed #F59E0B;
        border-radius: 16px;
        padding: 1.8rem;
        margin-top: 1rem;
        box-shadow: 6px 6px 0px #0F172A;
    }
    .receipt-header {
        border-bottom: 2px dashed #D97706;
        padding-bottom: 0.8rem;
        margin-bottom: 1rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    /* Tab Design Overrides */
    button[data-baseweb="tab"] {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        color: #475569 !important;
        background: #F1F5F9 !important;
        border: 2px solid #0F172A !important;
        border-radius: 10px 10px 0 0 !important;
        margin-right: 6px !important;
        padding: 0.6rem 1.2rem !important;
    }
    button[aria-selected="true"] {
        background: #FF5A5F !important;
        color: #FFFFFF !important;
        border-bottom: 2px solid #FF5A5F !important;
        box-shadow: 3px 3px 0px #0F172A !important;
    }

    /* Streamlit Button Styling */
    div.stButton > button {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 800 !important;
        font-size: 1.05rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        background: linear-gradient(135deg, #4F46E5 0%, #3B82F6 100%) !important;
        color: #FFFFFF !important;
        border: 3px solid #0F172A !important;
        border-radius: 12px !important;
        box-shadow: 4px 4px 0px #0F172A !important;
        padding: 0.6rem 1.4rem !important;
        transition: all 0.15s ease !important;
    }
    div.stButton > button:hover {
        transform: translate(-2px, -2px) !important;
        box-shadow: 6px 6px 0px #0F172A !important;
    }
    div.stButton > button:active {
        transform: translate(2px, 2px) !important;
        box-shadow: 2px 2px 0px #0F172A !important;
    }

    /* Form Inputs */
    input, select, textarea {
        border: 2px solid #0F172A !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
    }
</style>
""", unsafe_allow_globals=True)

# ---------------------------------------------------------
# Configuration & API Helper
# ---------------------------------------------------------
DEFAULT_API_URL = os.getenv("PAYMENT_API_URL", "http://app:8080")

st.sidebar.image("https://img.icons8.com/color/96/000000/docker.png", width=70)
st.sidebar.title("DevOps Console")
st.sidebar.caption("⚡ **Light Maximalism UI**")
st.sidebar.markdown("---")

api_url_input = st.sidebar.text_input("Payment API Target URL", value=DEFAULT_API_URL)
st.sidebar.caption("Container Network: `http://app:8080` | Local: `http://localhost:8080`")

API_BASE = api_url_input.rstrip('/')

st.sidebar.markdown("---")
st.sidebar.subheader("🏗️ Architecture Stack")
st.sidebar.markdown("""
<div style="background: #FFFFFF; border: 2px solid #0F172A; border-radius: 10px; padding: 0.8rem; box-shadow: 4px 4px 0px #0F172A;">
    <p style="margin:0 0 0.4rem 0;">🎨 <strong>GUI:</strong> Streamlit (Python 3.11)</p>
    <p style="margin:0 0 0.4rem 0;">☕ <strong>Backend:</strong> Java Spring Boot 3</p>
    <p style="margin:0 0 0.4rem 0;">🍃 <strong>Database:</strong> MongoDB 7</p>
    <p style="margin:0;">☁️ <strong>Deploy:</strong> AWS EC2 / AWS ECS</p>
</div>
""", unsafe_allow_globals=True)

# Helper API Request Handler
def make_api_request(endpoint, method="GET", json_data=None, timeout=5):
    url = f"{API_BASE}{endpoint}"
    try:
        if method.upper() == "GET":
            resp = requests.get(url, timeout=timeout)
        elif method.upper() == "POST":
            resp = requests.post(url, json=json_data, timeout=timeout)
        else:
            return None, "Unsupported HTTP Method"
        
        if 200 <= resp.status_code < 300:
            return resp.json(), None
        else:
            return None, f"HTTP {resp.status_code}: {resp.text}"
    except requests.exceptions.ConnectionError:
        return None, f"Backend Service unreachable at `{url}`. Verify container is active."
    except requests.exceptions.Timeout:
        return None, f"Request to `{url}` timed out."
    except Exception as e:
        return None, f"API Exception: {str(e)}"

# ---------------------------------------------------------
# Hero Banner & Service Health Check
# ---------------------------------------------------------
hello_data, hello_err = make_api_request("/api/hello", timeout=3)

st.markdown("""
<div class="hero-banner">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
        <div>
            <h1>💳 Payment Gateway Console</h1>
            <p>DevOps Containerized Microservice | Multi-Cloud Deployment (AWS EC2 & ECS)</p>
        </div>
        <div style="margin-top: 10px;">
""", unsafe_allow_globals=True)

if hello_data and hello_data.get("status") == "success":
    st.markdown(
        f'<span class="badge-online">🟢 SERVICE ONLINE | {hello_data.get("database", "MongoDB Active")}</span>',
        unsafe_allow_globals=True
    )
else:
    st.markdown(
        '<span class="badge-offline">🔴 SERVICE OFFLINE</span>',
        unsafe_allow_globals=True
    )

st.markdown("</div></div></div>", unsafe_allow_globals=True)

if hello_err:
    st.warning(f"⚠️ **Backend Unreachable**: {hello_err}")

# ---------------------------------------------------------
# Main Tabs Navigation
# ---------------------------------------------------------
tab_charge, tab_history, tab_stats, tab_messages, tab_export = st.tabs([
    "💳 Charge Payment",
    "📊 Analytics & History",
    "🖥️ System Telemetry",
    "💬 Message Log",
    "📁 Data Exports"
])

# Currency conversion rates relative to USD (simulated)
CURRENCY_RATES = {
    "USD ($)": 1.0,
    "EUR (€)": 0.92,
    "GBP (£)": 0.78,
    "INR (₹)": 83.5
}

# Session State for Amount Preset
if "selected_amount" not in st.session_state:
    st.session_state.selected_amount = 100.0

# =========================================================
# TAB 1: Charge Payment Operations (Enhanced)
# =========================================================
with tab_charge:
    st.markdown("### ⚡ Process Payment Transaction")
    st.caption("Consumes `POST /api/payments/charge` API with rich validation and receipt generation.")

    col_form, col_res = st.columns([1.1, 0.9], gap="large")

    with col_form:
        st.markdown('<div class="max-card max-card-indigo">', unsafe_allow_globals=True)
        st.markdown("#### 📝 Payment Details")

        # Quick Preset Buttons
        st.write("**Quick Amount Selection:**")
        preset_cols = st.columns(6)
        presets = [10, 25, 50, 100, 250, 500]
        for idx, val in enumerate(presets):
            if preset_cols[idx].button(f"${val}"):
                st.session_state.selected_amount = float(val)

        with st.form("payment_form", clear_on_submit=False):
            sender_input = st.text_input("Customer Name / Billing Handle *", value="Alex Morgan", placeholder="e.g. Alex Morgan")
            customer_email = st.text_input("Billing Email Address", value="alex.morgan@example.com", placeholder="alex@company.com")
            
            c_col1, c_col2 = st.columns(2)
            with c_col1:
                currency_selected = st.selectbox("Currency", list(CURRENCY_RATES.keys()), index=0)
            with c_col2:
                amount_input = st.number_input(
                    "Amount *",
                    min_value=1.0,
                    max_value=100000.0,
                    value=st.session_state.selected_amount,
                    step=10.0
                )

            m_col1, m_col2 = st.columns(2)
            with m_col1:
                method_input = st.selectbox(
                    "Payment Channel *",
                    ["Credit Card 💳", "UPI Payment 📲", "PayPal 🅿️", "NetBanking 🏦", "Crypto ₿"]
                )
            with m_col2:
                category_input = st.selectbox(
                    "Transaction Category",
                    ["SaaS Subscription", "Cloud Compute", "E-Commerce", "Consulting Service", "API Credits"]
                )

            st.markdown("---")
            submit_btn = st.form_submit_button("🚀 AUTHORIZE & CHARGE PAYMENT", use_container_width=True)

        st.markdown('</div>', unsafe_allow_globals=True)

    with col_res:
        st.markdown('<div class="max-card max-card-coral">', unsafe_allow_globals=True)
        st.markdown("#### 🧾 Payment Status & Digital Receipt")

        if submit_btn:
            if not sender_input.strip():
                st.error("❌ Please provide a valid Customer Name / Billing Handle.")
            elif amount_input <= 0:
                st.error("❌ Amount must be greater than zero.")
            else:
                with st.spinner("Authorizing transaction with Payment Service API..."):
                    clean_method = method_input.split()[0]
                    payload = {
                        "sender": f"{sender_input.strip()} ({customer_email})",
                        "amount": str(amount_input),
                        "method": clean_method
                    }
                    txn_data, err = make_api_request("/api/payments/charge", method="POST", json_data=payload)

                    if err:
                        st.error(f"❌ Payment Failed to Authorize: {err}")
                    elif txn_data:
                        txn_id = txn_data.get("txnId", "N/A")
                        status = txn_data.get("status", "UNKNOWN")
                        sender = txn_data.get("sender", sender_input)
                        amt = txn_data.get("amount", amount_input)
                        ts = txn_data.get("timestamp", time.time() * 1000)
                        formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ts / 1000.0))

                        if status == "SUCCESS":
                            st.balloons()
                            st.markdown(f"""
                            <div class="receipt-container">
                                <div class="receipt-header">
                                    <h3 style="margin:0; color:#B45309;">✅ DIGITAL PAYMENT RECEIPT</h3>
                                    <span style="background:#10B981; color:white; padding:4px 12px; border-radius:20px; font-weight:800;">APPROVED</span>
                                </div>
                                <p><strong>Receipt Reference:</strong> <code>{txn_id}</code></p>
                                <p><strong>Customer:</strong> {sender}</p>
                                <p><strong>Category:</strong> {category_input}</p>
                                <p><strong>Payment Channel:</strong> {method_input}</p>
                                <p><strong>Total Billed:</strong> <span style="font-size:1.5rem; font-weight:900; color:#0F172A;">{currency_selected.split()[1]} {amt}</span></p>
                                <p><strong>Timestamp:</strong> {formatted_time}</p>
                            </div>
                            """, unsafe_allow_globals=True)

                            receipt_json = json.dumps({
                                "receipt_id": txn_id,
                                "customer": sender,
                                "email": customer_email,
                                "amount": amt,
                                "currency": currency_selected,
                                "method": method_input,
                                "category": category_input,
                                "timestamp": formatted_time,
                                "status": status
                            }, indent=2)

                            st.download_button(
                                label="⬇️ Download Digital Receipt (JSON)",
                                data=receipt_json,
                                file_name=f"Receipt_{txn_id}.json",
                                mime="application/json"
                            )
                        else:
                            st.markdown(f"""
                            <div style="background:#FEF2F2; border:3px dashed #EF4444; border-radius:16px; padding:1.5rem; margin-top:1rem;">
                                <h3 style="color:#DC2626; margin:0 0 0.5rem 0;">❌ PAYMENT DECLINED</h3>
                                <p><strong>Transaction ID:</strong> <code>{txn_id}</code></p>
                                <p><strong>Reason:</strong> Simulated Payment Gateway Rejection.</p>
                                <p><strong>Time:</strong> {formatted_time}</p>
                            </div>
                            """, unsafe_allow_globals=True)

                        with st.expander("🔍 Inspect Gateway Response Payload"):
                            st.json(txn_data)
        else:
            st.info("👈 Fill out the payment details and click **AUTHORIZE & CHARGE PAYMENT** to execute a transaction.")

        st.markdown('</div>', unsafe_allow_globals=True)

# =========================================================
# TAB 2: Analytics & Transaction History
# =========================================================
with tab_history:
    st.markdown("### 📊 Transaction Analytics & Audit History")
    st.caption("Consumes `GET /api/payments/history` with high-contrast analytics visualization.")

    if st.button("🔄 Refresh Transaction Feed"):
        st.rerun()

    history_data, err = make_api_request("/api/payments/history")

    if err:
        st.error(f"Failed to fetch transaction records: {err}")
    elif not history_data:
        st.info("No transaction records found in database yet.")
    else:
        df = pd.DataFrame(history_data)

        if "timestamp" in df.columns:
            df["DateTime"] = pd.to_datetime(df["timestamp"], unit="ms")

        # Key Metrics Grid
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)

        total_txns = len(df)
        success_df = df[df["status"] == "SUCCESS"] if "status" in df.columns else pd.DataFrame()
        failed_df = df[df["status"] == "FAILED"] if "status" in df.columns else pd.DataFrame()

        total_vol = 0.0
        if "amount" in success_df.columns:
            total_vol = success_df["amount"].astype(float).sum()

        success_rate = (len(success_df) / total_txns * 100) if total_txns > 0 else 0

        with kpi1:
            st.markdown(f"""
            <div class="max-card max-card-indigo">
                <div class="metric-title">Total Processed</div>
                <div class="metric-number">{total_txns}</div>
            </div>
            """, unsafe_allow_globals=True)
        with kpi2:
            st.markdown(f"""
            <div class="max-card max-card-emerald">
                <div class="metric-title">Total Volume</div>
                <div class="metric-number">${total_vol:,.2f}</div>
            </div>
            """, unsafe_allow_globals=True)
        with kpi3:
            st.markdown(f"""
            <div class="max-card max-card-amber">
                <div class="metric-title">Success Rate</div>
                <div class="metric-number">{success_rate:.1f}%</div>
            </div>
            """, unsafe_allow_globals=True)
        with kpi4:
            st.markdown(f"""
            <div class="max-card max-card-coral">
                <div class="metric-title">Failed Transactions</div>
                <div class="metric-number">{len(failed_df)}</div>
            </div>
            """, unsafe_allow_globals=True)

        st.markdown("---")

        # Filters & Search
        f_col1, f_col2 = st.columns(2)
        with f_col1:
            status_filter = st.multiselect("Filter by Transaction Status", options=["SUCCESS", "FAILED"], default=["SUCCESS", "FAILED"])
        with f_col2:
            method_opts = list(df["method"].unique()) if "method" in df.columns else []
            method_filter = st.multiselect("Filter by Payment Method", options=method_opts, default=method_opts)

        filtered_df = df.copy()
        if "status" in filtered_df.columns and status_filter:
            filtered_df = filtered_df[filtered_df["status"].isin(status_filter)]
        if "method" in filtered_df.columns and method_filter:
            filtered_df = filtered_df[filtered_df["method"].isin(method_filter)]

        # Light Maximalist Plotly Charts
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### 💳 Volume Breakdown by Channel")
            if not filtered_df.empty and "method" in filtered_df.columns:
                fig_pie = px.pie(
                    filtered_df,
                    names="method",
                    hole=0.45,
                    color_discrete_sequence=["#4F46E5", "#FF5A5F", "#10B981", "#F59E0B", "#EC4899"]
                )
                fig_pie.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(family="Outfit", size=14, color="#0F172A")
                )
                st.plotly_chart(fig_pie, use_container_width=True)
        with c2:
            st.markdown("#### 📈 Status Frequency")
            if not filtered_df.empty and "status" in filtered_df.columns:
                status_counts = filtered_df["status"].value_counts().reset_index()
                fig_bar = px.bar(
                    status_counts,
                    x="status",
                    y="count",
                    color="status",
                    color_discrete_map={"SUCCESS": "#10B981", "FAILED": "#EF4444"}
                )
                fig_bar.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(family="Outfit", size=14, color="#0F172A")
                )
                st.plotly_chart(fig_bar, use_container_width=True)

        st.markdown("#### 📜 Detailed Transaction Audit Ledger")
        display_df = filtered_df.drop(columns=["timestamp"], errors="ignore") if "timestamp" in filtered_df.columns else filtered_df
        st.dataframe(display_df, use_container_width=True)

# =========================================================
# TAB 3: System Telemetry & Health
# =========================================================
with tab_stats:
    st.markdown("### 🖥️ Microservice Telemetry & System Stats")
    st.caption("Consumes `GET /api/system-stats` endpoint for real-time memory and CPU metrics.")

    if st.button("🔄 Poll System Metrics"):
        st.rerun()

    stats_data, err = make_api_request("/api/system-stats")

    if err:
        st.error(f"Unable to retrieve system statistics: {err}")
    elif stats_data:
        m1, m2, m3, m4 = st.columns(4)

        used_mem = stats_data.get("usedMemoryMb", 0)
        total_mem = stats_data.get("totalMemoryMb", 0)
        cpu_load = stats_data.get("cpuLoad", 0.0)
        uptime = stats_data.get("uptimeSeconds", 0)

        with m1:
            st.markdown(f"""
            <div class="max-card max-card-indigo">
                <div class="metric-title">JVM Memory Used</div>
                <div class="metric-number">{used_mem} MB</div>
                <small style="color:#64748B;">Total: {total_mem} MB</small>
            </div>
            """, unsafe_allow_globals=True)
        with m2:
            st.markdown(f"""
            <div class="max-card max-card-amber">
                <div class="metric-title">CPU Load</div>
                <div class="metric-number">{cpu_load:.1f}%</div>
            </div>
            """, unsafe_allow_globals=True)
        with m3:
            st.markdown(f"""
            <div class="max-card max-card-emerald">
                <div class="metric-title">Service Uptime</div>
                <div class="metric-number">{uptime}s</div>
                <small style="color:#64748B;">{uptime//60} mins active</small>
            </div>
            """, unsafe_allow_globals=True)
        with m4:
            st.markdown(f"""
            <div class="max-card max-card-coral">
                <div class="metric-title">MongoDB Records</div>
                <div class="metric-number">{stats_data.get('totalTransactions', 0)}</div>
            </div>
            """, unsafe_allow_globals=True)

        st.markdown("---")
        st.markdown("#### ⚙️ Runtime Environment Inspection")
        env_col1, env_col2 = st.columns(2)
        with env_col1:
            st.json({
                "Operating System": stats_data.get("osName"),
                "OS Version": stats_data.get("osVersion"),
                "Java Virtual Machine": stats_data.get("javaVersion")
            })
        with env_col2:
            st.json({
                "MongoDB Messages Count": stats_data.get("totalMessages"),
                "MongoDB Transactions Count": stats_data.get("totalTransactions"),
                "Detected Host URL": stats_data.get("detectedUrl")
            })

# =========================================================
# TAB 4: System Messages
# =========================================================
with tab_messages:
    st.markdown("### 💬 System Message & Audit Board")
    st.caption("Consumes `GET /api/messages` and `POST /api/messages` to log operational notes.")

    msg_col1, msg_col2 = st.columns([1, 1], gap="large")

    with msg_col1:
        st.markdown('<div class="max-card max-card-indigo">', unsafe_allow_globals=True)
        st.markdown("#### ✍️ Post New Log Entry")
        with st.form("msg_form", clear_on_submit=True):
            msg_sender = st.text_input("Sender Handle", value="DevOps Console Operator")
            msg_text = st.text_area("Log Content", placeholder="Enter deployment or operational message...")
            msg_submit = st.form_submit_button("💬 POST MESSAGE TO MONGO")

            if msg_submit:
                if not msg_text.strip():
                    st.warning("Please type a message before posting.")
                else:
                    msg_res, err = make_api_request("/api/messages", method="POST", json_data={"sender": msg_sender, "text": msg_text})
                    if err:
                        st.error(f"Failed to record message: {err}")
                    else:
                        st.success("Message recorded in MongoDB!")
                        st.rerun()
        st.markdown('</div>', unsafe_allow_globals=True)

    with msg_col2:
        st.markdown("#### 📜 Live MongoDB Feed")
        messages, err = make_api_request("/api/messages")
        if err:
            st.error(f"Could not retrieve messages: {err}")
        elif not messages:
            st.info("No messages stored in database.")
        else:
            for msg in reversed(messages):
                ts = msg.get("timestamp", 0)
                formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ts / 1000.0)) if ts else ""
                st.markdown(f"""
                <div style="background: #FFFFFF; border: 2px solid #0F172A; border-left: 6px solid #4F46E5; border-radius: 10px; padding: 1rem; margin-bottom: 0.8rem; box-shadow: 4px 4px 0px #0F172A;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <strong style="color:#4F46E5; font-size:1.05rem;">{msg.get('sender', 'Anonymous')}</strong>
                        <span style="color:#64748B; font-size:0.8rem; font-weight:600;">{formatted_time}</span>
                    </div>
                    <p style="margin: 0.5rem 0 0 0; color:#0F172A; font-size:0.95rem;">{msg.get('text', '')}</p>
                </div>
                """, unsafe_allow_globals=True)

# =========================================================
# TAB 5: Data Exports
# =========================================================
with tab_export:
    st.markdown("### 📁 Export Application Records")
    st.caption("Consumes `/api/export/json` and `/api/export/excel` directly from backend API.")

    exp_col1, exp_col2 = st.columns(2)

    with exp_col1:
        st.markdown('<div class="max-card max-card-emerald">', unsafe_allow_globals=True)
        st.markdown("#### 📄 Full Database Backup (JSON)")
        st.write("Extract complete MongoDB document backup containing transactions and system logs.")
        
        if st.button("Fetch Database Backup"):
            json_export, err = make_api_request("/api/export/json")
            if err:
                st.error(f"Export failed: {err}")
            elif json_export:
                json_str = json.dumps(json_export, indent=2)
                st.download_button(
                    label="⬇️ Download database_export.json",
                    data=json_str,
                    file_name="database_export.json",
                    mime="application/json"
                )
        st.markdown('</div>', unsafe_allow_globals=True)

    with exp_col2:
        st.markdown('<div class="max-card max-card-amber">', unsafe_allow_globals=True)
        st.markdown("#### 📊 CSV Spreadsheet Export")
        st.write("Generate clean CSV formatted transaction export for accounting and financial analysis.")

        if st.button("Fetch CSV Spreadsheet"):
            url = f"{API_BASE}/api/export/excel"
            try:
                resp = requests.get(url, timeout=5)
                if resp.status_code == 200:
                    st.download_button(
                        label="⬇️ Download transactions_export.csv",
                        data=resp.content,
                        file_name="transactions_export.csv",
                        mime="text/csv"
                    )
                else:
                    st.error(f"HTTP Error {resp.status_code}")
            except Exception as e:
                st.error(f"Error fetching CSV: {str(e)}")
        st.markdown('</div>', unsafe_allow_globals=True)
