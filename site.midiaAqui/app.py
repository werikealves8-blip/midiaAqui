import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="Downloader Pro", page_icon="⬇️")

st.title("⬇️ Downloader Pro")

link = st.text_input("Cole o link do vídeo aqui:")

if 'preparado' not in st.session_state: st.session_state.preparado = False
if 'anuncio_visto' not in st.session_state: st.session_state.anuncio_visto = False

if st.button("Preparar Download"):
    if link:
        st.session_state.preparado = True
    else:
        st.error("Cole um link válido.")

if st.session_state.preparado and not st.session_state.anuncio_visto:
    st.subheader("Escolha a qualidade:")
    qualidade = st.selectbox("Opções:", ["720p (MP4)", "1080p (MP4 - tenta o melhor disponível)", "Apenas Áudio (MP3)"])
    
    st.warning("⚠️ Assista ao anúncio para liberar o botão de download.")
    
    anuncio_html = """
    <div style="text-align: center; border: 1px solid #ccc; padding: 10px;">
        <script src="https://pl30146977.effectivecpmnetwork.com/68/ef/ed/68efedae0214a457f49cd05115af4be8.js"></script>
    </div>
    """
    st.components.v1.html(anuncio_html, height=250)
    
    if st.button("Já vi o anúncio, baixar agora!"):
        st.session_state.anuncio_visto = True
        st.session_state.qualidade_escolhida = qualidade
        st.rerun()

if st.session_state.anuncio_visto:
    st.success("✅ Download liberado!")
    
    if st.button("Iniciar Download"):
        try:
            pasta_temp = "downloads"
            os.makedirs(pasta_temp, exist_ok=True)
            
            # Função para atualizar a barra de progresso
            bar = st.progress(0)
            def progress_hook(d):
                if d['status'] == 'downloading':
                    try:
                        p = float(d['_percent_str'].replace('%',''))
                        bar.progress(p / 100)
                    except: pass
            
            q = st.session_state.qualidade_escolhida
            # Formatos que não precisam de FFmpeg
            if "MP3" in q: fmt = 'bestaudio/best'
            else: fmt = 'best[ext=mp4]/best'
            
            ydl_opts = {
                'outtmpl': f'{pasta_temp}/%(title)s.%(ext)s',
                'format': fmt,
                'progress_hooks': [progress_hook],
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(link, download=True)
                arquivo = ydl.prepare_filename(info)
                if "MP3" in q: 
                    arquivo = arquivo.replace(".webm", ".mp3").replace(".m4a", ".mp3")
            
            with open(arquivo, "rb") as f:
                st.download_button("Clique aqui para salvar o arquivo", data=f, file_name=os.path.basename(arquivo))
                
        except Exception as e:
            st.error(f"Erro: {e}. (Nota: Se o vídeo for 1080p+, o servidor pode não conseguir baixá-lo sem FFmpeg).")
