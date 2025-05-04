import streamlit as st
from utils import (
    coletar_dados_formulario,
    salvar_dados_csv,
    validar_documento,
    analisar_perfil_twitter
)
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

st.set_page_config(page_title="Know Your Fan", layout="centered")
st.title("Know Your Fan")
st.markdown("Preencha o formulário abaixo com seus dados como fã de e-sports:")

dados = coletar_dados_formulario()

if st.button("Enviar"):
    salvar_dados_csv(dados)
    st.success("Dados enviados com sucesso!")

st.subheader("Validação de Documento com IA")
uploaded_file = st.file_uploader("Faça upload do seu documento (imagem JPG/PNG)", type=["jpg", "jpeg", "png"])
if uploaded_file:
    validar_documento(uploaded_file, dados["Nome"], dados["CPF"])

st.subheader("Redes Sociais")

twitter_url = st.text_input("Link do seu perfil no Twitter")

if twitter_url:
    st.info("Analisando perfil do Twitter...")

    resultado = analisar_perfil_twitter(twitter_url)

    if resultado["sucesso"]:
        st.success(f"Foram coletados {resultado['total_coletado']} tweets.")
        if resultado["relacao_esports"]:
            st.success("Atividade relevante de e-sports detectada no perfil!")
        else:
            st.warning("Nenhuma atividade clara de e-sports detectada nos tweets recentes.")

        st.markdown("**Amostra de tweets:**")
        for t in resultado["amostra"]:
            st.markdown(f"- {t}")
    else:
        st.error(resultado["mensagem"])