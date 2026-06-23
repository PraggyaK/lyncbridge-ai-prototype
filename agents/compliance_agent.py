import json


def load_compliance_rules(file_path="data/compliance_rules.json"):
    """
    Loads compliance rules from JSON file.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def compliance_guardian_agent(product_concept, selected_supplier=None):
    """
    Creates compliance checklist and risk notes for the selected product.
    Prototype V1 uses category-level rules.
    """

    rules_data = load_compliance_rules()

    category = product_concept["category"]
    retailer = product_concept["retailer"]

    category_rules = rules_data.get(category, {
        "required_checks": [
            "Fiber content label required",
            "Care instruction label required",
            "Country of origin label required",
            "Pre-shipment inspection required"
        ],
        "documents_needed": [
            "Commercial invoice",
            "Packing list",
            "Bill of lading",
            "Inspection report"
        ],
        "risk_notes": [
            "Category-specific compliance rules need manual review"
        ]
    })

    compliance_score = 75
    risk_level = "Medium"

    supplier_notes = []

    if selected_supplier:
        supplier_compliance_score = selected_supplier.get("compliance_score", 75)

        if supplier_compliance_score >= 90:
            compliance_score = 92
            risk_level = "Low"
            supplier_notes.append("Supplier has strong compliance history.")
        elif supplier_compliance_score >= 84:
            compliance_score = 84
            risk_level = "Medium"
            supplier_notes.append("Supplier has acceptable compliance history.")
        else:
            compliance_score = 70
            risk_level = "High"
            supplier_notes.append("Supplier compliance score needs close review.")

        supplier_notes.append(
            f"Supplier country: {selected_supplier.get('country', 'Unknown')}"
        )

    retailer_specific_notes = []

    if retailer in ["HomeGoods", "TJX"]:
        retailer_specific_notes.append(
            "Retailer likely requires strict carton labeling, packaging accuracy, and routing-guide compliance."
        )
    elif retailer in ["Ross", "Burlington"]:
        retailer_specific_notes.append(
            "Retailer likely prioritizes value, packaging accuracy, and chargeback avoidance."
        )
    elif retailer == "Five Below":
        retailer_specific_notes.append(
            "Retailer likely requires low-cost packaging and fast-moving shelf-ready presentation."
        )
    else:
        retailer_specific_notes.append(
            "Retailer-specific routing guide should be reviewed before shipment."
        )

    output = {
        "category": category,
        "retailer": retailer,
        "compliance_score": compliance_score,
        "risk_level": risk_level,
        "required_checks": category_rules["required_checks"],
        "documents_needed": category_rules["documents_needed"],
        "risk_notes": category_rules["risk_notes"],
        "supplier_notes": supplier_notes,
        "retailer_specific_notes": retailer_specific_notes,
        "recommendation": (
            "Proceed with sample development, but complete compliance checklist "
            "before bulk production and require pre-shipment inspection."
        )
    }

    return output