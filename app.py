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

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700;800&display=swap');
    .main-title {
        color: #005A2D;
        font-family: 'Outfit', sans-serif;
        font-weight: 800;
        font-size: 2.4rem;
        margin-bottom: 0;
    }
    .sub-title {
        color: #666;
        font-size: 1rem;
        margin-bottom: 24px;
    }
    .card-label {
        font-weight: 700;
        font-size: 1.1rem;
        color: #005A2D;
        margin-bottom: 6px;
    }
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
    div.stButton > button:hover {
        background-color: #004020 !important;
    }
    </style>
""", unsafe_allow_html=True)

FONT_DIR = "fonts"
os.makedirs(FONT_DIR, exist_ok=True)

FONTS = {
    "roboto_regular": {
        "url": "https://github.com/google/fonts/raw/main/apache/roboto/static/Roboto-Regular.ttf",
        "fallback": ["C:\\Windows\\Fonts\\arial.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]
    },
    "roboto_bold": {
        "url": "https://github.com/google/fonts/raw/main/apache/roboto/static/Roboto-Bold.ttf",
        "fallback": ["C:\\Windows\\Fonts\\arialbd.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]
    },
    "roboto_medium": {
        "url": "https://github.com/google/fonts/raw/main/apache/roboto/static/Roboto-Medium.ttf",
        "fallback": ["C:\\Windows\\Fonts\\arial.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]
    }
}

@st.cache_resource
def load_font(font_key, size):
    font_info = FONTS[font_key]
    local_path = os.path.join(FONT_DIR, f"{font_key}.ttf")
    if not os.path.exists(local_path):
        try:
            response = requests.get(font_info["url"], timeout=5)
            if response.status_code == 200:
                with open(local_path, "wb") as f:
                    f.write(response.content)
        except Exception:
            pass
    if os.path.exists(local_path):
        try:
            return ImageFont.truetype(local_path, size)
        except Exception:
            pass
    for fallback_path in font_info["fallback"]:
        if os.path.exists(fallback_path):
            try:
                return ImageFont.truetype(fallback_path, size)
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

# ─────────────────────────────────────────────
#  CARD 1 — VOLUNTEER ID CARD
# ─────────────────────────────────────────────
def generate_id_card(name, volunteer_id, role, blood_group, validity_date, profile_image, signature_image=None):
    card = Image.new("RGBA", (660, 1020), "white")
    draw = ImageDraw.Draw(card)

    draw.rectangle([10, 10, 650, 1010], outline="#005A2D", width=8)
    draw.rectangle([14, 14, 646, 170], fill="#005A2D")
    draw.rectangle([14, 170, 646, 176], fill="#D4AF37")

    draw.ellipse([305, 25, 355, 75], fill="#005A2D", outline="#D4AF37", width=2)
    draw.ellipse([312, 32, 342, 62], fill="#D4AF37")
    draw.ellipse([317, 30, 345, 58], fill="#005A2D")
    draw.ellipse([336, 38, 340, 42], fill="#D4AF37")

    header_font = load_font("roboto_bold", 24)
    draw_centered_text(draw, "AL-MEHARBAN FOUNDATION", 92, header_font, "white")
    sub_font = load_font("roboto_regular", 14)
    draw_centered_text(draw, "Every Life Matters, Every Smile Counts", 128, sub_font, "#E0E0E0")

    photo_x1, photo_y1, photo_x2, photo_y2 = 200, 215, 460, 505
    draw.rectangle([photo_x1 - 3, photo_y1 - 3, photo_x2 + 3, photo_y2 + 3], outline="#CCCCCC", width=3)

    if profile_image is not None:
        try:
            w, h = profile_image.size
            target_w, target_h = 260, 290
            target_aspect = target_w / target_h
            img_aspect = w / h
            if img_aspect > target_aspect:
                new_width = int(h * target_aspect)
                left = (w - new_width) // 2
                cropped = profile_image.crop((left, 0, left + new_width, h))
            else:
                new_height = int(w / target_aspect)
                top = (h - new_height) // 2
                cropped = profile_image.crop((0, top, w, top + new_height))
            resized = cropped.resize((target_w, target_h), Image.Resampling.LANCZOS)
            card.paste(resized, (photo_x1, photo_y1))
        except Exception:
            draw.rectangle([photo_x1, photo_y1, photo_x2, photo_y2], fill="#F0F0F0")
    else:
        draw.rectangle([photo_x1, photo_y1, photo_x2, photo_y2], fill="#F0F0F0")
        draw.ellipse([295, 275, 365, 345], fill="#CCCCCC")
        draw.chord([240, 365, 420, 475], start=180, end=360, fill="#CCCCCC")

    name_font = get_autoscaled_font(draw, name.strip(), "roboto_bold", 520, 32)
    draw_centered_text(draw, name.strip(), 540, name_font, "#005A2D")
    role_font = get_autoscaled_font(draw, role.strip(), "roboto_medium", 520, 22)
    draw_centered_text(draw, role.strip(), 588, role_font, "#B46400")

    draw.rectangle([80, 635, 580, 815], fill="#F7FBF8", outline="#E2ECE5", width=2)
    label_font = load_font("roboto_bold", 17)
    val_font = load_font("roboto_medium", 17)

    draw.text((115, 658), "VOLUNTEER ID :", fill="#555555", font=label_font)
    draw.text((115, 712), "BLOOD GROUP  :", fill="#555555", font=label_font)
    draw.text((115, 766), "VALID UNTIL  :", fill="#555555", font=label_font)

    draw.text((300, 658), volunteer_id.strip().upper(), fill="#111111", font=val_font)
    bg_clean = blood_group.strip().upper()
    bg_color = "#B30000" if any(x in bg_clean for x in ["A", "B", "O", "AB"]) else "#111111"
    draw.text((300, 712), bg_clean, fill=bg_color, font=val_font)
    draw.text((300, 766), validity_date.strip(), fill="#111111", font=val_font)

    random.seed(volunteer_id)
    bar_x = 90
    while bar_x < 270:
        bw = random.choice([2, 3, 4, 6])
        draw.rectangle([bar_x, 845, bar_x + bw - 1, 890], fill="black")
        bar_x += bw + random.choice([2, 3, 4])
    barcode_font = load_font("roboto_regular", 11)
    draw.text((120, 898), f"*{volunteer_id.strip().upper()}*", fill="#555555", font=barcode_font)

    draw.line([390, 882, 570, 882], fill="#888888", width=2)

    sig_to_draw = signature_image
    if sig_to_draw is None and os.path.exists("signature_no_bg.png"):
        try:
            sig_to_draw = Image.open("signature_no_bg.png")
        except Exception:
            pass

    if sig_to_draw is not None:
        try:
            sw, sh = sig_to_draw.size
            max_sw, max_sh = 180, 60
            aspect = sw / sh
            if sw > max_sw or sh > max_sh:
                if aspect > max_sw / max_sh:
                    new_w, new_h = max_sw, int(max_sw / aspect)
                else:
                    new_h, new_w = max_sh, int(max_sh * aspect)
            else:
                new_w, new_h = sw, sh
            resized_sig = sig_to_draw.resize((new_w, new_h), Image.Resampling.LANCZOS)
            sig_x = 390 + (180 - new_w) // 2
            sig_y = 880 - new_h
            if resized_sig.mode == 'RGBA':
                card.paste(resized_sig, (sig_x, sig_y), resized_sig)
            else:
                card.paste(resized_sig, (sig_x, sig_y))
        except Exception:
            draw.line([410, 876, 428, 860, 455, 877, 482, 856, 510, 872, 538, 861, 560, 874], fill="#1C3D82", width=2)
    else:
        draw.line([410, 876, 428, 860, 455, 877, 482, 856, 510, 872, 538, 861, 560, 874], fill="#1C3D82", width=2)

    sig_font = load_font("roboto_bold", 11)
    draw.text((410, 890), "AUTHORIZED SIGNATURE", fill="#777777", font=sig_font)

    draw.rectangle([14, 944, 646, 950], fill="#D4AF37")
    draw.rectangle([14, 950, 646, 1006], fill="#005A2D")
    footer_font = load_font("roboto_regular", 13)
    draw_centered_text(draw, "If found, please return to office or contact admin.", 968, footer_font, "white")

    return card


# ─────────────────────────────────────────────
#  CARD 2 — APPOINTMENT / CONGRATULATION CARD
# ─────────────────────────────────────────────
def generate_appointment_card(name, role, location, profile_image, logo_image=None):
    W, H = 1080, 1080
    card = Image.new("RGBA", (W, H), "white")
    draw = ImageDraw.Draw(card)

    # Outer thick green border
    border = 22
    draw.rectangle([0, 0, W - 1, H - 1], outline="#1a6b1a", width=border)
    # Inner thin gold accent border
    draw.rectangle([30, 30, W - 31, H - 31], outline="#D4AF37", width=3)

    # ── HEADER ──
    # Logo area (top-left)
    logo_box_size = 110
    logo_x, logo_y = 55, 55

    if logo_image is not None:
        try:
            lw, lh = logo_image.size
            scale = logo_box_size / max(lw, lh)
            new_lw, new_lh = int(lw * scale), int(lh * scale)
            resized_logo = logo_image.resize((new_lw, new_lh), Image.Resampling.LANCZOS)
            lx = logo_x + (logo_box_size - new_lw) // 2
            ly = logo_y + (logo_box_size - new_lh) // 2
            if resized_logo.mode == 'RGBA':
                card.paste(resized_logo, (lx, ly), resized_logo)
            else:
                card.paste(resized_logo, (lx, ly))
        except Exception:
            _draw_placeholder_logo(draw, logo_x, logo_y, logo_box_size)
    else:
        _draw_placeholder_logo(draw, logo_x, logo_y, logo_box_size)

    # Foundation name (top-center, large)
    fname_font = load_font("roboto_bold", 52)
    draw_centered_text(draw, "AL-MEHARBAN FOUNDATION", 68, fname_font, "#1a5c1a", W)

    # Tagline
    tag_font = load_font("roboto_bold", 26)
    draw_centered_text(draw, "Every Life Matters, Every Smile Counts.", 138, tag_font, "#1a6b1a", W)

    # Small "Al-Meharban Foundation" label below logo
    small_font = load_font("roboto_regular", 18)
    draw.text((logo_x, logo_y + logo_box_size + 6), "Al-Meharban Foundation", fill="#1a6b1a", font=small_font)

    # ── GOLD DIVIDER ──
    draw.rectangle([55, 195, W - 55, 199], fill="#D4AF37")

    # ── PROFILE PHOTO ──
    photo_w, photo_h = 360, 400
    photo_x = (W - photo_w) // 2
    photo_y = 215
    # Frame (black border)
    draw.rectangle([photo_x - 5, photo_y - 5, photo_x + photo_w + 5, photo_y + photo_h + 5],
                   outline="#111111", width=5)

    if profile_image is not None:
        try:
            pw, ph = profile_image.size
            target_aspect = photo_w / photo_h
            img_aspect = pw / ph
            if img_aspect > target_aspect:
                new_pw = int(ph * target_aspect)
                left = (pw - new_pw) // 2
                cropped = profile_image.crop((left, 0, left + new_pw, ph))
            else:
                new_ph = int(pw / target_aspect)
                top = (ph - new_ph) // 2
                cropped = profile_image.crop((0, top, pw, top + new_ph))
            resized = cropped.resize((photo_w, photo_h), Image.Resampling.LANCZOS)
            card.paste(resized, (photo_x, photo_y))
        except Exception:
            _draw_placeholder_photo(draw, photo_x, photo_y, photo_w, photo_h)
    else:
        _draw_placeholder_photo(draw, photo_x, photo_y, photo_w, photo_h)

    # ── CONGRATULATIONS TEXT ──
    congrats_font = load_font("roboto_bold", 54)
    draw_centered_text(draw, "HEARTIEST CONGRATULATIONS", 650, congrats_font, "#1a5c1a", W)

    appt_font = load_font("roboto_bold", 30)
    draw_centered_text(draw, "On Appointment as " + role, 724, appt_font, "#111111", W)

    org_font = load_font("roboto_bold", 42)
    draw_centered_text(draw, "AL-MEHARBAN FOUNDATION", 784, org_font, "#1a5c1a", W)

    loc_font = load_font("roboto_bold", 28)
    if location.strip():
        draw_centered_text(draw, "From " + location.strip(), 844, loc_font, "#111111", W)

    # Name (large, bold, green)
    name_appt_font = get_autoscaled_font(draw, "Mr. " + name.strip(), "roboto_bold", W - 120, 52)
    draw_centered_text(draw, "Mr. " + name.strip(), 894, name_appt_font, "#1a5c1a", W)

    # ── GOLD DIVIDER before footer ──
    draw.rectangle([55, 958, W - 55, 962], fill="#D4AF37")

    # Together tagline
    together_font = load_font("roboto_bold", 20)
    draw_centered_text(draw, "TOGETHER WE CARE, TOGETHER WE CHANGE", 972, together_font, "#111111", W)

    # ── FOOTER ──
    draw.rectangle([0, 998, W, H], fill="#c8eac8")  # light mint green

    footer_font2 = load_font("roboto_bold", 22)
    draw_centered_text(draw, "Join us in making society!  Follow us Al-Meharban Foundation", 1008, footer_font2, "#111111", W)

    # Social icons text (simple text-based)
    social_font = load_font("roboto_regular", 19)
    socials = "f  /AlMeharbanFd        ig/al_meharban_foundation        tt/AlMeharban"
    draw_centered_text(draw, socials, 1046, social_font, "#333333", W)

    return card


def _draw_placeholder_logo(draw, x, y, size):
    draw.ellipse([x, y, x + size, y + size], outline="#1a6b1a", width=3, fill="#e8f5e9")
    cx, cy = x + size // 2, y + size // 2
    # Simple tree silhouette
    draw.polygon([cx, y + 12, cx - 28, cy + 10, cx + 28, cy + 10], fill="#1a6b1a")
    draw.polygon([cx, y + 28, cx - 20, cy + 22, cx + 20, cy + 22], fill="#1a6b1a")
    draw.rectangle([cx - 5, cy + 20, cx + 5, y + size - 10], fill="#1a6b1a")


def _draw_placeholder_photo(draw, px, py, pw, ph):
    draw.rectangle([px, py, px + pw, py + ph], fill="#F0F0F0")
    cx = px + pw // 2
    draw.ellipse([cx - 60, py + 50, cx + 60, py + 170], fill="#CCCCCC")
    draw.chord([cx - 110, py + 200, cx + 110, py + ph - 10], start=180, end=360, fill="#CCCCCC")


# ─────────────────────────────────────────────
#  UI
# ─────────────────────────────────────────────
st.markdown('<h1 class="main-title">Al-Meharban Foundation</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Volunteer ID Card + Appointment Card — Ek Form, Dono Cards</p>', unsafe_allow_html=True)

col_form, col_preview = st.columns([5, 7])

with col_form:
    st.subheader("Volunteer / Member Details")

    name = st.text_input("Full Name", value="Muhammad Umair Ahmed", max_chars=40)
    
    col1, col2 = st.columns(2)
    with col1:
        volunteer_id = st.text_input("Volunteer ID", value="AMF-2026-0042", max_chars=20)
    with col2:
        blood_group = st.selectbox("Blood Group",
            ["O+", "O-", "A+", "A-", "B+", "B-", "AB+", "AB-", "N/A"])

    col3, col4 = st.columns(2)
    with col3:
        role = st.text_input("Role / Designation", value="Community Leader", max_chars=40)
    with col4:
        validity_date = st.text_input("ID Valid Until", value="31-Dec-2027", max_chars=15)

    location = st.text_input("City / Area (for appointment card)", value="Malir Karachi", max_chars=40)

    st.markdown("---")
    st.subheader("Profile Photo")
    uploaded_file = st.file_uploader("Upload Photo (PNG, JPG, JPEG)",
                                     type=["png", "jpg", "jpeg"])

    st.subheader("Foundation Logo (optional)")
    uploaded_logo = st.file_uploader("Upload Logo (PNG recommended)",
                                     type=["png", "jpg", "jpeg"])

    st.subheader("Signature (optional)")
    uploaded_sig = st.file_uploader("Upload Signature Image",
                                    type=["png", "jpg", "jpeg"])

# Process images
profile_image = None
if uploaded_file:
    try:
        profile_image = Image.open(uploaded_file)
    except Exception as e:
        st.error(f"Photo load error: {e}")

logo_image = None
if uploaded_logo:
    try:
        logo_image = Image.open(uploaded_logo)
    except Exception as e:
        st.error(f"Logo load error: {e}")

signature_image = None
if uploaded_sig:
    try:
        signature_image = Image.open(uploaded_sig)
    except Exception as e:
        st.error(f"Signature load error: {e}")

# Generate both cards
id_card = generate_id_card(
    name=name, volunteer_id=volunteer_id, role=role,
    blood_group=blood_group, validity_date=validity_date,
    profile_image=profile_image, signature_image=signature_image
)

appt_card = generate_appointment_card(
    name=name, role=role, location=location,
    profile_image=profile_image, logo_image=logo_image
)

with col_preview:
    tab1, tab2 = st.tabs(["🪪  Volunteer ID Card", "🎖️  Appointment Card"])

    with tab1:
        st.markdown('<div class="card-label">Volunteer ID Card Preview</div>', unsafe_allow_html=True)
        st.image(id_card, caption="660 × 1020 px — Print Ready", use_container_width=True)

        png_buf = io.BytesIO()
        id_card.save(png_buf, format="PNG", dpi=(300, 300))
        pdf_buf = io.BytesIO()
        id_card.convert("RGB").save(pdf_buf, format="PDF", resolution=300.0)

        c1, c2 = st.columns(2)
        with c1:
            st.download_button("⬇️ Download ID Card PNG",
                               png_buf.getvalue(),
                               f"AMF_ID_{name.replace(' ', '_')}.png", "image/png")
        with c2:
            st.download_button("⬇️ Download ID Card PDF",
                               pdf_buf.getvalue(),
                               f"AMF_ID_{name.replace(' ', '_')}.pdf", "application/pdf")

    with tab2:
        st.markdown('<div class="card-label">Appointment Card Preview</div>', unsafe_allow_html=True)
        st.image(appt_card, caption="1080 × 1080 px — Social Media Ready", use_container_width=True)

        png_buf2 = io.BytesIO()
        appt_card.save(png_buf2, format="PNG", dpi=(300, 300))
        pdf_buf2 = io.BytesIO()
        appt_card.convert("RGB").save(pdf_buf2, format="PDF", resolution=300.0)

        c3, c4 = st.columns(2)
        with c3:
            st.download_button("⬇️ Download Appt. Card PNG",
                               png_buf2.getvalue(),
                               f"AMF_Appt_{name.replace(' ', '_')}.png", "image/png")
        with c4:
            st.download_button("⬇️ Download Appt. Card PDF",
                               pdf_buf2.getvalue(),
                               f"AMF_Appt_{name.replace(' ', '_')}.pdf", "application/pdf")

    st.markdown("---")
    st.markdown("**💡 Tip:** Dono cards ek sath download karne ke liye dono tabs se alag alag download karein.")