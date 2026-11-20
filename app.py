import platform
import shutil
import socket
import psutil
import streamlit as st
from ai_logic import analyze_with_ai

# =========================================================
# CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="AI PC Health Monitor",
    page_icon="🖥️",
    layout="wide",
    initial_sidebar_state="collapsed", 
)


# Load CSS & HTML Helper
def load_css(file_name):
  try:
    with open(file_name, encoding="utf-8") as f:
      st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
  except FileNotFoundError:
    pass


def load_html(file_name):
  try:
    with open(file_name, encoding="utf-8") as f:
      return f.read()
  except FileNotFoundError:
    return f"<h3>Error: File {file_name} tidak ditemukan!</h3>"


load_css("style.css")

# =========================================================
#  CUSTOM NAVBAR HTML 
# =========================================================
st.markdown(
    """
    <div class="fContainer">
      <nav class="wrapper">
      <div class="brand">
        <div class="first">AI PC</div>
        <div class="last">Health Monitor</div>
    </div>
      <ul class="navigation">
          <li class="navbar li"><a href="?page=home">Home</a></li>
          <li><a href="?page=about">About</a></li>
          <li><a href="?page=diagnostic">Diagnostic</a></li>
      </ul>
    </nav>
    </div>   
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="social-icons-container">
        <a href="https://www.instagram.com/fahri_1628" target="_blank" class="instagram-icon">
            <svg viewBox="0 0 24 24">
                <rect x="2" y="2" width="20" height="20" rx="5" ry="5" fill="none"></rect>
                <path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z" fill="none"></path>
                <line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line>
            </svg>
        </a>
    </div>
    """,
    unsafe_allow_html=True,
)


import base64
import streamlit as st


# Fungsi untuk membaca file video dan diubah ke base64  
current_page = st.query_params.get("page", "home")



def get_video_base64(video_path):
    with open(video_path, "rb") as video_file:
        encoded = base64.b64encode(video_file.read()).decode()
    return f"data:video/mp4;base64,{encoded}"

   
if current_page == "home":
    video_bg = get_video_base64("bg-video.mp4")
    st.markdown(
        f"""
        <video autoplay muted loop playsinline class="bg-video">
            <source src="{video_bg}" type="video/mp4">
        </video>
        """,
        unsafe_allow_html=True,
    )

if current_page != "home":
  st.markdown(
      """
        <style>
        /* Meniru persis gradasi gelap, kebiruan, dengan kilau ungu/magenta di background home */
        .stApp {
            background: 
                radial-gradient(circle at 75% 35%, rgba(168, 85, 247, 0.35) 0%, transparent 45%),
                radial-gradient(circle at 15% 85%, rgba(6, 182, 212, 0.25) 0%, transparent 50%),
                linear-gradient(135deg, #061528 0%, #0c2340 50%, #171f38 100%) !important;
            background-attachment: fixed;
        }
        </style>
        """,
      unsafe_allow_html=True,
  )

st.markdown(
    """
    <style>
    
    button[kind="secondary"], button {
        
        background: #ffffff2f !important;
        color: #ffffff !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3) !important;
        
       
        transition: all 0.4s ease-in-out !important;
    }

    
    button[kind="secondary"]:hover, button:hover {
        color: #ffffff !important;
        border-color: rgba(255, 255, 255, 0.8) !important;
        box-shadow: 0 6px 20px rgba(147, 51, 234, 0.5) !important;
        transform: translateY(-2px) !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# Mengambil status halaman dari URL (Query Parameters)
query_params = st.query_params
active_page = query_params.get("page", "home",)  # Default-nya ke halaman 'home'

# =========================================================
# PEMILIHAN HALAMAN BERDASARKAN NAVBAR
# =========================================================

if active_page == "home":
  # Membaca file home.html
  st.markdown(load_html("home.html"), unsafe_allow_html=True)

elif active_page == "diagnostic":
  # Ambil data hardware asli komputer
  cpu_usage = psutil.cpu_percent(interval=1)
  ram = psutil.virtual_memory()
  ram_usage = ram.percent
  ram_total = ram.total / (1024**3)
  ram_available = ram.available / (1024**3)

  disk = shutil.disk_usage("/")
  disk_total = disk.total / (1024**3)
  disk_used = disk.used / (1024**3)
  disk_percent = (disk.used / disk.total) * 100

  computer_name = socket.gethostname()
  system_name = platform.system()
  system_version = platform.version()
  processor = platform.processor()

  # Baca kerangka dari diagnostic.html lalu format datanya
  diag_template = load_html("diagnostic.html")
  rendered_html = diag_template.format(
      cpu_val=f"{cpu_usage:.1f}%",
      ram_val=f"{ram_usage:.1f}%",
      disk_val=f"{disk_percent:.1f}%",
  )
  st.markdown(rendered_html, unsafe_allow_html=True)

  # Progress bar tambahan
  col_l, col_r = st.columns(2)
  with col_l:
    st.write(f"**CPU Usage Detail:** {cpu_usage:.1f}%")
    st.progress(min(cpu_usage / 100, 1.0))
    st.write(f"**RAM Usage:** {ram_usage:.1f}% ({ram_total:.2f} GB Total)")
    st.progress(min(ram_usage / 100, 1.0))

  with col_r:
    st.write(f"**Disk Usage:** {disk_percent:.1f}%")
    st.progress(min(disk_percent / 100, 1.0))
    st.write(
        f"**Disk Free:** {(disk_total - disk_used):.2f} GB dari"
        f" {disk_total:.2f} GB"
    )

  # Tombol AI Diagnostic
  st.markdown("---")
  if st.button("🔍 ANALYZE PC WITH AI", use_container_width=True):
    with st.spinner("🤖 AI sedang menganalisis kondisi PC..."):
      ai_result, error = analyze_with_ai(
          computer_name,
          system_name,
          processor,
          cpu_usage,
          ram_usage,
          ram_total,
          ram_available,
          disk_percent,
          disk_total,
          disk_used,
      )

      if error:
        st.error("Gagal terhubung ke Ollama.")
        st.code(error)
      else:
        st.markdown(
            """
                <div class="ai-box">
                    <div class="ai-title">🤖 AI Diagnosis Result</div>
                </div>
                """,
            unsafe_allow_html=True,
        )
        st.markdown(ai_result)

elif active_page == "about":
  # Membaca file about.html
  st.markdown(load_html("about.html"), unsafe_allow_html=True)