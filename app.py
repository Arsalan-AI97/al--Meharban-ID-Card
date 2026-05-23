import streamlit as st
import io
import os
import random
from PIL import Image, ImageDraw, ImageFont
import requests

# Set page configuration
st.set_page_config(
    page_title="Al-Meharban Foundation - Volunteer ID Card Generator",
    page_icon="🪪",
    layout="wide"
)

# Custom Styling to match Deep Emerald Green theme
st.markdown("""
    <style>
    .main-title {
        color: #005A2D;
        font-family: 'Outfit', 'Inter', 'Segoe UI', sans-serif;
        font-weight: 800;
        font-size: 2.5rem;
        margin-bottom: 0px;
    }
    .sub-title {
        color: #555555;
        font-family: 'Inter', 'Segoe UI', sans-serif;
        font-size: 1.1rem;
        margin-bottom: 30px;
    }
    .instructions {
        background-color: #27a131;
        border-left: 5px solid #005A2D;
        padding: 15px;
        border-radius: 4px;
        margin-bottom: 20px;
        font-family: 'Inter', sans-serif;
        font-size: 0.95rem;
    }
    /* Style download buttons */
    div.stButton > button:first-child {
        background-color: #005A2D !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 12px 28px !important;
        font-size: 1rem !important;
        font-weight: bold !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1) !important;
    }
    div.stButton > button:first-child:hover {
        background-color: #004020 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 12px rgba(0, 90, 45, 0.25) !important;
    }
    </style>
""", unsafe_allow_html=True)

# Define directories
FONT_DIR = "fonts"
os.makedirs(FONT_DIR, exist_ok=True)

# Font URLs and local paths
FONTS = {
    "roboto_regular": {
        "url": "https://github.com/google/fonts/raw/main/apache/roboto/static/Roboto-Regular.ttf",
        "fallback": ["C:\\Windows\\Fonts\\arial.ttf", "C:\\Windows\\Fonts\\calibri.ttf", "C:\\Windows\\Fonts\\segoeui.ttf"]
    },
    "roboto_bold": {
        "url": "https://github.com/google/fonts/raw/main/apache/roboto/static/Roboto-Bold.ttf",
        "fallback": ["C:\\Windows\\Fonts\\arialbd.ttf", "C:\\Windows\\Fonts\\calibrib.ttf", "C:\\Windows\\Fonts\\segoeuib.ttf"]
    },
    "roboto_medium": {
        "url": "https://github.com/google/fonts/raw/main/apache/roboto/static/Roboto-Medium.ttf",
        "fallback": ["C:\\Windows\\Fonts\\arial.ttf", "C:\\Windows\\Fonts\\calibri.ttf", "C:\\Windows\\Fonts\\segoeui.ttf"]
    }
}

@st.cache_resource
def load_font(font_key, size):
    """
    Downloads Roboto font files from Google Fonts and caches them locally.
    Falls back gracefully to system fonts if offline, or default PIL font if none found.
    """
    font_info = FONTS[font_key]
    local_path = os.path.join(FONT_DIR, f"{font_key}.ttf")
    
    # Try downloading if font file doesn't exist
    if not os.path.exists(local_path):
        try:
            response = requests.get(font_info["url"], timeout=5)
            if response.status_code == 200:
                with open(local_path, "wb") as f:
                    f.write(response.content)
        except Exception:
            # Fall back silently if offline
            pass
            
    # Check if download succeeded and load it
    if os.path.exists(local_path):
        try:
            return ImageFont.truetype(local_path, size)
        except Exception:
            pass
            
    # Fallback to system fonts
    for fallback_path in font_info["fallback"]:
        if os.path.exists(fallback_path):
            try:
                return ImageFont.truetype(fallback_path, size)
            except Exception:
                pass
                
    # Ultimate fallback
    return ImageFont.load_default()

def get_autoscaled_font(draw, text, font_key, max_width, initial_size):
    """
    Measures text size and dynamically shrinks the font size until it fits within max_width.
    """
    size = initial_size
    while size > 10:
        font = load_font(font_key, size)
        bbox = draw.textbbox((0, 0), text, font=font)
        w = bbox[2] - bbox[0]
        if w <= max_width:
            return font
        size -= 2
    return load_font(font_key, 10)

def draw_centered_text(draw, text, y, font, fill_color, canvas_width=660):
    """
    Draws text perfectly centered horizontally at y-coordinate.
    """
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    x = (canvas_width - text_width) / 2
    draw.text((x, y), text, fill=fill_color, font=font)

def generate_id_card(name, volunteer_id, role, blood_group, validity_date, profile_image, signature_image=None):
    """
    Generates a 660x1020 high-quality CR80 vertical ID card using Pillow.
    """
    # 1. Initialize canvas (White background)
    card = Image.new("RGBA", (660, 1020), "white")
    draw = ImageDraw.Draw(card)
    
    # 2. Draw thick deep emerald green outer border
    # Outer bounds: 10, 10 to 650, 1010
    draw.rectangle([10, 10, 650, 1010], outline="#005A2D", width=8)
    
    # 3. Header Banner (Solid green block)
    # Inside bounds: 14 to 646. Y: 14 to 170
    draw.rectangle([14, 14, 646, 170], fill="#005A2D")
    
    # Golden border stripe separating header and body
    draw.rectangle([14, 170, 646, 176], fill="#D4AF37")
    
    # 4. Draw Header Branding & Logo
    # Draw logo emblem (crescent & star)
    draw.ellipse([305, 25, 355, 75], fill="#005A2D", outline="#D4AF37", width=2)
    # Draw crescent
    draw.ellipse([312, 32, 342, 62], fill="#D4AF37")
    draw.ellipse([317, 30, 345, 58], fill="#005A2D")
    # Draw star
    draw.ellipse([336, 38, 340, 42], fill="#D4AF37")
    
    # Header main text
    header_font = load_font("roboto_bold", 24)
    draw_centered_text(draw, "AL-MEHARBAN FOUNDATION", 92, header_font, "white")
    
    # Header subtext
    sub_font = load_font("roboto_regular", 14)
    draw_centered_text(draw, "Every Life Matters, Every Smile Counts", 128, sub_font, "#E0E0E0")
    
    # 5. Profile Picture (W: 260, H: 290, centered)
    # X coordinates: 200 to 460
    # Y coordinates: 215 to 505
    photo_x1, photo_y1 = 200, 215
    photo_x2, photo_y2 = 460, 505
    
    # Draw profile frame border (grey outline)
    draw.rectangle([photo_x1 - 3, photo_y1 - 3, photo_x2 + 3, photo_y2 + 3], outline="#CCCCCC", width=3)
    
    if profile_image is not None:
        # Load and cover crop the image to 260x290
        try:
            w, h = profile_image.size
            target_w, target_h = 260, 290
            target_aspect = target_w / target_h
            img_aspect = w / h
            
            if img_aspect > target_aspect:
                new_width = int(h * target_aspect)
                left = (w - new_width) // 2
                right = left + new_width
                top, bottom = 0, h
            else:
                new_height = int(w / target_aspect)
                top = (h - new_height) // 2
                bottom = top + new_height
                left, right = 0, w
                
            cropped_img = profile_image.crop((left, top, right, bottom))
            resized_img = cropped_img.resize((target_w, target_h), Image.Resampling.LANCZOS)
            
            # Paste into canvas
            card.paste(resized_img, (photo_x1, photo_y1))
        except Exception as e:
            # Fall back to drawing placeholder in case of error
            draw.rectangle([photo_x1, photo_y1, photo_x2, photo_y2], fill="#F0F0F0")
            draw.ellipse([295, 275, 365, 345], fill="#CCCCCC")
            draw.chord([240, 365, 420, 475], start=180, end=360, fill="#CCCCCC")
    else:
        # Vector placeholder profile drawing
        draw.rectangle([photo_x1, photo_y1, photo_x2, photo_y2], fill="#F0F0F0")
        # Head (centered at 330, Y=310, r=35)
        draw.ellipse([295, 275, 365, 345], fill="#CCCCCC")
        # Shoulders (arch centered at 330, Y=365)
        draw.chord([240, 365, 420, 475], start=180, end=360, fill="#CCCCCC")
        
    # 6. Volunteer Name & Role Details
    # Auto-scale volunteer name to fit card width (max width 520px)
    name_font = get_autoscaled_font(draw, name.strip(), "roboto_bold", 520, 32)
    draw_centered_text(draw, name.strip(), 540, name_font, "#005A2D")
    
    # Volunteer Role (Gold/Amber accent)
    role_font = get_autoscaled_font(draw, role.strip(), "roboto_medium", 520, 22)
    draw_centered_text(draw, role.strip(), 588, role_font, "#B46400")
    
    # 7. Metadata Grid Card (ID, Blood Group, Validity)
    # Box: X [80, 580], Y [635, 815]
    draw.rectangle([80, 635, 580, 815], fill="#F7FBF8", outline="#E2ECE5", width=2)
    
    label_font = load_font("roboto_bold", 17)
    val_font = load_font("roboto_medium", 17)
    
    # Rows Y-coordinates
    r1_y = 658
    r2_y = 712
    r3_y = 766
    
    # Labels (X = 110)
    draw.text((115, r1_y), "VOLUNTEER ID :", fill="#555555", font=label_font)
    draw.text((115, r2_y), "BLOOD GROUP  :", fill="#555555", font=label_font)
    draw.text((115, r3_y), "VALID UNTIL  :", fill="#555555", font=label_font)
    
    # Values (X = 300)
    draw.text((300, r1_y), volunteer_id.strip().upper(), fill="#111111", font=val_font)
    
    # Blood Group highlights in red if valid blood group format
    bg_clean = blood_group.strip().upper()
    bg_color = "#B30000" if any(x in bg_clean for x in ["A", "B", "O", "AB"]) else "#111111"
    draw.text((300, r2_y), bg_clean, fill=bg_color, font=val_font)
    
    draw.text((300, r3_y), validity_date.strip(), fill="#111111", font=val_font)
    
    # 8. Barcode & Signature
    # Draw simulated barcode based on volunteer_id hash for uniqueness
    random.seed(volunteer_id)
    bar_x = 90
    bar_y_start = 845
    bar_y_end = 890
    
    while bar_x < 270:
        bar_width = random.choice([2, 3, 4, 6])
        draw.rectangle([bar_x, bar_y_start, bar_x + bar_width - 1, bar_y_end], fill="black")
        gap_width = random.choice([2, 3, 4])
        bar_x += bar_width + gap_width
        
    # Under barcode text
    barcode_text_font = load_font("roboto_regular", 11)
    draw.text((120, 898), f"*{volunteer_id.strip().upper()}*", fill="#555555", font=barcode_text_font)
    
    # Draw signature line & text
    draw.line([390, 882, 570, 882], fill="#888888", width=2)
    
    # Try using uploaded signature or fallback to signature_no_bg.png
    sig_to_draw = signature_image
    if sig_to_draw is None:
        default_sig_path = "signature_no_bg.png"
        if os.path.exists(default_sig_path):
            try:
                sig_to_draw = Image.open(default_sig_path)
            except Exception:
                pass
                
    if sig_to_draw is not None:
        try:
            # Resize signature image to fit the signature area
            # The area width is 180, height could be around 60 (from Y=820 to 880)
            sig_w, sig_h = sig_to_draw.size
            max_sig_w = 180
            max_sig_h = 60
            
            # Calculate aspect ratio
            aspect = sig_w / sig_h
            if sig_w > max_sig_w or sig_h > max_sig_h:
                if aspect > max_sig_w / max_sig_h:
                    new_w = max_sig_w
                    new_h = int(max_sig_w / aspect)
                else:
                    new_h = max_sig_h
                    new_w = int(max_sig_h * aspect)
            else:
                new_w, new_h = sig_w, sig_h
                
            resized_sig = sig_to_draw.resize((new_w, new_h), Image.Resampling.LANCZOS)
            
            # Center horizontally in the 390-570 region (width 180)
            # Paste signature slightly above the line at Y=882
            sig_x = 390 + (180 - new_w) // 2
            sig_y = 880 - new_h
            
            if resized_sig.mode == 'RGBA':
                card.paste(resized_sig, (sig_x, sig_y), resized_sig)
            else:
                card.paste(resized_sig, (sig_x, sig_y))
        except Exception:
            # Fallback to simulated signature on error
            draw.line([410, 876, 428, 860, 455, 877, 482, 856, 510, 872, 538, 861, 560, 874], fill="#1C3D82", width=2)
    else:
        # Simulated cursive blue ink signature
        draw.line([410, 876, 428, 860, 455, 877, 482, 856, 510, 872, 538, 861, 560, 874], fill="#1C3D82", width=2)
    
    sig_font = load_font("roboto_bold", 11)
    draw.text((410, 890), "AUTHORIZED SIGNATURE", fill="#777777", font=sig_font)
    
    # 9. Footer Ribbon
    # Golden line separating body and footer
    draw.rectangle([14, 944, 646, 950], fill="#D4AF37")
    # Solid green block
    draw.rectangle([14, 950, 646, 1006], fill="#005A2D")
    
    # Footer Notice text
    footer_font = load_font("roboto_regular", 13)
    draw_centered_text(draw, "If found, please return to office or contact admin.", 968, footer_font, "white")
    
    return card

# App Header Layout
col_logo, col_title = st.columns([1, 12])
with col_title:
    st.markdown('<h1 class="main-title">Al-Meharban Foundation</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Automated Volunteer ID Card Generator • High Quality & Print-Ready</p>', unsafe_allow_html=True)

# Main columns: Left for Form input, Right for Real-time Card Preview
col_form, col_preview = st.columns([7, 5])

with col_form:
    st.markdown('<div class="instructions">💡 <b>Instructions:</b> Fill out the volunteer information below and upload a profile picture. The card preview on the right will update in real-time. You can then download the result as a high-resolution PNG or print-ready PDF.</div>', unsafe_allow_html=True)
    
    st.subheader("Volunteer Information Form")
    
    # Volunteer details input fields
    name = st.text_input("Full Name", value="Muhammad Bilal Ahmad", max_chars=40, help="Name of the volunteer (auto-scales if long)")
    
    col_row1_1, col_row1_2 = st.columns(2)
    with col_row1_1:
        volunteer_id = st.text_input("Volunteer ID", value="AMF-2026-9042", max_chars=20, help="Unique identifier, e.g. AMF-YYYY-XXXX")
    with col_row1_2:
        role = st.text_input("Role / Designation", value="Senior Welfare Officer", max_chars=35, help="Role, e.g. Welfare Officer, Educator, Medical Volunteer")
        
    col_row2_1, col_row2_2 = st.columns(2)
    with col_row2_1:
        blood_group = st.selectbox(
            "Blood Group", 
            options=["O+", "O-", "A+", "A-", "B+", "B-", "AB+", "AB-", "N/A"], 
            index=0, 
            help="Blood Group of the volunteer"
        )
    with col_row2_2:
        validity_date = st.text_input("Validity Date", value="31-Dec-2027", max_chars=15, help="ID expiration date, e.g. 31-Dec-2027")
        
    st.markdown("---")
    st.subheader("Profile Photo Upload")
    
    # Photo Upload Component (supports JPG, JPEG, PNG, PDF)
    uploaded_file = st.file_uploader(
        "Upload Volunteer Photo (supports PNG, JPG, JPEG or PDF)",
        type=["png", "jpg", "jpeg", "pdf"],
        help="Upload a portrait photo. If a PDF is uploaded, the first page will be automatically extracted."
    )
    
    st.subheader("Signature Upload")
    uploaded_sig = st.file_uploader(
        "Upload Signature Image (optional, supports PNG, JPG, JPEG)",
        type=["png", "jpg", "jpeg"],
        help="Upload a signature image to replace the default signature."
    )
    
    # Process uploaded profile image (including PDF extraction)
    profile_image = None
    if uploaded_file is not None:
        file_name = uploaded_file.name.lower()
        if file_name.endswith('.pdf'):
            try:
                import fitz as _fitz  # PyMuPDF (lazy import)
            except ImportError:
                _fitz = None
                st.warning("⚠️ Standard PDF processing library 'pymupdf' is not available. Please upload PNG/JPG format directly, or make sure PyMuPDF is installed.")

            if _fitz is not None:
                try:
                    # Read bytes and load PDF
                    pdf_bytes = uploaded_file.read()
                    doc = _fitz.open(stream=pdf_bytes, filetype="pdf")
                    if len(doc) > 0:
                        page = doc.load_page(0)
                        # Extract page with 150 DPI for standard photo crop
                        pix = page.get_pixmap(dpi=150)
                        img_data = pix.tobytes("png")
                        profile_image = Image.open(io.BytesIO(img_data))
                    else:
                        st.error("The uploaded PDF has no pages.")
                except Exception as e:
                    st.error(f"Error extracting image from PDF: {e}")
        else:
            try:
                # Open directly using PIL
                profile_image = Image.open(uploaded_file)
            except Exception as e:
                st.error(f"Error loading image file: {e}")

# Process uploaded signature image
signature_image = None
if uploaded_sig is not None:
    try:
        signature_image = Image.open(uploaded_sig)
    except Exception as e:
        st.error(f"Error loading signature image: {e}")

# Generate the ID card using Pillow Canvas Engine
id_card = generate_id_card(
    name=name,
    volunteer_id=volunteer_id,
    role=role,
    blood_group=blood_group,
    validity_date=validity_date,
    profile_image=profile_image,
    signature_image=signature_image
)

with col_preview:
    st.subheader("ID Card Live Preview")
    
    # Display the generated card
    st.image(id_card, caption="Vertical CR80 standard card preview (660 x 1020 pixels)", width="stretch")
    
    st.markdown("### Export options")
    
    # Prepare PNG bytes
    png_buf = io.BytesIO()
    id_card.save(png_buf, format="PNG", dpi=(300, 300))
    png_bytes = png_buf.getvalue()
    
    # Prepare PDF bytes (must convert to RGB first as PDF does not support RGBA transparency)
    pdf_buf = io.BytesIO()
    rgb_card = id_card.convert("RGB")
    rgb_card.save(pdf_buf, format="PDF", resolution=300.0)
    pdf_bytes = pdf_buf.getvalue()
    
    # Standard printable file name format
    file_base_name = f"AMF_ID_{name.replace(' ', '_')}"
    
    # Streamlit layout for side-by-side download buttons
    col_dl_png, col_dl_pdf = st.columns(2)
    with col_dl_png:
        st.download_button(
            label="⬇️ Download PNG",
            data=png_bytes,
            file_name=f"{file_base_name}.png",
            mime="image/png"
        )
    with col_dl_pdf:
        st.download_button(
            label="⬇️ Download PDF",
            data=pdf_bytes,
            file_name=f"{file_base_name}.pdf",
            mime="application/pdf"
        )