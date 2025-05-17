import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components
from streamlit_option_menu import option_menu



st.set_page_config(page_title='Dashboard Alimenticia Operacional', page_icon='', layout='wide')

df_equipamentos = pd.read_excel('equipamentos_tratado.xlsx')
df_materiais = pd.read_excel('materiais.xlsx')
df_uso_equipamentos = pd.read_excel('uso_equipamentos_tratado.xlsx')

st.sidebar.header('Selecione os Filtros')

# filtros

setor = st.sidebar.multiselect(
    'setores',
    options = df_equipamentos['Setor'].unique(),
    default = df_equipamentos['Setor'].unique(),
    key = 'setor'
)

status = st.sidebar.multiselect(
    'status_atual',
    options = df_equipamentos['Status_atual'].unique(),
    default = df_equipamentos['Status_atual'].unique(),
    key = 'status'
)

df_selecao = df_equipamentos.query('Setor in @setor and Status_atual in @status_atual')
# df_selecao['Tempo_parado_dias'][(df_equipamentos['Tempo_parado_dias'] > 9.1) & (df_equipamentos['Tipo_manutencao'] == 'Corretiva')]
# df_selecao['Custo_manutencao'][(df_equipamentos['Tempo_parado_dias'] > 9.1) & (df_equipamentos['Tipo_manutencao'] == 'Corretiva')]

def Graficos():
    barras_tempo_parado = px.bar(
        df_selecao['Tempo_parado_dias'][(df_equipamentos['Tempo_parado_dias'] > 9.1) & (df_equipamentos['Tipo_manutencao'] == 'Corretiva')],
        x='Id_equipamento',
        y='Tempo_parado_dias',
        color='Setor',
        barmode= 'group',
        title='Tempo parado das máquinas em manutenção corretiva'
    )
    
    barras_custo_manutancao_corretiva = px.bar(
        df_selecao,
        x = 'Máquinas (ID)',
        y= 'Custo de manutenção (R$)',
        color='Setor',
        barmode= 'group',
        title='Custo das máquinas em manutenção corretiva',
    )

    st.plotly_chart(barras_tempo_parado, use_container_widht=True)
    st.plotly_chart(barras_custo_manutancao_corretiva, use_container_widht=True)


def sideBar():
    with st.sidebar: 
        selecionado = option_menu(
            menu_title= 'Menu',
            options=['Home', 'Gráficos'],
            icons=['🏠', '⚙️'],
            default_index= 0 
        )
        
        Graficos()
    if selecionado == 'Gráficos': 
        Graficos()

sideBar()