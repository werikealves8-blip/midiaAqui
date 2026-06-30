import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="Downloader", page_icon="⬇️")

st.title("⬇️ Downloader")

link = st.text_input("Cole o link do vídeo:")

if 'liberado' not in st.session_state:
    st.session_state.liberado = False

# Anúncio simples (apenas link para evitar erro de script no servidor)
if st.button("Clique para assistir anúncio e liberar"):
    st.markdown("[CLIQUE AQUI PARA ASSISTIR ANÚNCIO](https://google.com)") # Substitua pelo link do anúncio
    st.session_state.liberado = True
    st.rerun()

if st.session_state.liberado:
    if link:
        try:
            with st.spinner("Buscando informações..."):
                ydl_opts = {'format': 'best[ext=mp4]/best'}
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(link, download=False)
                    url_download = info['url']
                    st.success("Pronto!")
                    st.video(url_download)
                    st.write(f"Título: {info['title']}")
        except Exception as e:
            st.error("Erro ao processar: O YouTube bloqueou a requisição. Tente um link diferente.")
