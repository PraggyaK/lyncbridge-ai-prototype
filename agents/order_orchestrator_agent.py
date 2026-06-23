from datetime import datetime, timedelta


def order_orchestrator_agent(product_concept, selected_supplier=None):
    """
    Creates a sourcing/order timeline from sampling to shipment.
    Prototype V1 uses estimated milestone logic.
    """

    product_name = product_concept["product_name"]
    category = product_concept["category"]
    retailer = product_concept["retailer"]

    lead_time_days = 45
    supplier_name = "Supplier not selected"
    supplier_country = "Unknown"

    if selected_supplier:
        lead_time_days = int(selected_supplier.get("lead_time_days", 45))
        supplier_name = selected_supplier.get("supplier_name", "Supplier not selected")
        supplier_country = selected_supplier.get("country", "Unknown")

    today = datetime.today()

    # Timeline assumptions
    concept_approval_days = 3
    sample_request_days = 2
    sample_development_days = 12
    sample_review_days = 5
    costing_confirmation_days = 3
    po_issue_days = 2
    production_days = lead_time_days
    inspection_days = 3
    shipment_booking_days = 4
    transit_days = 25

    concept_approval_date = today + timedelta(days=concept_approval_days)
    sample_request_date = concept_approval_date + timedelta(days=sample_request_days)
    sample_ready_date = sample_request_date + timedelta(days=sample_development_days)
    sample_approval_date = sample_ready_date + timedelta(days=sample_review_days)
    costing_final_date = sample_approval_date + timedelta(days=costing_confirmation_days)
    po_issue_date = costing_final_date + timedelta(days=po_issue_days)
    production_complete_date = po_issue_date + timedelta(days=production_days)
    inspection_date = production_complete_date + timedelta(days=inspection_days)
    shipment_booking_date = inspection_date + timedelta(days=shipment_booking_days)
    estimated_arrival_date = shipment_booking_date + timedelta(days=transit_days)

    milestones = [
        {
            "milestone": "Concept approval",
            "owner": "Buyer / Lync Bridge",
            "target_date": concept_approval_date.strftime("%Y-%m-%d"),
            "status": "Pending",
            "risk": "Low"
        },
        {
            "milestone": "Sample request sent to supplier",
            "owner": "Lync Bridge",
            "target_date": sample_request_date.strftime("%Y-%m-%d"),
            "status": "Pending",
            "risk": "Low"
        },
        {
            "milestone": "Sample development completed",
            "owner": supplier_name,
            "target_date": sample_ready_date.strftime("%Y-%m-%d"),
            "status": "Pending",
            "risk": "Medium"
        },
        {
            "milestone": "Sample review and approval",
            "owner": "Buyer / Lync Bridge",
            "target_date": sample_approval_date.strftime("%Y-%m-%d"),
            "status": "Pending",
            "risk": "Medium"
        },
        {
            "milestone": "Final costing and MOQ confirmation",
            "owner": "Lync Bridge / Supplier",
            "target_date": costing_final_date.strftime("%Y-%m-%d"),
            "status": "Pending",
            "risk": "Medium"
        },
        {
            "milestone": "Purchase order issued",
            "owner": "Buyer / Importer",
            "target_date": po_issue_date.strftime("%Y-%m-%d"),
            "status": "Pending",
            "risk": "Low"
        },
        {
            "milestone": "Bulk production completed",
            "owner": supplier_name,
            "target_date": production_complete_date.strftime("%Y-%m-%d"),
            "status": "Pending",
            "risk": "Medium" if lead_time_days <= 50 else "High"
        },
        {
            "milestone": "Final random inspection",
            "owner": "QC Inspector",
            "target_date": inspection_date.strftime("%Y-%m-%d"),
            "status": "Pending",
            "risk": "High"
        },
        {
            "milestone": "Shipment booking and document check",
            "owner": "Logistics / Lync Bridge",
            "target_date": shipment_booking_date.strftime("%Y-%m-%d"),
            "status": "Pending",
            "risk": "Medium"
        },
        {
            "milestone": "Estimated arrival at destination",
            "owner": "Logistics",
            "target_date": estimated_arrival_date.strftime("%Y-%m-%d"),
            "status": "Estimated",
            "risk": "Medium"
        }
    ]

    delay_risks = []

    if lead_time_days > 50:
        delay_risks.append("Supplier lead time is above 50 days; production delay risk is high.")
    elif lead_time_days > 40:
        delay_risks.append("Supplier lead time is moderate; timeline should be monitored closely.")
    else:
        delay_risks.append("Supplier lead time is relatively fast for this category.")

    if category == "Bedding":
        delay_risks.append("Bedding requires careful sample approval for size, quilting, print alignment, and wash performance.")
    elif category == "Bath":
        delay_risks.append("Bath products may need additional absorbency and GSM validation before bulk approval.")
    elif category == "Kitchen Textile":
        delay_risks.append("Kitchen textile sets require component count and heat-resistance checks where applicable.")

    routing_checklist = [
        "Confirm retailer routing guide before shipment",
        "Validate carton labels and PO number format",
        "Confirm master carton dimensions and weight",
        "Check packaging artwork and barcode placement",
        "Confirm inspection report before shipment release",
        "Verify commercial invoice, packing list, and bill of lading",
        "Confirm destination warehouse / DC instructions"
    ]

    output = {
        "product_name": product_name,
        "category": category,
        "retailer": retailer,
        "supplier_name": supplier_name,
        "supplier_country": supplier_country,
        "supplier_lead_time_days": lead_time_days,
        "estimated_total_timeline_days": (
            concept_approval_days
            + sample_request_days
            + sample_development_days
            + sample_review_days
            + costing_confirmation_days
            + po_issue_days
            + production_days
            + inspection_days
            + shipment_booking_days
            + transit_days
        ),
        "estimated_arrival_date": estimated_arrival_date.strftime("%Y-%m-%d"),
        "milestones": milestones,
        "delay_risks": delay_risks,
        "routing_checklist": routing_checklist,
        "recommendation": (
            "Proceed to sampling only after buyer confirms concept direction. "
            "Do not release shipment until inspection, routing guide, and export documents are complete."
        )
    }

    return output