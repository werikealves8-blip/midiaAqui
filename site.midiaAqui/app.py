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
    qualidade = st.selectbox("Opções:", ["Qualidade Média (360p)", "Qualidade Alta (720p)", "Apenas Áudio (MP3)"])
    
    st.warning("⚠️ Você precisa clicar no banner abaixo para liberar o download.")
    
    # Anúncio como link clicável para evitar redirecionamento forçado
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
                
                # Mapeamento de formatos sem FFmpeg
                if "MP3" in q:
                    fmt = 'bestaudio/best'
                elif "Alta" in q:
                    fmt = 'best[height<=720][ext=mp4]/best[ext=mp4]'
                else: # Média
                    fmt = 'best[height<=360][ext=mp4]/best[ext=mp4]'
                
                ydl_opts = {
                    'outtmpl': f'{pasta_temp}/%(title)s.%(ext)s',
                    'format': fmt,
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(link, download=True)
                    arquivo = ydl.prepare_filename(info)
                    if "MP3" in q: 
                        arquivo = arquivo.replace(".webm", ".mp3").replace(".m4a", ".mp3")
                
                with open(arquivo, "rb") as f:
                    st.download_button("Clique aqui para salvar o arquivo", data=f, file_name=os.path.basename(arquivo))
        except Exception as e:
            st.error(f"Erro no download: {e}. Tente outro link ou qualidade.")
