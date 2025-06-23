import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image, ImageDraw
import io
import pandas as pd
from streamlit_option_menu import option_menu

st.set_page_config(page_title="Web Paint Sederhana", layout="centered")
st.title("🎨 Web Paint Sederhana")
st.caption("Kreativitas Digital & Interaksi Visual Ringan")

# --- Inisialisasi session state untuk Undo/Redo ---
if 'undo_stack' not in st.session_state:
    st.session_state.undo_stack = []
if 'redo_stack' not in st.session_state:
    st.session_state.redo_stack = []
if 'canvas_image' not in st.session_state:
    st.session_state.canvas_image = None
if 'canvas_action' not in st.session_state:
    st.session_state.canvas_action = None

# --- Sidebar: Pengaturan ---
st.sidebar.header("Pengaturan Gambar")
with st.sidebar:
    selected_mode = option_menu(
        "Drawing tool",
        ["freedraw", "line", "rect", "circle", "polygon", "transform"],
        icons=["pencil", "arrows-angle-contract", "square", "circle", "triangle", "shuffle"],
        menu_icon="cast",
        default_index=0,
        orientation="vertical"
    )
drawing_mode = selected_mode
stroke_width = st.sidebar.slider("Stroke width: ", 1, 25, 3)
stroke_color = st.sidebar.color_picker("Stroke color hex: ")
drawings_with_fill = ["rect", "circle", "polygon"]
if drawing_mode in drawings_with_fill:
    fill_same_as_stroke = st.sidebar.checkbox("Fill color sama dengan stroke", False)
    if fill_same_as_stroke:
        fill_color_rgb = stroke_color
        fill_color_disabled = True
    else:
        fill_color_rgb = st.sidebar.color_picker("Fill color hex: ", "#FFA500")
        fill_color_disabled = False
    fill_alpha = st.sidebar.slider("Fill alpha (transparency):", 0, 255, 77)  # 77 ≈ 0.3 opacity
else:
    fill_color_rgb = "#FFA500"
    fill_alpha = 77
bg_color = st.sidebar.color_picker("Background color hex: ", "#eee")
bg_image = st.sidebar.file_uploader("Background image:", type=["png", "jpg"])
realtime_update = True
display_toolbar = True

# Konversi hex ke RGB
fill_color_rgb = fill_color_rgb.lstrip('#')
r, g, b = tuple(int(fill_color_rgb[i:i+2], 16) for i in (0, 2, 4))
fill_color_rgba = f"rgba({r}, {g}, {b}, {fill_alpha/255:.2f})"

# --- Ukuran kanvas ---
canvas_width = 600
canvas_height = 400

# --- Mapping mode ke st_canvas ---
mode_map = {
    "Free Draw": "freedraw",
    "Line": "line",
    "Rectangle": "rect",
    "Circle": "circle",
    "Polygon (Segitiga)": "polygon",
}

# --- Fungsi untuk menyimpan aksi ke undo_stack ---
def push_undo(data):
    st.session_state.undo_stack.append(data)
    st.session_state.redo_stack.clear()

def pop_undo():
    if st.session_state.undo_stack:
        data = st.session_state.undo_stack.pop()
        st.session_state.redo_stack.append(data)

def pop_redo():
    if st.session_state.redo_stack:
        data = st.session_state.redo_stack.pop()
        st.session_state.undo_stack.append(data)

# --- Tombol kontrol ---
# col1, col2, col3, col4 = st.columns(4)
# with col1:
#     undo = st.button("↩️ Undo")
# with col2:
#     redo = st.button("↪️ Redo")
# with col3:
#     clear = st.button("🗑️ Clear")
# with col4:
#     save = st.button("💾 Save PNG")

# --- Proses Undo/Redo/Clear ---
# if undo:
#     pop_undo()
#     st.session_state.canvas_action = 'undo'
# elif redo:
#     pop_redo()
#     st.session_state.canvas_action = 'redo'
# elif clear:
#     st.session_state.undo_stack.clear()
#     st.session_state.redo_stack.clear()
#     st.session_state.canvas_image = None
#     st.session_state.canvas_action = 'clear'
# else:
#     st.session_state.canvas_action = None

# --- Ambil data terakhir dari undo_stack untuk ditampilkan ---
if st.session_state.undo_stack:
    last_data = st.session_state.undo_stack[-1]
else:
    last_data = None

# --- Kanvas ---
if st.session_state.canvas_action in ['undo', 'redo', 'clear']:
    initial_drawing = last_data if isinstance(last_data, dict) else None
else:
    initial_drawing = None

canvas_result = st_canvas(
    fill_color=fill_color_rgba,
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=bg_color,
    background_image=Image.open(bg_image) if bg_image else None,
    update_streamlit=realtime_update,
    height=canvas_height,
    width=canvas_width,
    drawing_mode=drawing_mode,
    display_toolbar=display_toolbar,
    key="canvas",
    initial_drawing=initial_drawing,
)

# --- Simpan aksi baru ke undo_stack jika ada perubahan ---
if canvas_result.json_data is not None:
    if not st.session_state.undo_stack or (canvas_result.json_data != st.session_state.undo_stack[-1]):
        push_undo(canvas_result.json_data)

# --- Save PNG ---
def save_canvas_as_png(json_data):
    img = Image.new("RGB", (canvas_width, canvas_height), "white")
    draw = ImageDraw.Draw(img)
    # Untuk demo: hanya menyimpan gambar kanvas (tanpa parsing objek detail)
    # Untuk hasil lebih baik, gunakan render dari st_canvas
    return img

# Sembunyikan ikon download pada toolbar bawaan st_canvas
st.markdown(
    """
    <style>
    .toolbar button:first-child { display: none !important; }
    </style>
    """,
    unsafe_allow_html=True
)

# Tampilkan tombol custom download PNG di bawah kanvas
if canvas_result.image_data is not None:
    st.image(canvas_result.image_data)
    buf = io.BytesIO()
    img = Image.fromarray(canvas_result.image_data.astype('uint8'), 'RGBA').convert('RGB')
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    st.download_button("Download PNG", data=byte_im, file_name="web_paint.png", mime="image/png")

if canvas_result.json_data is not None:
    objects = pd.json_normalize(canvas_result.json_data["objects"])
    for col in objects.select_dtypes(include=["object"]).columns:
        objects[col] = objects[col].astype("str")
    st.dataframe(objects)

st.markdown("---")
st.markdown("**Petunjuk:** Pilih mode, warna, dan ukuran pena di sidebar. Undo/Redo untuk mengelola aksi. Clear untuk menghapus semua. Save untuk mengunduh hasil.") 