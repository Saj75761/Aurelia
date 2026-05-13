from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, EmailStr
from typing import List, Optional
import asyncio
import time
import random
import os

app = FastAPI(title="AURELIA API", version="1.0.0", description="The AURELIA Luxury Menswear API")

# ─── CORS ────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── STATIC FILES are mounted at the bottom after all API routes ─────────────

# ─── PYDANTIC MODELS ─────────────────────────────────────────────────────────

class CartItem(BaseModel):
    id: int
    name: str
    price: float
    quantity: int
    size: Optional[str] = None

class PaymentRequest(BaseModel):
    cart: List[CartItem]
    customer_name: str
    email: str
    total: float
    shipping_address: Optional[str] = None

class ChatMessage(BaseModel):
    message: str
    session_id: Optional[str] = None

class ContactForm(BaseModel):
    name: str
    email: str
    subject: str
    message: str
    phone: Optional[str] = None

# ─── PRODUCT DATA ─────────────────────────────────────────────────────────────

PRODUCTS = [
    {
        "id": 1,
        "name": "Obsidian Wool Suit",
        "price": 2850.00,
        "category": "Suits",
        "description": "Hand-tailored in Neapolitan tradition using super 180s Italian wool.",
        "image_url": "https://images.unsplash.com/photo-1594938298603-c8148c4dae35?w=800&q=80",
        "sizes": ["36", "38", "40", "42", "44", "46"],
        "badge": "Bestseller"
    },
    {
        "id": 2,
        "name": "Sea Island Dress Shirt",
        "price": 485.00,
        "category": "Shirts",
        "description": "Crafted from 140-thread-count Sea Island cotton with mother-of-pearl buttons.",
        "image_url": "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=800&q=80",
        "sizes": ["S", "M", "L", "XL", "XXL"],
        "badge": "New"
    },
    {
        "id": 3,
        "name": "Double-Faced Cashmere Overcoat",
        "price": 3200.00,
        "category": "Outerwear",
        "description": "Mongolian cashmere, double-faced construction, proprietary thermal interlining.",
        "image_url": "https://images.unsplash.com/photo-1548624313-0396c75e4b1a?w=800&q=80",
        "sizes": ["S", "M", "L", "XL"],
        "badge": "Limited"
    },
    {
        "id": 4,
        "name": "Goodyear Welt Oxford",
        "price": 920.00,
        "category": "Footwear",
        "description": "Handcrafted over 200 steps in our Florence atelier. Full-grain calf leather.",
        "image_url": "https://images.unsplash.com/photo-1614252235316-8c857d38b5f4?w=800&q=80",
        "sizes": ["7", "8", "9", "10", "11", "12"],
        "badge": ""
    },
    {
        "id": 5,
        "name": "Bespoke Linen Blazer",
        "price": 1680.00,
        "category": "Blazers",
        "description": "Italian linen, unstructured silhouette. The cornerstone of the modern gentleman's wardrobe.",
        "image_url": "https://images.unsplash.com/photo-1507679799987-c73779587ccf?w=800&q=80",
        "sizes": ["36", "38", "40", "42", "44"],
        "badge": ""
    },
    {
        "id": 6,
        "name": "Merino Turtleneck",
        "price": 395.00,
        "category": "Knitwear",
        "description": "Extra-fine 17.5 micron merino wool. Seamless construction for a second-skin fit.",
        "image_url": "https://images.unsplash.com/photo-1618354691373-d851c5c3a990?w=800&q=80",
        "sizes": ["S", "M", "L", "XL", "XXL"],
        "badge": "New"
    },
    {
        "id": 7,
        "name": "Silk Evening Scarf",
        "price": 245.00,
        "category": "Accessories",
        "description": "Hand-rolled edges, heavyweight mulberry silk with traditional paisley motif.",
        "image_url": "https://images.unsplash.com/photo-1520903920243-00d872a2d1c9?w=800&q=80",
        "sizes": ["OS"],
        "badge": ""
    },
    {
        "id": 8,
        "name": "Velvet Smoking Jacket",
        "price": 1850.00,
        "category": "Outerwear",
        "description": "Italian cotton velvet with quilted silk lapels and frog-fastening detail.",
        "image_url": "https://images.unsplash.com/photo-1593032465175-481ac7f401a0?w=800&q=80",
        "sizes": ["38", "40", "42", "44"],
        "badge": "Exclusive"
    },
    {
        "id": 9,
        "name": "Calfskin Dress Belt",
        "price": 320.00,
        "category": "Accessories",
        "description": "Hand-stitched in Florence. Solid brass buckle with palladium finish.",
        "image_url": "https://images.unsplash.com/photo-1624222247344-550fb86d742a?w=800&q=80",
        "sizes": ["32", "34", "36", "38"],
        "badge": ""
    },
    {
        "id": 10,
        "name": "Engraved Silver Cufflinks",
        "price": 450.00,
        "category": "Accessories",
        "description": "Solid sterling silver, hand-engraved with the AURELIA crest.",
        "image_url": "https://images.unsplash.com/photo-1610418342414-984483759367?w=800&q=80",
        "sizes": ["OS"],
        "badge": "Heirloom"
    },
    {
        "id": 11,
        "name": "Poplin Evening Shirt",
        "price": 525.00,
        "category": "Shirts",
        "description": "Giza 45 cotton poplin. Marcella bib front and double cuffs.",
        "image_url": "https://images.unsplash.com/photo-1598411037848-9cda9ec7c39f?w=800&q=80",
        "sizes": ["15", "15.5", "16", "16.5", "17"],
        "badge": ""
    },
    {
        "id": 12,
        "name": "Vicuna Overcoat",
        "price": 14500.00,
        "category": "Outerwear",
        "description": "The 'Fiber of the Gods'. Unmatched softness and warmth in a classic double-breasted cut.",
        "image_url": "https://images.unsplash.com/photo-1544923246-77307dd654ca?w=800&q=80",
        "sizes": ["40", "42", "44"],
        "badge": "Ultimate"
    }
]

# ─── AI CONCIERGE ─────────────────────────────────────────────────────────────

def ai_concierge(message: str) -> str:
    msg = message.lower().strip()

    # Greetings
    if any(w in msg for w in ["hello", "hi", "hey", "good morning", "good evening", "good afternoon", "greetings", "bonjour"]):
        return "Good evening. Welcome to AURELIA. I am your personal concierge, here to guide you through our world of exceptional craftsmanship. Whether you seek the perfect suit for a grand occasion or wish to explore our latest collection, I am entirely at your service."

    # Materials & Fabrics
    if any(w in msg for w in ["material", "fabric", "made of", "quality", "textile", "wool", "silk", "cashmere", "linen", "cotton"]):
        return "Our atelier sources exclusively from the world's most distinguished mills. Every AURELIA garment is crafted from hand-selected Italian silk, hand-sourced Mongolian cashmere, and super 180s wool from the historic Loro Piana mills. These are materials that drape with unparalleled elegance and grow more distinguished with every wear — a true heirloom."

    # Suits & Tailoring
    if any(w in msg for w in ["suit", "tailoring", "bespoke", "custom", "made to measure", "tailor"]):
        return "Each AURELIA suit is a testament to the Neapolitan tradition — an art form mastered over centuries. Our master tailors require three intimate fittings to sculpt a silhouette that is exclusively yours. We offer both made-to-measure and fully bespoke commissions, with construction commencing only after we have achieved an absolute understanding of your aesthetic vision."

    # Price & Investment
    if any(w in msg for w in ["price", "cost", "afford", "expensive", "value", "investment", "worth", "budget"]):
        return "At AURELIA, we regard each acquisition not as a purchase, but as an investment in one's legacy. Our pricing reflects the extraordinary rarity of our materials, the decades of mastery our artisans bring to every stitch, and the uncompromising standards of our atelier. We also offer a discreet, interest-free arrangement for our distinguished clientele — please speak with our concierge team to learn more."

    # Shipping & Delivery
    if any(w in msg for w in ["shipping", "delivery", "ship", "arrive", "dispatch", "send", "courier"]):
        return "Your AURELIA order is a ceremony in itself. Each piece is presented in our signature black lacquer box, wrapped in archival tissue, and hand-delivered by our white-glove courier service within 3–5 business days domestically. International orders arrive within 7–10 days, accompanied by real-time tracking, full insurance, and a personal note from your concierge."

    # Returns & Exchanges
    if any(w in msg for w in ["return", "exchange", "refund", "policy", "send back"]):
        return "We stand behind every thread. AURELIA offers a generous 30-day return and exchange policy for all unworn pieces in their original presentation. For bespoke commissions, our atelier will work in close collaboration with you across as many fittings as necessary until the result is nothing short of perfect. Your satisfaction is our singular obligation."

    # Shirts
    if any(w in msg for w in ["shirt", "dress shirt", "oxford shirt", "poplin", "button"]):
        return "Our dress shirts represent the apotheosis of refined dressing. Cut from 140-thread-count Italian poplin and Sea Island cotton — the rarest cotton in the world — each collar is meticulously hand-rolled and the buttons are fashioned from genuine mother-of-pearl harvested from the rivers of Polynesia. They are, simply put, the finest shirts in existence."

    # Outerwear
    if any(w in msg for w in ["coat", "overcoat", "jacket", "blazer", "outerwear", "trench"]):
        return "Our outerwear collection is designed for the gentleman who commands a room upon entry. The cashmere overcoats are double-faced, employing a proprietary interlining technology that achieves extraordinary warmth without sacrificing the drape. Each piece is a technical achievement as impressive as its aesthetic — architecture for the body."

    # Footwear
    if any(w in msg for w in ["shoe", "shoes", "oxford", "loafer", "footwear", "boot", "slipper"]):
        return "AURELIA footwear is handcrafted in our Florence atelier using the Goodyear welt construction — a method that allows for resoling and a lifetime of wear. Each pair requires over 200 individual handcrafted steps and is fashioned from full-grain calf leather that develops a rich, distinctive patina unique to its owner over decades of distinguished use."

    # Sizing
    if any(w in msg for w in ["size", "sizing", "measurement", "fit", "measure", "guide"]):
        return "We offer a complimentary virtual fitting consultation with our senior stylists, conducted via video at your convenience. For ready-to-wear pieces, our comprehensive size guide accounts for European, British, and Italian sizing conventions. We strongly recommend scheduling a consultation to ensure the result is entirely impeccable — precision is, after all, the cornerstone of our craft."

    # Knitwear
    if any(w in msg for w in ["knit", "knitwear", "sweater", "jumper", "turtleneck", "pullover"]):
        return "Our knitwear is constructed from extra-fine 17.5 micron merino wool — a fibre so delicate it sits imperceptibly against the skin. Each piece employs seamless construction techniques developed in collaboration with Italian knitwear artisans, resulting in a garment that is simultaneously technical and sublimely elegant."

    # Appointments
    if any(w in msg for w in ["appointment", "visit", "consultation", "meet", "book", "schedule"]):
        return "We would be honoured to welcome you. Private consultations are available at our flagship atelier by appointment. Our stylists will prepare a curated selection in advance, ensuring your time with us is as productive as it is pleasurable. Please use our Contact page to arrange your appointment, and we shall respond within the hour."

    # Care
    if any(w in msg for w in ["care", "clean", "wash", "maintain", "store", "preserve"]):
        return "Each AURELIA garment is accompanied by a detailed care compendium authored by our textile specialists. In brief: all fine woollens and cashmeres should be dry-cleaned annually and stored in our complimentary cedar-lined garment bags. Our atelier also offers a lifetime maintenance service — we believe the relationship between a gentleman and his tailor is one without an end date."

    # Thanks
    if any(w in msg for w in ["thank", "thanks", "thank you", "appreciate", "wonderful", "excellent", "perfect", "amazing"]):
        return "It is my absolute pleasure. At AURELIA, impeccable service is not a courtesy — it is our unwavering standard. Please do not hesitate to return should any further questions arise. We are, as always, entirely at your service."

    # Default — sophisticated fallback
    return "A most discerning inquiry. At AURELIA, we believe true luxury is not merely purchased — it is experienced, curated, and ultimately, inherited. I would be delighted to guide you with more precision. Might you share the occasion you are dressing for, or the particular garment you have in mind? The details, as always, are everything."


# ─── ROUTES ──────────────────────────────────────────────────────────────────



@app.get("/products")
async def get_products(category: Optional[str] = None):
    if category:
        filtered = [p for p in PRODUCTS if p["category"].lower() == category.lower()]
        return {"products": filtered, "total": len(filtered)}
    return {"products": PRODUCTS, "total": len(PRODUCTS)}


@app.post("/process-payment")
async def process_payment(payment: PaymentRequest):
    await asyncio.sleep(2)  # Simulated processing delay
    order_id = f"AUR-{random.randint(10000, 99999)}"
    return {
        "status": "success",
        "message": "Payment Successful. Welcome to the AURELIA family.",
        "order_id": order_id,
        "customer": payment.customer_name,
        "email": payment.email,
        "total": payment.total,
        "estimated_delivery": "3–5 business days",
        "items_ordered": len(payment.cart)
    }


@app.post("/chat")
async def chat(chat_message: ChatMessage):
    response = ai_concierge(chat_message.message)
    return {
        "response": response,
        "session_id": chat_message.session_id or f"session_{int(time.time())}"
    }


@app.post("/contact-submit")
async def contact_submit(form: ContactForm):
    return {
        "status": "success",
        "message": f"Thank you, {form.name}. Your inquiry has been received with the attention it deserves. A member of our concierge team will respond within 24 hours.",
        "reference": f"INQ-{random.randint(1000, 9999)}"
    }

# ─── PAGE ROUTES ─────────────────────────────────────────────────────────────

@app.get("/")
async def serve_index():
    return FileResponse("index.html")

@app.get("/about")
async def serve_about():
    return FileResponse("about.html")

@app.get("/contact")
async def serve_contact():
    return FileResponse("contact.html")

@app.get("/checkout")
async def serve_checkout():
    return FileResponse("checkout.html")

@app.get("/collections")
async def serve_collections():
    return FileResponse("collections.html")

# ─── STATIC FILES ─────────────────────────────────────────────────────────────
# Mount AFTER all API routes so API endpoints take priority.
# Serves style.css, script.js, hero.png etc. at their root paths.
app.mount("/", StaticFiles(directory=".", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
