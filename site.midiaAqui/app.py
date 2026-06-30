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
        st.error("Por favor, cole um link válido.")

if st.session_state.preparado and not st.session_state.anuncio_visto:
    st.subheader("Escolha a qualidade:")
    qualidade = st.selectbox("Qualidade", ["720p (MP4)", "1080p (MP4)", "Apenas Áudio (MP3)"])
    
    st.warning("⚠️ Clique no anúncio abaixo para liberar o botão de download.")
    
    # Anúncio fixo (sem forçar redirecionamento)
    anuncio_html = """
    <div style="text-align: center; border: 1px solid #ccc; padding: 10px;">
        <script src="https://pl30146977.effectivecpmnetwork.com/68/ef/ed/68efedae0214a457f49cd05115af4be8.js"></script>
    </div>
    """
    st.components.v1.html(anuncio_html, height=250)
    
    if st.button("Já interagi com o anúncio, baixar agora!"):
        st.session_state.anuncio_visto = True
        st.session_state.qualidade_escolhida = qualidade
        st.rerun()

if st.session_state.anuncio_visto:
    st.success("✅ Download liberado!")
    if st.button("Baixar arquivo"):
        try:
            with st.spinner('Processando arquivo...'):
                pasta_temp = "downloads"
                os.makedirs(pasta_temp, exist_ok=True)
                
                # Configurações de qualidade
                q = st.session_state.qualidade_escolhida
                if "720p" in q: fmt = 'bestvideo[height<=720]+bestaudio/best[height<=720]'
                elif "1080p" in q: fmt = 'bestvideo[height<=1080]+bestaudio/best[height<=1080]'
                else: fmt = 'bestaudio/best'
                
                ydl_opts = {'outtmpl': f'{pasta_temp}/%(title)s.%(ext)s', 'format': fmt}
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(link, download=True)
                    arquivo = ydl.prepare_filename(info)
                    if "MP3" in q: arquivo = arquivo.replace(".webm", ".mp3").replace(".m4a", ".mp3")
                
                with open(arquivo, "rb") as f:
                    st.download_button("Clique aqui para salvar", data=f, file_name=os.path.basename(arquivo))
        except Exception as e:
            st.error(f"Erro: {e}")
