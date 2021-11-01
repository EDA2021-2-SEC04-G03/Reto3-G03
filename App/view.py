"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """


import config as cf
import time
import sys
import controller
from prettytable import PrettyTable
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import list as lt
assert cf
import folium
from folium.plugins import MarkerCluster

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""
# ___________________________________________________
#  Ruta a los archivos
# ___________________________________________________

UFOfile = 'UFOS-utf8-large.csv'
# ___________________________________________________
#  Menu principal
# ___________________________________________________


def printMenu():
    print("Bienvenido")
    print("0- Cargar información en el catálogo")
    print("1- Consultar el número de avistamientos en una ciudad")
    print("2- Consultar el número de avistamientos por duración")
    print("3- Consultar el número de avistamientos por hora y minuto del día")
    print("4- Consultar el número de avistamientos en un rango de fechas")
    print("5- Consultar el número de avistamientos de una zona geográfica")
    print("6- Visualizar los avistamientos de una zona geográfica (BONO)")
    print("x-Salir ")

#Funciones para imprimir#
def printRegistro(lista):
    x = PrettyTable() 
    x.field_names = ["Fecha y hora","Ciudad", "Estado", "Pais", "Forma","Duracion (segundos)"]
    for i in lt.iterator(lista):
        x.add_row([str(i['fechahora']),str(i["ciudad"]),str(i["estado"]),str(i["pais"]),
            str(i["forma"]),str(i["duracionsegundos"])])
        x.max_width = 20
    print(x)
def printRegistroReq1(lista):
    x = PrettyTable() 
    x.field_names = ["Fecha y hora","Ciudad", "Estado", "Pais", "Forma","Duracion (segundos)"]
    for i in lt.iterator(lista):
        i=i["elements"][0]
        x.add_row([str(i['fechahora']),str(i["ciudad"]),str(i["estado"]),str(i["pais"]),
            str(i["forma"]),str(i["duracionsegundos"])])
        x.max_width = 20
    print(x)
def printRegistroReq5(lista):
    x = PrettyTable() 
    x.field_names = ["Fecha y hora","Ciudad, País","Duracion (segundos)","Forma","Latitud","Longitud"]
    for i in lt.iterator(lista):
        ciudadPais=str(i["ciudad"])+", "+str(i["pais"])
        x.add_row([str(i['fechahora']),ciudadPais,str(i["duracionsegundos"]),str(i["forma"]),str(i["latitud"]),str(i["longitud"])])
        x.max_width = 20
    print(x)   
def mapaBONO(lista, lati,longi):
    m = folium.Map(location=[lati, longi], zoom_start=4.5)
    marker_cluster = MarkerCluster().add_to(m)
    for i in lt.iterator(lista):
        lat= i["latitud"]
        lon=i["longitud"]
        ciudadPais=str(i["ciudad"])+"-"+str(i["pais"])
        tooltipp="Click para mas información"
        folium.Marker(
            location=[lat, lon],
            popup='</p><strong>Fecha y Hora:<strong></p>'+str(i['fechahora'])+'<p>Ciudad-País:</p>'+ciudadPais+
                    '</p><p>Forma:</p>'+str(i["forma"]) +'<p>Duración:</p>'+str(i["duracionsegundos"])+
                    '<p>Longitud:</p>'+str(i["longitud"])+'</p><p>Latitud:</p>'+str(i["latitud"])+'</p>',
            tooltip=tooltipp,
            icon=folium.Icon(color="green", icon="ok-sign"),
                    ).add_to(marker_cluster)
    m.save("mapa"+str(lati)+"-"+str(longi)+".html")


"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if inputs[0]=="x" or inputs[0].isnumeric()==False:  
        print("Hasta Luego, gracias") 
        sys.exit(0)
    elif int(inputs[0]) == 0:
        start_time = time.process_time()
        print("Cargando información de los archivos ....")
        catalogo = controller.init()
        controller.loadData(catalogo, UFOfile)
        print("El total de avistamientos cargados:"+ str(controller.registrosSize(catalogo)))
        primeras= lt.subList(catalogo["registros"],1,5)
        ultimas= lt.subList(catalogo["registros"],lt.size(catalogo["registros"])-4,5)
        print("Los primeros 5 registros cargados son:")  
        printRegistro(primeras)
        print("Los ultimos 5 registros cargados son:") 
        printRegistro(ultimas)
        stop_time = time.process_time()
        timepaso= stop_time-start_time
        print("Tiempo transcurrido "+ str(timepaso))
    elif int(inputs[0]) == 1:
        nombreCiudad = input('Nombre de la ciudad a consultar\n')
        registrosCiudad= controller.registrosPorCiudad(catalogo,nombreCiudad)
        if registrosCiudad==None or lt.size(registrosCiudad) == 0:
            print("Ciudad no encontrada/no hay registros para la ciudad ingresada")
        else:
            print("El total de avistamientos en "+ nombreCiudad+ " es: "+ str(lt.size(registrosCiudad)))
            if lt.size(registrosCiudad) <= 3:
                print("Hay 3 o menos registros, estos son:")
                printRegistroReq1(registrosCiudad)
            elif lt.size(registrosCiudad) > 3:
                primeras= lt.subList(registrosCiudad,1,3)
                ultimas= lt.subList(registrosCiudad,lt.size(registrosCiudad)-2,3)
                print("Los primeros 3 registros son:") 
                printRegistroReq1(primeras)
                print("Los ultimos 3 registros son:") 
                printRegistroReq1(ultimas)
    elif int(inputs[0]) == 2:
        limiteMinimo  = float(input('Ingrese el límite inferior en segundos (mínimo):  '))
        limiteMaximo= float(input('Ingrese el límite superior en segundos (máximo):  '))
        registrosEnRango= controller.registrosEnRangoDuracion(catalogo,limiteMaximo,limiteMinimo)
        if registrosEnRango==None or lt.size(registrosEnRango)==0:
            print("No se encontraron avistaamientos, en este rango. Revise el orden de entrada")
        else:
            print("El total de avistamientos entre "+ str(limiteMinimo)+ " y "+
                     str(limiteMaximo)+" es: "+ str(lt.size(registrosEnRango)))
            if lt.size(registrosEnRango) <= 3:
                print("Hay 3 o menos registros, estos son:")
                printRegistro(registrosEnRango)
            elif lt.size(registrosEnRango) > 3:
                primeras= lt.subList(registrosEnRango,1,3)
                ultimas= lt.subList(registrosEnRango,lt.size(registrosEnRango)-2,3)
                print("Los primeros 3 registros son:")  
                printRegistro(primeras)
                print("Los ultimos 3 registros son:") 
                printRegistro(ultimas)

    elif int(inputs[0]) == 3:
        inferior=input("Ingrese el limite inferior en formato HH:MM ")
        superior=input("Ingrese el limite superior en formato HH:MM ")
        dicRta=controller.NumAvistamientosPorHoraMinuto(catalogo,inferior,superior)
        numAvistamientos=dicRta["avistamientos"]
        info=dicRta['info']
        
        print("Hay  "+str(numAvistamientos)+" avistamientos entre "+str(inferior)+" y "+ str(superior))
        primeros=lt.subList(info,1,3)
        size=lt.size(info)
        ult=lt.subList(info,size-2,3)
        print("Los primeros 3 registros son:")
        x = PrettyTable() 
        x.field_names = ["Fecha y hora","Ciudad", "Estado", "Pais", "Forma","Duracion (segundos)"]
        for i in lt.iterator(primeros):
            x.add_row([str(i["fechahora"]),str(i["ciudad"]),str(i["estado"]),str(i["pais"]),
            str(i["forma"]),str(i["duracionsegundos"])])
        x.max_width = 20
        print(x)
        print("------------------------------")
        print("Los ultimos 3 registros son:")
        a = PrettyTable() 
        a.field_names = ["Fecha y hora","Ciudad", "Estado", "Pais", "Forma","Duracion (segundos)"]
        for i in lt.iterator(ult):
            x.add_row([str(i["fechahora"]),str(i["ciudad"]),str(i["estado"]),str(i["pais"]),
            str(i["forma"]),str(i["duracionsegundos"])])
        x.max_width = 20
        print(a)
    elif int(inputs[0]) == 4:
        limiteMinimo  = input('Ingrese el límite inferior en formato AAAA-MM-DD:  ')
        limiteMaximo= input('Ingrese el límite superior en formato AAAA-MM-DD:  ')
        registrosEnRango= controller.registrosenRangoFecha(catalogo,limiteMinimo,limiteMaximo)
        if registrosEnRango==None or lt.size(registrosEnRango)==0:
            print("No se encontraron avistaamientos, en este rango. Revise entrada")
        else:
            print("El total de avistamientos entre "+ str(limiteMinimo)+ " y "+
                     str(limiteMaximo)+" es: "+ str(lt.size(registrosEnRango)))
            if lt.size(registrosEnRango) <= 3:
                print("Hay 3 o menos registros, estos son:")
                printRegistro(registrosEnRango)
            elif lt.size(registrosEnRango) > 3:
                primeras= lt.subList(registrosEnRango,1,3)
                ultimas= lt.subList(registrosEnRango,lt.size(registrosEnRango)-2,3)
                print("Los primeros 3 registros son:")  
                printRegistro(primeras)
                print("Los ultimos 3 registros son:") 
                printRegistro(ultimas)
    elif int(inputs[0])==5:
        maxLatitud= round(float(input("Ingrese el limite máximo de latitud ")),2)
        minLatitud=round(float(input("Ingrese el limite minimo de latitud ")),2)
        maxLongitud=round(float(input("Ingrese el limite máximo de longitud ")),2)
        minLongitud=round(float(input("Ingrese el limite minimo de longitud ")),2)
        registrosArea=controller.avistamientosPorZonaGeografica(catalogo,minLongitud,maxLongitud,minLatitud,maxLatitud)
        if registrosArea==None or lt.isEmpty(registrosArea)==True:
            print("No se encontraron avistamientos en el área")
        else:
            print("El total de avistamientos en el área es: "+ str(lt.size(registrosArea)))
            
            if lt.size(registrosArea) <= 5:
                print(str(registrosArea))
                print("Hay 5 o menos registros, estos son:")
                printRegistroReq5(registrosArea)
            elif lt.size(registrosArea) > 5:
                primeras= lt.subList(registrosArea,1,5)
                ultimas= lt.subList(registrosArea,lt.size(registrosArea)-4,5)
                print("Los primeros 5 registros son:")
                printRegistroReq5(primeras)
                print("Los ultimos 5 registros son:") 
                printRegistroReq5(ultimas)
    elif int(inputs[0])==6:
        maxLatitud= round(float(input("Ingrese el limite máximo de latitud ")),2)
        minLatitud=round(float(input("Ingrese el limite minimo de latitud ")),2)
        maxLongitud=round(float(input("Ingrese el limite máximo de longitud ")),2)
        minLongitud=round(float(input("Ingrese el limite minimo de longitud ")),2)
        registrosArea=controller.avistamientosPorZonaGeografica(catalogo,minLongitud,maxLongitud,minLatitud,maxLatitud)
        if registrosArea==None or lt.isEmpty(registrosArea)==True:
            print("No se encontraron avistamientos en el área")
        else:
            print("El total de avistamientos en el área es: "+ str(lt.size(registrosArea)))
            lati= (maxLatitud+minLatitud)/2
            longi=(maxLongitud+minLongitud)/2
            mapaBONO(registrosArea, lati,longi)
            print("Se ha guardado el mapa en el archivo:"+ "mapa"+str(lati)+"-"+str(longi)+".html")           
    elif int(inputs[0]) > 7:
        print("No disponible")
        pass
    else:
        sys.exit(0)

