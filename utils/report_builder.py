def build_final_report(
    trend_output,
    product_concept,
    supplier_results,
    landed_cost_output,
    compliance_output,
    quality_output,
    buyer_pitch_output,
    order_output=None
):
    """
    Builds a complete markdown-style sourcing report from all agent outputs.
    """

    top_supplier = supplier_results[0] if supplier_results else None

    if top_supplier:
        supplier_section = f"""
## 4. Recommended Supplier

**Supplier Name:** {top_supplier['supplier_name']}  
**Country:** {top_supplier['country']}  
**Speciality:** {top_supplier['speciality']}  
**FOB Range:** {top_supplier['fob_range']}  
**MOQ:** {top_supplier['min_moq']} units  
**Lead Time:** {top_supplier['lead_time_days']} days  
**QC Score:** {top_supplier['qc_score']}/100  
**Compliance Score:** {top_supplier['compliance_score']}/100  
**Match Score:** {top_supplier['match_score']}/100  

**Why this supplier matched:**
"""
        for reason in top_supplier["reasons"]:
            supplier_section += f"- {reason}\n"
    else:
        supplier_section = """
## 4. Recommended Supplier

No supplier match was found. Supplier validation is required before sampling.
"""

    compliance_checks = "\n".join(
        [f"- {check}" for check in compliance_output["required_checks"]]
    )

    documents_needed = "\n".join(
        [f"- {doc}" for doc in compliance_output["documents_needed"]]
    )

    qc_risks = "\n".join(
        [f"- {risk}" for risk in quality_output["key_qc_risks"]]
    )

    inspection_plan = "\n".join(
        [f"- {step}" for step in quality_output["inspection_plan"]]
    )

    next_steps = "\n".join(
        [f"- {step}" for step in buyer_pitch_output["next_steps"]]
    )

    # Step 11F: Optional Order Orchestrator section
    order_section = ""

    if order_output:
        milestone_lines = "\n".join(
            [
                f"- {item['milestone']} | Owner: {item['owner']} | "
                f"Target Date: {item['target_date']} | Risk: {item['risk']}"
                for item in order_output["milestones"]
            ]
        )

        routing_lines = "\n".join(
            [f"- {item}" for item in order_output["routing_checklist"]]
        )

        delay_lines = "\n".join(
            [f"- {item}" for item in order_output["delay_risks"]]
        )

        order_section = f"""
---

## 8. Order Orchestration Timeline

**Supplier:** {order_output['supplier_name']}  
**Supplier Country:** {order_output['supplier_country']}  
**Supplier Lead Time:** {order_output['supplier_lead_time_days']} days  
**Estimated Total Timeline:** {order_output['estimated_total_timeline_days']} days  
**Estimated Arrival Date:** {order_output['estimated_arrival_date']}  

### Milestone Plan

{milestone_lines}

### Delay Risk Notes

{delay_lines}

### Routing Guide Checklist

{routing_lines}

### Order Recommendation

{order_output['recommendation']}
"""

    report = f"""
# Lync Bridge AI Sourcing Report

## 1. Executive Summary

{buyer_pitch_output['executive_summary']}

**Short Buyer Pitch:**  
{buyer_pitch_output['short_pitch']}

---

## 2. Buyer Requirement

**Target Retailer:** {product_concept['retailer']}  
**Product Category:** {product_concept['category']}  
**Season:** {product_concept['season']}  
**Target FOB:** ${product_concept['target_fob']}  
**Trend Direction:** {trend_output['trend_name']}  

---

## 3. Product Concept

**Product Name:** {product_concept['product_name']}  
**Product Type:** {product_concept['product_type']}  
**Estimated FOB Range:** {product_concept['estimated_fob_range']}  

### Concept Summary

{product_concept['concept_summary']}

### Color Direction

**Hero Colors:** {", ".join(product_concept['hero_colors'])}

**Supporting Colors:** {", ".join(product_concept['supporting_colors']) if product_concept['supporting_colors'] else "N/A"}

### Pattern Direction

{", ".join(product_concept['pattern_direction'])}

### Material Recommendation

{", ".join(product_concept['material_recommendation'])}

### Components

{", ".join(product_concept['components'])}

### Sample Brief

{product_concept['sample_brief']}

---

{supplier_section}

---

## 5. Landed Cost Estimate

**Base FOB:** ${landed_cost_output['base_fob']}  
**Freight:** ${landed_cost_output['freight_cost']}  
**Duty / Tariff:** ${landed_cost_output['duty_cost']}  
**Packaging:** ${landed_cost_output['packaging_cost']}  
**Inspection / QC:** ${landed_cost_output['inspection_cost']}  
**Warehouse / Handling:** ${landed_cost_output['warehouse_cost']}  
**Risk Buffer:** ${landed_cost_output['risk_buffer_cost']}  

**Estimated Landed Cost:** ${landed_cost_output['estimated_landed_cost']}  
**Suggested Wholesale Price:** ${landed_cost_output['suggested_wholesale_price']}  
**Gross Profit Per Unit:** ${landed_cost_output['gross_profit_per_unit']}  
**Estimated Gross Margin:** {landed_cost_output['gross_margin_percent']}%  

---

## 6. Compliance Review

**Compliance Score:** {compliance_output['compliance_score']}/100  
**Compliance Risk Level:** {compliance_output['risk_level']}  

### Required Checks

{compliance_checks}

### Documents Needed

{documents_needed}

### Compliance Recommendation

{compliance_output['recommendation']}

---

## 7. Quality Risk Review

**QC Risk Level:** {quality_output['risk_level']}  
**Supplier QC Score:** {quality_output['supplier_qc_score']}/100  

### Key QC Risks

{qc_risks}

### Inspection Plan

{inspection_plan}

### QC Recommendation

{quality_output['recommendation']}

{order_section}

---

## 9. Buyer Value

{buyer_pitch_output['buyer_value']}

---

## 10. Commercial Summary

{buyer_pitch_output['commercial_summary']}

---

## 11. Risk Summary

{buyer_pitch_output['risk_summary']}

---

## 12. Recommended Next Steps

{next_steps}

---

*Generated by Lync Bridge AI Sourcing Copilot.*
"""

    return report.strip()


def build_html_report(final_report):
    """
    Converts markdown-style report text into a simple printable HTML report.
    This is lightweight and Streamlit-friendly.
    """

    html_content = final_report

    html_content = html_content.replace("&", "&amp;")
    html_content = html_content.replace("<", "&lt;")
    html_content = html_content.replace(">", "&gt;")

    lines = html_content.split("\n")
    converted_lines = []

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("# "):
            converted_lines.append(f"<h1>{stripped[2:]}</h1>")
        elif stripped.startswith("## "):
            converted_lines.append(f"<h2>{stripped[3:]}</h2>")
        elif stripped.startswith("### "):
            converted_lines.append(f"<h3>{stripped[4:]}</h3>")
        elif stripped.startswith("- "):
            converted_lines.append(f"<li>{stripped[2:]}</li>")
        elif stripped == "---":
            converted_lines.append("<hr>")
        elif stripped == "":
            converted_lines.append("<br>")
        else:
            line = stripped.replace("**", "<strong>", 1)

            while "**" in line:
                line = line.replace("**", "</strong>", 1)
                if "**" in line:
                    line = line.replace("**", "<strong>", 1)

            converted_lines.append(f"<p>{line}</p>")

    body = "\n".join(converted_lines)

    html_report = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Lync Bridge AI Sourcing Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 40px;
            line-height: 1.6;
            color: #222;
            background: #ffffff;
        }}

        h1 {{
            color: #12355b;
            border-bottom: 3px solid #12355b;
            padding-bottom: 10px;
        }}

        h2 {{
            color: #1b4965;
            margin-top: 32px;
            border-bottom: 1px solid #ddd;
            padding-bottom: 6px;
        }}

        h3 {{
            color: #2f6690;
            margin-top: 20px;
        }}

        p {{
            font-size: 14px;
        }}

        li {{
            margin-bottom: 6px;
            font-size: 14px;
        }}

        hr {{
            border: none;
            border-top: 1px solid #ddd;
            margin: 28px 0;
        }}

        .footer {{
            margin-top: 40px;
            font-size: 12px;
            color: #666;
            border-top: 1px solid #ddd;
            padding-top: 12px;
        }}

        @media print {{
            body {{
                margin: 20mm;
            }}

            button {{
                display: none;
            }}
        }}
    </style>
</head>
<body>
    {body}

    <div class="footer">
        Generated by Lync Bridge AI Sourcing Copilot.
    </div>
</body>
</html>
"""

    return html_report.strip()