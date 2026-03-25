import os
import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
from PIL import Image
import time
import glob

from gtts import gTTS
from googletrans import Translator

# Quitar fondo blanco del botón de Bokeh
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Fondo y base ── */
html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"], .main {
    background: #ffffff !important;
    color: #1a1a2e !important;
}

[data-testid="stMainBlockContainer"] {
    background: #ffffff !important;
}

[data-testid="stHeader"] {
    background: transparent !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #f3f0ff !important;
    border-right: 1px solid rgba(124, 58, 237, 0.15) !important;
}

[data-testid="stSidebar"] * {
    color: #2d2d4e !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* ── Tipografía general ── */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Playfair Display', serif !important;
    color: #f0eaff !important;
    letter-spacing: -0.5px;
}

p, div, span, label, .stMarkdown {
    font-family: 'DM Sans', sans-serif !important;
    color: #2d2d4e !important;
}

/* ── Título principal ── */
[data-testid="stMarkdownContainer"] h2 {
    font-size: 2.2rem !important;
    background: linear-gradient(90deg, #c084fc, #818cf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
}

/* ── Subtítulo ── */
[data-testid="stMarkdownContainer"] p {
    font-size: 0.95rem !important;
    line-height: 1.7 !important;
    color: #5a5a7a !important;
}

/* ── Layout organizado ── */
[data-testid="stAppViewContainer"] > section > div {
    max-width: 700px;
    margin: 0 auto;
    padding: 2rem 1.5rem;
}

/* ── Imagen centrada ── */
[data-testid="stImage"] {
    display: flex;
    justify-content: center;
    margin: 0.5rem auto 2rem auto;
    filter: drop-shadow(0 0 24px rgba(192, 132, 252, 0.35));
}

/* ── Espaciado entre controles ── */
[data-testid="stSelectbox"],
[data-testid="stCheckbox"],
[data-testid="stButton"] {
    margin-bottom: 0.6rem !important;
}

/* ── Título h1 "Texto a Audio" ── */
h1 {
    font-size: 1.6rem !important;
    color: #c084fc !important;
    border-bottom: 1px solid rgba(192, 132, 252, 0.2);
    padding-bottom: 0.5rem;
    margin-bottom: 1.2rem !important;
}

/* ── Selectboxes ── */
[data-testid="stSelectbox"] > div > div {
    background: #f8f5ff !important;
    border: 1px solid rgba(124, 58, 237, 0.25) !important;
    border-radius: 12px !important;
    color: #1a1a2e !important;
    font-family: 'DM Sans', sans-serif !important;
    transition: border-color 0.2s ease;
}

[data-testid="stSelectbox"] > div > div:hover {
    border-color: rgba(192, 132, 252, 0.7) !important;
}

[data-testid="stSelectbox"] label {
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    color: #c084fc !important;
    font-size: 0.85rem !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

/* ── Botón "convertir" ── */
[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #7c3aed, #4f46e5) !important;
    color: #7c3aed !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.6rem 2rem !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 1rem !important;
    letter-spacing: 0.05em;
    box-shadow: 0 4px 20px rgba(124, 58, 237, 0.45) !important;
    transition: transform 0.15s ease, box-shadow 0.15s ease !important;
}

[data-testid="stButton"] > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(124, 58, 237, 0.6) !important;
}

/* ── Checkbox ── */
[data-testid="stCheckbox"] label {
    font-family: 'DM Sans', sans-serif !important;
    color: #2d2d4e !important;
}

/* ── Audio player ── */
audio {
    width: 100%;
    border-radius: 12px;
    filter: hue-rotate(240deg) saturate(0.8);
}

/* ── Texto de salida ── */
[data-testid="stMarkdownContainer"] h2 + * {
    background: rgba(255,255,255,0.04);
    border-left: 3px solid #c084fc;
    padding: 0.75rem 1rem;
    border-radius: 0 10px 10px 0;
}

/* ── Bokeh (botón de micrófono) ── */
div[data-testid="stBokehChart"],
div[data-testid="stBokehChart"] > *,
div[data-testid="stBokehChart"] iframe {
    background-color: #ffffff !important;
    background: #ffffff !important;
}

div[data-testid="stBokehChart"] {
    display: flex;
    justify-content: center;
    border-radius: 14px;
    overflow: hidden;
}

.bk-root, .bk-root *, .bk, .bk * {
    background-color: transparent !important;
}

/* ── Divisores ── */
hr {
    border-color: rgba(192, 132, 252, 0.2) !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(192,132,252,0.3); border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# ── Inyectar CSS dentro del iframe de Bokeh para matar el fondo blanco ──
st.markdown("""
<script>
(function fixBokehBg() {
    function inject() {
        document.querySelectorAll('iframe').forEach(function(iframe) {
            try {
                var doc = iframe.contentDocument || iframe.contentWindow.document;
                if (!doc) return;
                var style = doc.createElement('style');
                style.textContent = 'html,body{background:#ffffff!important;} .bk,.bk-root,.bk-canvas-wrapper,.bk-plot-wrapper,.bk-toolbar-box{background:#ffffff!important;}';
                doc.head && doc.head.appendChild(style);
            } catch(e) {}
        });
    }
    setTimeout(inject, 300);
    setTimeout(inject, 1000);
    setTimeout(inject, 2500);
    var observer = new MutationObserver(inject);
    observer.observe(document.body, {childList: true, subtree: true});
})();
</script>
""", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center;'>Bienvenido al traductor</h2>", unsafe_allow_html=True)
st.subheader("""
    La herramienta procesará tu mensaje y te mostrará la traducción de forma rápida y sencilla para facilitar la comprensión
    """)

image = Image.open('traductor.png')
st.image(image,width=300)

with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>Bienvenido al traductor</h2>", unsafe_allow_html=True)
    st.write("""
    Escribe el texto que deseas traducir en el campo correspondiente y selecciona el idioma al que quieres traducirlo.
    La herramienta procesará tu mensaje y te mostrará la traducción de forma rápida y sencilla para facilitar la comprensión
    entre diferentes idiomas.
    """)

stt_button = Button(label=" Escuchar 🎤", width=300, height=50) 

stt_button.js_on_event("button_click", CustomJS(code=""" 
    var recognition = new webkitSpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = true;
    recognition.lang = 'es-ES';

    
    recognition.onresult = function (e) {
        var value = "";
        for (var i = e.resultIndex; i < e.results.length; ++i) {
            if (e.results[i].isFinal) {
                value += e.results[i][0].transcript;
            }
        }
        if ( value != "") {
            document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
        }
    }
    
    recognition.onend = function() {
        console.log("Reconocimiento detenido");
    }
    
    recognition.start();
"""))

result = streamlit_bokeh_events(
    stt_button,
    events="GET_TEXT",
    key="listen",
    refresh_on_update=False,
    override_height=75,
    debounce_time=0)

if result:
    if "GET_TEXT" in result:
        st.write(result.get("GET_TEXT"))
    try:
        os.mkdir("temp")
    except:
        pass

    st.title("Texto a Audio")
    translator = Translator()
    
    text = str(result.get("GET_TEXT"))
    
    in_lang = st.selectbox(
        "Selecciona el lenguaje de Entrada",
        ("Inglés", "Español", "Bengali", "Coreano", "Mandarín", "Japonés"),
    )

    if in_lang == "Inglés":
        input_language = "en"
    elif in_lang == "Español":
        input_language = "es"
    elif in_lang == "Bengali":
        input_language = "bn"
    elif in_lang == "Coreano":
        input_language = "ko"
    elif in_lang == "Mandarín":
        input_language = "zh-cn"
    elif in_lang == "Japonés":
        input_language = "ja"
    
    out_lang = st.selectbox(
        "Selecciona el lenguaje de salida",
        ("Inglés", "Español", "Bengali", "Coreano", "Mandarín", "Japonés"),
    )

    if out_lang == "Inglés":
        output_language = "en"
    elif out_lang == "Español":
        output_language = "es"
    elif out_lang == "Bengali":
        output_language = "bn"
    elif out_lang == "Coreano":
        output_language = "ko"
    elif out_lang == "Mandarín":
        output_language = "zh-cn"
    elif out_lang == "Japonés":
        output_language = "ja"
    
    english_accent = st.selectbox(
        "Selecciona el acento",
        (
            "Defecto",
            "Español",
            "Reino Unido",
            "Estados Unidos",
            "Canada",
            "Australia",
            "Irlanda",
            "Sudáfrica",
        ),
    )
    
    if english_accent == "Defecto":
        tld = "com"
    elif english_accent == "Español":
        tld = "com.mx"
    elif english_accent == "Reino Unido":
        tld = "co.uk"
    elif english_accent == "Estados Unidos":
        tld = "com"
    elif english_accent == "Canada":
        tld = "ca"
    elif english_accent == "Australia":
        tld = "com.au"
    elif english_accent == "Irlanda":
        tld = "ie"
    elif english_accent == "Sudáfrica":
        tld = "co.za"
    
    def text_to_speech(input_language, output_language, text, tld):
        translation = translator.translate(text, src=input_language, dest=output_language)
        trans_text = translation.text
        tts = gTTS(trans_text, lang=output_language, tld=tld, slow=False)
        try:
            my_file_name = text[0:20]
        except:
            my_file_name = "audio"
        tts.save(f"temp/{my_file_name}.mp3")
        return my_file_name, trans_text
    
    display_output_text = st.checkbox("Mostrar el texto")
    
    if st.button("convertir"):
        result, output_text = text_to_speech(input_language, output_language, text, tld)
        audio_file = open(f"temp/{result}.mp3", "rb")
        audio_bytes = audio_file.read()
        st.markdown("## Tú audio:")
        st.audio(audio_bytes, format="audio/mp3", start_time=0)
    
        if display_output_text:
            st.markdown("## Texto de salida:")
            st.write(output_text)
    
    def remove_files(n):
        mp3_files = glob.glob("temp/*mp3")
        if len(mp3_files) != 0:
            now = time.time()
            n_days = n * 86400
            for f in mp3_files:
                if os.stat(f).st_mtime < now - n_days:
                    os.remove(f)
                    print("Deleted ", f)

    remove_files(7)
