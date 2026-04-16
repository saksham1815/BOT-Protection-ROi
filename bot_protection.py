import streamlit as st

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Bot Protection ROI Dashboard",
    page_icon="🛡️",
    layout="wide",
)

# ─── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600;700&display=swap');

:root {
    --bg: #0d1117;
    --card: #161b22;
    --card2: #1c2128;
    --border: #30363d;
    --primary: #58a6ff;
    --green: #3fb950;
    --red: #f85149;
    --yellow: #d29922;
    --text: #e6edf3;
    --muted: #8b949e;
}

html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stSidebar"] {
    background-color: var(--card) !important;
    border-right: 1px solid var(--border);
}

[data-testid="stSidebar"] * {
    color: var(--text) !important;
}

h1, h2, h3 {
    font-family: 'Space Mono', monospace !important;
    color: var(--text) !important;
}

.metric-card {
    background: var(--card2);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px 24px;
    margin: 8px 0;
}

.metric-label {
    font-size: 12px;
    color: var(--muted);
    letter-spacing: 0.08em;
    text-transform: uppercase;
    font-weight: 500;
}

.metric-value {
    font-family: 'Space Mono', monospace;
    font-size: 28px;
    font-weight: 700;
    color: var(--green);
    margin-top: 4px;
}

.metric-value.red { color: var(--red); }
.metric-value.blue { color: var(--primary); }
.metric-value.yellow { color: var(--yellow); }

.badge {
    display: inline-block;
    background: rgba(88,166,255,0.12);
    color: var(--primary);
    border: 1px solid rgba(88,166,255,0.3);
    border-radius: 20px;
    padding: 2px 12px;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.05em;
    margin-bottom: 16px;
}

.section-header {
    font-family: 'Space Mono', monospace;
    font-size: 11px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--muted);
    border-bottom: 1px solid var(--border);
    padding-bottom: 8px;
    margin: 20px 0 12px;
}

div[data-testid="stSelectbox"] label,
div[data-testid="stNumberInput"] label,
div[data-testid="stTextInput"] label {
    color: var(--muted) !important;
    font-size: 13px !important;
    font-weight: 500 !important;
}

div[data-testid="stSelectbox"] > div > div,
div[data-testid="stNumberInput"] input,
div[data-testid="stTextInput"] input {
    background-color: var(--card2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
}

button[kind="primary"], button[data-testid="baseButton-primary"] {
    background: var(--primary) !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-family: 'DM Sans', sans-serif !important;
}

div[data-testid="stRadio"] label {
    color: var(--text) !important;
}

.roi-positive { color: #3fb950; font-weight: 700; }
.roi-negative { color: #f85149; font-weight: 700; }

.hero-banner {
    background: linear-gradient(135deg, #1c2128 0%, #161b22 50%, #0d1117 100%);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 32px 36px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}

.hero-banner::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(88,166,255,0.08) 0%, transparent 70%);
    border-radius: 50%;
}

.hero-title {
    font-family: 'Space Mono', monospace;
    font-size: 26px;
    font-weight: 700;
    color: var(--text);
    margin: 0 0 6px;
}

.hero-sub {
    color: var(--muted);
    font-size: 14px;
    margin: 0;
}

div[data-testid="stMetric"] {
    background: var(--card2);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 16px !important;
}

div[data-testid="stMetric"] label {
    color: var(--muted) !important;
    font-size: 12px !important;
}

div[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: var(--green) !important;
    font-family: 'Space Mono', monospace !important;
}

.stButton > button {
    width: 100%;
    background: var(--primary) !important;
    color: #000 !important;
    font-weight: 700 !important;
    border-radius: 8px !important;
    border: none !important;
    padding: 12px !important;
    font-size: 15px !important;
    letter-spacing: 0.02em !important;
    transition: all 0.2s ease !important;
}

.stButton > button:hover {
    background: #79b8ff !important;
    transform: translateY(-1px);
}

div[data-testid="column"] {
    padding: 0 8px;
}

.result-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    margin-top: 16px;
}
</style>
""", unsafe_allow_html=True)


# ─── Helpers ───────────────────────────────────────────────────────────────────
def parse_number(value, default=0.0):
    try:
        if value:
            return float(str(value).replace(',', '').strip())
        return default
    except:
        return default


def fmt(v):
    return "{:,.0f}".format(v)


def get_multiplier(period):
    return {'Monthly': 1, 'Quarterly': 3, 'Half Yearly': 6, 'Yearly': 12}.get(period, 1)


def metric_card(label, value, color="green"):
    color_map = {"green": "#3fb950", "blue": "#58a6ff", "red": "#f85149", "yellow": "#d29922"}
    c = color_map.get(color, "#3fb950")
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value" style="color:{c}">₹{value}</div>
    </div>
    """, unsafe_allow_html=True)


# ─── Calculators ───────────────────────────────────────────────────────────────
def calculate_ticket_booking_roi(seats, price, normal_conv, attack_conv,
                                  blocked_pct, mitigation, infra_cost,
                                  protection_cost, period):
    multiplier = get_multiplier(period)
    nc = normal_conv / 100
    ac = attack_conv / 100
    bp = blocked_pct / 100
    mit = mitigation / 100

    expected = seats * price * nc * multiplier
    impacted = seats * (1 - bp) * price * ac * multiplier
    loss = expected - impacted
    recovered = loss * mit
    infra_saved = ((seats * multiplier) / 1000) * infra_cost
    roi = recovered + infra_saved - protection_cost
    roi_ratio = (recovered + infra_saved) / protection_cost if protection_cost else 0

    return dict(expected=expected, impacted=impacted, loss=loss,
                recovered=recovered, infra_saved=infra_saved,
                roi=roi, roi_ratio=roi_ratio)


def calculate_scraping_roi(model, requests, period, value, l2b, impact_med,
                            conversion_drop, aov, total_revenue, price_impact,
                            data_rate, lead_conv, deal_value,
                            infra_cost, protection_cost):
    multiplier = get_multiplier(period)
    requests_total = requests * multiplier
    revenue = 0
    model_used = ""

    if model == "Auto (Recommended)":
        if l2b > 0:
            revenue = (requests_total * impact_med / l2b) * value
            model_used = "L2B Model"
        else:
            revenue = requests_total * value * impact_med
            model_used = "Value per Request (Auto Fallback)"
    elif model == "L2B Model":
        revenue = (requests_total * impact_med / l2b) * value if l2b > 0 else 0
        model_used = "L2B Model"
    elif model == "Conversion Impact":
        revenue = requests_total * (conversion_drop / 100) * aov
        model_used = "Conversion Impact"
    elif model == "Price Undercut Impact":
        revenue = total_revenue * (price_impact / 100)
        model_used = "Price Undercut"
    elif model == "Value per Request":
        revenue = requests_total * value * impact_med
        model_used = "Value per Request"
    elif model == "Lead Theft Model":
        leads = requests_total * (data_rate / 100)
        revenue = leads * (lead_conv / 100) * deal_value
        model_used = "Lead Theft"

    infra_saved = (requests_total / 1000) * infra_cost
    roi = revenue + infra_saved - protection_cost
    roi_ratio = (revenue + infra_saved) / protection_cost if protection_cost else 0

    return dict(revenue=revenue, infra_saved=infra_saved, roi=roi,
                roi_ratio=roi_ratio, model_used=model_used)


def calculate_ato_roi(login_attempts, attack_rate, success_rate,
                      account_value, fraud_loss, recovery_cost,
                      detection, mitigation, infra_cost, protection_cost):
    ar = attack_rate / 100
    sr = success_rate / 100
    det = detection / 100
    mit = mitigation / 100

    attacks = login_attempts * ar
    successful = attacks * sr
    loss_per_account = account_value + fraud_loss + recovery_cost
    total_loss = successful * loss_per_account
    prevented = successful * det * mit
    recovered = prevented * loss_per_account
    infra_saved = (login_attempts / 1000) * infra_cost
    roi = recovered + infra_saved - protection_cost
    roi_ratio = (recovered + infra_saved) / protection_cost if protection_cost else 0

    return dict(attacks=attacks, successful=successful, total_loss=total_loss,
                recovered=recovered, infra_saved=infra_saved,
                roi=roi, roi_ratio=roi_ratio)


# ─── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
    <div class="hero-title">🛡️ Bot Protection ROI Dashboard</div>
    <p class="hero-sub">Analyze ROI across Monthly, Quarterly, Half-Yearly, and Yearly periods</p>
</div>
""", unsafe_allow_html=True)

# ─── Navigation ────────────────────────────────────────────────────────────────
page = st.sidebar.radio(
    "Navigation",
    ["🏠 Home", "🎟️ Ticket Booking", "🕷️ Scraping", "🔐 Account Takeover (ATO)"],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.markdown("<div style='color:#8b949e;font-size:12px;'>Bot Protection ROI Suite</div>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# HOME
# ═══════════════════════════════════════════════════════════════════════════════
if page == "🏠 Home":
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="metric-card" style="text-align:center;cursor:pointer;">
            <div style="font-size:36px;margin-bottom:8px;">🎟️</div>
            <div style="font-family:'Space Mono',monospace;font-weight:700;font-size:15px;margin-bottom:4px;">Ticket Booking</div>
            <div style="color:#8b949e;font-size:13px;">Seat spinning & scalping attack ROI</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-card" style="text-align:center;cursor:pointer;">
            <div style="font-size:36px;margin-bottom:8px;">🕷️</div>
            <div style="font-family:'Space Mono',monospace;font-weight:700;font-size:15px;margin-bottom:4px;">Scraping</div>
            <div style="color:#8b949e;font-size:13px;">Data scraping & competitive intel ROI</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="metric-card" style="text-align:center;cursor:pointer;">
            <div style="font-size:36px;margin-bottom:8px;">🔐</div>
            <div style="font-family:'Space Mono',monospace;font-weight:700;font-size:15px;margin-bottom:4px;">Account Takeover</div>
            <div style="color:#8b949e;font-size:13px;">ATO credential stuffing ROI</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">How to use</div>
        <div style="margin-top:12px;color:#e6edf3;font-size:14px;line-height:1.7;">
            Select an attack vector from the <b>sidebar</b>, fill in your business parameters,
            choose a time period, and click <b>Calculate ROI</b> to see your projected
            protection value and return on investment.
        </div>
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# TICKET BOOKING
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🎟️ Ticket Booking":
    st.markdown("<div class='badge'>SEAT SPINNING ROI</div>", unsafe_allow_html=True)
    st.markdown("## 🎟️ Ticket Booking ROI")
    st.markdown("<p style='color:#8b949e;margin-top:-12px;'>All values are calculated based on selected time period</p>", unsafe_allow_html=True)

    left, right = st.columns([1, 1], gap="large")

    with left:
        st.markdown("<div class='section-header'>Traffic Parameters</div>", unsafe_allow_html=True)
        seats = st.number_input("Total Seats / Inventory", min_value=0.0, value=100000.0, step=1000.0, format="%.0f")
        price = st.number_input("Average Ticket Price (₹)", min_value=0.0, value=1500.0, step=100.0)
        period = st.selectbox("Time Period", ["Monthly", "Quarterly", "Half Yearly", "Yearly"])

        st.markdown("<div class='section-header'>Conversion Rates</div>", unsafe_allow_html=True)
        normal_conv = st.number_input("Normal Conversion Rate (%)", min_value=0.0, max_value=100.0, value=5.0, step=0.1)
        attack_conv = st.number_input("Conversion Rate Under Attack (%)", min_value=0.0, max_value=100.0, value=1.5, step=0.1)
        blocked_pct = st.number_input("% Traffic Blocked by Bots", min_value=0.0, max_value=100.0, value=30.0, step=1.0)
        mitigation = st.number_input("Mitigation Effectiveness (%)", min_value=0.0, max_value=100.0, value=80.0, step=1.0)

        st.markdown("<div class='section-header'>Costs</div>", unsafe_allow_html=True)
        infra_cost = st.number_input("Infra Cost per 1K Requests (₹)", min_value=0.0, value=25.0, step=1.0)
        protection_cost = st.number_input("Bot Protection Cost (₹)", min_value=0.0, value=200000.0, step=10000.0, format="%.0f")

        calc = st.button("Calculate ROI", key="ticket_calc", type="primary")

    with right:
        st.markdown("<div class='section-header'>Results</div>", unsafe_allow_html=True)
        if calc:
            r = calculate_ticket_booking_roi(seats, price, normal_conv, attack_conv,
                                              blocked_pct, mitigation, infra_cost,
                                              protection_cost, period)

            metric_card("Expected Revenue (No Attack)", fmt(r['expected']), "blue")
            metric_card("Revenue Under Attack", fmt(r['impacted']), "yellow")
            metric_card("Revenue Loss", fmt(r['loss']), "red")

            st.markdown("<br>", unsafe_allow_html=True)
            metric_card("Revenue Recovered", fmt(r['recovered']), "green")
            metric_card("Infra Savings", fmt(r['infra_saved']), "green")

            roi_color = "green" if r['roi'] >= 0 else "red"
            metric_card("Net ROI", fmt(r['roi']), roi_color)

            ratio_color = "green" if r['roi_ratio'] >= 1 else "red"
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">ROI Ratio</div>
                <div class="metric-value" style="color:{'#3fb950' if r['roi_ratio']>=1 else '#f85149'}">
                    {r['roi_ratio']:.2f}x
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Bar chart
            import pandas as pd
            chart_data = pd.DataFrame({
                "Category": ["Expected", "Under Attack", "Recovered", "Infra Saved"],
                "Value (₹)": [r['expected'], r['impacted'], r['recovered'], r['infra_saved']]
            })
            st.markdown("<div class='section-header'>Breakdown Chart</div>", unsafe_allow_html=True)
            st.bar_chart(chart_data.set_index("Category"), color="#58a6ff")
        else:
            st.markdown("""
            <div class="metric-card" style="text-align:center;padding:48px;">
                <div style="font-size:48px;margin-bottom:16px;">🎟️</div>
                <div style="color:#8b949e;">Fill in the parameters and click<br><b style='color:#e6edf3;'>Calculate ROI</b></div>
            </div>
            """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# SCRAPING
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🕷️ Scraping":
    st.markdown("<div class='badge'>SCRAPING ROI</div>", unsafe_allow_html=True)
    st.markdown("## 🕷️ Scraping ROI")
    st.markdown("<p style='color:#8b949e;margin-top:-12px;'>Revenue scales automatically based on selected time period</p>", unsafe_allow_html=True)

    left, right = st.columns([1, 1], gap="large")

    with left:
        st.markdown("<div class='section-header'>Model Selection</div>", unsafe_allow_html=True)
        model = st.selectbox("Calculation Model", [
            "Auto (Recommended)", "L2B Model", "Conversion Impact",
            "Price Undercut Impact", "Value per Request", "Lead Theft Model"
        ])

        st.markdown("<div class='section-header'>Base Parameters</div>", unsafe_allow_html=True)
        requests = st.number_input("Requests per Month", min_value=0.0, value=50000.0, step=1000.0, format="%.0f")
        period = st.selectbox("Time Period", ["Monthly", "Quarterly", "Half Yearly", "Yearly"], key="scr_period")

        # Dynamic fields
        value = l2b = impact_med = 0.0
        conversion_drop = aov = 0.0
        total_revenue = price_impact = 0.0
        data_rate = lead_conv = deal_value = 0.0

        if model in ["Auto (Recommended)", "L2B Model", "Value per Request"]:
            st.markdown("<div class='section-header'>Model Parameters</div>", unsafe_allow_html=True)
            value = st.number_input("Value per Booking/Session (₹)", min_value=0.0, value=2000.0, step=100.0)
            if model in ["Auto (Recommended)", "L2B Model"]:
                l2b = st.number_input("Lookups to Booking Ratio (L2B)", min_value=0.0, value=0.0, step=1.0,
                                      help="Leave 0 for Auto fallback to Value per Request")
            impact_med = st.number_input("Impact / Scrape Fraction", min_value=0.0, max_value=1.0, value=0.3, step=0.01)

        elif model == "Conversion Impact":
            st.markdown("<div class='section-header'>Model Parameters</div>", unsafe_allow_html=True)
            conversion_drop = st.number_input("Conversion Drop (%)", min_value=0.0, max_value=100.0, value=2.0, step=0.1)
            aov = st.number_input("Average Order Value (₹)", min_value=0.0, value=2000.0, step=100.0)

        elif model == "Price Undercut Impact":
            st.markdown("<div class='section-header'>Model Parameters</div>", unsafe_allow_html=True)
            total_revenue = st.number_input("Total Revenue (₹)", min_value=0.0, value=50000000.0, step=100000.0, format="%.0f")
            price_impact = st.number_input("Revenue Loss from Undercutting (%)", min_value=0.0, max_value=100.0, value=5.0, step=0.1)

        elif model == "Lead Theft Model":
            st.markdown("<div class='section-header'>Model Parameters</div>", unsafe_allow_html=True)
            data_rate = st.number_input("Data Extraction Rate (%)", min_value=0.0, max_value=100.0, value=10.0, step=0.5)
            lead_conv = st.number_input("Lead Conversion Rate (%)", min_value=0.0, max_value=100.0, value=5.0, step=0.5)
            deal_value = st.number_input("Average Deal Value (₹)", min_value=0.0, value=5000.0, step=500.0)

        st.markdown("<div class='section-header'>Costs</div>", unsafe_allow_html=True)
        infra_cost = st.number_input("Infra Cost per 1K Requests (₹)", min_value=0.0, value=25.0, step=1.0, key="scr_infra")
        protection_cost = st.number_input("Bot Protection Cost (₹)", min_value=0.0, value=200000.0, step=10000.0, format="%.0f", key="scr_prot")

        calc = st.button("Calculate ROI", key="scr_calc", type="primary")

    with right:
        st.markdown("<div class='section-header'>Results</div>", unsafe_allow_html=True)
        if calc:
            r = calculate_scraping_roi(
                model, requests, period, value, l2b, impact_med,
                conversion_drop, aov, total_revenue, price_impact,
                data_rate, lead_conv, deal_value,
                infra_cost, protection_cost
            )

            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Model Used</div>
                <div style="font-family:'Space Mono',monospace;font-size:16px;color:#58a6ff;margin-top:6px;font-weight:700;">
                    {r['model_used']}
                </div>
            </div>
            """, unsafe_allow_html=True)

            metric_card("Revenue at Risk / Saved", fmt(r['revenue']), "green")
            metric_card("Infra Savings", fmt(r['infra_saved']), "blue")

            roi_color = "green" if r['roi'] >= 0 else "red"
            metric_card("Net ROI", fmt(r['roi']), roi_color)

            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">ROI Ratio</div>
                <div class="metric-value" style="color:{'#3fb950' if r['roi_ratio']>=1 else '#f85149'}">
                    {r['roi_ratio']:.2f}x
                </div>
            </div>
            """, unsafe_allow_html=True)

            import pandas as pd
            chart_data = pd.DataFrame({
                "Category": ["Revenue Saved", "Infra Saved", "Protection Cost"],
                "Value (₹)": [r['revenue'], r['infra_saved'], protection_cost]
            })
            st.markdown("<div class='section-header'>Breakdown Chart</div>", unsafe_allow_html=True)
            st.bar_chart(chart_data.set_index("Category"), color="#58a6ff")
        else:
            st.markdown("""
            <div class="metric-card" style="text-align:center;padding:48px;">
                <div style="font-size:48px;margin-bottom:16px;">🕷️</div>
                <div style="color:#8b949e;">Fill in the parameters and click<br><b style='color:#e6edf3;'>Calculate ROI</b></div>
            </div>
            """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# ATO
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🔐 Account Takeover (ATO)":
    st.markdown("<div class='badge'>ATO ROI</div>", unsafe_allow_html=True)
    st.markdown("## 🔐 Account Takeover ROI")
    st.markdown("<p style='color:#8b949e;margin-top:-12px;'>Credential stuffing & account takeover attack analysis</p>", unsafe_allow_html=True)

    left, right = st.columns([1, 1], gap="large")

    with left:
        st.markdown("<div class='section-header'>Traffic & Attack</div>", unsafe_allow_html=True)
        login_attempts = st.number_input("Login Attempts", min_value=0.0, value=1000000.0, step=10000.0, format="%.0f")
        attack_rate = st.number_input("Attack Traffic (%)", min_value=0.0, max_value=100.0, value=10.0, step=0.5)
        success_rate = st.number_input("Attack Success Rate (%)", min_value=0.0, max_value=100.0, value=2.0, step=0.1)

        st.markdown("<div class='section-header'>Business Impact per Account</div>", unsafe_allow_html=True)
        account_value = st.number_input("Account Value (₹)", min_value=0.0, value=5000.0, step=100.0)
        fraud_loss = st.number_input("Fraud Loss per Account (₹)", min_value=0.0, value=2000.0, step=100.0)
        recovery_cost = st.number_input("Recovery Cost per Account (₹)", min_value=0.0, value=500.0, step=50.0)

        st.markdown("<div class='section-header'>Protection Effectiveness</div>", unsafe_allow_html=True)
        detection = st.number_input("Detection Rate (%)", min_value=0.0, max_value=100.0, value=85.0, step=1.0)
        mitigation = st.number_input("Mitigation Rate (%)", min_value=0.0, max_value=100.0, value=90.0, step=1.0)

        st.markdown("<div class='section-header'>Costs</div>", unsafe_allow_html=True)
        infra_cost = st.number_input("Infra Cost per 1K Requests (₹)", min_value=0.0, value=25.0, step=1.0, key="ato_infra")
        protection_cost = st.number_input("Bot Protection Cost (₹)", min_value=0.0, value=500000.0, step=10000.0, format="%.0f", key="ato_prot")

        calc = st.button("Calculate ROI", key="ato_calc", type="primary")

    with right:
        st.markdown("<div class='section-header'>Results</div>", unsafe_allow_html=True)
        if calc:
            r = calculate_ato_roi(login_attempts, attack_rate, success_rate,
                                   account_value, fraud_loss, recovery_cost,
                                   detection, mitigation, infra_cost, protection_cost)

            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Attack Attempts</div>
                    <div class="metric-value" style="color:#d29922;font-size:22px;">{fmt(r['attacks'])}</div>
                </div>
                """, unsafe_allow_html=True)
            with col_b:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Successful Takeovers</div>
                    <div class="metric-value" style="color:#f85149;font-size:22px;">{fmt(r['successful'])}</div>
                </div>
                """, unsafe_allow_html=True)

            metric_card("Total Loss Without Protection", fmt(r['total_loss']), "red")
            metric_card("Value Recovered", fmt(r['recovered']), "green")
            metric_card("Infra Savings", fmt(r['infra_saved']), "blue")

            roi_color = "green" if r['roi'] >= 0 else "red"
            metric_card("Net ROI", fmt(r['roi']), roi_color)

            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">ROI Ratio</div>
                <div class="metric-value" style="color:{'#3fb950' if r['roi_ratio']>=1 else '#f85149'}">
                    {r['roi_ratio']:.2f}x
                </div>
            </div>
            """, unsafe_allow_html=True)

            import pandas as pd
            chart_data = pd.DataFrame({
                "Category": ["Total Loss", "Recovered", "Infra Saved"],
                "Value (₹)": [r['total_loss'], r['recovered'], r['infra_saved']]
            })
            st.markdown("<div class='section-header'>Breakdown Chart</div>", unsafe_allow_html=True)
            st.bar_chart(chart_data.set_index("Category"), color="#58a6ff")
        else:
            st.markdown("""
            <div class="metric-card" style="text-align:center;padding:48px;">
                <div style="font-size:48px;margin-bottom:16px;">🔐</div>
                <div style="color:#8b949e;">Fill in the parameters and click<br><b style='color:#e6edf3;'>Calculate ROI</b></div>
            </div>
            """, unsafe_allow_html=True)
