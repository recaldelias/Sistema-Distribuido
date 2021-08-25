#!/usr/bin/env python

import asyncio

import websockets
import json



async def hello():
    async with websockets.connect('ws://localhost:8765') as websocket:

        name=""
        while name!= "exit":
            


            greeting = await websocket.recv()
            respuesta = json.dumps(greeting)

            # for consult in greeting:
            #     print(consult)
            
            print("< {}".format(greeting))
            #print("< {}".format(greeting))
            name = input(" = ")
            await websocket.send(name)
            print("> {}".format(name))
            

asyncio.get_event_loop().run_until_complete(hello())

