from dataclasses import dataclass, field
from typing import List
import re


VALID_PLATFORMS = ["Marketplace Listing", "Instagram", "Facebook", "WhatsApp", "Website SEO"]
VALID_TONES = ["Warm", "Premium", "Heritage", "Playful", "Minimal"]
VALID_BUYERS = ["Conscious Shoppers", "Gift Buyers", "Home Decor Lovers", "Tourists", "Boutique Retailers"]
VALID_LANGUAGES = ["English", "Hindi + English", "Local-language friendly English"]


@dataclass
class ValidationResult:
    is_valid: bool = True
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    def add_error(self, message: str) -> None:
        self.errors.append(message)
        self.is_valid = False

    def add_warning(self, message: str) -> None:
        self.warnings.append(message)


def sanitize_text(value: str, max_len: int = 600) -> str:
    value = (value or "").strip()
    value = re.sub(r"\s+", " ", value)
    value = re.sub(r"[<>{}|\\^`]", "", value)
    return value[:max_len]


def validate_inputs(
    craft_name: str,
    artisan_story: str,
    materials: str,
    location: str,
    platform: str,
    tone: str,
    buyer: str,
    language: str,
) -> ValidationResult:
    result = ValidationResult()

    craft_name = (craft_name or "").strip()
    artisan_story = (artisan_story or "").strip()
    materials = (materials or "").strip()
    location = (location or "").strip()

    if len(craft_name) < 3:
        result.add_error("Add the craft or product name, such as handwoven cotton scarf or blue pottery bowl.")
    if len(artisan_story) < 20:
        result.add_error("Add a short maker story so the assistant can create authentic storytelling.")
    if len(materials) < 5:
        result.add_error("Add materials or process details, such as terracotta, natural dyes, cane weaving, or hand carving.")
    if len(location) < 2:
        result.add_error("Add the artisan location or community.")

    if platform not in VALID_PLATFORMS:
        result.add_error(f"Choose a valid primary channel: {', '.join(VALID_PLATFORMS)}.")
    if tone not in VALID_TONES:
        result.add_error(f"Choose a valid tone: {', '.join(VALID_TONES)}.")
    if buyer not in VALID_BUYERS:
        result.add_error(f"Choose a valid buyer segment: {', '.join(VALID_BUYERS)}.")
    if language not in VALID_LANGUAGES:
        result.add_error(f"Choose a valid language mode: {', '.join(VALID_LANGUAGES)}.")

    if len(artisan_story) > 500:
        result.add_warning("The story is rich. The assistant will condense it into buyer-friendly copy.")
    if tone == "Premium" and buyer == "Tourists":
        result.add_warning("Premium tourist copy works best when you include a portability or gifting angle.")

    return result
