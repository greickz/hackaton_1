import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu

st.set_page_config(page_title='Dashboard Alimentícia Operacional', page_icon='', layout='wide')

df_equipamentos = pd.read_excel('equipamentos_tratado.xlsx')
df_materiais = pd.read_excel('materiais.xlsx')
df_uso_equipamentos = pd.read_excel('uso_equipamentos_tratado.xlsx')

st.sidebar.header('Selecione os Filtros')

setor = st.sidebar.multiselect(
    'Setores',
    options=df_equipamentos['Setor'].unique(),
    default=df_equipamentos['Setor'].unique()
)

status = st.sidebar.multiselect(
    'Status Atual',
    options=df_equipamentos['Status_atual'].unique(),
    default=df_equipamentos['Status_atual'].unique()
)

df_filtrado = df_equipamentos.query('Setor in @setor and Status_atual in @status')

df_corretiva = df_filtrado[
    (df_filtrado['Tipo_manutencao'] == 'Corretiva') &
    (df_filtrado['Tempo_parado_dias'] > 9.1)
]

def Graficos():
    st.title('Custo e Tempo de Manutenção Corretiva')

    fig_tempo = px.bar(
        df_corretiva,
        x='Id_equipamento',
        y='Tempo_parado_dias',
        color='Setor',
        color_discrete_sequence=px.colors.qualitative.Set2,
        title='⏱ Tempo Parado (>9 dias) - Manutenção Corretiva',
        labels={'Tempo_parado_dias': 'Dias Parado', 'Id_equipamento': 'Equipamento'}
    )
    fig_tempo.update_layout(
        xaxis_title='ID do Equipamento',
        yaxis_title='Tempo Parado (dias)',
        barmode='stack',
        xaxis={'categoryorder': 'total ascending'},
        margin=dict(t=50, b=30)
    )

    fig_custo = px.bar(
        df_corretiva,
        x='Id_equipamento',
        y='Custo_manutencao',
        color='Setor',
        color_discrete_sequence=px.colors.qualitative.Pastel,
        title='💸 Custo da Manutenção Corretiva',
        labels={'Custo_manutencao': 'R$', 'Id_equipamento': 'Equipamento'}
    )
    fig_custo.update_layout(
        xaxis_title='ID do Equipamento',
        yaxis_title='Custo da Manutenção (R$)',
        barmode='stack',
        xaxis={'categoryorder': 'total ascending'},
        margin=dict(t=50, b=30)
    )

    st.plotly_chart(fig_tempo, use_container_width=True)
    st.plotly_chart(fig_custo, use_container_width=True)

def sideBar():
    with st.sidebar:
        selecionado = option_menu(
            menu_title='Menu',
            options=['Gráficos'],
            icons=['bar-chart'],
            default_index=0
        )
    if selecionado == 'Gráficos':
        Graficos()

sideBar()
