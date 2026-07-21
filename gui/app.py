import os
import time
import requests
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------------
# Page Configuration & Styling
# ---------------------------------------------------------
st.set_page_config(
    page_title="DevOps Payment Gateway Console",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (CSS)
st.markdown("""
<style>
    /* Main Theme Overrides */
    .main {
        background-color: #0e1117;
    }
    .stApp {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Hero Header */
    .hero-container {
        background: linear-gradient(135deg, #1e1e2f 0%, #0f172a 100%);
        padding: 1.8rem;
        border-radius: 12px;
        border: 1px solid #334155;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
        margin-bottom: 1.5rem;
    }
    .hero-title {
        color: #38bdf8;
        font-size: 2.2rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .hero-subtitle {
        color: #94a3b8;
        font-size: 1.05rem;
        margin-top: 0.3rem;
    }
    
    /* Status Badges */
    .status-online {
        background-color: #065f46;
        color: #34d399;
        padding: 0.35rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }
    .status-offline {
        background-color: #7f1d1d;
        color: #f87171;
        padding: 0.35rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }
    
    /* Metric Cards */
    .metric-card {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 1.2rem;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #f8fafc;
    }
    .metric-label {
        color: #94a3b8;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Custom Result Cards */
    .txn-success-card {
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid #10b981;
        border-radius: 10px;
        padding: 1.2rem;
        margin-top: 1rem;
    }
    .txn-failed-card {
        background: rgba(239, 68, 68, 0.1);
        border: 1px solid #ef4444;
        border-radius: 10px;
        padding: 1.2rem;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_globals=True)

# ---------------------------------------------------------
# Environment & API Helper Functions
# ---------------------------------------------------------
DEFAULT_API_URL = os.getenv("PAYMENT_API_URL", "http://app:8080")

# Sidebar Configuration
st.sidebar.image("https://img.icons8.com/color/96/000000/docker.png", width=70)
st.sidebar.title("DevOps Console")
st.sidebar.markdown("---")

api_url_input = st.sidebar.text_input("Payment Service URL", value=DEFAULT_API_URL)
st.sidebar.caption("Inside Docker Compose network: `http://app:8080`. Local dev: `http://localhost:8080`.")

API_BASE = api_url_input.rstrip('/')

st.sidebar.markdown("---")
st.sidebar.subheader("Architecture Stack")
st.sidebar.markdown("""
- **GUI**: Python (Streamlit)
- **Backend**: Java Spring Boot
- **Database**: MongoDB 7
- **Container**: Docker Multi-Container
""")

# API Helper with Exception Handling
def make_api_request(endpoint, method="GET", json_data=None, timeout=5):
    url = f"{API_BASE}{endpoint}"
    try:
        if method.upper() == "GET":
            resp = requests.get(url, timeout=timeout)
        elif method.upper() == "POST":
            resp = requests.post(url, json=json_data, timeout=timeout)
        else:
            return None, "Unsupported HTTP Method"
        
        if resp.status_code >= 200 and resp.status_code < 300:
            return resp.json(), None
        else:
            return None, f"Server returned HTTP {resp.status_code}: {resp.text}"
    except requests.exceptions.ConnectionError:
        return None, f"Unable to connect to Payment Service at `{url}`. Is the backend container running?"
    except requests.exceptions.Timeout:
        return None, f"Request to `{url}` timed out."
    except Exception as e:
        return None, f"Error communicating with API: {str(e)}"

# ---------------------------------------------------------
# Application Header & Health Check
# ---------------------------------------------------------
hello_data, hello_err = make_api_request("/api/hello", timeout=3)

st.markdown("""
<div class="hero-container">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
        <div>
            <h1 class="hero-title">💳 Payment Gateway Console</h1>
            <p class="hero-subtitle">Microservice Architecture | Multi-Container Docker Application</p>
        </div>
        <div style="margin-top: 10px;">
""", unsafe_allow_globals=True)

if hello_data and hello_data.get("status") == "success":
    st.markdown(
        f'<span class="status-online">🟢 Payment Service Online | {hello_data.get("database", "DB Active")}</span>',
        unsafe_allow_globals=True
    )
else:
    st.markdown(
        '<span class="status-offline">🔴 Payment Service Offline</span>',
        unsafe_allow_globals=True
    )

st.markdown("</div></div></div>", unsafe_allow_globals=True)

if hello_err:
    st.error(f"⚠️ **Backend Service Unreachable**: {hello_err}")
    st.info("💡 **Troubleshooting**: Ensure `app` container is started and accessible at configured API URL.")

# ---------------------------------------------------------
# Main Tabs Navigation
# ---------------------------------------------------------
tab_charge, tab_history, tab_stats, tab_messages, tab_export = st.tabs([
    "💳 Charge Payment",
    "📊 Transaction History",
    "🖥️ System Health",
    "💬 System Messages",
    "📁 Data Export"
])

# =========================================================
# TAB 1: Charge Payment Operations
# =========================================================
with tab_charge:
    st.subheader("Process New Payment Transaction")
    st.caption("Consumes `POST /api/payments/charge` to create real-time payment transactions.")

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        with st.form("payment_form", clear_on_submit=False):
            sender_input = st.text_input("Customer Name / Payer", placeholder="e.g. Alice Smith")
            amount_input = st.number_input("Amount (INR ₹)", min_value=1.0, max_value=500000.0, value=500.0, step=50.0)
            method_input = st.selectbox(
                "Payment Method",
                ["UPI", "Credit Card", "Debit Card", "NetBanking", "Wallet"]
            )
            
            submit_btn = st.form_submit_button("🚀 Submit Payment", use_container_width=True)

    with col2:
        st.subheader("Transaction Result")
        if submit_btn:
            if not sender_input.strip():
                st.warning("Please enter a valid customer / payer name.")
            else:
                with st.spinner("Processing payment with Payment Service API..."):
                    payload = {
                        "sender": sender_input.strip(),
                        "amount": str(amount_input),
                        "method": method_input
                    }
                    txn_data, err = make_api_request("/api/payments/charge", method="POST", json_data=payload)

                    if err:
                        st.error(f"❌ Payment Failed to Execute: {err}")
                    elif txn_data:
                        txn_id = txn_data.get("txnId", "N/A")
                        status = txn_data.get("status", "UNKNOWN")
                        sender = txn_data.get("sender", sender_input)
                        amt = txn_data.get("amount", amount_input)
                        method = txn_data.get("method", method_input)
                        ts = txn_data.get("timestamp", 0)

                        formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ts / 1000.0)) if ts else "Now"

                        if status == "SUCCESS":
                            st.balloons()
                            st.success(f"✅ **Payment Charged Successfully!**")
                            st.markdown(f"""
                            <div class="txn-success-card">
                                <h3>Transaction ID: <code>{txn_id}</code></h3>
                                <p><strong>Status:</strong> <span style="color:#34d399; font-weight:bold;">{status}</span></p>
                                <p><strong>Customer:</strong> {sender}</p>
                                <p><strong>Amount:</strong> ₹{amt}</p>
                                <p><strong>Method:</strong> {method}</p>
                                <p><strong>Time:</strong> {formatted_time}</p>
                            </div>
                            """, unsafe_allow_globals=True)
                        else:
                            st.error(f"❌ **Payment Transaction Declined!**")
                            st.markdown(f"""
                            <div class="txn-failed-card">
                                <h3>Transaction ID: <code>{txn_id}</code></h3>
                                <p><strong>Status:</strong> <span style="color:#f87171; font-weight:bold;">{status}</span></p>
                                <p><strong>Customer:</strong> {sender}</p>
                                <p><strong>Amount:</strong> ₹{amt}</p>
                                <p><strong>Reason:</strong> Simulated gateway rejection or invalid amount.</p>
                                <p><strong>Time:</strong> {formatted_time}</p>
                            </div>
                            """, unsafe_allow_globals=True)

                        with st.expander("🔍 View Raw API JSON Response"):
                            st.json(txn_data)
        else:
            st.info("Fill in the payment form on the left and click **Submit Payment** to process a transaction.")

# =========================================================
# TAB 2: Transaction History & Analytics
# =========================================================
with tab_history:
    st.subheader("Transaction History & Analytics")
    st.caption("Consumes `GET /api/payments/history` and displays live metrics from MongoDB.")

    if st.button("🔄 Refresh History Data"):
        st.rerun()

    history_data, err = make_api_request("/api/payments/history")

    if err:
        st.error(f"Failed to fetch transaction history: {err}")
    elif not history_data:
        st.warning("No transactions recorded yet in database.")
    else:
        df = pd.DataFrame(history_data)

        if "timestamp" in df.columns:
            df["DateTime"] = pd.to_datetime(df["timestamp"], unit="ms")

        # Top Summary KPIs
        col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)

        total_txns = len(df)
        success_df = df[df["status"] == "SUCCESS"] if "status" in df.columns else pd.DataFrame()
        failed_df = df[df["status"] == "FAILED"] if "status" in df.columns else pd.DataFrame()

        total_volume = 0.0
        if "amount" in success_df.columns:
            total_volume = success_df["amount"].astype(float).sum()

        success_rate = (len(success_df) / total_txns * 100) if total_txns > 0 else 0

        with col_kpi1:
            st.metric("Total Transactions", total_txns)
        with col_kpi2:
            st.metric("Successful Volume", f"₹{total_volume:,.2f}")
        with col_kpi3:
            st.metric("Success Rate", f"{success_rate:.1f}%")
        with col_kpi4:
            st.metric("Failed Count", len(failed_df))

        st.markdown("---")

        # Filters
        f_col1, f_col2 = st.columns(2)
        with f_col1:
            status_filter = st.multiselect("Filter by Status", options=["SUCCESS", "FAILED"], default=["SUCCESS", "FAILED"])
        with f_col2:
            method_options = list(df["method"].unique()) if "method" in df.columns else []
            method_filter = st.multiselect("Filter by Payment Method", options=method_options, default=method_options)

        filtered_df = df.copy()
        if "status" in filtered_df.columns and status_filter:
            filtered_df = filtered_df[filtered_df["status"].isin(status_filter)]
        if "method" in filtered_df.columns and method_filter:
            filtered_df = filtered_df[filtered_df["method"].isin(method_filter)]

        # Visual Charts
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### Transactions by Payment Method")
            if not filtered_df.empty and "method" in filtered_df.columns:
                fig_method = px.pie(filtered_df, names="method", hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
                fig_method.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#f8fafc")
                st.plotly_chart(fig_method, use_container_width=True)
        with c2:
            st.markdown("#### Status Breakdown")
            if not filtered_df.empty and "status" in filtered_df.columns:
                fig_status = px.bar(
                    filtered_df["status"].value_counts().reset_index(),
                    x="status", y="count",
                    color="status",
                    color_discrete_map={"SUCCESS": "#10b981", "FAILED": "#ef4444"}
                )
                fig_status.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#f8fafc")
                st.plotly_chart(fig_status, use_container_width=True)

        st.markdown("#### Transaction Records Table")
        display_df = filtered_df.drop(columns=["timestamp"], errors="ignore") if "timestamp" in filtered_df.columns else filtered_df
        st.dataframe(display_df, use_container_width=True)

# =========================================================
# TAB 3: System Health & Metrics
# =========================================================
with tab_stats:
    st.subheader("Payment Service Telemetry & MongoDB Stats")
    st.caption("Consumes `GET /api/system-stats` to display real-time backend resource usage.")

    if st.button("🔄 Refresh Telemetry"):
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
            st.metric("JVM Memory Used", f"{used_mem} MB", f"Total: {total_mem} MB")
        with m2:
            st.metric("CPU Load", f"{cpu_load:.1f}%")
        with m3:
            st.metric("Service Uptime", f"{uptime} secs", f"{uptime//60} mins")
        with m4:
            st.metric("Total DB Transactions", stats_data.get("totalTransactions", 0))

        st.markdown("---")
        st.subheader("System Environment Details")

        col_env1, col_env2 = st.columns(2)
        with col_env1:
            st.json({
                "Operating System": stats_data.get("osName"),
                "OS Version": stats_data.get("osVersion"),
                "Java Version": stats_data.get("javaVersion")
            })
        with col_env2:
            st.json({
                "MongoDB Messages Count": stats_data.get("totalMessages"),
                "MongoDB Transactions Count": stats_data.get("totalTransactions"),
                "Detected Backend Host": stats_data.get("detectedUrl")
            })

# =========================================================
# TAB 4: System Messages
# =========================================================
with tab_messages:
    st.subheader("System Messages & Console Board")
    st.caption("Consumes `GET /api/messages` and `POST /api/messages`.")

    msg_col1, msg_col2 = st.columns([1, 1], gap="large")

    with msg_col1:
        st.markdown("#### Post a System Log / Message")
        with st.form("msg_form", clear_on_submit=True):
            msg_sender = st.text_input("Sender", value="Python GUI Console")
            msg_text = st.text_area("Message Content", placeholder="Enter message to store in MongoDB...")
            msg_submit = st.form_submit_button("💬 Send Message")

            if msg_submit:
                if not msg_text.strip():
                    st.warning("Please type a message before submitting.")
                else:
                    msg_res, err = make_api_request("/api/messages", method="POST", json_data={"sender": msg_sender, "text": msg_text})
                    if err:
                        st.error(f"Failed to post message: {err}")
                    else:
                        st.success("Message stored in MongoDB!")
                        st.rerun()

    with msg_col2:
        st.markdown("#### MongoDB Message Feed")
        messages, err = make_api_request("/api/messages")
        if err:
            st.error(f"Could not load messages: {err}")
        elif not messages:
            st.info("No messages found.")
        else:
            for msg in reversed(messages):
                ts = msg.get("timestamp", 0)
                formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ts / 1000.0)) if ts else ""
                st.markdown(f"""
                <div style="background: #1e293b; padding: 0.8rem; border-radius: 8px; margin-bottom: 0.6rem; border-left: 4px solid #38bdf8;">
                    <strong style="color: #38bdf8;">{msg.get('sender', 'Anonymous')}</strong>
                    <span style="float: right; color: #64748b; font-size: 0.8rem;">{formatted_time}</span>
                    <p style="margin-top: 0.4rem; color: #e2e8f0;">{msg.get('text', '')}</p>
                </div>
                """, unsafe_allow_globals=True)

# =========================================================
# TAB 5: Data Export
# =========================================================
with tab_export:
    st.subheader("Export Application Data")
    st.caption("Consumes `/api/export/json` and `/api/export/excel` directly from Payment Service.")

    exp_col1, exp_col2 = st.columns(2)

    with exp_col1:
        st.markdown("#### 📄 JSON Database Export")
        st.write("Download full database backup including messages and transaction records in JSON format.")
        
        if st.button("Fetch JSON Export"):
            json_export, err = make_api_request("/api/export/json")
            if err:
                st.error(f"Failed to fetch JSON export: {err}")
            elif json_export:
                import json
                json_str = json.dumps(json_export, indent=2)
                st.download_button(
                    label="⬇️ Download database_export.json",
                    data=json_str,
                    file_name="database_export.json",
                    mime="application/json"
                )

    with exp_col2:
        st.markdown("#### 📊 CSV / Excel Transaction Export")
        st.write("Download formatted transaction history ready for Excel analysis.")

        if st.button("Fetch CSV Export"):
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
