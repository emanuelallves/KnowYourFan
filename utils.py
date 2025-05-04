import os
import pandas as pd
from PIL import Image
import pytesseract
import streamlit as st
from datetime import date
import snscrape.modules.twitter as sntwitter

def coletar_dados_formulario():
    st.subheader("Dados pessoais")
    nome = st.text_input("Nome completo")
    cpf = st.text_input("CPF")
    endereco = st.text_input("Endereço completo")

    st.subheader("Seus interesses em e-sports")
    jogos = st.multiselect(
        "Quais jogos você acompanha ou joga?",
        ["CS", "Valorant", "League of Legends", "Outro"]
    )
    times = st.text_input("Times favoritos de e-sports")

    st.subheader("Participação em eventos e atividades")
    eventos = st.text_area("Liste eventos de e-sports que participou no último ano (presencial ou online)")
    streams = st.text_input("Canais/Streamers que costuma assistir")

    st.subheader("Compras relacionadas a e-sports")
    compras = st.text_area("Produtos comprados relacionados a e-sports")

    data_submissao = date.today()

    return {
        "Nome": nome,
        "CPF": cpf,
        "Endereço": endereco,
        "Jogos": ", ".join(jogos),
        "Times": times,
        "Eventos": eventos,
        "Streams": streams,
        "Compras": compras,
        "Data de Submissão": data_submissao
    }

def salvar_dados_csv(dados, caminho_csv="./dados_fan.csv"):
    df = pd.DataFrame([dados])
    if os.path.exists(caminho_csv):
        df.to_csv(caminho_csv, mode="a", header=False, index=False)
    else:
        df.to_csv(caminho_csv, index=False)

def validar_documento(uploaded_file, nome, cpf):
    image = Image.open(uploaded_file)
    st.image(image, caption="Documento enviado", use_column_width=True)
    st.info("Extraindo informações com OCR...")

    text = pytesseract.image_to_string(image, lang="por")
    st.text_area("Texto extraído do documento:", text, height=200)

    nome_validado = nome.lower() in text.lower()
    cpf_validado = cpf.replace(".", "").replace("-", "") in text.replace(".", "").replace("-", "")

    if nome_validado and cpf_validado:
        st.success("Documento validado com sucesso: nome e CPF conferem!")
    else:
        st.error("Validação falhou: nome ou CPF não encontrados no documento.")

def analisar_perfil_twitter(twitter_url):
    try:
        username = twitter_url.strip("/").split("/")[-1]

        tweets = []
        for i, tweet in enumerate(sntwitter.TwitterUserScraper(username).get_items()):
            try:
                tweets.append(tweet.content)
            except Exception:
                continue
            if i >= 50:
                break

        if not tweets:
            return {
                "sucesso": False,
                "mensagem": "Nenhum tweet encontrado.",
                "relacao_esports": False,
                "amostra": []
            }

        # Termos de e-sports
        esports_terms = [
            "furia", "csgo", "valorant", "league of legends", "esports",
            "cblol", "major", "stream", "gamer", "fnatic", "riot", "twitch"
        ]
        tweets_text = " ".join(tweets).lower()
        relacao_esports = any(term in tweets_text for term in esports_terms)

        return {
            "sucesso": True,
            "relacao_esports": relacao_esports,
            "mensagem": "Análise concluída.",
            "amostra": tweets[:5],
            "total_coletado": len(tweets)
        }

    except Exception as e:
        return {
            "sucesso": False,
            "mensagem": f"Erro ao analisar Twitter: {e}",
            "relacao_esports": False,
            "amostra": []
        }