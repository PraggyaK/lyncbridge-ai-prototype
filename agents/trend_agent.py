import json
from utils.llm_client import call_llm

def load_json(file_path):
    """
    Loads JSON data from a file.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def trend_scout_agent(category, retailer, season, style_direction):
    """
    Generates trend intelligence based on product category, retailer, season, and style direction.
    Uses mock trend data for prototype V1.
    """

    trend_data = load_json("data/trend_signals.json")
    retailer_data = load_json("data/retailer_profiles.json")

    category_trends = trend_data.get(category, {})
    selected_trend = category_trends.get(season)

    # Fallback if exact season is not available
    if not selected_trend and category_trends:
        selected_trend = list(category_trends.values())[0]

    retailer_profile = retailer_data.get(retailer, {})

    if not selected_trend:
        selected_trend = {
            "trend_name": "Commercial Value Trend",
            "colors": ["ivory", "soft grey", "muted blue"],
            "patterns": ["simple border", "small scale print", "solid texture"],
            "materials": ["cotton blend", "microfiber"],
            "retail_angle": "safe, value-led design suitable for discount retail"
        }

    output = {
        "trend_name": selected_trend["trend_name"],
        "category": category,
        "season": season,
        "retailer": retailer,
        "colors": selected_trend["colors"],
        "patterns": selected_trend["patterns"],
        "materials": selected_trend["materials"],
        "retail_angle": selected_trend["retail_angle"],
        "retailer_positioning": retailer_profile.get("positioning", "value-led retailer"),
        "retailer_style_fit": retailer_profile.get("preferred_style", []),
        "price_sensitivity": retailer_profile.get("price_sensitivity", "medium"),
        "quality_expectation": retailer_profile.get("quality_expectation", "medium"),
        "style_direction": style_direction,
        "insight": (
            f"{selected_trend['trend_name']} fits {retailer} because it combines "
            f"{selected_trend['retail_angle']} with the requested style direction: "
            f"{style_direction}."
        )
    }

    return output
def llm_trend_scout_agent(category, retailer, season, style_direction, base_trend_output):
    """
    Enhances the rule-based trend output using an LLM.
    If LLM is unavailable, returns the original rule-based output.
    """

    prompt = f"""
You are a senior trend intelligence analyst for a US discount retail sourcing agency.

Create enhanced trend intelligence for this buyer requirement.

Buyer Requirement:
- Category: {category}
- Retailer: {retailer}
- Season: {season}
- Style Direction: {style_direction}

Base trend data:
- Trend name: {base_trend_output['trend_name']}
- Colors: {base_trend_output['colors']}
- Patterns: {base_trend_output['patterns']}
- Materials: {base_trend_output['materials']}
- Retail angle: {base_trend_output['retail_angle']}

Return a concise markdown output with these exact sections:

## Trend Narrative
## Why It Fits The Retailer
## Color Direction
## Pattern Direction
## Material Direction
## Commercial Notes

Keep it realistic for discount retail sourcing. Do not overpromise.
"""

    llm_output = call_llm(prompt)

    if llm_output is None:
        return {
            "llm_available": False,
            "enhanced_trend_markdown": None
        }

    return {
        "llm_available": True,
        "enhanced_trend_markdown": llm_output
    }