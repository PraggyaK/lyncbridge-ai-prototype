def quality_sentinel_agent(product_concept, selected_supplier=None):
    """
    Generates QC risk profile and inspection plan.
    Prototype V1 uses category + supplier quality score.
    """

    category = product_concept["category"]
    product_name = product_concept["product_name"]
    materials = product_concept["material_recommendation"]
    patterns = product_concept["pattern_direction"]

    category_qc_risks = {
        "Bedding": [
            "Stitching inconsistency",
            "Color bleeding after wash",
            "Shrinkage variation",
            "Print alignment mismatch",
            "Incorrect size tolerance",
            "Packaging damage during transit"
        ],
        "Bath": [
            "Low absorbency",
            "Lint shedding",
            "Uneven towel GSM",
            "Color variation across set",
            "Shrinkage after washing"
        ],
        "Cushions": [
            "Weak seams",
            "Uneven filling",
            "Embroidery defects",
            "Fabric shade variation",
            "Incorrect cushion size"
        ],
        "Throws": [
            "Pilling after use",
            "Color shedding",
            "Uneven edge finishing",
            "Fabric weight inconsistency",
            "Packaging compression damage"
        ],
        "Kitchen Textile": [
            "Poor heat resistance",
            "Weak stitching",
            "Color bleeding",
            "Incorrect set components",
            "Packaging presentation issues"
        ]
    }

    risks = category_qc_risks.get(category, [
        "General stitching issue",
        "Color variation",
        "Packaging defect",
        "Incorrect labeling"
    ])

    supplier_qc_score = 75
    risk_level = "Medium"

    if selected_supplier:
        supplier_qc_score = selected_supplier.get("qc_score", 75)

        if supplier_qc_score >= 90:
            risk_level = "Low"
        elif supplier_qc_score >= 84:
            risk_level = "Medium"
        else:
            risk_level = "High"

    inspection_plan = [
        "Approve pre-production sample before bulk production",
        "Check material quality against approved sample",
        "Verify color, size, stitching, labeling, and packaging",
        "Conduct final random inspection before shipment"
    ]

    if risk_level in ["Medium", "High"]:
        inspection_plan.insert(
            2,
            "Conduct during-production inspection to catch issues early"
        )

    if category == "Bedding":
        inspection_plan.append("Perform wash test for shrinkage and colorfastness.")
    elif category == "Bath":
        inspection_plan.append("Check towel GSM, absorbency, lint shedding, and wash performance.")
    elif category == "Kitchen Textile":
        inspection_plan.append("Review heat resistance for mitts and pot holders where applicable.")

    output = {
        "product_name": product_name,
        "category": category,
        "risk_level": risk_level,
        "supplier_qc_score": supplier_qc_score,
        "key_qc_risks": risks,
        "materials_to_check": materials,
        "patterns_to_check": patterns,
        "inspection_plan": inspection_plan,
        "recommendation": (
            f"{product_name} has a {risk_level.lower()} QC risk profile. "
            "Do not approve bulk shipment without inspection report and sample comparison."
        )
    }

    return output