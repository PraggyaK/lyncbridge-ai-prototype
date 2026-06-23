from utils.llm_client import call_llm

def product_concept_agent(trend_output, target_fob):
    """
    Converts trend intelligence into a buyer-ready product concept.
    Uses rule-based logic for prototype V1.
    """

    category = trend_output["category"]
    retailer = trend_output["retailer"]
    season = trend_output["season"]
    trend_name = trend_output["trend_name"]
    colors = trend_output["colors"]
    patterns = trend_output["patterns"]
    materials = trend_output["materials"]
    retail_angle = trend_output["retail_angle"]

    # Product naming logic
    if category == "Bedding":
        product_name = f"{trend_name} 3-Piece Quilt Set"
        product_type = "Quilt Set"
        size_options = ["Twin", "Full/Queen", "King"]
        components = ["1 quilt", "2 pillow shams"]
        estimated_fob_min = round(target_fob - 1.2, 2)
        estimated_fob_max = round(target_fob + 0.8, 2)

    elif category == "Bath":
        product_name = f"{trend_name} 6-Piece Towel Set"
        product_type = "Towel Set"
        size_options = ["Hand Towel", "Bath Towel", "Washcloth"]
        components = ["2 bath towels", "2 hand towels", "2 washcloths"]
        estimated_fob_min = round(target_fob - 0.8, 2)
        estimated_fob_max = round(target_fob + 0.6, 2)

    elif category == "Cushions":
        product_name = f"{trend_name} Decorative Cushion"
        product_type = "Decorative Cushion"
        size_options = ["18x18 inch", "20x20 inch"]
        components = ["1 cushion cover", "polyester insert"]
        estimated_fob_min = round(target_fob - 0.5, 2)
        estimated_fob_max = round(target_fob + 0.5, 2)

    elif category == "Throws":
        product_name = f"{trend_name} Cozy Throw Blanket"
        product_type = "Throw Blanket"
        size_options = ["50x60 inch", "60x70 inch"]
        components = ["1 throw blanket"]
        estimated_fob_min = round(target_fob - 0.7, 2)
        estimated_fob_max = round(target_fob + 0.7, 2)

    elif category == "Kitchen Textile":
        product_name = f"{trend_name} Kitchen Textile Set"
        product_type = "Kitchen Textile Set"
        size_options = ["Standard kitchen set"]
        components = ["2 kitchen towels", "1 oven mitt", "1 pot holder"]
        estimated_fob_min = round(target_fob - 0.4, 2)
        estimated_fob_max = round(target_fob + 0.4, 2)

    else:
        product_name = f"{trend_name} Value Home Product"
        product_type = "Home Textile Product"
        size_options = ["Standard size"]
        components = ["Assorted product components"]
        estimated_fob_min = round(target_fob - 0.5, 2)
        estimated_fob_max = round(target_fob + 0.5, 2)

    # Avoid negative FOB estimates
    estimated_fob_min = max(1, estimated_fob_min)

    concept = {
        "product_name": product_name,
        "product_type": product_type,
        "category": category,
        "retailer": retailer,
        "season": season,
        "trend_name": trend_name,
        "concept_summary": (
            f"{product_name} is a trend-led {category.lower()} concept designed for {retailer}. "
            f"It uses {', '.join(colors[:3])} tones, {patterns[0]} styling, and "
            f"{materials[0]} construction to deliver {retail_angle}."
        ),
        "hero_colors": colors[:3],
        "supporting_colors": colors[3:],
        "pattern_direction": patterns,
        "material_recommendation": materials,
        "size_options": size_options,
        "components": components,
        "estimated_fob_range": f"${estimated_fob_min} - ${estimated_fob_max}",
        "target_fob": target_fob,
        "buyer_fit": (
            f"This concept fits {retailer} because it gives a high perceived-value look "
            f"while staying close to the target FOB of ${target_fob}."
        ),
        "sample_brief": (
            f"Develop sample for {product_name}. Use main colors {', '.join(colors[:3])}. "
            f"Primary pattern direction: {patterns[0]}. Recommended material: {materials[0]}. "
            f"Target FOB should remain around ${target_fob}."
        )
    }

    return concept
def llm_product_concept_agent(product_concept):
    """
    Enhances the product concept into a more polished buyer/product-development note.
    Falls back if LLM is unavailable.
    """

    prompt = f"""
You are a product development manager for home textile sourcing.

Convert this product concept into a polished product-development brief.

Product Concept:
{product_concept}

Return markdown with these exact sections:

## Product Story
## Design Details
## Materials & Construction
## Retailer Fit
## Sampling Notes
## Cost Discipline Notes

Keep it practical and suitable for US off-price / discount retail.
"""

    llm_output = call_llm(prompt)

    if llm_output is None:
        return {
            "llm_available": False,
            "enhanced_product_markdown": None
        }

    return {
        "llm_available": True,
        "enhanced_product_markdown": llm_output
    }