import base64
import time
from datetime import datetime
from html import escape
from pathlib import Path

import streamlit as st

from ai_workflow import generate_marketplace_kit
from validation import sanitize_text


APP_DIR = Path(__file__).parent
BANNER_PATH = APP_DIR / "assets" / "artisan-market-banner.png"

st.set_page_config(
    page_title="RangRajasthan Market",
    page_icon="RR",
    layout="wide",
    initial_sidebar_state="collapsed",
)


PRODUCTS = [
    {
        "id": "blue-pottery-bowl",
        "name": "Jaipur Blue Pottery Serving Bowl",
        "artist": "Meera Kumawat",
        "city": "Jaipur",
        "region": "Dhundhar",
        "category": "Pottery",
        "price": 1299,
        "mrp": 1599,
        "rating": 4.9,
        "reviews": 86,
        "orders": 218,
        "likes": 3800,
        "stock": 14,
        "top": True,
        "delivery": "3-5 days",
        "image": "https://images.unsplash.com/photo-1610701596007-11502861dcfa?auto=format&fit=crop&w=1000&q=80",
        "gallery": [
            "https://images.unsplash.com/photo-1610701596007-11502861dcfa?auto=format&fit=crop&w=1000&q=80",
            "https://images.unsplash.com/photo-1578749556568-bc2c40e68b61?auto=format&fit=crop&w=1000&q=80",
        ],
        "story": "Hand-painted quartz clay bowl made in a family workshop that keeps Jaipur blue pottery alive.",
        "caption": "A little piece of Jaipur for your table. Hand-painted, small-batch, and made to be gifted.",
        "description": "This serving bowl is painted by hand with mineral-inspired blue motifs and finished in a glossy glaze. Each piece has slight brush variations, making it feel personal rather than factory-made.",
        "materials": "Quartz clay, glass powder, natural pigments, transparent glaze",
        "care": "Wipe gently with a damp cloth. Avoid microwave use.",
        "tags": ["Blue pottery", "Jaipur", "Hand painted", "Gifting"],
    },
    {
        "id": "bagru-dupatta",
        "name": "Bagru Block Print Cotton Dupatta",
        "artist": "Rafiq Chhipa",
        "city": "Bagru",
        "region": "Jaipur Rural",
        "category": "Textile",
        "price": 1890,
        "mrp": 2300,
        "rating": 4.8,
        "reviews": 61,
        "orders": 154,
        "likes": 2900,
        "stock": 9,
        "top": True,
        "delivery": "4-7 days",
        "image": "https://images.unsplash.com/photo-1610030469983-98e550d6193c?auto=format&fit=crop&w=1000&q=80",
        "gallery": [
            "https://images.unsplash.com/photo-1610030469983-98e550d6193c?auto=format&fit=crop&w=1000&q=80",
            "https://images.unsplash.com/photo-1594736797933-d0401ba2fe65?auto=format&fit=crop&w=1000&q=80",
        ],
        "story": "Natural dyed cotton dupatta printed with hand-carved wooden blocks in Bagru.",
        "caption": "Slow fashion from Rajasthan: block by block, color by color, made by hand.",
        "description": "A breathable cotton dupatta with layered Bagru block motifs. It is made in small batches using hand printing, so minor pattern shifts are part of its handmade charm.",
        "materials": "Cotton, natural dyes, hand-carved wooden blocks",
        "care": "Cold wash separately. Dry in shade.",
        "tags": ["Bagru", "Natural dye", "Cotton", "Slow fashion"],
    },
    {
        "id": "jodhpur-wood-lamp",
        "name": "Carved Sheesham Table Lamp",
        "artist": "Kailash Suthar",
        "city": "Jodhpur",
        "region": "Marwar",
        "category": "Home Decor",
        "price": 2450,
        "mrp": 2990,
        "rating": 4.7,
        "reviews": 39,
        "orders": 96,
        "likes": 1800,
        "stock": 6,
        "top": False,
        "delivery": "5-8 days",
        "image": "https://images.unsplash.com/photo-1513506003901-1e6a229e2d15?auto=format&fit=crop&w=1000&q=80",
        "gallery": [
            "https://images.unsplash.com/photo-1513506003901-1e6a229e2d15?auto=format&fit=crop&w=1000&q=80",
            "https://images.unsplash.com/photo-1540932239986-30128078f3c5?auto=format&fit=crop&w=1000&q=80",
        ],
        "story": "Locally carved sheesham wood lamp inspired by old Jodhpur jharokha patterns.",
        "caption": "Warm light, carved by hand. Built for homes that love detail.",
        "description": "A warm table lamp with carved wood detailing and a restrained profile for modern homes. The pattern references old window forms from the blue city.",
        "materials": "Sheesham wood, brass fittings, cotton shade",
        "care": "Dust with a dry cloth. Keep away from moisture.",
        "tags": ["Jodhpur", "Wood craft", "Home decor", "Lamp"],
    },
    {
        "id": "lac-bangles",
        "name": "Jaipur Lac Bangles Set",
        "artist": "Saira Bano",
        "city": "Jaipur",
        "region": "Dhundhar",
        "category": "Jewellery",
        "price": 799,
        "mrp": 999,
        "rating": 4.9,
        "reviews": 132,
        "orders": 321,
        "likes": 4600,
        "stock": 22,
        "top": True,
        "delivery": "2-4 days",
        "image": "https://images.unsplash.com/photo-1605100804763-247f67b3557e?auto=format&fit=crop&w=1000&q=80",
        "gallery": [
            "https://images.unsplash.com/photo-1605100804763-247f67b3557e?auto=format&fit=crop&w=1000&q=80",
            "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?auto=format&fit=crop&w=1000&q=80",
        ],
        "story": "Bright lac bangles shaped and finished by hand for festivals, gifting, and daily color.",
        "caption": "Color from the bazaars of Jaipur, finished by artisan hands.",
        "description": "A vibrant lac bangle set with festive color and hand-applied detailing. Made for gifting, wedding functions, and everyday styling.",
        "materials": "Lac, mirror accents, metal base, hand finishing",
        "care": "Store separately. Avoid perfume and water contact.",
        "tags": ["Lac", "Jewellery", "Festival", "Jaipur"],
    },
    {
        "id": "kota-doria-saree",
        "name": "Kota Doria Cotton Saree",
        "artist": "Nirmala Bairwa",
        "city": "Kota",
        "region": "Hadoti",
        "category": "Textile",
        "price": 3600,
        "mrp": 4200,
        "rating": 4.8,
        "reviews": 47,
        "orders": 77,
        "likes": 2100,
        "stock": 4,
        "top": False,
        "delivery": "5-9 days",
        "image": "https://images.unsplash.com/photo-1610189017367-b1dd245a6f85?auto=format&fit=crop&w=1000&q=80",
        "gallery": [
            "https://images.unsplash.com/photo-1610189017367-b1dd245a6f85?auto=format&fit=crop&w=1000&q=80",
            "https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?auto=format&fit=crop&w=1000&q=80",
        ],
        "story": "Lightweight Kota Doria weave with airy khat checks, made for Rajasthan summers.",
        "caption": "A saree that feels like air and carries the discipline of the loom.",
        "description": "A light cotton saree with the signature open Kota Doria check. It drapes softly and is made for warm days, formal gatherings, and heritage-led wardrobes.",
        "materials": "Cotton yarn, handloom weave, zari border",
        "care": "Dry clean recommended for first wash.",
        "tags": ["Kota Doria", "Saree", "Handloom", "Cotton"],
    },
    {
        "id": "miniature-painting",
        "name": "Udaipur Miniature Painting",
        "artist": "Devendra Sharma",
        "city": "Udaipur",
        "region": "Mewar",
        "category": "Painting",
        "price": 5200,
        "mrp": 6500,
        "rating": 5.0,
        "reviews": 29,
        "orders": 42,
        "likes": 5200,
        "stock": 3,
        "top": True,
        "delivery": "6-10 days",
        "image": "https://images.unsplash.com/photo-1579783900882-c0d3dad7b119?auto=format&fit=crop&w=1000&q=80",
        "gallery": [
            "https://images.unsplash.com/photo-1579783900882-c0d3dad7b119?auto=format&fit=crop&w=1000&q=80",
            "https://images.unsplash.com/photo-1541961017774-22349e4a1262?auto=format&fit=crop&w=1000&q=80",
        ],
        "story": "Fine brush miniature painting inspired by Mewar court art and lake city palettes.",
        "caption": "A royal detail from Udaipur, painted slowly enough to hold your gaze.",
        "description": "A collectible miniature painting created with patient brushwork and a layered color palette. It is shipped framed with authenticity details from the artist.",
        "materials": "Handmade paper, natural pigment style colors, fine brush",
        "care": "Keep framed and away from direct sunlight.",
        "tags": ["Udaipur", "Miniature", "Painting", "Mewar"],
    },
]

REVIEWS = [
    ("Aditi", "Beautiful packaging and the product felt genuinely handmade.", 5),
    ("Rohan", "Loved the story card. It made the gift feel personal.", 5),
    ("Neha", "Good quality and quick delivery. Would buy again.", 4),
]


def image_data_uri(path: Path) -> str:
    if not path.exists():
        return ""
    return "data:image/png;base64," + base64.b64encode(path.read_bytes()).decode("utf-8")


def rupees(value: int) -> str:
    return f"INR {value:,}"


def product_lookup() -> dict:
    return {product["id"]: product for product in PRODUCTS}


def cart_total() -> int:
    cart = st.session_state.get("cart", {})
    lookup = product_lookup()
    return sum(lookup[item_id]["price"] * qty for item_id, qty in cart.items())


def add_to_cart(product_id: str, qty: int = 1) -> None:
    cart = st.session_state.setdefault("cart", {})
    cart[product_id] = cart.get(product_id, 0) + qty
    st.toast("Added to cart")


def wishlist_toggle(product_id: str) -> None:
    wishlist = st.session_state.setdefault("wishlist", set())
    if product_id in wishlist:
        wishlist.remove(product_id)
        st.toast("Removed from wishlist")
    else:
        wishlist.add(product_id)
        st.toast("Saved to wishlist")


def ai_suggestions(product: dict) -> dict:
    score = min(99, int((product["rating"] * 12) + (product["likes"] / 95) + (product["orders"] / 8)))
    return {
        "score": score,
        "caption": (
            f"From {product['city']} to your home: {product['name']} by {product['artist']}. "
            f"Small-batch, handmade, and rooted in Rajasthan's craft tradition."
        ),
        "reel": (
            "Use a 12-second reel: process close-up, artisan face, final product in use, "
            f"then a price and stock frame showing {product['stock']} pieces left."
        ),
        "seo": [
            f"handmade {product['name'].lower()}",
            f"{product['city'].lower()} artisan craft",
            f"buy {product['category'].lower()} online India",
            "Rajasthani handmade gift",
        ],
        "engagement": [
            "Pin a comment with price, delivery time, care instructions, and WhatsApp support.",
            "Ask buyers to vote on the next color, motif, or size.",
            "Post the making process before the product photo to build trust first.",
        ],
    }


def init_state() -> None:
    st.session_state.setdefault("cart", {})
    st.session_state.setdefault("wishlist", set())
    st.session_state.setdefault("orders", [])
    st.session_state.setdefault("selected_product", PRODUCTS[0]["id"])
    st.session_state.setdefault("studio_kit", None)
    st.session_state.setdefault("seller_products", [])


def product_score(product: dict) -> int:
    return min(100, int(product["rating"] * 10 + product["orders"] / 4 + product["likes"] / 140 + product["stock"]))


def render_css() -> None:
    banner_uri = image_data_uri(BANNER_PATH)
    st.markdown(
        f"""
<style>
:root {{
  --ink: #1f1712;
  --muted: #74675f;
  --paper: #fff8ee;
  --surface: #ffffff;
  --line: #eadfce;
  --soft: #f5ebdc;
  --terra: #b95532;
  --maroon: #782437;
  --indigo: #253f72;
  --green: #4b7048;
  --gold: #c88a2d;
}}
html, body, [class*="css"] {{
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}}
.stApp {{
  color: var(--ink);
  background:
    linear-gradient(180deg, rgba(255,248,238,.96), rgba(255,248,238,.96)),
    repeating-linear-gradient(45deg, rgba(120,36,55,.05) 0 1px, transparent 1px 20px);
}}
#MainMenu, footer, header {{ visibility: hidden; }}
.block-container {{ max-width: 1420px; padding: 1rem 1.6rem 3rem; }}
.topbar {{
  position: sticky;
  top: 0;
  z-index: 20;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  padding: .78rem 1rem;
  margin-bottom: 1rem;
  background: rgba(255,248,238,.94);
  border: 1px solid var(--line);
  border-radius: 8px;
  backdrop-filter: blur(14px);
}}
.brand {{ display:flex; align-items:center; gap:.75rem; }}
.mark {{
  width:42px; height:42px; border-radius:8px;
  display:grid; place-items:center;
  color:white; font-weight:950;
  background:linear-gradient(135deg,var(--maroon),var(--terra));
}}
.brand h1 {{ margin:0; font-size:1.18rem; letter-spacing:0; }}
.brand span, .navhint {{ color:var(--muted); font-size:.8rem; font-weight:700; }}
.hero {{
  min-height: 380px;
  border: 1px solid rgba(31,23,18,.14);
  border-radius: 8px;
  overflow:hidden;
  background:
    linear-gradient(90deg, rgba(31,23,18,.92) 0%, rgba(31,23,18,.66) 48%, rgba(31,23,18,.18) 100%),
    url("{banner_uri}");
  background-size: cover;
  background-position:center;
  display:flex;
  align-items:end;
  padding:2rem;
}}
.hero h2 {{
  color:#fff8ee;
  margin:0 0 .75rem;
  max-width:900px;
  font-size:clamp(2.4rem,5.9vw,5.4rem);
  line-height:.92;
  letter-spacing:0;
}}
.hero p {{ color:rgba(255,248,238,.9); max-width:760px; margin:0; font-size:1.02rem; line-height:1.55; }}
.trustbar, .metrics {{
  display:grid;
  grid-template-columns: repeat(4,minmax(0,1fr));
  gap:1px;
  background:var(--line);
  border:1px solid var(--line);
  border-radius:8px;
  overflow:hidden;
  margin:1rem 0 1.2rem;
}}
.trustbar div, .metric {{
  background:#fff;
  padding:1rem;
}}
.trustbar b, .metric b {{ display:block; color:var(--maroon); font-size:1.18rem; }}
.trustbar span, .metric span {{ color:var(--muted); font-size:.82rem; }}
.section-title {{
  display:flex;
  align-items:end;
  justify-content:space-between;
  gap:1rem;
  margin:1.15rem 0 .75rem;
}}
.section-title h2 {{ margin:0; font-size:1.45rem; letter-spacing:0; }}
.section-title p {{ margin:.16rem 0 0; color:var(--muted); font-size:.9rem; }}
.product-card, .panel, .post-card, .checkout, .detail-shell {{
  background:#fff;
  border:1px solid var(--line);
  border-radius:8px;
  overflow:hidden;
  box-shadow: 0 12px 28px rgba(88,54,30,.07);
}}
.product-card {{ margin-bottom:.7rem; }}
.product-image {{
  min-height:238px;
  background-size:cover;
  background-position:center;
  position:relative;
}}
.product-image span {{
  position:absolute;
  top:.7rem; left:.7rem;
  background:rgba(31,23,18,.84);
  color:#fff8ee;
  padding:.28rem .58rem;
  border-radius:999px;
  font-size:.74rem;
  font-weight:850;
}}
.product-body, .panel, .post-card, .checkout {{ padding:1rem; }}
.row-between {{ display:flex; align-items:start; justify-content:space-between; gap:.8rem; }}
.row-between h3 {{ margin:0; font-size:1.02rem; letter-spacing:0; }}
.price {{ color:var(--maroon); font-weight:900; white-space:nowrap; }}
.mrp {{ color:var(--muted); text-decoration:line-through; font-size:.78rem; }}
p {{ line-height:1.55; }}
.muted, .product-body p, .post-card p, .panel p {{ color:var(--muted); font-size:.9rem; }}
.seller {{ color:var(--green); font-size:.8rem; font-weight:850; margin-top:.5rem; }}
.tag-row {{ display:flex; flex-wrap:wrap; gap:.35rem; margin-top:.7rem; }}
.tag-row span, .pill {{
  display:inline-flex;
  background:var(--soft);
  color:var(--indigo);
  border:1px solid var(--line);
  border-radius:999px;
  padding:.23rem .58rem;
  font-size:.74rem;
  font-weight:800;
}}
.detail-shell {{ padding:1rem; }}
.detail-image {{
  min-height:460px;
  border-radius:8px;
  background-size:cover;
  background-position:center;
  border:1px solid var(--line);
}}
.mini-grid {{ display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:.65rem; }}
.mini-stat {{ background:#fff; border:1px solid var(--line); border-radius:8px; padding:.8rem; }}
.mini-stat b {{ display:block; color:var(--maroon); }}
.mini-stat span {{ color:var(--muted); font-size:.78rem; }}
.post-head {{ display:flex; align-items:center; gap:.75rem; margin-bottom:.75rem; }}
.avatar {{
  width:44px; height:44px; border-radius:50%;
  display:grid; place-items:center;
  background:linear-gradient(135deg,var(--gold),var(--terra));
  color:white; font-weight:950;
}}
.post-img {{ height:330px; border-radius:8px; background-size:cover; background-position:center; margin:.8rem 0; }}
.ai-box {{
  background:#f7f1e8;
  border:1px solid var(--line);
  border-left:4px solid var(--indigo);
  border-radius:8px;
  padding:1rem;
  margin-bottom:.85rem;
}}
.ai-box h3 {{ margin:0 0 .42rem; font-size:1rem; }}
.stButton > button {{
  background:var(--maroon) !important;
  color:white !important;
  border:none !important;
  border-radius:8px !important;
  min-height:2.55rem;
  font-weight:850 !important;
}}
.stButton > button:hover {{ background:#641d2d !important; }}
.stTabs [data-baseweb="tab-list"] {{ gap:.35rem; }}
.stTabs [data-baseweb="tab"] {{
  background:#fff;
  border:1px solid var(--line);
  border-radius:8px;
  padding:.45rem .8rem;
}}
.stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"], .stNumberInput input {{
  border-radius:8px !important;
}}
@media (max-width: 900px) {{
  .block-container {{ padding:.75rem; }}
  .topbar {{ align-items:flex-start; flex-direction:column; }}
  .hero {{ min-height:430px; padding:1rem; }}
  .trustbar, .metrics {{ grid-template-columns:repeat(2,minmax(0,1fr)); }}
  .detail-image {{ min-height:300px; }}
  .post-img, .product-image {{ min-height:230px; height:230px; }}
}}
</style>
""",
        unsafe_allow_html=True,
    )


def section(title: str, subtitle: str = "") -> None:
    st.markdown(
        f"""
<div class="section-title">
  <div>
    <h2>{escape(title)}</h2>
    <p>{escape(subtitle)}</p>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )


def product_card(product: dict, index: int) -> None:
    badge = "Top Project" if product["top"] else product["city"]
    discount = int((1 - product["price"] / product["mrp"]) * 100)
    st.markdown(
        f"""
<div class="product-card">
  <div class="product-image" style="background-image:url('{product["image"]}')">
    <span>{badge} · {discount}% off</span>
  </div>
  <div class="product-body">
    <div class="row-between">
      <h3>{escape(product["name"])}</h3>
      <div><div class="price">{rupees(product["price"])}</div><div class="mrp">{rupees(product["mrp"])}</div></div>
    </div>
    <p>{escape(product["story"])}</p>
    <div class="seller">By {escape(product["artist"])} · {escape(product["city"])} · {product["rating"]} rating · {product["orders"]} orders</div>
    <div class="tag-row">{"".join(f"<span>{escape(tag)}</span>" for tag in product["tags"][:3])}</div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )
    c1, c2, c3 = st.columns([1, 1, 1])
    with c1:
        if st.button("View", key=f"view_{product['id']}_{index}", use_container_width=True):
            st.session_state["selected_product"] = product["id"]
            st.toast("Open the Product Detail tab to view details")
    with c2:
        if st.button("Cart", key=f"cart_{product['id']}_{index}", use_container_width=True):
            add_to_cart(product["id"])
    with c3:
        label = "Saved" if product["id"] in st.session_state["wishlist"] else "Save"
        if st.button(label, key=f"wish_{product['id']}_{index}", use_container_width=True):
            wishlist_toggle(product["id"])


def render_product_detail(product: dict) -> None:
    idea = ai_suggestions(product)
    left, right = st.columns([1.1, .9], gap="large")
    with left:
        st.markdown(f'<div class="detail-image" style="background-image:url(\'{product["image"]}\')"></div>', unsafe_allow_html=True)
        st.markdown(
            f"""
<div class="trustbar">
  <div><b>{product["rating"]}/5</b><span>{product["reviews"]} verified reviews</span></div>
  <div><b>{product["orders"]}</b><span>orders completed</span></div>
  <div><b>{product["delivery"]}</b><span>estimated delivery</span></div>
  <div><b>{product["stock"]}</b><span>pieces left</span></div>
</div>
""",
            unsafe_allow_html=True,
        )
    with right:
        st.markdown(
            f"""
<div class="detail-shell">
  <div class="pill">Authentic Rajasthani Craft</div>
  <h2>{escape(product["name"])}</h2>
  <p class="muted">Sold by <b>{escape(product["artist"])}</b> from {escape(product["city"])}, {escape(product["region"])}</p>
  <div class="row-between">
    <div><span class="price" style="font-size:1.55rem">{rupees(product["price"])}</span><br><span class="mrp">{rupees(product["mrp"])}</span></div>
    <div class="pill">AI highlight score {idea["score"]}/100</div>
  </div>
  <p>{escape(product["description"])}</p>
  <p><b>Materials:</b> {escape(product["materials"])}</p>
  <p><b>Care:</b> {escape(product["care"])}</p>
  <div class="tag-row">{"".join(f"<span>{escape(tag)}</span>" for tag in product["tags"])}</div>
</div>
""",
            unsafe_allow_html=True,
        )
        qty = st.number_input("Quantity", min_value=1, max_value=product["stock"], value=1, step=1)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Add to cart", type="primary", use_container_width=True):
                add_to_cart(product["id"], int(qty))
        with c2:
            if st.button("Buy now", use_container_width=True):
                add_to_cart(product["id"], int(qty))
                st.toast("Go to Cart & Checkout to complete the order")

    section("AI Sales Suggestions", "How the artist can showcase this product better.")
    a1, a2, a3 = st.columns(3)
    with a1:
        st.markdown(f'<div class="ai-box"><h3>Caption</h3><p>{escape(idea["caption"])}</p></div>', unsafe_allow_html=True)
    with a2:
        st.markdown(f'<div class="ai-box"><h3>Reel Plan</h3><p>{escape(idea["reel"])}</p></div>', unsafe_allow_html=True)
    with a3:
        tags = "".join(f"<span>{escape(tag)}</span>" for tag in idea["seo"])
        st.markdown(f'<div class="ai-box"><h3>SEO Keywords</h3><div class="tag-row">{tags}</div></div>', unsafe_allow_html=True)

    section("Customer Reviews", "Verified buyer feedback builds trust.")
    cols = st.columns(3)
    for col, (name, text, stars) in zip(cols, REVIEWS):
        with col:
            st.markdown(f'<div class="panel"><b>{escape(name)} · {stars}/5</b><p>{escape(text)}</p></div>', unsafe_allow_html=True)


def render_cart() -> None:
    cart = st.session_state.get("cart", {})
    lookup = product_lookup()
    cart_col, checkout_col = st.columns([1.25, .75], gap="large")
    with cart_col:
        if not cart:
            st.markdown('<div class="checkout"><h3>Your cart is empty</h3><p class="muted">Add products from the marketplace or artist feed.</p></div>', unsafe_allow_html=True)
        else:
            for item_id, qty in list(cart.items()):
                product = lookup[item_id]
                st.markdown(
                    f"""
<div class="checkout">
  <div class="row-between">
    <div>
      <h3>{escape(product["name"])}</h3>
      <p class="muted">Seller: {escape(product["artist"])} · {escape(product["city"])} · Quantity: {qty} · Delivery {product["delivery"]}</p>
    </div>
    <b class="price">{rupees(product["price"] * qty)}</b>
  </div>
</div>
""",
                    unsafe_allow_html=True,
                )
                c1, c2, c3 = st.columns(3)
                with c1:
                    if st.button("Add one", key=f"plus_{item_id}", use_container_width=True):
                        cart[item_id] += 1
                        st.rerun()
                with c2:
                    if st.button("Minus one", key=f"minus_{item_id}", use_container_width=True):
                        cart[item_id] -= 1
                        if cart[item_id] <= 0:
                            cart.pop(item_id)
                        st.rerun()
                with c3:
                    if st.button("Remove", key=f"remove_{item_id}", use_container_width=True):
                        cart.pop(item_id)
                        st.rerun()

    with checkout_col:
        st.markdown('<div class="checkout">', unsafe_allow_html=True)
        st.subheader("Order Summary")
        subtotal = cart_total()
        delivery = 99 if subtotal else 0
        platform_fee = 29 if subtotal else 0
        total = subtotal + delivery + platform_fee
        st.write(f"Subtotal: **{rupees(subtotal)}**")
        st.write(f"Delivery: **{rupees(delivery)}**")
        st.write(f"Platform support fee: **{rupees(platform_fee)}**")
        st.divider()
        st.write(f"Total: **{rupees(total)}**")
        name = st.text_input("Buyer name")
        phone = st.text_input("Phone number")
        pincode = st.text_input("Pincode")
        address = st.text_area("Delivery address", height=90)
        payment = st.selectbox("Payment method", ["UPI", "Card", "Cash on delivery"])
        if st.button("Place demo order", type="primary", use_container_width=True, disabled=not cart):
            if name.strip() and phone.strip() and pincode.strip() and address.strip():
                order_id = f"RR{datetime.now().strftime('%H%M%S')}"
                st.session_state["orders"].append(
                    {"id": order_id, "total": total, "payment": payment, "items": dict(cart), "created": datetime.now().strftime("%d %b %Y, %I:%M %p")}
                )
                st.session_state["cart"] = {}
                st.success(f"Demo order {order_id} placed. The artist receives product, buyer, and delivery details.")
            else:
                st.error("Add buyer name, phone, pincode, and delivery address.")
        st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state["orders"]:
        section("Order History", "Recent demo orders placed in this session.")
        for order in reversed(st.session_state["orders"]):
            st.markdown(
                f'<div class="checkout"><b>{order["id"]}</b><p class="muted">{order["created"]} · {order["payment"]} · {rupees(order["total"])}</p></div>',
                unsafe_allow_html=True,
            )


init_state()
render_css()

cart_count = sum(st.session_state["cart"].values())
wish_count = len(st.session_state["wishlist"])

st.markdown(
    f"""
<div class="topbar">
  <div class="brand">
    <div class="mark">RR</div>
    <div>
      <h1>RangRajasthan Market</h1>
      <span>Professional social commerce for Rajasthani artists</span>
    </div>
  </div>
  <div class="navhint">Cart: {cart_count} · Wishlist: {wish_count} · Verified artisans · AI seller studio</div>
</div>
""",
    unsafe_allow_html=True,
)

tabs = st.tabs(["Explore", "Product Detail", "Artist Feed", "AI Seller Studio", "Seller Dashboard", "Cart & Checkout"])

with tabs[0]:
    st.markdown(
        """
<section class="hero">
  <div>
    <h2>Rajasthan's artists, ready for digital buyers.</h2>
    <p>A full social-commerce marketplace where buyers discover craft through posts, shop verified products, save favorites, and checkout directly while artists use AI to improve captions, SEO, photos, and engagement.</p>
  </div>
</section>
<div class="trustbar">
  <div><b>Verified</b><span>artist profiles and craft stories</span></div>
  <div><b>Secure</b><span>demo checkout flow with order summary</span></div>
  <div><b>Social</b><span>post feed connected to products</span></div>
  <div><b>AI</b><span>seller growth and listing studio</span></div>
</div>
""",
        unsafe_allow_html=True,
    )

    section("Marketplace", "Search, filter, save, and buy Rajasthani craft products.")
    search = st.text_input("Search products, artists, cities, or craft tags", placeholder="Try Jaipur, textile, gifting, painting")
    f1, f2, f3, f4 = st.columns([1, 1, 1, 1])
    with f1:
        category = st.selectbox("Category", ["All"] + sorted({p["category"] for p in PRODUCTS}))
    with f2:
        city = st.selectbox("City", ["All Rajasthan"] + sorted({p["city"] for p in PRODUCTS}))
    with f3:
        price_band = st.selectbox("Price", ["Any price", "Under INR 1,500", "INR 1,500-3,000", "Above INR 3,000"])
    with f4:
        sort = st.selectbox("Sort", ["Top projects first", "Most liked", "Highest rated", "Price low to high"])

    filtered = PRODUCTS
    query = search.strip().lower()
    if query:
        filtered = [
            p for p in filtered
            if query in " ".join([p["name"], p["artist"], p["city"], p["category"], *p["tags"]]).lower()
        ]
    if category != "All":
        filtered = [p for p in filtered if p["category"] == category]
    if city != "All Rajasthan":
        filtered = [p for p in filtered if p["city"] == city]
    if price_band == "Under INR 1,500":
        filtered = [p for p in filtered if p["price"] < 1500]
    elif price_band == "INR 1,500-3,000":
        filtered = [p for p in filtered if 1500 <= p["price"] <= 3000]
    elif price_band == "Above INR 3,000":
        filtered = [p for p in filtered if p["price"] > 3000]

    if sort == "Most liked":
        filtered = sorted(filtered, key=lambda p: p["likes"], reverse=True)
    elif sort == "Highest rated":
        filtered = sorted(filtered, key=lambda p: p["rating"], reverse=True)
    elif sort == "Price low to high":
        filtered = sorted(filtered, key=lambda p: p["price"])
    else:
        filtered = sorted(filtered, key=lambda p: (not p["top"], -product_score(p)))

    cols = st.columns(3)
    for index, product in enumerate(filtered):
        with cols[index % 3]:
            product_card(product, index)

with tabs[1]:
    section("Product Detail", "Amazon-style detail page with buying controls, trust signals, reviews, and AI sales suggestions.")
    selected_id = st.selectbox("Choose product", [p["id"] for p in PRODUCTS], format_func=lambda pid: product_lookup()[pid]["name"], index=[p["id"] for p in PRODUCTS].index(st.session_state["selected_product"]))
    st.session_state["selected_product"] = selected_id
    render_product_detail(product_lookup()[selected_id])

with tabs[2]:
    section("Artist Feed", "Instagram-style discovery where every post is shoppable.")
    left, right = st.columns([1.35, .8], gap="large")
    with left:
        for index, product in enumerate(PRODUCTS):
            st.markdown(
                f"""
<div class="post-card">
  <div class="post-head">
    <div class="avatar">{escape(product["artist"][0])}</div>
    <div><b>{escape(product["artist"])}</b><span class="muted">{escape(product["city"])}, Rajasthan · {escape(product["category"])}</span></div>
  </div>
  <p>{escape(product["caption"])}</p>
  <div class="post-img" style="background-image:url('{product["image"]}')"></div>
  <div class="row-between"><span class="muted">{product["likes"]:,} likes · {product["orders"]} orders · {product["reviews"]} reviews</span><b class="price">{rupees(product["price"])}</b></div>
</div>
""",
                unsafe_allow_html=True,
            )
            c1, c2, c3 = st.columns(3)
            with c1:
                if st.button("Shop post", key=f"shop_post_{product['id']}_{index}", use_container_width=True):
                    add_to_cart(product["id"])
            with c2:
                if st.button("Open detail", key=f"detail_post_{product['id']}_{index}", use_container_width=True):
                    st.session_state["selected_product"] = product["id"]
                    st.toast("Open the Product Detail tab")
            with c3:
                if st.button("AI boost", key=f"boost_{product['id']}_{index}", use_container_width=True):
                    st.session_state["selected_product"] = product["id"]
                    st.rerun()
    with right:
        selected = product_lookup()[st.session_state["selected_product"]]
        idea = ai_suggestions(selected)
        st.markdown(
            f"""
<div class="ai-box">
  <h3>AI Boost Panel</h3>
  <p><b>{escape(selected["name"])}</b></p>
  <p><b>Highlight score:</b> {idea["score"]}/100</p>
  <p><b>Caption:</b> {escape(idea["caption"])}</p>
  <p><b>Reel:</b> {escape(idea["reel"])}</p>
</div>
""",
            unsafe_allow_html=True,
        )
        for tip in idea["engagement"]:
            st.info(tip)

with tabs[3]:
    section("AI Seller Studio", "Artists generate listing copy, captions, SEO tags, photo direction, and a weekly posting plan.")
    form_col, output_col = st.columns([.9, 1.45], gap="large")
    with form_col:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        craft_name = st.text_input("Product name", value="Molela terracotta wall plaque")
        artist_story = st.text_area(
            "Artist story",
            value="A Molela family artist shapes devotional terracotta plaques by hand, using clay traditions passed down across generations near Nathdwara.",
            height=120,
        )
        materials = st.text_area("Materials and process", value="local terracotta clay, hand moulding, sun drying, kiln firing, natural earthy finish", height=85)
        location = st.text_input("Rajasthan location", value="Molela, Rajsamand")
        price_range = st.text_input("Price range", value="INR 1,200 to INR 3,800")
        target = st.selectbox("Main selling channel", ["Marketplace Listing", "Instagram", "Facebook", "WhatsApp", "Website SEO"])
        goal = st.selectbox("Growth goal", ["More orders", "More profile visits", "Festival gifting", "Boutique wholesale"])
        if st.button("Generate AI selling kit", type="primary", use_container_width=True):
            with st.spinner("AI is building the seller kit..."):
                start = time.time()
                st.session_state["studio_kit"] = generate_marketplace_kit(
                    craft_name=sanitize_text(craft_name, 120),
                    artisan_story=sanitize_text(f"{artist_story} Growth goal: {goal}", 760),
                    materials=sanitize_text(materials, 400),
                    location=sanitize_text(location, 120),
                    price_range=sanitize_text(price_range, 80),
                    platform=target,
                    tone="Heritage",
                    buyer="Conscious Shoppers",
                    language="English",
                )
                st.session_state["studio_elapsed"] = round(time.time() - start, 1)
        st.markdown("</div>", unsafe_allow_html=True)

    with output_col:
        kit = st.session_state.get("studio_kit")
        if not kit:
            st.markdown('<div class="ai-box"><h3>AI output appears here</h3><p>Generate a seller kit to create marketplace-ready content and growth recommendations.</p></div>', unsafe_allow_html=True)
        else:
            if kit.get("_error"):
                st.info(kit["_error"])
            st.markdown(f'<div class="ai-box"><h3>{escape(kit.get("listing_title", "Listing"))}</h3><p>{escape(kit.get("brand_story", ""))}</p></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="ai-box"><h3>Product Description</h3><p>{escape(kit.get("listing_description", ""))}</p></div>', unsafe_allow_html=True)
            post_cols = st.columns(3)
            for col, post in zip(post_cols, kit.get("social_posts", [])[:3]):
                with col:
                    st.markdown(f'<div class="ai-box"><h3>{escape(post.get("channel", ""))}</h3><p>{escape(post.get("copy", ""))}<br><b>{escape(post.get("cta", ""))}</b></p></div>', unsafe_allow_html=True)
            tags = "".join(f"<span>{escape(tag)}</span>" for tag in kit.get("seo_tags", []))
            st.markdown(f'<div class="ai-box"><h3>SEO Tags</h3><div class="tag-row">{tags}</div></div>', unsafe_allow_html=True)
            action_cols = st.columns(3)
            for col, title, items in zip(
                action_cols,
                ["Photo Direction", "Outreach", "Next Actions"],
                [kit.get("photo_shot_list", []), kit.get("outreach_ideas", []), kit.get("next_steps", [])],
            ):
                with col:
                    st.markdown(f'<div class="panel"><h3>{title}</h3>', unsafe_allow_html=True)
                    for item in items:
                        st.markdown(f"- {item}")
                    st.markdown("</div>", unsafe_allow_html=True)

with tabs[4]:
    section("Seller Dashboard", "Operational view for artists: sales, reach, product health, and listing readiness.")
    d1, d2, d3, d4 = st.columns(4)
    total_revenue = sum(p["price"] * p["orders"] for p in PRODUCTS)
    total_likes = sum(p["likes"] for p in PRODUCTS)
    avg_rating = sum(p["rating"] for p in PRODUCTS) / len(PRODUCTS)
    with d1:
        st.metric("Gross craft GMV", rupees(total_revenue))
    with d2:
        st.metric("Community likes", f"{total_likes:,}")
    with d3:
        st.metric("Avg rating", f"{avg_rating:.1f}/5")
    with d4:
        st.metric("Low stock items", sum(1 for p in PRODUCTS if p["stock"] <= 6))

    left, right = st.columns([1.2, .8], gap="large")
    with left:
        st.markdown('<div class="panel"><h3>Product Performance</h3>', unsafe_allow_html=True)
        for product in sorted(PRODUCTS, key=product_score, reverse=True):
            st.write(f"**{product['name']}** - {product['orders']} orders, {product['likes']:,} likes, {product['stock']} in stock")
            st.progress(product_score(product) / 100)
        st.markdown("</div>", unsafe_allow_html=True)
    with right:
        st.markdown('<div class="panel"><h3>Add New Artist Project</h3>', unsafe_allow_html=True)
        seller_name = st.text_input("Artist name", key="seller_name")
        project_name = st.text_input("Project/product name", key="project_name")
        project_city = st.text_input("City/village", key="project_city")
        project_price = st.number_input("Price", min_value=100, max_value=50000, value=1500, step=100)
        project_story = st.text_area("Short craft story", key="project_story", height=90)
        if st.button("Save draft project", use_container_width=True):
            if seller_name and project_name and project_city and project_story:
                st.session_state["seller_products"].append(
                    {"artist": seller_name, "name": project_name, "city": project_city, "price": project_price, "story": project_story}
                )
                st.success("Draft saved. Next step: add photos and publish after verification.")
            else:
                st.error("Fill artist name, product name, city, and story.")
        st.markdown("</div>", unsafe_allow_html=True)

        if st.session_state["seller_products"]:
            st.markdown('<div class="panel"><h3>Draft Projects</h3>', unsafe_allow_html=True)
            for draft in st.session_state["seller_products"]:
                st.write(f"**{draft['name']}** by {draft['artist']} - {draft['city']} - {rupees(int(draft['price']))}")
            st.markdown("</div>", unsafe_allow_html=True)

with tabs[5]:
    section("Cart & Checkout", "Full demo checkout with quantities, delivery details, payment mode, and order history.")
    render_cart()
