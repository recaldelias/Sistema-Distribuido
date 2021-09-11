#!/usr/bin/env python

# WS server example

import asyncio
# from asyncio.windows_events import NULL
import websockets


import random
from datetime import datetime

NMAX=50

class Hospital:
    def __init__(self,id,nombre,cantidadcamas,estadocamas):
        self.id=id
        self.nombre=nombre
        self.cantidadcamas=cantidadcamas
        self.estadocamas=estadocamas
    def imprimir(self):

        string= "El "+self.nombre+" cuenta con "+str(self.cantidadcamas)+" camas y sus estados son:\n"
        string2=''
        for i in self.estadocamas:
            string2=string2+i+' '
        string= string + string2+'\n'
        #print(string)
        return string
        
    def agregarcama(self):
        self.cantidadcamas+=1
        self.estadocamas.append("desocupado")
    def cambiarestadocama(self,i):
        if( i < self.cantidadcamas):
            if self.estadocamas[i]=='desocupado': self.estadocamas[i]='ocupado'
            else: self.estadocamas[i]='desocupado'
        else:
            return -1
    def eliminarcama(self,i):
        self.cantidadcamas-=1
        self.estadocamas=self.estadocamas[0:i-1]+self.estadocamas[i+1:]
        

def crearhospital(i):
    id=i
    nombre="Hospital"+str(i+1)
    cantidad=random.randrange(10,20,1)
    camas=[]
    for i in range(cantidad):
        camas.append(random.choice(['ocupado','desocupado']))
    return Hospital(id,nombre,cantidad,camas)

def buscar(list,consulta):
    for i in list:
        if i.id==consulta-1:
            return i
    return -1


    
BDhospitales=[]
for i in range(NMAX):
    BDhospitales.append(crearhospital(i))

async def hello(websocket, path):
    f=open("log.txt",'a+')
    query=0
    while 1:
        
        if query==0: await websocket.send("Que desea hacer?:\n\t1 Para ver el estado de todos los hospitales\n\t2 Para ver un hospital en especifico\n\texit para cortar la conexion")
        query = await websocket.recv()
        if(query=='1'):
            hospitales=""
            for i in BDhospitales:
                hospitales=hospitales+i.imprimir()
            now = datetime.now()
            f.write('tipo_1, 0, Se vio el estado de todos los hospitales, '+now.strftime("%d/%m/%Y %H:%M:%S")+"\n")
            await websocket.send(hospitales+"\nQue desea hacer?:\n\t1 Para ver el estado de todos los hospitales\n\t2 Para ver un hospital en especifico\n\texit para cortar la conexion")
        elif(query=='2'):
            salir=False
            await websocket.send("Envie el numero del hospital(1-50)")
            consulta = await websocket.recv()
            a=buscar(BDhospitales,int(consulta)) 
            if a!=-1:
                while(salir!=True):
                    send="Que desea hacer?:\n\t1 Para ver estado\n\t2 Para crear cama \n\t3 Para eliminar cama\n\t4 Para ocupar una cama\n\t5 Para Desocupar una cama\n\t6 Para cambiar a otro hospital\n\t7 Ver Menu\n\texit para cortar la conexion"
                    await websocket.send(send)
                    consulta = await websocket.recv()
                    if consulta=='1':
                        send=a.imprimir()
                    elif consulta=='2':
                        a.agregarcama()
                        BDhospitales[a.id]=a
                        now = datetime.now()
                        send="Se añadio una cama en el estado desocupado, utilize la opcion 1 para ver los cambios"
                        f.write('tipo_2, 0, Se añadio una cama, '+now.strftime("%d/%m/%Y %H:%M:%S")+"\n")
                    elif consulta=='3':
                        await websocket.send(a.imprimir()+"\nQue cama nro desea eliminar?")
                        respuesta= await websocket.recv()
                        a.eliminarcama(int(respuesta))
                        BDhospitales[a.id]=a
                        send='Se elimino la cama'+respuesta+', utilize la opcion 1 para ver los cambios'
                        now = datetime.now()
                        f.write('tipo_3, 0, Se elimino una cama, '+now.strftime("%d/%m/%Y %H:%M:%S")+"\n")
                    elif consulta=='4':
                        await websocket.send(a.imprimir()+"\nQue cama desea ocupar?")
                        respuesta= await websocket.recv()
                        b=a.cambiarestadocama(int(respuesta))
                        if (b == -1):
                            now = datetime.now()
                            f.write('tipo_4, -1, No existe esa cama, '+now.strftime("%d/%m/%Y %H:%M:%S")+"\n")
                            # await websocket.send("Esa cama no existe\n")
                            # respuesta= await websocket.recv()
                            send = "Esa cama no existe"
                        else:
                            now = datetime.now()
                            f.write('tipo_4, 0, Se ocupo la cama'+respuesta+ ',' +now.strftime("%d/%m/%Y %H:%M:%S")+"\n")
                            send='Se ocupo la cama nro '+respuesta+' Utilize la opcion 1 para ver los cambios'
                    elif consulta=='5':
                        await websocket.send(a.imprimir()+"\nQue cama desea desocupar?")
                        respuesta= await websocket.recv()
                        b=a.cambiarestadocama(int(respuesta))
                        print(b)
                        if (b == -1):
                            now = datetime.now()
                            f.write('tipo_5, -1, No existe esa cama, '+now.strftime("%d/%m/%Y %H:%M:%S")+"\n")
                            # await websocket.send("Esa cama no existe\n")
                            # respuesta= await websocket.recv()
                            send = "Esa cama no existe"
                        else:
                            now = datetime.now()
                            f.write('tipo_5, 0, Se ocupo la cama'+respuesta+ ',' +now.strftime("%d/%m/%Y %H:%M:%S")+"\n")
                            send='Se desocupo la cama nro '+respuesta+' Utilize la opcion 1 para ver los cambios'                       
                    elif consulta=='6':
                        salir=True
                        send=""
                        query=0
                    elif consulta=='7':
                        send="Que desea hacer?:\n\t1 Para ver estado\n\t2 Para crear cama \n\t3 Para eliminar cama\n\t4 Para ocupar una cama\n\t5 Para Desocupar una cama\n\t6 Para cambiar a otro hospital\n\t7 Ver Menu\n\texit para cortar la conexion"   
                        
                    if(consulta!='6'):
                        await websocket.send(send)
                        consulta = await websocket.recv()
        else:
            greeting = f"Error"
            await websocket.send(greeting)
            f.write('tipo_, -1, Opcion no valida'+respuesta+ ',' +now.strftime("%d/%m/%Y %H:%M:%S")+"\n")
            print(f"> {greeting}")
    f.close()
start_server = websockets.serve(hello, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()



