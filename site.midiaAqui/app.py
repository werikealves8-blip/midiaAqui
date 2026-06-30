import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="Downloader Pro", page_icon="⬇️")

# Inicializa o estado do anúncio
if 'anuncio_visto' not in st.session_state:
    st.session_state.anuncio_visto = False

st.title("⬇️ Downloader Pro")

link = st.text_input("Cole o link do vídeo aqui:")

# Lógica de estados
if not st.session_state.anuncio_visto:
    st.warning("⚠️ Você precisa ver o anúncio para liberar o download.")
    
    # Botão que "abre" o anúncio
    if st.button("Assistir anúncio para liberar download"):
        # Aqui injetamos o HTML do anúncio
        anuncio_html = """
        <div style="padding: 20px; border: 2px solid #ff4b4b; border-radius: 10px; text-align: center;">
            <p>Assista ao anúncio abaixo e feche-o para continuar:</p>
            <script src="https://pl30146977.effectivecpmnetwork.com/68/ef/ed/68efedae0214a457f49cd05115af4be8.js"></script>
        </div>
        """
        st.components.v1.html(anuncio_html, height=400)
        
        # Botão para o usuário confirmar que terminou
        if st.button("Já assisti, liberar download!"):
            st.session_state.anuncio_visto = True
            st.rerun() # Atualiza a página para mostrar o botão de baixar
else:
    st.success("✅ Anúncio verificado! O download está liberado.")
    if st.button("Baixar Vídeo Agora"):
        if not link:
            st.error("Cole um link válido.")
        else:
            try:
                with st.spinner('Baixando...'):
                    pasta_temp = "downloads"
                    os.makedirs(pasta_temp, exist_ok=True)
                    
                    ydl_opts = {
                        'outtmpl': f'{pasta_temp}/%(title)s.%(ext)s',
                        'format': 'best[ext=mp4]/best',
                    }
                    
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(link, download=True)
                        arquivo = ydl.prepare_filename(info)
                    
                    with open(arquivo, "rb") as f:
                        st.download_button("Clique aqui para salvar o vídeo", data=f, file_name=os.path.basename(arquivo))
            except Exception as e:
                st.error(f"Erro no download: {e}")