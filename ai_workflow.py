"""
Core generation workflow for Artisan Atlas AI.

The app works with or without a HuggingFace token. When a token is available,
it asks an instruction model for structured marketplace strategy. Otherwise it
uses a deterministic local generator so demos remain instant and reliable.
"""

import json
import os
import re
from typing import Optional

import requests
from dotenv import load_dotenv

load_dotenv()

HF_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN", "")
PRIMARY_MODEL = "mistralai/Mistral-7B-Instruct-v0.3"
FALLBACK_MODEL = "HuggingFaceH4/zephyr-7b-beta"
HF_API_BASE = "https://api-inference.huggingface.co/models"

PLATFORM_RULES = {
    "Marketplace Listing": {
        "goal": "convert browsing shoppers with a clear title, story, and benefits",
        "length": "80-140 word product description",
        "tip": "Lead with materials, process, and the human story behind the object.",
    },
    "Instagram": {
        "goal": "create visual desire, discovery, and saves",
        "length": "120-220 characters with skimmable line breaks",
        "tip": "Pair the product with a making-process visual or close-up detail.",
    },
    "Facebook": {
        "goal": "build local community support and word-of-mouth",
        "length": "50-90 words",
        "tip": "Mention the place, occasion, and why buying local matters.",
    },
    "WhatsApp": {
        "goal": "make a warm direct-sales message easy to forward",
        "length": "40-70 words",
        "tip": "Keep it personal, include price cue or availability, and ask for replies.",
    },
    "Website SEO": {
        "goal": "help search engines and shoppers understand the craft",
        "length": "concise SEO title, meta description, and keywords",
        "tip": "Use material, place, technique, and buyer intent phrases.",
    },
}

TONE_DESCRIPTORS = {
    "Warm": "human, grounded, welcoming, community-minded",
    "Premium": "refined, calm, quality-focused, elegant",
    "Heritage": "tradition-rich, place-aware, respectful of craft lineage",
    "Playful": "bright, friendly, energetic, approachable",
    "Minimal": "clear, modern, restrained, product-led",
}

BUYER_DESCRIPTORS = {
    "Conscious Shoppers": "buyers who care about sustainability, maker stories, and fair value",
    "Gift Buyers": "people looking for meaningful gifts with a personal story",
    "Home Decor Lovers": "buyers styling homes, studios, cafes, and cozy corners",
    "Tourists": "visitors looking for portable, authentic local memories",
    "Boutique Retailers": "store owners seeking small-batch products with margin and story",
}


def build_system_prompt() -> str:
    return (
        "You are an expert marketplace strategist for local artisans. "
        "You help makers sell online without flattening their culture, story, or voice. "
        "Return only strict JSON. No markdown, no commentary outside JSON."
    )


def build_user_prompt(
    craft_name: str,
    artisan_story: str,
    materials: str,
    location: str,
    price_range: str,
    platform: str,
    tone: str,
    buyer: str,
    language: str,
) -> str:
    rules = PLATFORM_RULES.get(platform, PLATFORM_RULES["Marketplace Listing"])
    tone_desc = TONE_DESCRIPTORS.get(tone, tone)
    buyer_desc = BUYER_DESCRIPTORS.get(buyer, buyer)
    return f"""
Create a digital marketplace kit for a local artisan.

Inputs:
- Craft/product: {craft_name}
- Artisan story: {artisan_story}
- Materials/process: {materials}
- Location/community: {location}
- Price range: {price_range}
- Primary channel: {platform}
- Tone: {tone} ({tone_desc})
- Buyer segment: {buyer} ({buyer_desc})
- Output language: {language}

Channel guidance:
- Goal: {rules["goal"]}
- Length: {rules["length"]}
- Tip: {rules["tip"]}

Return strict JSON with this exact shape:
{{
  "brand_story": "a polished maker story in 80-120 words",
  "listing_title": "search-friendly product title",
  "listing_description": "marketplace-ready description",
  "social_posts": [
    {{"channel": "Instagram", "copy": "...", "cta": "..."}},
    {{"channel": "Facebook", "copy": "...", "cta": "..."}},
    {{"channel": "WhatsApp", "copy": "...", "cta": "..."}}
  ],
  "seo_tags": ["tag one", "tag two"],
  "photo_shot_list": ["shot idea 1", "shot idea 2", "shot idea 3"],
  "outreach_ideas": ["partnership idea 1", "partnership idea 2", "partnership idea 3"],
  "trust_signals": ["proof point 1", "proof point 2", "proof point 3"],
  "next_steps": ["action 1", "action 2", "action 3"]
}}
"""


def build_instruct_prompt(system: str, user: str) -> str:
    return f"<s>[INST] {system}\n\n{user} [/INST]"


def call_hf_inference(prompt: str, model: str = PRIMARY_MODEL) -> str:
    headers = {"Authorization": f"Bearer {HF_API_TOKEN}", "Content-Type": "application/json"}
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 1800,
            "temperature": 0.78,
            "top_p": 0.9,
            "repetition_penalty": 1.12,
            "do_sample": True,
            "return_full_text": False,
        },
        "options": {"wait_for_model": True, "use_cache": False},
    }
    response = requests.post(f"{HF_API_BASE}/{model}", headers=headers, json=payload, timeout=120)
    response.raise_for_status()
    result = response.json()
    if isinstance(result, list) and result:
        return result[0].get("generated_text", "")
    if isinstance(result, dict):
        return result.get("generated_text", str(result))
    return str(result)


def extract_json_from_text(text: str) -> Optional[dict]:
    text = re.sub(r"```(?:json)?", "", text).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    match = re.search(r"\{[\s\S]*\}", text)
    if not match:
        return None
    try:
        return json.loads(match.group())
    except json.JSONDecodeError:
        return None


def _clean_slug(text: str) -> str:
    words = re.findall(r"[A-Za-z0-9]+", text.lower())
    return " ".join(words[:5]) if words else "handmade craft"


def generate_fallback_kit(
    craft_name: str,
    artisan_story: str,
    materials: str,
    location: str,
    price_range: str,
    platform: str,
    tone: str,
    buyer: str,
    language: str,
) -> dict:
    craft = craft_name.strip() or "handmade craft"
    place = location.strip() or "the local community"
    process = materials.strip() or "locally sourced materials and hand-finished details"
    story = artisan_story.strip() or "Each piece is shaped slowly by hand, carrying the maker's eye for detail and care."
    price = price_range.strip() or "accessible small-batch pricing"
    slug = _clean_slug(craft)

    brand_story = (
        f"From {place}, this artisan practice turns {process} into pieces with a real sense of touch. "
        f"{story} The result is {craft} made for people who want objects with origin, patience, "
        f"and a maker's signature rather than mass-produced sameness."
    )

    return {
        "brand_story": brand_story,
        "listing_title": f"Handmade {craft} from {place} | {tone} Artisan Gift",
        "listing_description": (
            f"Bring home {craft} crafted in {place} using {process}. Each piece is made in small batches, "
            f"so natural variations become part of its character. Ideal for {buyer.lower()}, this item "
            f"offers a meaningful alternative to factory-made decor and gifts. Price range: {price}."
        ),
        "social_posts": [
            {
                "channel": "Instagram",
                "copy": f"Made by hand in {place}, this {craft} carries the quiet beauty of real craft. Save it for your next thoughtful gift or home refresh.",
                "cta": "Message to order or ask for available pieces.",
            },
            {
                "channel": "Facebook",
                "copy": f"Local craft deserves a wider audience. This {craft} is shaped with {process}, carrying the story of {place} into everyday spaces.",
                "cta": "Share with someone who loves handmade work.",
            },
            {
                "channel": "WhatsApp",
                "copy": f"New handmade {craft} available from {place}. Small-batch, personal, and made with {process}.",
                "cta": "Reply for photos, price, and delivery options.",
            },
        ],
        "seo_tags": [
            f"handmade {slug}",
            f"{place.lower()} artisan",
            "local handmade gifts",
            "small batch craft",
            f"{slug} online",
            "artisan marketplace",
            "ethical handmade decor",
            "maker story",
        ],
        "photo_shot_list": [
            "Close-up of texture, weave, glaze, grain, or hand-finished detail.",
            "Artisan hands at work to prove process and authenticity.",
            "Styled use-case photo showing scale in a home, gift, or boutique setting.",
        ],
        "outreach_ideas": [
            "Partner with a local cafe, homestay, or boutique for a maker-of-the-month display.",
            "Create a short making-process reel and ask local tourism pages to reshare it.",
            "Offer a limited gift bundle for festivals, weddings, or corporate gifting.",
        ],
        "trust_signals": [
            "Mention small-batch production and natural variations clearly.",
            "Add care instructions, delivery timeline, and return/exchange policy.",
            "Show maker name, location, and process photos near the buy button.",
        ],
        "next_steps": [
            f"Publish the {platform.lower()} version first with three strong product photos.",
            "Ask two existing customers for short testimonials or photos.",
            "Track which post gets saves, shares, and direct messages, then reuse that angle.",
        ],
        "_fallback": True,
        "_error": (
            "No HuggingFace API token found. Showing local AI-style demo output. "
            "Add HUGGINGFACEHUB_API_TOKEN to .env for live model generation."
        )
        if not HF_API_TOKEN
        else "",
    }


def generate_marketplace_kit(
    craft_name: str,
    artisan_story: str,
    materials: str,
    location: str,
    price_range: str,
    platform: str,
    tone: str,
    buyer: str,
    language: str,
) -> dict:
    if not HF_API_TOKEN:
        return generate_fallback_kit(craft_name, artisan_story, materials, location, price_range, platform, tone, buyer, language)

    system_prompt = build_system_prompt()
    user_prompt = build_user_prompt(craft_name, artisan_story, materials, location, price_range, platform, tone, buyer, language)
    full_prompt = build_instruct_prompt(system_prompt, user_prompt)

    for model in [PRIMARY_MODEL, FALLBACK_MODEL]:
        try:
            parsed = extract_json_from_text(call_hf_inference(full_prompt, model=model))
            if parsed and parsed.get("brand_story") and parsed.get("social_posts"):
                parsed["_model_used"] = model
                return parsed
        except Exception:
            continue

    kit = generate_fallback_kit(craft_name, artisan_story, materials, location, price_range, platform, tone, buyer, language)
    kit["_error"] = "Live model generation was unavailable, so a local marketplace kit was created."
    return kit


def score_kit(kit: dict) -> dict:
    description = kit.get("listing_description", "")
    tags = kit.get("seo_tags", [])
    posts = kit.get("social_posts", [])
    completeness = min(1.0, sum(bool(kit.get(k)) for k in ["brand_story", "listing_title", "listing_description"]) / 3)
    discoverability = min(1.0, len(tags) / 8)
    reach = min(1.0, len(posts) / 3)
    clarity = 1.0 if 120 <= len(description) <= 900 else 0.78
    return {
        "story": round((completeness + clarity) / 2, 2),
        "seo": round(discoverability, 2),
        "reach": round(reach, 2),
        "overall": round((completeness + discoverability + reach + clarity) / 4, 2),
    }
