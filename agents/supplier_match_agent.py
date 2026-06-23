import pandas as pd


def load_suppliers(file_path="data/suppliers.csv"):
    """
    Loads supplier data from CSV.
    """
    return pd.read_csv(file_path)


def calculate_supplier_score(row, category, target_fob, country_preference):
    """
    Scores each supplier based on:
    - category match
    - FOB price fit
    - QC score
    - compliance score
    - lead time
    - country preference
    """

    score = 0
    reasons = []

    # Category match
    if row["category"].lower() == category.lower():
        score += 30
        reasons.append("Strong category match")
    else:
        return 0, ["Category does not match"]

    # FOB price fit
    if row["fob_min"] <= target_fob <= row["fob_max"]:
        score += 25
        reasons.append("Target FOB fits supplier price range")
    elif row["fob_min"] <= target_fob + 2:
        score += 12
        reasons.append("FOB slightly above target but still possible")
    else:
        reasons.append("FOB may be outside ideal range")

    # Quality score
    qc_points = row["qc_score"] * 0.15
    score += qc_points

    if row["qc_score"] >= 88:
        reasons.append("Strong QC performance")
    elif row["qc_score"] >= 82:
        reasons.append("Acceptable QC performance")
    else:
        reasons.append("QC needs closer monitoring")

    # Compliance score
    compliance_points = row["compliance_score"] * 0.15
    score += compliance_points

    if row["compliance_score"] >= 88:
        reasons.append("Strong compliance history")
    elif row["compliance_score"] >= 82:
        reasons.append("Acceptable compliance history")
    else:
        reasons.append("Compliance risk needs review")

    # Lead time score
    if row["lead_time_days"] <= 35:
        score += 10
        reasons.append("Fast lead time")
    elif row["lead_time_days"] <= 50:
        score += 6
        reasons.append("Moderate lead time")
    else:
        score += 2
        reasons.append("Longer lead time")

    # Country preference
    if country_preference != "Any":
        if row["country"].lower() == country_preference.lower():
            score += 10
            reasons.append("Matches preferred sourcing country")
        else:
            reasons.append("Does not match preferred country")

    return round(score, 2), reasons


def supplier_match_agent(category, target_fob, country_preference="Any"):
    """
    Returns top 3 suppliers for the selected category and target FOB.
    """

    suppliers = load_suppliers()
    results = []

    for _, row in suppliers.iterrows():
        score, reasons = calculate_supplier_score(
            row=row,
            category=category,
            target_fob=target_fob,
            country_preference=country_preference
        )

        if score > 0:
            results.append({
                "supplier_name": row["supplier_name"],
                "country": row["country"],
                "category": row["category"],
                "min_moq": row["min_moq"],
                "fob_range": f"${row['fob_min']} - ${row['fob_max']}",
                "lead_time_days": row["lead_time_days"],
                "qc_score": row["qc_score"],
                "compliance_score": row["compliance_score"],
                "speciality": row["speciality"],
                "match_score": score,
                "reasons": reasons
            })

    results = sorted(results, key=lambda x: x["match_score"], reverse=True)

    return results[:3]