import streamlit as st 
from PIL import Image 
from haversine import haversine
import haversine

st.set_page_config(
    page_title='Home',

)  
  
image = Image.open( 'Logo.png')
st.sidebar.image( image, width=120 )

st.sidebar.markdown( '### Cury Company ')
st.sidebar.markdown( '## Fastest Delivery in Town')
st.sidebar.markdown( """___""")

st.write( '# Curry Company Growth Dashboard')

st.markdown(
    """
    Growth Dashboard foi construído para acompanhar as métricas de crescimento dos Entregadores e Restaurantes.
    ### Como utilizar esse Growth Dashboard? 
    - Visão Empresa:
        - Visão Gerencial: Métricas gerais de comportamento.
        - Visão Geográfica: Insights de geolocalização.
    - Visão Entregador:
        - Acompanhamento dos indicadores semanais de crescimento.
    - Visão Restaurantes: 
        - Indicadore semanais de crescimento dos restaurantes.
    ### ask for Help
    - Time de Data Science no Discord
    - @rsds2707
""" )
         
    
    


