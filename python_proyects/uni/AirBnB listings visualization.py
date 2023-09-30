        ### GRUPO 3 - ALAN TURING ##
    #Recursado Programacion 2 (2022)
    #Profesores: 
        # Colussi, Natalia
        # Marotte, Damian
    #Integrantes:
        # -Bacalini Nicolas
        # -Bernard Bruno
        # -Sanchez Santiago

###################################################################

## IMPORTAR LIBRERIAS ##

import streamlit as st
import pandas as pd

###################################################################
                          # INPUT DATA #
###################################################################

listings = pd.read_csv('listings.csv')
listings_detailed = pd.read_csv('listings_detailed.csv')

###################################################################

# Funcion que filtra por barrios.
@st.cache
def filter_barrio(df,barrio):
    """
    filter_barrio: DataFrame string -> DataFrame
    
    Si el barrio seleccionado en el selectbox es 'Todos', devuelve
    un DataFrame con los valores de latitud y longitud
    Si el barrio seleccionado en el selectbox es un barrio
    en especifico, devuelve un DataFrame con los valores de
    latitud y longitud de todos los listings de ese barrio.

    """
    if barrio == "Todos":
        df_resultado = df
    else:
        df_resultado = df.loc[df['neighbourhood_cleansed'] == barrio]
    return df_resultado

# Funcion que filtra por tipo de cuartos.
@st.cache
def filter_cuarto(df,cuarto):
    """
    filter_cuarto: DataFrame string -> DataFrame
    
    Si el cuarto seleccionado en el selectbox es 'Todos', devuelve
    un DataFrame con los valores de latitud y longitud
    Si el barrio seleccionado en el selectbox es un barrio
    en especifico, devuelve un DataFrame con los valores de
    latitud y longitud de todos los listings de ese barrio.
    
    """
    if cuarto == "Todos":
        df_cuartos = df[["latitude","longitude"]]
    else:
        df_cuartos = df.loc[df['room_type']==cuarto]
        #df_cuartos=cuartos[["latitude","longitude"]]
    return df_cuartos

### Condiciones para la funcion filter_amenities ###
# Condicion de pileta.
def condicion_pileta(i):
    """
    condicion_pileta : int -> boolean
    
    condicion a cumplir cuando se seleccionan la opcion de
    pileta y no la de estacionamiento

    """
    amenities = listings_detailed["amenities"] # Dataframe de amenities.
    return (("Pool" in amenities[i])\
               or("Private pool" in amenities[i])\
               or("Shared outdoor pool" in amenities[i])\
               or("Shared pool" in amenities[i]))

# Condicion de estacionamiento.
def condicion_estacionamiento(i):
    """
    condicion_estacionamiento : int -> boolean
    
    condicion a cumplir cuando se seleccionan la opcion de
    estacionamiento y no la de pileta

    """
    amenities=listings_detailed["amenities"] # Dataframe de amenities.
    return "Free parking on premises" in amenities[i]

#####################################################
# Funcion que filtra por amenities (estacionamiento y pileta).
@st.cache
def filter_amenities(df,estacionamiento,pileta): 
    """
    filter_amenities : DataFrame boolean boolean -> DataFrame

    segun las opciones elegidas en los checkbox, crea un
    nuevo dataframe con los listings relevantes
 
    """
    df_resultado = pd.DataFrame()

    if estacionamiento:       
        if pileta:
            for i in range (len(df)): 
                if condicion_estacionamiento(i) and condicion_pileta(i):
                    df_resultado = df_resultado.append(df.loc[i])
                    
        else:
            for i in range (len(df)): 
                if condicion_estacionamiento(i):
                    df_resultado = df_resultado.append(df.loc[i]) 
    elif pileta:
        for i in range (len(df)): 
            if condicion_pileta(i):
                df_resultado = df_resultado.append(df.loc[i])
    else:
        df_resultado = df
        
    return df_resultado

#####################################################

# Dataframe de latitudes y longitudes solamente.
@st.cache
def df_latlong(df):
    """
    df_latlong : DataFrame -> DataFrame
    
    recibe un dataframe, devuelve las columnas con la informacion
    de latitud y longitud

    """
    return df[["latitude","longitude"]]


# contar la cantidad de habitaciciones de cada tipo hay por barrio

def contarHabitaciones(df_habitaciones_viena,barrio):
    """
    contarHabitaciones : DataFrame, DataFrame -> void
    recibe dos dataframe y imprime la cantidad de habitaciones que hay segun su tipo
    ejemplos:
    barrio = Todos
    Entire home/apt = 8550
    Private room  = 2761
    Shared room = 66
    Hotel room = 66

    """
    for i in df_habitaciones_viena:
            st.write(i) 
            st.write(len(filter_cuarto(barrio,i)))

################# Funcion principal. #################
def main():
    """
    Funcion main
    """
    #################################################################

    # Dataframe que contiene la palabra "todos" y los barrios de Viena.
    df_palabra_todos = pd.DataFrame({0:['Todos']})
    df_barrios_viena = listings_detailed['neighbourhood_cleansed'].drop_duplicates() 
    barrios = pd.concat([df_palabra_todos,df_barrios_viena])

    #################################################################

    # Dataframe que contiene los tipos de cuartos en Viena.
    df_habitaciones_viena = listings['room_type'].drop_duplicates()
    tipo_habitacion = pd.concat([df_palabra_todos,df_habitaciones_viena])

    #################################################################

    # Filtro segun amenities.
    pileta = st.sidebar.checkbox("Pileta")
    estacionamiento = st.sidebar.checkbox("Estacionamiento Gratis")
    df_amenities = filter_amenities(listings_detailed,estacionamiento,pileta)
    #####################
    # Filtro segun barrios.
    seleccion_barrio = st.sidebar.selectbox('Barrio:',barrios)
    df_barrio = filter_barrio(df_amenities,seleccion_barrio)
    #####################
    # Filtro segun tipo de cuartos.
    seleccion_cuarto = st.sidebar.selectbox('Tipo de alojamiento:',tipo_habitacion)
    df_cuarto = filter_cuarto(df_barrio,seleccion_cuarto)

    #################################################################
    
    # Dataframe de las latitudes y longitudes segun los filtros
    df_latitudes_longitudes = df_latlong(df_barrio)

    #################################################################
    
    # Titulo principal. #
    st.title(
    """
    Viena, Austria
    """)

    # Mapa #
    st.map(df_latitudes_longitudes)

    ##### Grafico de barras #####
    st.write(
    """
    # Precio promedio por barrio
    """)
    promedio_barrios=listings.groupby("neighbourhood")["price"].mean()
    st.bar_chart(promedio_barrios, height=400)

    ### texto para saber cuantas habitaciones de cada tipo hay en total o por barrrio

    st.write(
    """
    Cantidad de residecias de cada tipo segun barrio
    """)

    tipo_habitaciones = pd.concat([df_palabra_todos,df_barrios_viena])

    opcion = st.selectbox('Barrio', tipo_habitaciones)
    
    barrio= filter_barrio(df_amenities,opcion)

    # Funcion contar habitaciones.
    contarHabitaciones(df_habitaciones_viena,barrio)

main()
