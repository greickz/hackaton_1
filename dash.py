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

df_selecao = df_equipamentos.query('Setor in @setor and Status_atual in @status')
# df_selecao['Tempo_parado_dias'][(df_equipamentos['Tempo_parado_dias'] > 9.1) & (df_equipamentos['Tipo_manutencao'] == 'Corretiva')]
# df_selecao['Custo_manutencao'][(df_equipamentos['Tempo_parado_dias'] > 9.1) & (df_equipamentos['Tipo_manutencao'] == 'Corretiva')]

def Graficos():
    st.title('Custo e Tempo de Manutenção de Máquinas em Manutenção Corretiva')
    
    df_selecao['nova'] = df_selecao['Tempo_parado_dias'][(df_equipamentos['Tempo_parado_dias'] > 9.1) & (df_equipamentos['Tipo_manutencao'] == 'Corretiva')]
    
    
    barras_tempo_parado = px.bar(
        df_selecao,
        x='Id_equipamento',
        y='Tempo_parado_dias',
        color='Setor',
        barmode= 'group',
        title='Tempo parado das máquinas em manutenção corretiva'
    )
    
    barras_custo_manutancao_corretiva = px.bar(
        df_selecao,
        x = 'Id_equipamento',
        y= 'Custo_manutencao',
        color='Setor',
        barmode= 'group',
        title='Custo das máquinas em manutenção corretiva',
    )
    
    barras_tempo_parado.update_layout(barmode='stack', xaxis={'categoryorder': 'total descending'})

    st.plotly_chart(barras_tempo_parado, use_container_widht=True)
    st.plotly_chart(barras_custo_manutancao_corretiva, use_container_widht=True)


def sideBar():
    with st.sidebar: 
        selecionado = option_menu(
            menu_title= 'Menu',
            options=['Gráficos'],
            icons=['🏠', '⚙️'],
            default_index= 0 
        )
        
    if selecionado == 'Gráficos': 
        Graficos()

sideBar()