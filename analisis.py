# analisis.py

import pandas as pd

def cargar_datos(archivo_csv):
    return pd.read_csv(archivo_csv, delimiter=';')

def filtrar_por_anos(df, anos):
    return df[df['matricula'].isin(anos)]

def analisis_periodo(df):
    return df['Periodos'].value_counts()

def analisis_tipo_de_hecho(df):
    return df['Tipo_de_hecho'].value_counts()

def analisis_genero(df):
    return df['Genero'].value_counts()

def analisis_nacionalidad(df, paises_seleccionados):
    if paises_seleccionados:
        df_filtrado = df[df['Nacionalidad'].isin(paises_seleccionados)]
    else:
        df_filtrado = df
    return df_filtrado['Nacionalidad'].value_counts()

def analisis_ano_nacimiento(df):
    return df['Nacimiento'].value_counts()

def analisis_edad(df):
    return df['Edad'].describe()

def analisis_departamento_colegio(df):
    return df['Departamento_Colegio'].value_counts()

def analisis_distrito_residencia(df):
    return df['Distrito_Residencia'].value_counts()

def analisis_provincia_residencia(df):
    return df['Provincia_Residencia'].value_counts()

def analisis_departamento_residencia(df):
    return df['Departamento_Residencia'].value_counts()

def analisis_modalidad(df):
    return df['Modalidad'].value_counts()

def analisis_metodologia(df):
    return df['Metodologia'].value_counts()

def analisis_facultad(df):
    return df['Facultad'].value_counts()

def analisis_especialidad(df):
    return df['Especialidad'].value_counts()

def analisis_ciclo_relativo(df):
    return df['Ciclo_Relativo'].value_counts()
