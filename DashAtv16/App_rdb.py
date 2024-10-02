from streamlit import exception
import streamlit as st
import pandas as pd
import plotly.express as px


try:

    st.set_page_config(layout="wide")

    # Título Geral do Dashboard

    st.header(":blue[Imóveis para Alugar - Brasil]", divider="gray")
    #st.title('Imóveis para Alugar - Brasil')

    st.subheader(":gray[Aluno: Renato David Brito]")
    st.subheader(":gray[Matrícula: 20242001475]", divider="gray")
    # Importação e tratamento inicial dos dados

    dados = pd.read_csv("/home/renato/PycharmProjects/DashAtv16/Dados/houses_to_rent_v2.csv")

    # Traduzindo os títulos do dataframe

    dados_br = dados.rename(columns = {"city": "Cidade", "area": "Área do imóvel", "rooms": "Qtd Quartos", "bathroom": "Qtd Banheiros", "parking spaces": "Qtd Garagens", "floor": "Andar do Imóvel", "animal": "Permite Animais", "furniture": "Mobiliado", "hoa (R$)": "Taxa de Condomínio", "rent amount (R$)": "Valor do Aluguel (R$)", "property tax (R$)": "Valor do IPTU (R$)", "fire insurance (R$)": "Seguro contra Incêndio (R$)", "total (R$)": "Total (R$)" })

    # Traduzir os valores nas colunas "animal" e "furniture":

    dados_br["Permite Animais"] = dados_br["Permite Animais"].replace({"acept": "Sim", "not acept": "Não"})

    dados_br["Mobiliado"] = dados_br["Mobiliado"].replace({"furnished": "Sim", "not furnished": "Não"})

    # Criando faixas de valores de aluguel para segmentação dos dados no dashboard

    # Função para categorizar as faixas de preço do aluguel

    def categoria_aluguel(valor):
        if valor < 1000:
            return "até R$ 1000"
        elif 1000 <= valor <2000:
            return "Entre R$ 1000 e R$ 1999"
        elif 2000 <= valor <3000:
            return "Entre R$ 2000 e R$ 2999"
        elif 3000 <= valor <4000:
            return "Entre R$ 3000 e R$ 3999"
        elif 4000 <= valor <5000:
            return "Entre R$ 4000 e R$ 4999"
        elif 5000 <= valor:
            return "Acima de R$ 5000"
    # Aplicar a função à coluna de valor do aluguel

    dados_br["Faixas de Preço"] = dados_br["Valor do Aluguel (R$)"].apply(categoria_aluguel)

    # Incluindo barra lateral para filtragem

    with st.sidebar:

        st.write("Selecione as opções abaixo para visualizar:")

        cidade = st.multiselect("Cidade", options=dados_br["Cidade"].unique(), default=dados_br["Cidade"].unique())
        mobiliado = st.selectbox("Imóvel Mobiliado?", options=dados_br["Mobiliado"].unique())
        aceita_animais = st.selectbox("Aceita Animais?", options=dados_br["Permite Animais"].unique())
        faixa_preço = st.selectbox("Escolha a faixa de preços de aluguel",
                                                             options = ["até R$ 1000", "Entre R$ 1000 e R$ 1999", "Entre R$ 2000 e R$ 2999", "Entre R$ 3000 e R$ 3999", "Entre R$ 4000 e R$ 4999", "Acima de R$ 5000"])
        quartos = st.selectbox("Número de Quartos", options=sorted(dados_br["Qtd Quartos"].unique()))
        banheiros = st.selectbox("Número de Banheiros", options = sorted(dados_br["Qtd Banheiros"].unique()))

    # Filtrar os dados com base nas seleções

    dados_filtro = dados_br[
        (dados_br["Cidade"].isin(cidade)) &
        (dados_br["Mobiliado"] == (mobiliado)) &
        (dados_br["Permite Animais"] == (aceita_animais)) &
        (dados_br["Faixas de Preço"] == (faixa_preço)) &
        (dados_br["Qtd Quartos"] == (quartos)) &
        (dados_br["Qtd Banheiros"] == (banheiros))
    ]

    # Dividindo a tela

    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)

    # Segmentando o dataset para os gráficos

    # Quantidade de imóveis por cidade

    imoveis_qtd = dados_br.groupby("Cidade")["Cidade"].count() # dados estáticos, sem relação com os elementos de seleção
    imoveis_cidade = imoveis_qtd.sort_values(ascending=False) # dados estáticos, sem relação com os elementos de seleção

    imoveis_qtd_fil = dados_filtro.groupby("Cidade")["Cidade"].count() # dados filtrados pelos elementos de seleção
    imoveis_cidade_fil = imoveis_qtd_fil.sort_values(ascending=False) # dados filtrados pelos elementos de seleção


    fig_qtd = px.bar(imoveis_cidade, x = imoveis_cidade.index, y = imoveis_cidade.values, color="Cidade", text_auto=True, title= "Total de Imóveis Disponíveis por Cidade")
    # Removendo as linhas dos eixos
    fig_qtd.update_layout(
        xaxis=dict(showgrid=False),  # Remover a linha do eixo X
        yaxis=dict(showgrid=False)   # Remover a linha do eixo Y
    )
    # Removendo as linhas de grade
    fig_qtd.update_layout(
        #xaxis=dict(showticklabels=False),  # Remover a linha do eixo X
        yaxis=dict(showticklabels=False)   # Remover a linha do eixo Y
    )

    # Nomeando os eixos
    fig_qtd.update_layout(
        xaxis_title='Cidades',
        yaxis_title=None
    )

    # Gráfico com filtro de seleção para a quantidade de imóveis por cidade

    fig_qtd_fil = px.bar(imoveis_cidade_fil, x = imoveis_cidade_fil.index, y = imoveis_cidade_fil.values, color="Cidade", text_auto=True, title= "Total de Imóveis Disponíveis por Cidade (Filtrado)")
    # Removendo as linhas dos eixos
    fig_qtd_fil.update_layout(
        xaxis=dict(showgrid=False),  # Remover a linha do eixo X
        yaxis=dict(showgrid=False)   # Remover a linha do eixo Y
    )
    # Removendo as linhas de grade
    fig_qtd_fil.update_layout(
        #xaxis=dict(showticklabels=False),  # Remover a linha do eixo X
        yaxis=dict(showticklabels=False)   # Remover a linha do eixo Y
    )

    # Nomeando os eixos
    fig_qtd_fil.update_layout(
        xaxis_title='Cidades',
        yaxis_title=None
    )

    # Plotagem dos gráficos
    col1.plotly_chart(fig_qtd)
    col3.plotly_chart(fig_qtd_fil)

    # Valor médio do aluguel por cidade

    aluguel_cid = dados_br.groupby("Cidade")["Valor do Aluguel (R$)"].mean() # dados estáticos, sem relação com os elementos de seleção
    aluguel_medio = aluguel_cid.sort_values(ascending=False) # dados estáticos, sem relação com os elementos de seleção

    aluguel_cid_fil = dados_filtro.groupby("Cidade")["Valor do Aluguel (R$)"].mean() # dados filtrados pelos elementos de seleção
    aluguel_medio_fil = aluguel_cid_fil.sort_values(ascending=False) # dados filtrados pelos elementos de seleção


    fig_alu = px.bar(aluguel_medio, x = aluguel_medio.index, y = aluguel_medio.values, color="Valor do Aluguel (R$)", text_auto=True, title= "Valor médio do aluguel por Cidade - em R$")
    # Removendo as linhas dos eixos
    fig_alu.update_layout(
        xaxis=dict(showgrid=False),  # Remover a linha do eixo X
        yaxis=dict(showgrid=False)   # Remover a linha do eixo Y
    )
    # Removendo as linhas de grade
    fig_alu.update_layout(
        #xaxis=dict(showticklabels=False),  # Remover a linha do eixo X
        yaxis=dict(showticklabels=False)   # Remover a linha do eixo Y
    )

    # Nomeando os eixos
    fig_alu.update_layout(
        xaxis_title='Cidades',
        yaxis_title=None
    )

    # Gráfico com filtro de seleção para o valor médio do aluguel por cidade

    fig_alu_fil = px.bar(aluguel_medio_fil, x = aluguel_medio_fil.index, y = aluguel_medio_fil.values, color="Valor do Aluguel (R$)", text_auto=True, title= "Valor médio do aluguel por Cidade - em R$ (Filtrado)")
    # Removendo as linhas dos eixos
    fig_alu_fil.update_layout(
        xaxis=dict(showgrid=False),  # Remover a linha do eixo X
        yaxis=dict(showgrid=False)   # Remover a linha do eixo Y
    )
    # Removendo as linhas de grade
    fig_alu_fil.update_layout(
        #xaxis=dict(showticklabels=False),  # Remover a linha do eixo X
        yaxis=dict(showticklabels=False)   # Remover a linha do eixo Y
    )

    # Nomeando os eixos
    fig_alu_fil.update_layout(
        xaxis_title='Cidades',
        yaxis_title=None
    )

    # Plotagem dos gráficos
    col2.plotly_chart(fig_alu)
    col4.plotly_chart(fig_alu_fil)

    st.subheader(":blue[Base de dados filtrada]", divider="gray")
    #st.write(dados_filtro )
    st.dataframe(dados_filtro.style.highlight_max(axis=0))

except:
    st.error(
        'Seus critérios de filtro não retornaram nenhuma combinação válida na base de dados atual, por gentileza atualize a página e tente outras combinações.',
        icon="🚨")
