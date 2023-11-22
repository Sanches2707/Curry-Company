# Libraries
import streamlit as st
from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go
import re


# Bibliotecas necessárias
import folium
import pandas as pd
import numpy as np

from PIL import Image
from datetime import time
from datetime import datetime
from streamlit_folium import folium_static

# ----------------------------------------
# Funções 
# ----------------------------------------
def country_maps( df1 ):
    df_aux = ( df1.loc[: , ['City' , 'Road_traffic_density' , 'Delivery_location_latitude' , 'Delivery_location_longitude']]
                  .groupby(['City', 'Road_traffic_density'])
                  .median()
                  .reset_index() )                   
        
    map = folium.Map()
    for index, location_info in df_aux.iterrows() :
        folium.Marker( [location_info['Delivery_location_latitude'],
                         location_info['Delivery_location_longitude']],
                         popup=location_info[['City', 'Road_traffic_density']]).add_to(map)

    folium_static( map, width=1024 , height=600 )
    return None


def order_share_by_week( df1 ):
    df_aux01 = df1.loc[:, ['ID', 'week_of_year']].groupby('week_of_year').count().reset_index()
    df_aux02 = ( df1.loc[:, ['Delivery_person_ID', 'week_of_year']]
                    .groupby('week_of_year')
                    .nunique()
                    .reset_index() )
    
    df_aux = pd.merge( df_aux01, df_aux02, how='inner', on='week_of_year' )
    df_aux['order_by_deliver'] = df_aux['ID'] / df_aux['Delivery_person_ID']
        
    fig = px.line( df_aux, x='week_of_year', y='order_by_deliver' )
    
    return fig     


def order_by_week( df1 ):            
    # criar coluna de semana
    df1['week_of_year'] = df1['Order_Date'].dt.strftime( '%U' )
    df_aux =df1.loc[:,['ID', 'week_of_year']].groupby('week_of_year').count().reset_index()
    fig =px.line(df_aux, x='week_of_year', y='ID')

    return fig    


def traffic_order_city( df1 ):            
    df_aux = ( df1.loc[:, ['ID', 'City', 'Road_traffic_density']]
                  .groupby(['City', 'Road_traffic_density'])
                  .count()
                  .reset_index() )

    fig = px.scatter( df_aux, x= 'City' , y= 'Road_traffic_density', size='ID')
    # cod dele =fig = px.scatter( df_aux, x= 'City', y='Road_traffic_density', size='ID', color='City' )
                
    return fig 


def traffic_order_share( df1 ):            
    df_aux = ( df1.loc[:, ['ID', 'Road_traffic_density']]
                  .groupby('Road_traffic_density')
                  .count()
                  .reset_index() )
    df_aux =df_aux.loc[df_aux['Road_traffic_density'] != "NaN", :]
    df_aux['entregas_perc'] = df_aux['ID'] / df_aux['ID'].sum()

    fig = px.pie(df_aux, values= 'entregas_perc', names= 'Road_traffic_density')

    return fig



def order_metric( df1 ):
    # Order metric
    cols = ['ID', 'Order_Date']
    # Seleção de linhas
    df_aux = df1.loc[:, cols].groupby('Order_Date').count().reset_index()
       
    # Desenhar o gráfico de linha    
    fig = px.bar(df_aux, x= 'Order_Date', y= 'ID')

    return fig 


# 1. Limpeza do Dataframe

def clean_code( df1 ):

    # o comando !=, significa diferente
    linhas_selecionadas = (df1['Delivery_person_Age'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas ,:].copy()

    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype(int)


    # 2. convertendo a coluna Ratings de texto para número decimal (float), pois ela está como (object) texto  == string
    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype(float)

    # 3. Convertendo a coluna order_date de texto para data
    df1['Order_Date'] =pd.to_datetime(df1['Order_Date'], format='%d-%m-%Y')


    # 4. convertendo a coluna multiple_deliveries de texto para número inteiro (int)
    linhas_selecionadas = (df1['multiple_deliveries'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas,:].copy()
    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype(int)


    df1.loc[:, 'ID'] = df1.loc[:,'ID'].str.strip()
    df1.loc[:, 'Road_traffic_density'] = df1.loc[:,'Road_traffic_density'].str.strip()
    df1.loc[:, 'Type_of_order'] = df1.loc[:,'Type_of_order'].str.strip()
    df1.loc[:, 'Type_of_vehicle'] = df1.loc[:,'Type_of_vehicle'].str.strip()
    df1.loc[:, 'City'] = df1.loc[:,'City'].str.strip()
    df1.loc[:, 'Festival'] = df1.loc[:,'Festival'].str.strip()


    # Excluir as linhas com a idade dos entregadores vazia
    # ( Conceito de seleção condicional )
    linhas_vazia = df1['Delivery_person_Age'] != 'NaN '
    df1 = df1.loc[linhas_vazia, :]

    # Conversão de texto/categoria/string para números inteiros
    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype(int)

    # Conversão de texto/categoria/string para números decimais
    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype( float )

    # Conversão de texto para data
    df1['Order_Date'] = pd.to_datetime( df1['Order_Date'], format='%d-%m-%Y' )

    # Remove as linhas da coluna multiple_deliveries que tenham o
    # conteúdo igual a 'NaN '
    linhas_vazia = df1['multiple_deliveries'] != 'NaN '
    df1 = df1.loc[linhas_vazia, :]
    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype( int)

    # Comando para remover o texto de números
    df1 = df1.reset_index(drop=True )
    for i in range( len( df1 ) ):
        df1.loc[i, 'Time_taken(min)'] = re.findall( r'\d+' , df.loc[i,'Time_taken(min)'])

    return df1

#---------------------------Início da Estrutura lógica do código ---------------------

# Import dataset
# --------------------------
df = pd.read_csv ('arquivo train/train.csv')

# Limpando os dados
# ----------------------------
df1 = clean_code( df )

# ==========================================
# Barra lateral
# ==========================================
st.header( 'Marketplace - Visão Cliente' )

image_path = 'Logo.png'
image= Image.open( image_path )
st.sidebar.image( image, width=120 )


st.sidebar.markdown( '# Cury Company ' )
st.sidebar.markdown( '## Fastest Delivery in Town')
st.sidebar.markdown( """___""")

st.sidebar.markdown( '## Selecione uma data limite')

date_slider = st.sidebar.slider(
    'Até qual o valor?',
    value =datetime( 2022, 4, 13 ),
    min_value=datetime( 2022, 2, 11 ),
    max_value=datetime( 2022, 4, 6 ),
    format='DD-MM-YYYY' )

st.sidebar.markdown( """___""")


traffic_options = st.sidebar.multiselect(
    'Quai as condições do trânsito',
    ['Low', 'Medium', 'High', 'Jam'],
    default=['Low', 'Medium', 'High', 'Jam'] )

st.sidebar.markdown( """___""")
st.sidebar.markdown( '### Powered by Comunidade DS')


linhas_selecionadas = df1['Order_Date'] < date_slider
df1 =df1.loc[linhas_selecionadas, :]

#st.dataframe( df1 )

# ==========================================
# Layout no Streamlit
# ==========================================
tab1, tab2, tab3 = st.tabs( ['Visão Gerencial', 'Visão Tática', 'Visão Geográfica'] )

with tab1:
    with st.container():
        # Order metric
        st.markdown( '# Orders by Day' )
        fig = order_metric( df1 )
        st.plotly_chart( fig, use_container_width=True )     


    with st.container():   
        col1, col2 = st.columns( 2 )

        with col1:
            st.header( "Traffic Order Share" )
            fig = traffic_order_share( df1 )            
            st.plotly_chart( fig, use_container_width=True)          
           

        with col2:
            st.header( "Traffic Order City" )          
            fig = traffic_order_city( df1 )                     
            st.plotly_chart( fig, use_container_width=True)
        
                   
with tab2:
    with st.container():
        st.markdown( "## Order by Week " )
        fig = order_by_week( df1 )
        st.plotly_chart( fig, user_container_width=True )


 
    with st.container():
        st.markdown( "## Order Share by Week" )
        fig = order_share_by_week( df1 )
        st.plotly_chart( fig, use_container_width=True )

       
        
with tab3:
    st.markdown( "# Country Maps")
    country_maps( df1 )











