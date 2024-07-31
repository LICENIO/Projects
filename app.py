# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import folium_static  # Asegúrate de importar folium_static

from analisis import (
    cargar_datos, filtrar_por_anos, analisis_periodo, analisis_tipo_de_hecho, analisis_genero,
    analisis_nacionalidad, analisis_ano_nacimiento, analisis_edad, analisis_departamento_colegio,
    analisis_distrito_residencia, analisis_provincia_residencia, analisis_departamento_residencia,
    analisis_modalidad, analisis_metodologia, analisis_facultad, analisis_especialidad, analisis_ciclo_relativo
)

# Función para cargar los datos
def cargar_datos(archivo_csv):
    return pd.read_csv(archivo_csv, delimiter=';')

# Función para filtrar por años
def filtrar_por_anos(df, anos):
    return df[df['matricula'].isin(anos)]

# Función para análisis de nacionalidad
def analisis_nacionalidad(df, paises_seleccionados):
    counts = df['Nacionalidad'].value_counts()
    return counts

# Definición de los países con sus códigos
nacionalidades_codigos = {
    'Alemania': 'DEU',
    'Argentina': 'ARG',
    'Bolivia': 'BOL',
    'Brasil': 'BRA',
    'Chile': 'CHL',
    'China': 'CHN',
    'Colombia': 'COL',
    'Corea Republica': 'KOR',
    'España': 'ESP',
    'Estados Unidos': 'USA',
    'Francia': 'FRA',
    'Guatemala': 'GTM',
    'Italia': 'ITA',
    'Japon': 'JPN',
    'Mexico': 'MEX',
    'Nueva Zelandia': 'NZL',
    'Paraguay': 'PRY',
    'Perú': 'PER',
    'RSS de Ucrania': 'UKR',
    'Rusia': 'RUS',
    'Suiza': 'CHE',
    'Venezuela': 'VEN'
}

# Título de la aplicación
st.title('Análisis de Matrícula Universitaria 2016-2022')

# Cargar los datos
df = cargar_datos('matricula_uni.csv')

# Configuración de la barra lateral
st.sidebar.title('Filtros')

# Filtro de años basado en el campo 'matricula'
anos = st.sidebar.multiselect(
    'Selecciona el/los años de matrícula',
    options=df['matricula'].unique(),
    default=df['matricula'].unique()
)

# Filtro de campo
campos = [
    'matricula', 'Periodos', 'Tipo_de_hecho', 'Genero', 'Nacionalidad',
    'Nacimiento', 'Edad', 'Departamento_Colegio', 'Distrito_Residencia',
    'Provincia_Residencia', 'Departamento_Residencia', 'Facultad',
    'Especialidad', 'Ciclo_Relativo'
]

campo_seleccionado = st.sidebar.selectbox('Selecciona el campo a analizar', campos)

# Lógica para mostrar países seleccionables solo cuando se analiza la Nacionalidad
if campo_seleccionado == 'Nacionalidad':
    st.sidebar.subheader('Selecciona los países')
    paises_seleccionados = st.sidebar.multiselect(
        'Selecciona los países',
        options=nacionalidades_codigos.keys(),  # Usamos las claves del diccionario de nacionalidades
        default=list(nacionalidades_codigos.keys())  # Por defecto, seleccionamos todos los países
    )
else:
    paises_seleccionados = list(nacionalidades_codigos.keys())  # Seleccionamos todos los países por defecto

# Filtrar datos por años de matrícula
df_filtrado = filtrar_por_anos(df, anos)

# Mostrar datos filtrados
st.write(f'Datos filtrados para los años: {anos}')
st.dataframe(df_filtrado)

# Análisis del campo seleccionado
st.subheader(f'Distribución de {campo_seleccionado}')
if campo_seleccionado == 'Periodos':
    counts = analisis_periodo(df_filtrado)
    st.bar_chart(counts)
elif campo_seleccionado == 'Tipo_de_hecho':
    counts = analisis_tipo_de_hecho(df_filtrado)
    fig = px.pie(values=counts.values, names=counts.index, title=f'Distribución de {campo_seleccionado}')
    st.plotly_chart(fig)
elif campo_seleccionado == 'Genero':
    counts = analisis_genero(df_filtrado)
    fig = px.pie(values=counts.values, names=counts.index, title=f'Distribución de {campo_seleccionado}')
    st.plotly_chart(fig)
elif campo_seleccionado == 'Nacionalidad':
    counts = analisis_nacionalidad(df_filtrado, paises_seleccionados)
    
    # Filtrar los datos por las nacionalidades presentes en los países seleccionados
    counts_filtered = counts[counts.index.isin(paises_seleccionados)]
    
    # Crear el gráfico de barras
    st.subheader(f'Distribución de {campo_seleccionado} (Gráfico de Barras)')
    fig_barras = px.bar(counts_filtered, x=counts_filtered.index, y=counts_filtered.values, 
                        title=f'Distribución de {campo_seleccionado}')
    st.plotly_chart(fig_barras)
    
    # Crear el mapa geográfico
    st.subheader(f'Distribución de {campo_seleccionado} (Mapa Geográfico)')
    fig_mapa = go.Figure(data=go.Choropleth(
        locations=[nacionalidades_codigos[n] for n in counts_filtered.index],
        z=counts_filtered.values,
        text=counts_filtered.index,
        colorscale='Viridis',
        marker_line_color='white',
        colorbar_title='Cantidad'
    ))

    fig_mapa.update_layout(
        title=f'Distribución de Nacionalidades',
        geo=dict(
            showframe=False,
            projection_type='equirectangular'
        )
    )

    st.plotly_chart(fig_mapa)
    
# Aquí continúa el resto del código para los otros campos seleccionados...

# Aquí continúa el resto del código para los otros campos seleccionados...

elif campo_seleccionado == 'Nacimiento':
    counts = analisis_ano_nacimiento(df_filtrado)
    fig = px.histogram(df_filtrado, x='Nacimiento', nbins=20, title=f'Distribución de {campo_seleccionado}')
    st.plotly_chart(fig)
elif campo_seleccionado == 'Edad':
    stats = analisis_edad(df_filtrado)
    st.write(stats)
    fig = px.histogram(df_filtrado, x='Edad', nbins=20, title=f'Distribución de {campo_seleccionado}')
    st.plotly_chart(fig)
elif campo_seleccionado == 'Departamento_Colegio':
    counts = analisis_departamento_colegio(df_filtrado)
    fig = px.bar(counts, x=counts.index, y=counts.values, title=f'Distribución de {campo_seleccionado}')
    st.plotly_chart(fig)
elif campo_seleccionado == 'Distrito_Residencia':
    counts = analisis_distrito_residencia(df_filtrado)
    fig = px.bar(counts, x=counts.index, y=counts.values, title=f'Distribución de {campo_seleccionado}')
    st.plotly_chart(fig)
elif campo_seleccionado == 'Provincia_Residencia':
    counts = analisis_provincia_residencia(df_filtrado)
    fig = px.bar(counts, x=counts.index, y=counts.values, title=f'Distribución de {campo_seleccionado}')
    st.plotly_chart(fig)

elif campo_seleccionado == 'Departamento_Residencia':
    counts = analisis_departamento_residencia(df_filtrado)
    st.subheader(f'Distribución de {campo_seleccionado}')
    st.bar_chart(counts)

    # Cargar el archivo GeoJSON de los departamentos del Perú
    import json
    import folium

    with open('peru_departamental_simple.geojson') as f:
        geo_json_data = json.load(f)

    # Preparar los datos para el mapa
    map_data = counts.reset_index()
    map_data.columns = ['Departamento', 'Cantidad']

    # Crear el mapa de calor
    # Crear el mapa de calor
    m = folium.Map(location=[-9.19, -75.0152], zoom_start=6, tiles='OpenStreetMap')

    folium.Choropleth(
        geo_data=geo_json_data,
        name='choropleth',
        data=map_data,
        columns=['Departamento', 'Cantidad'],
        key_on='feature.properties.NOMBDEP',
        fill_color='YlGn',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=f'Distribución de {campo_seleccionado}'
    ).add_to(m)

    folium.LayerControl().add_to(m)

    st.subheader(f'Mapa de Distribución por Departamento')
    folium_static(m)


elif campo_seleccionado == 'Modalidad':
    counts = analisis_modalidad(df_filtrado)
    fig = px.pie(values=counts.values, names=counts.index, title=f'Distribución de {campo_seleccionado}')
    st.plotly_chart(fig)
elif campo_seleccionado == 'Metodologia':
    counts = analisis_metodologia(df_filtrado)
    fig = px.bar(counts, x=counts.index, y=counts.values, title=f'Distribución de {campo_seleccionado}')
    st.plotly_chart(fig)
elif campo_seleccionado == 'Facultad':
    counts = analisis_facultad(df_filtrado)
    fig = px.bar(counts, x=counts.index, y=counts.values, title=f'Distribución de {campo_seleccionado}')
    st.plotly_chart(fig)
elif campo_seleccionado == 'Especialidad':
    counts = analisis_especialidad(df_filtrado)
    fig = px.bar(counts, x=counts.index, y=counts.values, title=f'Distribución de {campo_seleccionado}')
    st.plotly_chart(fig)
elif campo_seleccionado == 'Ciclo_Relativo':
    counts = analisis_ciclo_relativo(df_filtrado)
    fig = px.bar(counts, x=counts.index, y=counts.values, title=f'Distribución de {campo_seleccionado}')
    st.plotly_chart(fig)
