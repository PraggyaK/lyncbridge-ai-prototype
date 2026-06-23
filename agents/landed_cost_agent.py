def landed_cost_agent(product_concept, selected_supplier=None):
    """
    Estimates landed cost and suggested wholesale price.
    Prototype V1 uses simplified assumptions.
    """

    target_fob = float(product_concept["target_fob"])
    category = product_concept["category"]
    retailer = product_concept["retailer"]

    # Category-based assumptions
    category_cost_rules = {
        "Bedding": {
            "freight_rate": 0.10,
            "duty_rate": 0.08,
            "packaging_rate": 0.04,
            "inspection_rate": 0.02,
            "warehouse_rate": 0.04,
            "target_margin": 0.22
        },
        "Bath": {
            "freight_rate": 0.09,
            "duty_rate": 0.07,
            "packaging_rate": 0.03,
            "inspection_rate": 0.02,
            "warehouse_rate": 0.04,
            "target_margin": 0.20
        },
        "Cushions": {
            "freight_rate": 0.12,
            "duty_rate": 0.09,
            "packaging_rate": 0.05,
            "inspection_rate": 0.02,
            "warehouse_rate": 0.05,
            "target_margin": 0.24
        },
        "Throws": {
            "freight_rate": 0.11,
            "duty_rate": 0.08,
            "packaging_rate": 0.04,
            "inspection_rate": 0.02,
            "warehouse_rate": 0.04,
            "target_margin": 0.22
        },
        "Kitchen Textile": {
            "freight_rate": 0.08,
            "duty_rate": 0.07,
            "packaging_rate": 0.03,
            "inspection_rate": 0.02,
            "warehouse_rate": 0.03,
            "target_margin": 0.20
        }
    }

    rules = category_cost_rules.get(category, category_cost_rules["Bedding"])

    # Supplier lead-time risk adjustment
    lead_time_risk_buffer = 0

    if selected_supplier:
        lead_time = selected_supplier.get("lead_time_days", 45)

        if lead_time > 50:
            lead_time_risk_buffer = 0.03
        elif lead_time > 40:
            lead_time_risk_buffer = 0.015

    freight_cost = round(target_fob * rules["freight_rate"], 2)
    duty_cost = round(target_fob * rules["duty_rate"], 2)
    packaging_cost = round(target_fob * rules["packaging_rate"], 2)
    inspection_cost = round(target_fob * rules["inspection_rate"], 2)
    warehouse_cost = round(target_fob * rules["warehouse_rate"], 2)
    risk_buffer_cost = round(target_fob * lead_time_risk_buffer, 2)

    landed_cost = round(
        target_fob
        + freight_cost
        + duty_cost
        + packaging_cost
        + inspection_cost
        + warehouse_cost
        + risk_buffer_cost,
        2
    )

    target_margin = rules["target_margin"]

    suggested_wholesale_price = round(
        landed_cost / (1 - target_margin),
        2
    )

    gross_profit_per_unit = round(
        suggested_wholesale_price - landed_cost,
        2
    )

    gross_margin_percent = round(
        (gross_profit_per_unit / suggested_wholesale_price) * 100,
        2
    )

    cost_output = {
        "category": category,
        "retailer": retailer,
        "base_fob": target_fob,
        "freight_cost": freight_cost,
        "duty_cost": duty_cost,
        "packaging_cost": packaging_cost,
        "inspection_cost": inspection_cost,
        "warehouse_cost": warehouse_cost,
        "risk_buffer_cost": risk_buffer_cost,
        "estimated_landed_cost": landed_cost,
        "target_margin_percent": round(target_margin * 100, 2),
        "suggested_wholesale_price": suggested_wholesale_price,
        "gross_profit_per_unit": gross_profit_per_unit,
        "gross_margin_percent": gross_margin_percent,
        "assumptions": {
            "freight_rate": f"{round(rules['freight_rate'] * 100, 2)}%",
            "duty_rate": f"{round(rules['duty_rate'] * 100, 2)}%",
            "packaging_rate": f"{round(rules['packaging_rate'] * 100, 2)}%",
            "inspection_rate": f"{round(rules['inspection_rate'] * 100, 2)}%",
            "warehouse_rate": f"{round(rules['warehouse_rate'] * 100, 2)}%"
        }
    }

    if selected_supplier:
        cost_output["supplier_used"] = selected_supplier["supplier_name"]
        cost_output["supplier_country"] = selected_supplier["country"]
        cost_output["supplier_lead_time"] = selected_supplier["lead_time_days"]

    return cost_output