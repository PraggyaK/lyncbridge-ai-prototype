import streamlit as st

from agents.supplier_match_agent import supplier_match_agent
from agents.trend_agent import trend_scout_agent, llm_trend_scout_agent
from agents.product_concept_agent import product_concept_agent, llm_product_concept_agent
from agents.compliance_agent import compliance_guardian_agent
from agents.quality_agent import quality_sentinel_agent
from agents.buyer_pitch_agent import buyer_pitch_agent, llm_buyer_pitch_agent
from agents.landed_cost_agent import landed_cost_agent
from agents.order_orchestrator_agent import order_orchestrator_agent
from utils.report_builder import build_final_report, build_html_report


st.set_page_config(
    page_title="Lync Bridge AI Sourcing",
    page_icon="🌍",
    layout="wide"
)


# -----------------------------
# UI STYLING
# -----------------------------
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #111827 45%, #1e293b 100%);
        color: #f8fafc;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #020617 0%, #111827 100%);
        border-right: 1px solid rgba(148, 163, 184, 0.2);
    }

    section[data-testid="stSidebar"] label {
        color: #e5e7eb !important;
        font-weight: 600;
    }

    div[data-baseweb="select"] > div,
    input {
        background-color: #020617 !important;
        border-radius: 12px !important;
        border: 1px solid rgba(148, 163, 184, 0.3) !important;
        color: #f8fafc !important;
    }

    .stButton > button {
        width: 100%;
        border-radius: 12px;
        border: 0;
        background: linear-gradient(135deg, #38bdf8 0%, #2563eb 100%);
        color: white;
        font-weight: 700;
        padding: 0.7rem 1rem;
        box-shadow: 0 10px 25px rgba(37, 99, 235, 0.35);
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #7dd3fc 0%, #3b82f6 100%);
        color: white;
        transform: translateY(-1px);
    }

    .stDownloadButton > button {
        border-radius: 12px;
        border: 1px solid rgba(56, 189, 248, 0.5);
        background: rgba(15, 23, 42, 0.9);
        color: #e0f2fe;
        font-weight: 700;
    }

    button[data-baseweb="tab"] {
        background: rgba(15, 23, 42, 0.8);
        border-radius: 12px 12px 0 0;
        margin-right: 4px;
        color: #cbd5e1;
        font-weight: 600;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #0ea5e9 0%, #2563eb 100%);
        color: white;
    }

    div[data-testid="stMetric"] {
        background: rgba(15, 23, 42, 0.82);
        padding: 1rem;
        border-radius: 16px;
        border: 1px solid rgba(148, 163, 184, 0.25);
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.25);
    }

    div[data-testid="stMetric"] label {
        color: #cbd5e1 !important;
    }

    div[data-testid="stMetric"] div {
        color: #f8fafc !important;
    }

    div[data-testid="stTable"] {
        background: rgba(15, 23, 42, 0.85);
        border-radius: 16px;
        padding: 1rem;
        border: 1px solid rgba(148, 163, 184, 0.2);
    }

    .hero-card {
        background: radial-gradient(circle at top left, rgba(56, 189, 248, 0.35), transparent 35%),
                    linear-gradient(135deg, rgba(15, 23, 42, 0.98), rgba(30, 41, 59, 0.95));
        border: 1px solid rgba(125, 211, 252, 0.35);
        border-radius: 24px;
        padding: 2rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.35);
    }

    .hero-title {
        font-size: 2.6rem;
        font-weight: 900;
        margin-bottom: 0.4rem;
        color: #f8fafc;
    }

    .hero-subtitle {
        font-size: 1.05rem;
        color: #cbd5e1;
        max-width: 850px;
        line-height: 1.6;
    }

    .pill {
        display: inline-block;
        background: rgba(14, 165, 233, 0.16);
        border: 1px solid rgba(125, 211, 252, 0.45);
        color: #bae6fd;
        padding: 0.35rem 0.75rem;
        border-radius: 999px;
        font-size: 0.82rem;
        font-weight: 700;
        margin-right: 0.4rem;
        margin-bottom: 0.4rem;
    }

    .premium-card {
        background: rgba(15, 23, 42, 0.86);
        border: 1px solid rgba(148, 163, 184, 0.25);
        border-radius: 20px;
        padding: 1.2rem;
        margin-bottom: 1rem;
        box-shadow: 0 14px 35px rgba(0, 0, 0, 0.22);
        min-height: 130px;
    }

    .card-title {
        font-size: 0.9rem;
        color: #93c5fd;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.4rem;
    }

    .card-value {
        font-size: 1.15rem;
        color: #f8fafc;
        font-weight: 800;
    }

    .card-note {
        font-size: 0.9rem;
        color: #cbd5e1;
        margin-top: 0.35rem;
    }

    .agent-card {
        background: rgba(2, 6, 23, 0.62);
        border: 1px solid rgba(148, 163, 184, 0.22);
        border-radius: 16px;
        padding: 1rem;
        margin-bottom: 0.7rem;
        min-height: 112px;
    }

    .agent-name {
        font-weight: 800;
        color: #f8fafc;
    }

    .agent-status {
        color: #86efac;
        font-weight: 700;
        font-size: 0.88rem;
    }

    .soft-warning {
        background: rgba(250, 204, 21, 0.12);
        border: 1px solid rgba(250, 204, 21, 0.35);
        color: #fef3c7;
        padding: 1rem;
        border-radius: 16px;
        margin-top: 1rem;
    }

    .success-box {
        background: rgba(34, 197, 94, 0.13);
        border: 1px solid rgba(74, 222, 128, 0.35);
        color: #dcfce7;
        padding: 1rem;
        border-radius: 16px;
        margin-bottom: 1rem;
        font-weight: 700;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# -----------------------------
# SMALL UI HELPERS
# -----------------------------
def show_soft_warning():
    st.markdown(
        """
        <div class="soft-warning">
            ⚠️ LLM-enhanced output is unavailable right now. 
            The rule-based agent output is still working. 
            Check your API key, .env file, or Streamlit secrets before enabling this in demo.
        </div>
        """,
        unsafe_allow_html=True
    )


def render_agent_workflow_summary():
    st.markdown("### 🤖 Agent Workflow Summary")

    agent_col1, agent_col2, agent_col3 = st.columns(3)

    agents = [
        ("🔮 Trend Scout", "Completed", "Detected trend direction and retail fit."),
        ("🧵 Product Concept", "Completed", "Generated buyer-ready product concept."),
        ("🏭 Supplier Match", "Completed", "Ranked suppliers by price, QC, compliance, and lead time."),
        ("💰 Landed Cost", "Completed", "Estimated landed cost, wholesale price, and gross margin."),
        ("🛡️ Compliance Guardian", "Completed", "Generated compliance checklist and document needs."),
        ("🧪 Quality Sentinel", "Completed", "Identified QC risks and inspection plan."),
        ("📦 Order Orchestrator", "Completed", "Built sampling, PO, production, and shipment timeline."),
        ("🛍️ Buyer Pitch", "Completed", "Created buyer-facing pitch and next steps."),
    ]

    for index, agent in enumerate(agents):
        target_col = [agent_col1, agent_col2, agent_col3][index % 3]

        with target_col:
            st.markdown(
                f"""
                <div class="agent-card">
                    <div class="agent-name">{agent[0]}</div>
                    <div class="agent-status">● {agent[1]}</div>
                    <div class="card-note">{agent[2]}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


# -----------------------------
# HERO
# -----------------------------
st.markdown(
    """
    <div class="hero-card">
        <div class="hero-title">🌍 Lync Bridge AI Sourcing Copilot</div>
        <div class="hero-subtitle">
            An agentic sourcing engine that converts a buyer requirement into a 
            trend-led product concept, supplier shortlist, landed-cost estimate, 
            compliance review, QC risk plan, order timeline, and buyer-ready pitch.
        </div>
        <br>
        <span class="pill">Trend Intelligence</span>
        <span class="pill">Supplier Matching</span>
        <span class="pill">Landed Costing</span>
        <span class="pill">Compliance + QC</span>
        <span class="pill">Order Orchestration</span>
        <span class="pill">Buyer Pitch</span>
    </div>
    """,
    unsafe_allow_html=True,
)


# -----------------------------
# SIDEBAR INPUTS
# -----------------------------
st.sidebar.markdown("## 🧾 Buyer Requirement")
st.sidebar.caption("Enter the buyer brief and let the sourcing agents generate a full plan.")

category = st.sidebar.selectbox(
    "Product Category",
    ["Bedding", "Bath", "Kitchen Textile", "Cushions", "Throws"],
)

retailer = st.sidebar.selectbox(
    "Target Retailer",
    ["HomeGoods", "Ross", "Burlington", "Five Below", "Big Lots"],
)

season = st.sidebar.selectbox(
    "Season",
    ["Spring 2026", "Summer 2026", "Fall 2026", "Holiday 2026"],
)

target_fob = st.sidebar.number_input(
    "Target FOB Price ($)",
    min_value=1.0,
    max_value=100.0,
    value=12.0,
    step=0.5,
)

country = st.sidebar.selectbox(
    "Preferred Sourcing Country",
    ["Any", "India", "Bangladesh", "China", "Vietnam", "Turkey"],
)

style_direction = st.sidebar.text_input(
    "Style Direction",
    value="Soft luxury, muted colors, premium discount retail look",
)

use_llm = st.sidebar.checkbox(
    "Use LLM-enhanced outputs",
    value=False,
    help="Turn this on only after your API key is configured. The prototype still works without it.",
)

if use_llm:
    st.sidebar.warning("LLM mode is on. Make sure your API key is configured.")
else:
    st.sidebar.info("Demo-safe mode: using stable rule-based agents.")


# -----------------------------
# MAIN APP
# -----------------------------
if st.sidebar.button("Generate Sourcing Plan"):
    st.markdown(
        """
        <div class="success-box">
            ✅ Agentic workflow completed successfully. Your sourcing plan is ready.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.header("Generated AI Sourcing Plan")

    trend_output = trend_scout_agent(
        category=category,
        retailer=retailer,
        season=season,
        style_direction=style_direction,
    )

    product_concept = product_concept_agent(
        trend_output=trend_output,
        target_fob=target_fob,
    )

    supplier_results = supplier_match_agent(
        category=category,
        target_fob=target_fob,
        country_preference=country,
    )

    selected_supplier = supplier_results[0] if supplier_results else None

    landed_cost_output = landed_cost_agent(
        product_concept=product_concept,
        selected_supplier=selected_supplier,
    )

    compliance_output = compliance_guardian_agent(
        product_concept=product_concept,
        selected_supplier=selected_supplier,
    )

    quality_output = quality_sentinel_agent(
        product_concept=product_concept,
        selected_supplier=selected_supplier,
    )

    order_output = order_orchestrator_agent(
        product_concept=product_concept,
        selected_supplier=selected_supplier,
    )

    buyer_pitch_output = buyer_pitch_agent(
        trend_output=trend_output,
        product_concept=product_concept,
        supplier_results=supplier_results,
        landed_cost_output=landed_cost_output,
        compliance_output=compliance_output,
        quality_output=quality_output,
    )

    enhanced_trend_output = None
    enhanced_product_output = None
    enhanced_pitch_output = None

    if use_llm:
        enhanced_trend_output = llm_trend_scout_agent(
            category=category,
            retailer=retailer,
            season=season,
            style_direction=style_direction,
            base_trend_output=trend_output,
        )

        enhanced_product_output = llm_product_concept_agent(
            product_concept=product_concept,
        )

        enhanced_pitch_output = llm_buyer_pitch_agent(
            buyer_pitch_output=buyer_pitch_output,
        )

    final_report = build_final_report(
        trend_output=trend_output,
        product_concept=product_concept,
        supplier_results=supplier_results,
        landed_cost_output=landed_cost_output,
        compliance_output=compliance_output,
        quality_output=quality_output,
        buyer_pitch_output=buyer_pitch_output,
        order_output=order_output,
    )

    html_report = build_html_report(final_report)

    top_supplier_name = selected_supplier["supplier_name"] if selected_supplier else "No supplier selected"
    top_supplier_score = selected_supplier["match_score"] if selected_supplier else "N/A"

    col_a, col_b, col_c, col_d = st.columns(4)

    with col_a:
        st.markdown(
            f"""
            <div class="premium-card">
                <div class="card-title">Product Concept</div>
                <div class="card-value">{product_concept['product_name']}</div>
                <div class="card-note">{product_concept['category']} · {product_concept['season']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_b:
        st.markdown(
            f"""
            <div class="premium-card">
                <div class="card-title">Top Supplier</div>
                <div class="card-value">{top_supplier_name}</div>
                <div class="card-note">Match Score: {top_supplier_score}/100</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_c:
        st.markdown(
            f"""
            <div class="premium-card">
                <div class="card-title">Landed Cost</div>
                <div class="card-value">${landed_cost_output['estimated_landed_cost']}</div>
                <div class="card-note">Wholesale: ${landed_cost_output['suggested_wholesale_price']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_d:
        st.markdown(
            f"""
            <div class="premium-card">
                <div class="card-title">Risk View</div>
                <div class="card-value">QC: {quality_output['risk_level']}</div>
                <div class="card-note">Compliance: {compliance_output['risk_level']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    render_agent_workflow_summary()

    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(
        [
            "Trend Intelligence",
            "Product Concept",
            "Supplier Match",
            "Costing",
            "Compliance & QC",
            "Order Timeline",
            "Buyer Pitch",
            "Final Report",
        ]
    )

    with tab1:
        st.subheader("🔮 Trend Scout Agent")
        st.markdown(f"### {trend_output['trend_name']}")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Category**")
            st.write(trend_output["category"])

            st.markdown("**Season**")
            st.write(trend_output["season"])

            st.markdown("**Target Retailer**")
            st.write(trend_output["retailer"])

            st.markdown("**Retailer Positioning**")
            st.write(trend_output["retailer_positioning"])

        with col2:
            st.markdown("**Price Sensitivity**")
            st.write(trend_output["price_sensitivity"])

            st.markdown("**Quality Expectation**")
            st.write(trend_output["quality_expectation"])

            st.markdown("**Requested Style Direction**")
            st.write(trend_output["style_direction"])

        st.divider()

        st.markdown("### 🎨 Color Direction")
        st.write(", ".join(trend_output["colors"]))

        st.markdown("### 🧵 Pattern Direction")
        st.write(", ".join(trend_output["patterns"]))

        st.markdown("### 🪡 Material Direction")
        st.write(", ".join(trend_output["materials"]))

        st.markdown("### 🛍️ Retail Angle")
        st.write(trend_output["retail_angle"])

        st.markdown("### 💡 Agent Insight")
        st.success(trend_output["insight"])

        if use_llm and enhanced_trend_output:
            st.divider()
            st.markdown("### 🤖 LLM-Enhanced Trend Intelligence")

            if enhanced_trend_output["llm_available"]:
                st.markdown(enhanced_trend_output["enhanced_trend_markdown"])
            else:
                show_soft_warning()

    with tab2:
        st.subheader("🧵 Product Concept Agent")
        st.markdown(f"## {product_concept['product_name']}")
        st.success(product_concept["concept_summary"])

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Product Details")
            st.write(f"**Product Type:** {product_concept['product_type']}")
            st.write(f"**Category:** {product_concept['category']}")
            st.write(f"**Season:** {product_concept['season']}")
            st.write(f"**Target Retailer:** {product_concept['retailer']}")
            st.write(f"**Trend Direction:** {product_concept['trend_name']}")
            st.write(f"**Target FOB:** ${product_concept['target_fob']}")
            st.write(f"**Estimated FOB Range:** {product_concept['estimated_fob_range']}")

        with col2:
            st.markdown("### Size Options")
            for size in product_concept["size_options"]:
                st.write(f"- {size}")

            st.markdown("### Components")
            for component in product_concept["components"]:
                st.write(f"- {component}")

        st.divider()

        st.markdown("### 🎨 Color Direction")
        st.write("**Hero Colors:**")
        for color in product_concept["hero_colors"]:
            st.write(f"- {color}")

        if product_concept["supporting_colors"]:
            st.write("**Supporting Colors:**")
            for color in product_concept["supporting_colors"]:
                st.write(f"- {color}")

        st.markdown("### 🪡 Pattern Direction")
        for pattern in product_concept["pattern_direction"]:
            st.write(f"- {pattern}")

        st.markdown("### 🧶 Material Recommendation")
        for material in product_concept["material_recommendation"]:
            st.write(f"- {material}")

        st.divider()

        st.markdown("### 🛍️ Buyer Fit")
        st.info(product_concept["buyer_fit"])

        st.markdown("### 📦 Sample Brief")
        st.write(product_concept["sample_brief"])

        if use_llm and enhanced_product_output:
            st.divider()
            st.markdown("### 🤖 LLM-Enhanced Product Development Brief")

            if enhanced_product_output["llm_available"]:
                st.markdown(enhanced_product_output["enhanced_product_markdown"])
            else:
                show_soft_warning()

    with tab3:
        st.subheader("🏭 Supplier Match Agent")
        suppliers = supplier_results

        if suppliers:
            for index, supplier in enumerate(suppliers, start=1):
                st.markdown(f"### #{index} {supplier['supplier_name']}")
                st.write(f"**Country:** {supplier['country']}")
                st.write(f"**Speciality:** {supplier['speciality']}")
                st.write(f"**FOB Range:** {supplier['fob_range']}")
                st.write(f"**MOQ:** {supplier['min_moq']}")
                st.write(f"**Lead Time:** {supplier['lead_time_days']} days")
                st.write(f"**QC Score:** {supplier['qc_score']}/100")
                st.write(f"**Compliance Score:** {supplier['compliance_score']}/100")
                st.write(f"**Match Score:** {supplier['match_score']}/100")

                st.markdown("**Why this supplier matched:**")
                for reason in supplier["reasons"]:
                    st.write(f"- {reason}")

                st.divider()
        else:
            st.warning("No matching suppliers found for this category and target FOB.")

    with tab4:
        st.subheader("💰 Landed Cost Agent")

        if selected_supplier:
            st.info(
                f"Costing based on top supplier: "
                f"{landed_cost_output['supplier_used']} "
                f"({landed_cost_output['supplier_country']})"
            )
        else:
            st.warning("No supplier selected. Costing uses category-level assumptions only.")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Base FOB", f"${landed_cost_output['base_fob']}")
            st.metric("Estimated Landed Cost", f"${landed_cost_output['estimated_landed_cost']}")

        with col2:
            st.metric("Suggested Wholesale", f"${landed_cost_output['suggested_wholesale_price']}")
            st.metric("Gross Profit / Unit", f"${landed_cost_output['gross_profit_per_unit']}")

        with col3:
            st.metric("Target Margin", f"{landed_cost_output['target_margin_percent']}%")
            st.metric("Gross Margin", f"{landed_cost_output['gross_margin_percent']}%")

        st.divider()

        st.markdown("### Cost Breakdown")

        cost_table = {
            "Cost Component": [
                "Base FOB",
                "Freight",
                "Duty / Tariff",
                "Packaging",
                "Inspection / QC",
                "Warehouse / Handling",
                "Risk Buffer",
                "Estimated Landed Cost",
            ],
            "Amount ($)": [
                landed_cost_output["base_fob"],
                landed_cost_output["freight_cost"],
                landed_cost_output["duty_cost"],
                landed_cost_output["packaging_cost"],
                landed_cost_output["inspection_cost"],
                landed_cost_output["warehouse_cost"],
                landed_cost_output["risk_buffer_cost"],
                landed_cost_output["estimated_landed_cost"],
            ],
        }

        st.table(cost_table)

        st.markdown("### Assumptions Used")

        for assumption, value in landed_cost_output["assumptions"].items():
            readable_name = assumption.replace("_", " ").title()
            st.write(f"**{readable_name}:** {value}")

        st.caption(
            "Note: This is a prototype estimate. Real costing should connect to actual HS codes, "
            "freight quotes, tariff data, packaging specs, and retailer chargeback rules."
        )

    with tab5:
        st.subheader("🛡️ Compliance Guardian Agent")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Compliance Score", f"{compliance_output['compliance_score']}/100")
            st.metric("Compliance Risk Level", compliance_output["risk_level"])

        with col2:
            st.write("**Category:**", compliance_output["category"])
            st.write("**Retailer:**", compliance_output["retailer"])

        st.markdown("### Required Compliance Checks")
        for check in compliance_output["required_checks"]:
            st.write(f"- {check}")

        st.markdown("### Documents Needed")
        for doc in compliance_output["documents_needed"]:
            st.write(f"- {doc}")

        st.markdown("### Compliance Risk Notes")
        for note in compliance_output["risk_notes"]:
            st.warning(note)

        st.markdown("### Supplier Notes")
        for note in compliance_output["supplier_notes"]:
            st.info(note)

        st.markdown("### Retailer-Specific Notes")
        for note in compliance_output["retailer_specific_notes"]:
            st.write(f"- {note}")

        st.success(compliance_output["recommendation"])

        st.divider()

        st.subheader("🧵 Quality Sentinel Agent")

        col3, col4 = st.columns(2)

        with col3:
            st.metric("QC Risk Level", quality_output["risk_level"])
            st.metric("Supplier QC Score", f"{quality_output['supplier_qc_score']}/100")

        with col4:
            st.write("**Product:**", quality_output["product_name"])
            st.write("**Category:**", quality_output["category"])

        st.markdown("### Key QC Risks")
        for risk in quality_output["key_qc_risks"]:
            st.write(f"- {risk}")

        st.markdown("### Materials to Check")
        for material in quality_output["materials_to_check"]:
            st.write(f"- {material}")

        st.markdown("### Pattern / Construction Checks")
        for pattern in quality_output["patterns_to_check"]:
            st.write(f"- {pattern}")

        st.markdown("### Recommended Inspection Plan")
        for step in quality_output["inspection_plan"]:
            st.write(f"- {step}")

        st.success(quality_output["recommendation"])

    with tab6:
        st.subheader("📦 Order Orchestrator Agent")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Supplier", order_output["supplier_name"])

        with col2:
            st.metric("Lead Time", f"{order_output['supplier_lead_time_days']} days")

        with col3:
            st.metric("Total Timeline", f"{order_output['estimated_total_timeline_days']} days")

        st.info(f"Estimated arrival date: **{order_output['estimated_arrival_date']}**")

        st.divider()

        st.markdown("### Milestone Plan")
        st.table(order_output["milestones"])

        st.markdown("### Delay Risk Notes")
        for risk in order_output["delay_risks"]:
            st.warning(risk)

        st.markdown("### Routing Guide Checklist")
        for item in order_output["routing_checklist"]:
            st.write(f"- {item}")

        st.success(order_output["recommendation"])

    with tab7:
        st.subheader("🛍️ Buyer Pitch Agent")

        st.markdown(f"## {buyer_pitch_output['pitch_headline']}")

        st.markdown("### Executive Summary")
        st.success(buyer_pitch_output["executive_summary"])

        st.markdown("### Buyer Value")
        st.write(buyer_pitch_output["buyer_value"])

        st.markdown("### Supplier Summary")
        st.info(buyer_pitch_output["supplier_summary"])

        st.markdown("### Commercial Summary")
        st.write(buyer_pitch_output["commercial_summary"])

        st.markdown("### Risk Summary")
        st.warning(buyer_pitch_output["risk_summary"])

        st.markdown("### Recommended Next Steps")
        for step in buyer_pitch_output["next_steps"]:
            st.write(f"- {step}")

        st.divider()

        st.markdown("### Short Buyer Pitch")
        st.code(buyer_pitch_output["short_pitch"], language="text")

        if use_llm and enhanced_pitch_output:
            st.divider()
            st.markdown("### 🤖 LLM-Enhanced Buyer Pitch")

            if enhanced_pitch_output["llm_available"]:
                st.markdown(enhanced_pitch_output["enhanced_pitch_markdown"])
            else:
                show_soft_warning()

    with tab8:
        st.subheader("📄 Final AI Sourcing Report")
        st.markdown(final_report)

        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            st.download_button(
                label="Download Report as Markdown",
                data=final_report,
                file_name="lync_bridge_ai_sourcing_report.md",
                mime="text/markdown",
            )

        with col2:
            st.download_button(
                label="Download Printable HTML Report",
                data=html_report,
                file_name="lync_bridge_ai_sourcing_report.html",
                mime="text/html",
            )

        st.info(
            "Tip: Open the downloaded HTML file in Chrome, then press Ctrl+P and choose "
            "'Save as PDF' to create a polished PDF report."
        )

else:
    st.info("Fill the buyer requirement in the sidebar and click **Generate Sourcing Plan**.")