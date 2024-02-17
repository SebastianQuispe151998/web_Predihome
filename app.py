from sys import stderr

from flask import Flask, render_template, request
import pickle
import numpy as np

import streamlit as st
import pandas as pd 
import streamlit.components.v1 as stc
import time 
from streamlit_option_menu import option_menu
import plotly.express as px

import webbrowser
import streamlit as st
from UI import *
import os

#configuramos el title de nuestra pagina
st.set_page_config(page_title="Análisis de Viviendas", page_icon="🧱", layout="wide")  

selected = option_menu(
    menu_title=None,
    options=["Inicio","Compra","Alquiler","Mapa"],
    icons=['house','book','book','map'],
    default_index=0,
    orientation="horizontal",
    styles={
                "container": {"padding": "0!important", "background-color": "#fafafa"},
                "icon": {"color": "black", "font-size": "20px"},
                "nav-link": {
                    "font-size": "25px",
                    "text-align": "left",
                    "margin": "2px",
                    "--hover-color": "#eee",
                },
                "nav-link-selected": {"background-color": "grey"},
            },
)


st.title("Análisis de Viviendas en Madrid")

theme_plotly = None

df = pd.read_csv(f"C:/UE/PROYECTO/flask_web_pisos/data/viviendas_web.csv",sep=",",header=0)



logo_path= "static/images/logo.png"
st.sidebar.image(logo_path, width=250)

df_vivienda_unique = df['Tipo_vivienda'].unique()
df_habitaciones_unique = df['Habitaciones'].sort_values(ascending=True).unique()
df_banos_unique = df['Baños'].sort_values(ascending=True).unique()
df_municipios_unique = df['Municipio'].unique()

st.sidebar.header("Por favor filtre aquí:")

Tipo_vivienda = st.sidebar.multiselect('Tipo de vivienda:',df_vivienda_unique,default=df_vivienda_unique)
Municipio = st.sidebar.multiselect('Municipio:',df_municipios_unique,default=None)
Habitaciones = st.sidebar.selectbox('Habitaciones',df_habitaciones_unique)
Baños = st.sidebar.selectbox('Baños',df_banos_unique)


df_selection = df.query(
    "Tipo_vivienda == @Tipo_vivienda & Municipio == @Municipio & Habitaciones == @Habitaciones"
)

#Declaracion de funciones

#Funcion Home Page
def HomePage():
    #1. print dataframe
    with st.expander("💵 Mi database de Viviendas en Madrid 🏠"):
#st.dataframe(df_selection,use_container_width=True)
        shwdata = st.multiselect('Filtro :', df_selection.columns, default=["Tipo_vivienda","Municipio", "Habitaciones","Baños"])
        st.dataframe(df_selection[shwdata],use_container_width=True)

def Graphs():
    total_habitantes = int(df_selection["Habitantes (2022)"].sum())
    average_rating = round(df_selection["Rating"].mean(), 1)
    #star_rating = ":star:" * int(round(average_rating, 0))
    average_habitantes = round(df_selection["Habitantes (2022)"].mean(), 2)

    Habitantes_by_businessType = (
    df_selection.groupby(by=["Tipo_vivienda"]).count()[["Habitantes (2022)"]].sort_values(by="Habitantes (2022)")
    )
    fig_Habitantes = px.bar(
        Habitantes_by_businessType,
        x="Habitantes (2022)",
        y=Habitantes_by_businessType.index,
        orientation="h",
        title="Habitantes (2022) por Tipo_vivienda",
        color_discrete_sequence=["#0083B8"] * len(Habitantes_by_businessType),
        template="plotly_white",
    )

    fig_Habitantes.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False))
    )

def ProgressBar():
    st.markdown("""<style>.stProgress > div > div > div > div { background-image: linear-gradient(to right, #99ff99 , #FFFF00)}</style>""",unsafe_allow_html=True,)
    target=30000000000
    current=df_selection["Habitantes (2022)"].sum()
    percent=round((current/target*100))
    my_bar = st.progress(0)

    if percent>100:
        st.subheader("Target 100 complited")
    else:
        st.write("you have ", percent, " % " ," of ", (format(target, ',d')), " TZS")
    for percent_complete in range(percent):
        time.sleep(0.1)
        my_bar.progress(percent_complete + 1,text="Target percentage")

def sideBar():
    with st.sidebar:
        selected=option_menu(
        menu_title="Menu",
        options=["Home","Progress"],
        icons=["house","eye"],
        menu_icon="cast", #option
        default_index=0, #option
        )


#Funcion Mapa
def abrir_mapa():
    st.markdown("""
    <h1 style='
        text-align: center;
        color: #3498db;
        font-size: 4em;
        font-weight: bold;
        text-shadow: 2px 2px 4px #aaaaaa;
        margin-bottom: 20px;
    '>
    Construyamos un Futuro
    </h1>
    """, unsafe_allow_html=True)
    # Agregar imagen
    imagen_url = "static/images/somos.JPG"  # Reemplaza esto con la URL o la ruta local de tu imagen
    st.image(imagen_url, caption='SI SOMOS 🧑‍💻', use_column_width=True)    
    # Especifica la ruta completa al archivo HTML o la URL
    # Ruta relativa al archivo HTML
    ruta_relativa = 'html/mapa_madrid.html'

    # Obtiene la ruta completa al archivo HTML
    ruta_html = os.path.abspath(ruta_relativa)

    # Abre el archivo HTML en el navegador web predeterminado

    if st.button('Abrir Mapa'):
        # Abre el archivo HTML en el navegador web predeterminado
        webbrowser.open('file://' + ruta_html)


if selected == "Inicio":
    sideBar()
    HomePage()
    try:
        st.markdown("""---""") #Diferencia entre dos
        total_habitantes = float(df_selection['Habitantes (2022)'].unique().sum())
        vivienda_mode = df_selection['Tipo_vivienda'].mode().iloc[0]

        total1,total2 = st.columns(2,gap='large')
        with total1:
            st.info('Total de habitantes en Madrid 👫', icon="🔍")
            st.metric(label = 'nº habitantes', value= f"{total_habitantes:,.0f}")

        with total2:
            st.info('Tipo de vivienda que mas se encuentra 🏘', icon="🔍")
            st.metric(label='Tipo vivienda', value=f"{vivienda_mode}")
        Graphs()
        ProgressBar()
    except:
        st.warning("Empiece escogiendo un Municipio ")


if selected == "Compra":
    st.title(f"You have selected {selected}")


if selected == "Alquiler":
    st.title(f"You have selected {selected}")

if selected == "Mapa":
    abrir_mapa()


footer="""<style>
a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
height:7%;
bottom: 0;
width: 100%;
background-color: #243946;
color: white;
text-align: center;
}
</style>
"""