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
