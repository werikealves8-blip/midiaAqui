import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="Downloader Pro", page_icon="⬇️")

st.title("⬇️ Downloader Pro")

link = st.text_input("Cole o link do vídeo aqui:")

# Inicializa estados
if 'preparado' not in st.session_state: st.session_state.preparado = False
if 'anuncio_visto' not in st.session_state: st.session_state.anuncio_visto = False

if st.button("Preparar Download"):
    if link:
        st.session_state.preparado = True
    else:
        st.error("Cole um link válido.")

if st.session_state.preparado and not st.session_state.anuncio_visto:
    st.subheader("Escolha a qualidade:")
    qualidade = st.selectbox("Opções:", ["Qualidade Média (360p)", "Qualidade Alta (720p)", "Apenas Áudio (MP3)"])
    
    st.warning("⚠️ Clique no banner abaixo para liberar o download.")
    
    # Anúncio clicável
    st.markdown("""
    <a href="https://pl30146977.effectivecpmnetwork.com/68/ef/ed/68efedae0214a457f49cd05115af4be8.js" target="_blank">
        <div style="background-color: #ff4b4b; color: white; padding: 20px; text-align: center; border-radius: 10px; cursor: pointer;">
            CLIQUE AQUI PARA ASSISTIR O ANÚNCIO E LIBERAR O DOWNLOAD
        </div>
    </a>
    """, unsafe_allow_html=True)
    
    if st.button("Já assisti o anúncio, liberar download!"):
        st.session_state.anuncio_visto = True
        st.session_state.qualidade_escolhida = qualidade
        st.rerun()

if st.session_state.anuncio_visto:
    st.success("✅ Download liberado!")
    
    if st.button("Iniciar Download"):
        try:
            with st.spinner('Baixando...'):
                pasta_temp = "downloads"
                os.makedirs(pasta_temp, exist_ok=True)
                
                q = st.session_state.qualidade_escolhida
                
                # Formatos configurados para não precisar de FFmpeg e evitar erro 403
                if "MP3" in q:
                    fmt = 'bestaudio/best'
                elif "Alta" in q:
                    fmt = 'best[height<=720][ext=mp4]/best[ext=mp4]'
                else:
                    fmt = 'best[height<=360][ext=mp4]/best[ext=mp4]'
                
                ydl_opts = {
                    'outtmpl': f'{pasta_temp}/%(title)s.%(ext)s',
                    'format': fmt,
                    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'nocheckcertificate': True,
                    'quiet': True
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(link, download=True)
                    arquivo = ydl.prepare_filename(info)
                    if "MP3" in q: 
                        arquivo = arquivo.replace(".webm", ".mp3").replace(".m4a", ".mp3")
                
                with open(arquivo, "rb") as f:
                    st.download_button("Clique aqui para salvar o arquivo", data=f, file_name=os.
