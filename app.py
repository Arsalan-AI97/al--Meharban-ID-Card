import streamlit as st
import io
import os
import random
from PIL import Image, ImageDraw, ImageFont
import requests

st.set_page_config(
    page_title="Al-Meharban Foundation - Dual Card Generator",
    page_icon="🪪",
    layout="wide"
)

# ── STREAMLIT CUSTOM DESIGN STYLING ──
st.markdown("""
    <style>
    .main-title {
        color: #005A2D;
        font-weight: 800;
        font-size: 2.4rem;
        margin-bottom: 10;
    }
    .sub-title { color: #666; font-size: 1rem; margin-bottom: 24px; }
    .card-label { font-weight: 700; font-size: 1.1rem; color: #005A2D; margin-bottom: 6px; }
    div.stButton > button {
        background-color: #005A2D !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 10px 24px !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        width: 100% !important;
    }
    div.stButton > button:hover { background-color: #004020 !important; }
    </style>
""", unsafe_allow_html=True)

FONT_DIR = "fonts"
os.makedirs(FONT_DIR, exist_ok=True)

# ── LOGO FILE PATH AUTO-DETECTION ──
def _find_logo_path():
    candidates = []
    try:
        candidates.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "amf_logo_nobg.jpg"))
    except Exception:
        pass
    candidates.append(os.path.join(os.getcwd(), "amf_logo_nobg.jpg"))
    candidates.append(os.path.join(os.getcwd(), "amf_logo.jpeg"))
    candidates.append("/home/claude/amf_logo_nobg.jpg")
    for p in candidates:
        if os.path.exists(p):
            return p
    return None

DEFAULT_LOGO_PATH = _find_logo_path()

@st.cache_resource
def _preload_logo():
    path = _find_logo_path()
    if path:
        try:
            return Image.open(path).convert("RGBA")
        except Exception:
            pass
    return None

FONTS = {
    "roboto_regular": {
        "url": "https://github.com/google/fonts/raw/main/apache/roboto/static/Roboto-Regular.ttf",
        "fallback": ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "C:\\Windows\\Fonts\\arial.ttf"]
    },
    "roboto_bold": {
        "url": "https://github.com/google/fonts/raw/main/apache/roboto/static/Roboto-Bold.ttf",
        "fallback": ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "C:\\Windows\\Fonts\\arialbd.ttf"]
    },
    "roboto_medium": {
        "url": "https://github.com/google/fonts/raw/main/apache/roboto/static/Roboto-Medium.ttf",
        "fallback": ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "C:\\Windows\\Fonts\\arial.ttf"]
    }
}

@st.cache_resource
def load_font(font_key, size):
    font_info = FONTS[font_key]
    local_path = os.path.join(FONT_DIR, f"{font_key}.ttf")
    if not os.path.exists(local_path):
        try:
            r = requests.get(font_info["url"], timeout=5)
            if r.status_code == 200:
                with open(local_path, "wb") as f:
                    f.write(r.content)
        except Exception:
            pass
    if os.path.exists(local_path):
        try:
            return ImageFont.truetype(local_path, size)
        except Exception:
            pass
    for fp in font_info["fallback"]:
        if os.path.exists(fp):
            try:
                return ImageFont.truetype(fp, size)
            except Exception:
                pass
    return ImageFont.load_default()

def get_autoscaled_font(draw, text, font_key, max_width, initial_size):
    size = initial_size
    while size > 10:
        font = load_font(font_key, size)
        bbox = draw.textbbox((0, 0), text, font=font)
        if (bbox[2] - bbox[0]) <= max_width:
            return font
        size -= 2
    return load_font(font_key, 10)

def draw_centered_text(draw, text, y, font, fill_color, canvas_width=660):
    bbox = draw.textbbox((0, 0), text, font=font)
    x = (canvas_width - (bbox[2] - bbox[0])) / 2
    draw.text((x, y), text, fill=fill_color, font=font)

def paste_logo(card, logo_img, x, y, target_size):
    try:
        lw, lh = logo_img.size
        scale = target_size / max(lw, lh)
        nw, nh = int(lw * scale), int(lh * scale)
        resized = logo_img.resize((nw, nh), Image.Resampling.LANCZOS)
        ox = x + (target_size - nw) // 2
        oy = y + (target_size - nh) // 2
        if resized.mode == 'RGBA':
            card.paste(resized, (ox, oy), resized)
        else:
            resized_rgba = resized.convert("RGBA")
            card.paste(resized_rgba, (ox, oy), resized_rgba)
    except Exception:
        pass

def load_default_logo():
    cached = _preload_logo()
    if cached is not None:
        return cached
    path = _find_logo_path()
    if path and os.path.exists(path):
        try:
            return Image.open(path).convert("RGBA")
        except Exception:
            pass
    return None


# ═══════════════════════════════════════════════════
#  CARD 1 — VOLUNTEER ID CARD  (660 × 1020 px)
# ═══════════════════════════════════════════════════
def generate_id_card(name, volunteer_id, role, blood_group, validity_date,
                     profile_image, signature_image=None, logo_image=None):
    card = Image.new("RGBA", (660, 1020), "white")
    draw = ImageDraw.Draw(card)

    # Outer border
    draw.rectangle([10, 10, 650, 1010], outline="#005A2D", width=8)

    # Header banner
    draw.rectangle([14, 14, 646, 185], fill="#005A2D")
    draw.rectangle([14, 185, 646, 191], fill="#D4AF37")

    # ── Problem 1 Fix: Logo Perfectly Centered ──
    logo = logo_image or load_default_logo()
    if logo:
        logo_bg_size = 80
        logo_bg_x = (660 - logo_bg_size) // 2
        logo_bg_y = 18
        paste_logo(card, logo, logo_bg_x, logo_bg_y, logo_bg_size)
    else:
        draw.ellipse([305, 25, 355, 75], fill="#005A2D", outline="#D4AF37", width=2)

    # Header texts shifted down beneath centered logo
    header_font = load_font("roboto_bold", 22)
    draw_centered_text(draw, "AL-MEHARBAN FOUNDATION", 104, header_font, "white", 660)
    sub_font = load_font("roboto_regular", 13)
    draw_centered_text(draw, "Every Life Matters, Every Smile Counts", 136, sub_font, "#D4F0C8", 660)
    tagline_font = load_font("roboto_regular", 11)
    draw_centered_text(draw, "Together We Care, Together We Change", 158, tagline_font, "#aaddaa", 660)

    # ── Profile Photo Frame & Paste ──
    px1, py1, px2, py2 = 220, 215, 440, 475
    draw.rectangle([px1 - 3, py1 - 3, px2 + 3, py2 + 3], outline="#CCCCCC", width=3)
    if profile_image is not None:
        try:
            pw, ph = profile_image.size
            tw, th = 220, 260
            if pw / ph > tw / th:
                nw = int(ph * tw / th)
                cropped = profile_image.crop(((pw - nw) // 2, 0, (pw - nw) // 2 + nw, ph))
            else:
                nh = int(pw * th / tw)
                cropped = profile_image.crop((0, (ph - nh) // 2, pw, (ph - nh) // 2 + nh))
            resized = cropped.resize((tw, th), Image.Resampling.LANCZOS)
            card.paste(resized, (px1, py1))
        except Exception:
            _placeholder_photo(draw, px1, py1, px2, py2)
    else:
        _placeholder_photo(draw, px1, py1, px2, py2)

    # ── Professional Name & Role Formatting ──
    name_font = get_autoscaled_font(draw, name.strip(), "roboto_bold", 520, 30)
    draw_centered_text(draw, name.strip(), 510, name_font, "#005A2D", 660)
    role_font = get_autoscaled_font(draw, role.strip(), "roboto_medium", 520, 20)
    draw_centered_text(draw, role.strip(), 555, role_font, "#B46400", 660)

    # ── Information Data Grid ──
    draw.rectangle([80, 610, 580, 790], fill="#F7FBF8", outline="#E2ECE5", width=2)
    lf = load_font("roboto_bold", 16)
    vf = load_font("roboto_medium", 16)
    rows = [(625, "VOLUNTEER ID :", volunteer_id.strip().upper(), "#111111"),
            (675, "BLOOD GROUP  :", blood_group.strip().upper(),
             "#B30000" if any(x in blood_group.upper() for x in ["A","B","O"]) else "#111111"),
            (725, "VALID UNTIL  :", validity_date.strip(), "#111111")]
    for ry, label, val, vc in rows:
        draw.text((115, ry), label, fill="#555555", font=lf)
        draw.text((300, ry), val,   fill=vc,        font=vf)

    # ── Barcode Logic ──
    random.seed(volunteer_id)
    bx = 90
    while bx < 270:
        bw = random.choice([2, 3, 4])
        draw.rectangle([bx, 830, bx + bw - 1, 875], fill="black")
        bx += bw + random.choice([2, 3])
    draw.text((120, 882), f"*{volunteer_id.strip().upper()}*", fill="#555555", font=load_font("roboto_regular", 11))

    # ── Problem 2 Fix: Actual Signature Loader ──
    draw.line([390, 865, 570, 865], fill="#888888", width=2)
    sig = signature_image
    if sig is None and os.path.exists("signature_no_bg.png"):
        try:
            sig = Image.open("signature_no_bg.png")
        except Exception:
            pass
    if sig:
        try:
            sw, sh = sig.size
            mw, mh = 160, 50
            aspect = sw / sh
            nw = min(mw, int(mh * aspect))
            nh = int(nw / aspect)
            rs = sig.resize((nw, nh), Image.Resampling.LANCZOS)
            sx = 390 + (180 - nw) // 2
            sy = 865 - nh - 2
            if rs.mode == 'RGBA':
                card.paste(rs, (sx, sy), rs)
            else:
                card.paste(rs, (sx, sy))
        except Exception:
            _fallback_sig(draw)
    else:
        _fallback_sig(draw)
        
    draw.text((410, 873), "AUTHORIZED SIGNATURE", fill="#777777", font=load_font("roboto_bold", 10))

    # ── Bottom ID Footer ──
    draw.rectangle([14, 940, 646, 946], fill="#D4AF37")
    draw.rectangle([14, 946, 646, 1006], fill="#005A2D")
    draw_centered_text(draw, "If found, please return to office or contact admin.",
                       965, load_font("roboto_regular", 12), "white", 660)

    return card

def _placeholder_photo(draw, x1, y1, x2, y2):
    draw.rectangle([x1, y1, x2, y2], fill="#F0F0F0")
    cx = (x1 + x2) // 2
    draw.ellipse([cx - 45, y1 + 30, cx + 45, y1 + 120], fill="#CCCCCC")
    draw.chord([cx - 80, y1 + 140, cx + 80, y2 - 10], start=180, end=360, fill="#CCCCCC")

def _fallback_sig(draw):
    draw.line([410, 858, 428, 845, 455, 860, 482, 842, 510, 856, 538, 846, 560, 858], fill="#1C3D82", width=2)


# ═══════════════════════════════════════════════════
#  CARD 2 — APPOINTMENT CARD (660 × 760 px - Optimized)
# ═══════════════════════════════════════════════════
def generate_appointment_card(name, role, location, profile_image, logo_image=None):
    W, H = 660, 760  # Height perfectly condensed for professional compact look
    card = Image.new("RGBA", (W, H), "white")
    draw = ImageDraw.Draw(card)

    # Dark green outer border
    draw.rectangle([10, 10, W - 11, H - 11], outline="#1a6b1a", width=8)
    # Gold accent frame line
    draw.rectangle([22, 22, W - 23, H - 23], outline="#D4AF37", width=2)

    # ══ HEADER SECTION ══
    logo = logo_image or load_default_logo()
    logo_size = 70
    logo_x, logo_y = 35, 35
    if logo:
        paste_logo(card, logo, logo_x, logo_y, logo_size)

    # Problem 3 Fix: Closed tight spacing directly under the logo
    small_lbl = load_font("roboto_bold", 11)
    draw.text((logo_x, logo_y + logo_size + 3), "Al-Meharban Foundation", fill="#1a6b1a", font=small_lbl)

    # Foundation structured typography
    fn_font = load_font("roboto_bold", 22)
    draw_centered_text(draw, "AL-MEHARBAN FOUNDATION", 38, fn_font, "#1a5c1a", W)

    tg_font = load_font("roboto_bold", 13)
    draw_centered_text(draw, "Every Life Matters, Every Smile Counts.", 70, tg_font, "#1a6b1a", W)
    
    tg2_font = load_font("roboto_regular", 11)
    draw_centered_text(draw, "Together We Care, Together We Change", 90, tg2_font, "#555555", W)

    # Gold Divider Line
    draw.rectangle([35, 130, W - 35, 133], fill="#D4AF37")

    # ══ PROFILE PHOTO (Proportional & Professional Size) ══
    pw, ph = 190, 215
    px = (W - pw) // 2
    py = 155
    draw.rectangle([px - 4, py - 4, px + pw + 4, py + ph + 4], outline="#1a6b1a", width=4)

    if profile_image is not None:
        try:
            iw, ih = profile_image.size
            ta = pw / ph
            if iw / ih > ta:
                nw = int(ih * ta)
                cropped = profile_image.crop(((iw - nw) // 2, 0, (iw - nw) // 2 + nw, ih))
            else:
                nh = int(iw / ta)
                cropped = profile_image.crop((0, (ih - nh) // 2, iw, (ih - nh) // 2 + nh))
            card.paste(cropped.resize((pw, ph), Image.Resampling.LANCZOS), (px, py))
        except Exception:
            _appt_placeholder_photo(draw, px, py, pw, ph)
    else:
        _appt_placeholder_photo(draw, px, py, pw, ph)

    # ══ TEXT CONTENT (Balanced Font Sizes & Clean Positions) ══
    cg_font = load_font("roboto_bold", 22)
    draw_centered_text(draw, "HEARTIEST CONGRATULATIONS", 400, cg_font, "#1a5c1a", W)

    ap_font = load_font("roboto_bold", 16)
    draw_centered_text(draw, "On Appointment as " + role.strip(), 440, ap_font, "#111111", W)

    org_font = load_font("roboto_bold", 19)
    draw_centered_text(draw, "AL-MEHARBAN FOUNDATION", 470, org_font, "#1a5c1a", W)

    if location.strip():
        loc_font = load_font("roboto_bold", 14)
        draw_centered_text(draw, "From " + location.strip(), 500, loc_font, "#111111", W)

    # Auto-scaled green Candidate Name
    display_name = name.strip()
    nm_font = get_autoscaled_font(draw, display_name, "roboto_bold", W - 80, 26)
    draw_centered_text(draw, display_name, 530, nm_font, "#1a5c1a", W)

    # Gold separator line before footer
    draw.rectangle([35, 655, W - 35, 658], fill="#D4AF37")

    # Bottom Tagline
    tg3_font = load_font("roboto_bold", 12)
    draw_centered_text(draw, "TOGETHER WE CARE, TOGETHER WE CHANGE", 670, tg3_font, "#111111", W)

    # ══ CONSOLIDATED FOOTER ══
    draw.rectangle([24, 695, W - 24, 748], fill="#c8eac8")
    ft_font = load_font("roboto_bold", 11)
    draw_centered_text(draw, "Join us in making society!  |  Follow us Al-Meharban Foundation", 703, ft_font, "#1a4a1a", W)
    sc_font = load_font("roboto_regular", 10)
    draw_centered_text(draw, "f  /AlMeharbanFd        ig/al_meharban_foundation        tt/AlMeharban", 723, sc_font, "#333333", W)

    return card

def _appt_placeholder_photo(draw, px, py, pw, ph):
    draw.rectangle([px, py, px + pw, py + ph], fill="#F0F0F0")
    cx = px + pw // 2
    draw.ellipse([cx - 45, py + 40, cx + 45, py + 130], fill="#CCCCCC")
    draw.chord([cx - 80, py + 150, cx + 80, py + ph - 10], start=180, end=360, fill="#CCCCCC")


# ═══════════════════════════════════════════════════
#  STREAMLIT GENERATOR UI FRONTEND
# ═══════════════════════════════════════════════════
st.markdown('<h1 class="main-title">Al-Meharban Foundation</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Volunteer ID Card + Appointment Card — Ek Form, Dono Cards | Logo Automatic</p>',
            unsafe_allow_html=True)

col_form, col_preview = st.columns([5, 7])

with col_form:
    st.subheader("Volunteer / Member Details")

    name = st.text_input("Full Name", value="Muhammad Umair Ahmed", max_chars=40)

    c1, c2 = st.columns(2)
    with c1:
        volunteer_id = st.text_input("Volunteer ID", value="AMF-2026-0042", max_chars=20)
    with c2:
        blood_group = st.selectbox("Blood Group",
            ["O+", "O-", "A+", "A-", "B+", "B-", "AB+", "AB-", "N/A"])

    c3, c4 = st.columns(2)
    with c3:
        role = st.text_input("Role / Designation", value="Community Leader", max_chars=40)
    with c4:
        validity_date = st.text_input("ID Valid Until", value="31-Dec-2027", max_chars=15)

    location = st.text_input("City / Area (Appointment Card)", value="Malir Karachi", max_chars=40)

    title_prefix = st.radio("Title for Appointment Card", ["Mr.", "Ms.", "Dr.", "None"], horizontal=True)

    st.markdown("---")
    st.subheader("Profile Photo")
    uploaded_file = st.file_uploader("Upload Photo (PNG, JPG)", type=["png", "jpg", "jpeg"])

    st.subheader("Foundation Logo (optional override)")
    st.info("✅ Al-Meharban Foundation ka official logo already set hai. Sirf override karna ho to upload karein.")
    uploaded_logo = st.file_uploader("Upload Custom Logo (PNG recommended)", type=["png", "jpg", "jpeg"])

    st.subheader("Signature (optional)")
    uploaded_sig = st.file_uploader("Upload Signature Image", type=["png", "jpg", "jpeg"])

# Image Processors
profile_image = None
if uploaded_file:
    try:
        profile_image = Image.open(uploaded_file)
    except Exception as e:
        st.error(f"Photo error: {e}")

logo_image = None
if uploaded_logo:
    try:
        logo_image = Image.open(uploaded_logo).convert("RGBA")
    except Exception as e:
        st.error(f"Logo error: {e}")

signature_image = None
if uploaded_sig:
    try:
        signature_image = Image.open(uploaded_sig)
    except Exception as e:
        st.error(f"Signature error: {e}")

def _appt_name(name, prefix):
    if prefix == "None":
        return name.strip()
    return f"{prefix} {name.strip()}"

# Generator Execution
id_card = generate_id_card(
    name=name, volunteer_id=volunteer_id, role=role,
    blood_group=blood_group, validity_date=validity_date,
    profile_image=profile_image, signature_image=signature_image,
    logo_image=logo_image
)

appt_card = generate_appointment_card(
    name=_appt_name(name, title_prefix),
    role=role, location=location,
    profile_image=profile_image,
    logo_image=logo_image
)

with col_preview:
    tab1, tab2 = st.tabs(["🪪  Volunteer ID Card", "🎖️  Appointment Card"])

    with tab1:
        st.markdown('<div class="card-label">Volunteer ID Card Preview</div>', unsafe_allow_html=True)
        st.image(id_card, caption="660 × 1020 px — Print Ready", use_container_width=True)

        png1 = io.BytesIO()
        id_card.save(png1, format="PNG", dpi=(300, 300))
        pdf1 = io.BytesIO()
        id_card.convert("RGB").save(pdf1, format="PDF", resolution=300.0)

        ca, cb = st.columns(2)
        with ca:
            st.download_button("⬇️ Download ID PNG",
                               png1.getvalue(),
                               f"AMF_ID_{name.replace(' ','_')}.png", "image/png")
        with cb:
            st.download_button("⬇️ Download ID PDF",
                               pdf1.getvalue(),
                               f"AMF_ID_{name.replace(' ','_')}.pdf", "application/pdf")

    with tab2:
        st.markdown('<div class="card-label">Appointment Card Preview</div>', unsafe_allow_html=True)
        st.image(appt_card, caption="660 × 760 px — Compact & Social Media Ready", use_container_width=True)

        png2 = io.BytesIO()
        appt_card.save(png2, format="PNG", dpi=(300, 300))
        pdf2 = io.BytesIO()
        appt_card.convert("RGB").save(pdf2, format="PDF", resolution=300.0)

        cc, cd = st.columns(2)
        with cc:
            st.download_button("⬇️ Download Appt. PNG",
                               png2.getvalue(),
                               f"AMF_Appt_{name.replace(' ','_')}.png", "image/png")
        with cd:
            st.download_button("⬇️ Download Appt. PDF",
                               pdf2.getvalue(),
                               f"AMF_Appt_{name.replace(' ','_')}.pdf", "application/pdf")

    st.markdown("---")
    st.caption("💡 Dono cards ek saath tayar hain — tabs switch karke alag alag download karein.")