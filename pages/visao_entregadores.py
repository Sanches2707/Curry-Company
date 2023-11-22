# Libraries
import streamlit as st
from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go
import re

from datetime import time

from datetime import datetime

# Bibliotecas necessárias
import pandas as pd
from PIL import Image
import folium
from streamlit_folium import folium_static

# ----------------------------------------
# Funções 
# ----------------------------------------
def top_delivers( df1, top_asc ):            
    df2 = ( df1.loc[:, ['Delivery_person_ID', 'City', 'Time_taken(min)']]
               .groupby( [ 'City','Delivery_person_ID'] )
               .max().sort_values( ['City', 'Time_taken(min)'], ascending=top_asc ).reset_index() )

    df_aux01 = df2.loc[df2['City'] == 'Metropolitian', :].head(10)
    df_aux02 = df2.loc[df2['City'] == 'Urban', :].head(10)
    df_aux03 = df2.loc[df2['City'] == 'Semi-Urban', :].head(10)

    df3 = pd.concat( [df_aux01, df_aux02, df_aux03] ).reset_index( drop=True )

    return df3


# 1. Limpeza do Dataframe

def clean_code( df1 ):
    # 1. convertendo a coluna Age de texto para número
    linhas_selecionadas = (df1['Delivery_person_Age'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas ,:].copy()

    linhas_selecionadas = (df1['Road_traffic_density'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas ,:].copy()

    linhas_selecionadas = (df1['City'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas ,:].copy()

    linhas_selecionadas = (df1['Festival'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas ,:].copy()

    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype(int)
    df1.shape

    # 2. convertendo a coluna Ratings de texto para número decimal (float), pois ela está como (object) texto  == string
    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype(float)

    # 3. Convertendo a coluna order_date de texto para data
    df1['Order_Date'] =pd.to_datetime(df1['Order_Date'], format='%d-%m-%Y')

    # 4. convertendo a coluna multiple_deliveries de texto para número inteiro (int)
    linhas_selecionadas = (df1['multiple_deliveries'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas,:].copy()
    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype(int)

    # 5. Removendo os espaços dentro de strings/texto/object
    #df1 = df1.reset_index( drop=True )
    #for i in range(len(df1)) :
    #df1.loc[i, 'ID'] = df1.loc[i, 'ID'].strip()
    #df1.loc[i, 'Delivery_person_ID'] = df1.loc[i, 'ID'].strip()

    # 6. Removendo os espaços dentro de strings/text/object

    df1.loc[:, 'ID'] = df1.loc[:,'ID'].str.strip()
    df1.loc[:, 'Road_traffic_density'] = df1.loc[:,'Road_traffic_density'].str.strip()
    df1.loc[:, 'Type_of_order'] = df1.loc[:,'Type_of_order'].str.strip()
    df1.loc[:, 'Type_of_vehicle'] = df1.loc[:,'Type_of_vehicle'].str.strip()
    df1.loc[:, 'City'] = df1.loc[:,'City'].str.strip()
    df1.loc[:, 'Festival'] = df1.loc[:,'Festival'].str.strip()

    # 7. Limpando a coluna de Time_Taken

    df1['Time_taken(min)'] = df1['Time_taken(min)'].apply( lambda x: x.split( '(min) ') [1] )
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype( int )

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
st.header(' Marketplace - Visão Entregadores')

image_path = 'Logo.png'
image= Image.open( image_path )
st.sidebar.image( image, width=120 )



st.sidebar.markdown( '### Cury Company ')
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

# Filtro de data
linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas, :]

# Filtro de trânsito
linhas_selecionadas = df1['Road_traffic_density'].isin( traffic_options )
df1 = df1.loc[linhas_selecionadas, :]


# ==========================================
# Layout no Streamlit
# ==========================================
tab1, tab2, tab3 = st.tabs( ['Visão Gerencial', '_', '_'] )

with tab1:
    with st.container():
        st.title( 'Overall Metrics' ) 

        col1, col2, col3, col4 = st.columns( 4, gap='large' )
        with col1:
            
            # A maior idade dos entregadores
            maior_idade =  df1.loc[:, 'Delivery_person_Age'].max() 
            col1.metric( 'Maior de idade', maior_idade )
            

        with col2:
            
            # A menor idade dos entregadores
            menor_idade = df1.loc[:, 'Delivery_person_Age'].min() 
            col2.metric( 'Menor de Idade', menor_idade )

        with col3:
            # A maior idade dos entregadores
            
            melhor_condicao = df1.loc[:, 'Vehicle_condition'].max()
            col3.metric( 'Melhor condição', melhor_condicao ) 

        with col4:
            # A menor idade dos entregadores
            
            pior_condicao = df1.loc[:, 'Vehicle_condition'].min()
            col4.metric( 'Pior condição', pior_condicao ) 

    with st.container():
        st.markdown( """___""" )  
        st.title( 'Avaliações' ) 

        col1, col2 = st.columns( 2 )
        with col1:
            st.markdown( '##### Avaliação médias por Entregador' ) 
            df_avg = ( df1.loc[: , [ 'Delivery_person_ID', 'Delivery_person_Ratings']]
                          .groupby('Delivery_person_ID')
                          .mean()
                          .reset_index() )
            st.dataframe( df_avg )
              

        with col2:
            st.markdown( '##### Avaliação médias por trânsito')
            df_avg_std_rating_by_traffic = ( df1.loc[:, ['Delivery_person_Ratings', 'Road_traffic_density']]
                                                .groupby('Road_traffic_density')
                                                .agg( {'Delivery_person_Ratings' : ['mean' , 'std']} ) )

            # mudança de nome das colunas
            df_avg_std_rating_by_traffic.columns = ['Delivery_mean', 'Delivery_std']

            # reset di index
            df_avg_std_rating_by_traffic =df_avg_std_rating_by_traffic.reset_index()
            st.dataframe( df_avg_std_rating_by_traffic )



            st.markdown( '##### Avaliação média por clima') 
            df_avg_std_rating_by_weather = ( df1.loc[:, ['Delivery_person_Ratings', 'Weatherconditions']]
                                                .groupby('Weatherconditions')
                                                .agg( {'Delivery_person_Ratings' : ['mean' , 'std']} ) )

            # mudança de nome das colunas
            df_avg_std_rating_by_weather.columns = ['Delivery_mean', 'Delivery_std']

            # reset di index
            df_avg_std_rating_by_weather =df_avg_std_rating_by_weather.reset_index()
            st.dataframe( df_avg_std_rating_by_weather )



    with st.container():     
        st.markdown( """___""" ) 
        st.title( 'Velocidade de Entrega' ) 

        col1, col2, = st.columns ( 2 )  

        with col1:
            st.markdown( '##### Top Entregadores mais rápidos' )
            df3 = top_delivers( df1, top_asc=True )
            st.dataframe( df3 )

        with col2:
            st.markdown( '##### Top Entregadores mais lentos' )
            df3 = top_delivers( df1, top_asc=False )
            st.dataframe( df3 )
            
            
            
            
          
            
            

    


