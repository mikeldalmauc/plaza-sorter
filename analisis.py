import pandas as pd

# Cargar el archivo CSV
file_path_csv = 'plazas.csv'
df = pd.read_csv(file_path_csv)


municipios_incluir = [
    'LAUDIO/LLODIO'
]

asignaturas = {
    'INFORMATICA' : 60,
   #'INFORMATICA EN INGLES': 40,
   # 'SISTEMAS Y APLICACIONES INFORMATICAS': 40,
    
    'MATEMATICAS': 25,
    #'MATEMATICAS EN INGLES': 25,
    #'MATEMATICAS (ESO 1-2)': 25,
    'DIBUJO' : 23,
    #'DIBUJO EN INGLES': 23, 
   # 'TECNOLOGIA EN INGLES': 22,
    'TECNOLOGIA' : 22,
    'INSTALACIONES ELECTROTECNICAS': -9999,
    'EQUIPOS ELECTRONICOS': -9999,
    'ADMINISTRACION DE EMPRESAS': -9999,
    'EPA AMBITO CIENTIFICO-TECNOLOGICO': -9999,
    'PROCESOS DE GESTION ADMINISTRATIVA': -9999,
    'DIVERSIFICACION CURRICULAR CIENT-TECN': -9999,
    'PROCESOS COMERCIALES': -9999,
    'AAT (EQ. ELECTRON.)': -9999,
    'AAT (PC. GEST. ADMIN.)': -9999,
}

municipios = {
    'GALDAKAO': 30,
    'ARRIGORRIAGA': 25,
    'AMOREBIETA-ETXANO': 22,
    'BILBAO': 20,
    'BASAURI': 15,
    'ZAMUDIO': 10,
    'LEZAMA': 10,
    'LARRABETZU': 10,
    'LEMONA': 10,
    'BEDIA': 10,
    'ETXEBARRI': 10,
    'ZARATAMO': 10,
    'USÁNSOLO': 10,
    'LAUDIO/LLODIO': 8,
    'MUNGIA': 8,
    'GERNIKA-LUMO': 8,
    'SESTAO': 7,
    'BARAKALDO': 6,
    'ERANDIO': 5,
    'LEIOA': 4,
    'IGORRE': 4,
    'AMURRIO': 3,
    
    'MUTRIKU': -9999,
    'DERIO': -9999,
    'ONDARROA': -9999,
    'PLENTZIA': -9999,
    'BERMEO': -9999,
    'ZALLA': -9999,
    'LEKEITIO': -9999,
    'SOPELA': -9999,
    'VALLE DE TRÁPAGA-TRA': -9999,
    'ZUMAIA': -9999,
    'ARRATZU': -9999,
    'BALMASEDA': -9999,
    'GETXO': -9999,
    'GÜEÑES': -9999,
    'MARKINA-XEMEIN': -9999,
    'MUSKIZ': -9999,
    'MUTRIKU': -9999,
    'DERIO': -9999,
    'ONDARROA': -9999,
    'PLENTZIA': -9999,
    'BERMEO': -9999,
    'ZALLA': -9999,
    'LEKEITIO': -9999,
    'SOPELA': -9999,
    'KARRANTZA HARANA/VAL': -9999,
    'ZUMAIA': -9999,
}

centros = {
    'CIFP ELORRIETA-ERREKA MARI LHII': 1,
    'CIFP TXURDINAGA LHII': 2,
    'CIFP CONSTRUCCIÓN BIZKAIA LHII': -30,
}

provincias = {
    'BIZKAIA': 100,
    'GIPUZKOA': -9999,
    'ALAVA': -9999
}

tipo_centro = {
    'CIFP': 20,
    'IES': 5,
    'CPI': 1,
    'CEPA': 1
}

jornada = {
    '0' : 50,
    '18' : 50,
    '15' : -9999,
    '12' : -9999,
    '9' : -9999
}

puntaje_individual = {
   15687 : -9999,
   51008 : -9999,
   58684 : 4,
    53997 : 7,
   53997: -10,
   58685: 3,
   58686: 3,
   53988: 5,
   53919: 4,
   54000: -10,
   53922: 4,
   51142: -9999
}

# Definir una función para calcular el puntaje de cada plaza
def calcular_puntaje(row):
    puntaje = 0
    
    # Puntaje por provincia
    provincia = row['TH'].upper()
    for key, value in provincias.items():
        if key in provincia:
            puntaje += value
        
    # Inlcuir municipios de provincias excluidas
    municipio = row['MUNICIPIO'].upper()
    for muni in municipios_incluir:
        if muni in municipio:
            puntaje += 9999
        
    # Puntaje por cercanía a municipios específicos
    for key, value in municipios.items():
        if key in municipio:
            puntaje += value
            puntaje += 0.1*value # Para desempates - aumenta el peso de la cercania
          
                
    # Puntaje por asignatura
    asignatura = row['ASIGNATURA'].upper()
    for key, value in asignaturas.items():
        if key in asignatura:
            puntaje += value
        
    # Puntaje por tipo de centro
    centro = row['CENTRO'].upper()
    for key, value in tipo_centro.items():
        if key in centro:
            puntaje += value
    
    # Puntaje por centro
    for key, value in centros.items():
        if key in centro:
            puntaje += value
            
    # Puntaje por jornada
    nhoras = row['NHORAS']
    for key, value in jornada.items():
        if key == str(nhoras):
            puntaje += value
            

    # Puntaje individual
    nplaza = row['N.PLAZA']
    for key, value in puntaje_individual.items():
        if key == nplaza:
            puntaje += value
            
    return puntaje


# Aplicar la función de puntaje a cada fila
df['PUNTAJE'] = df.apply(calcular_puntaje, axis=1)

# Ordenar el dataframe por puntaje en orden descendente y obtener el top 100
top_100_df = df.sort_values(by='PUNTAJE', ascending=False).head(1500)

# Mejorar la salida de datos
output_df = top_100_df[['N.PLAZA', 'TH', 'MUNICIPIO','CENTRO','ASIGNATURA', 'NHORAS', 'PLAZA', 'OBSERVACIONES', 'PUNTAJE']]

# Mostrar el top 100
print(output_df)

# Opcional: guardar la salida a un nuevo archivo CSV
output_df.to_csv('top_todas_plazas.csv', index=False)
