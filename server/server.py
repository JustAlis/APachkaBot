import asyncio
import json
from config import HOST, PORT
from handlers import *
from services import *
from registrator import Registrator, ServiceRegistrator
from message import Message

class _Server:
    def __init__(self):
        self.handlers = dict()
        Registrator.set_handlers(server=self)

        self.services = []
        ServiceRegistrator.set_services(server=self)

            
    async def run_server(self):
        loop = asyncio.get_event_loop()

        for service in self.services:
            loop.create_task(service())

        server = await asyncio.start_server(self.handle_client, HOST, PORT)
        async with server:
            await server.serve_forever()


    async def handle_client(self, reader, writer):
        request = ''
        header = body = None

        while True:
            buffer = (await reader.read(1024)).decode('utf8')
            request+=buffer

            if not request.startswith("POST"):
                writer.close()
                await writer.wait_closed()
                return
            
            try:
                header, body = request.split('\r\n\r\n', 1)
                body = json.loads(body)
                break
            except:
                continue

        writer.close()
        await writer.wait_closed()
        # request_method, headers = header.split('\r\n', 1)
        # request_method = request_method.split('/')[0].replace(' ', '')
        user = body.get('user_id')
        content = body.get('content')
        handler, *text = content.split(' ')
        text = ' '.join(text)

        handler = self.handlers.get(handler)
        message = Message(text=text, user=user)

        if handler is None:
            handler = self.handlers.get('error')
            await handler(message=message)

        else:
            await handler(message=message)

Server = _Server()

#Older version

#import socket
# class Server:
#     def __init__(self):
#         ServiceRegistrator.set_services(server=self)
#         Registrator.set_handlers(server=self)

    #     self.server = socket.create_server(IP, PORT)
    #     self.server.listen(50)
    #     self.server.setblocking(False)


    # def stop(self):
    #     self.server.close()
            
    # async def run_server(self):
    #     loop = asyncio.get_event_loop()

    #     for service in self.services:
    #         loop.create_task(service())

    #     while True:
    #         client_socket, _ = await loop.sock_accept(self.server)
    #         loop.create_task(self.handle_client(client_socket))

    # async def handle_client(self, client_socket):
    #     loop = asyncio.get_event_loop()

    #     writer = ''
    #     header = body = None

    #     while True:
    #         request = (await loop.sock_recv(client_socket, 1024)).decode('utf-8')
    #         writer+=request
    #         try:
    #             header, body = writer.split('\r\n\r\n', 1)
    #             if not header.startswith("POST"):
    #                 while True:
    #                     print('oops')
    #                 client_socket.shutdown(socket.SHUT_RDWR)
    #                 client_socket.close()
    #                 return
    #             body = json.loads(body)
    #             break

    #         except:
    #             continue
    #     print({"data": writer})
    #     client_socket.shutdown(socket.SHUT_RDWR)
    #     client_socket.close()

    #     # request_method, headers = header.split('\r\n', 1)
    #     # request_method = request_method.split('/')[0].replace(' ', '')

    #     user = body.get('user_id')
    #     content = body.get('content')
    #     handler, *message = content.split(' ')
    #     message = ' '.join(message)

    #     handler = self.handlers.get(handler)

    #     if handler is None:
    #         handler = self.handlers.get('error')
    #         resp = await handler(message=message, user=user)
    #         await self.send_answer(resp=resp, user=user)

    #     else:
    #         resp = await handler(message=message, user=user)
    #         await self.send_answer(resp=resp, user=user)

