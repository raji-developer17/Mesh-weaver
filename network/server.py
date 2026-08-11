import asyncio, json
class MeshServer:
    def __init__(self, node): self.node=node
    async def start(self):
        server = await asyncio.start_server(self.handle_client, self.node.host, self.node.port)
        async with server: await server.serve_forever()
    async def handle_client(self, reader, writer):
        data = await reader.read(65536)
        try:
            msg = json.loads(data.decode())
            if msg['type']=='ping': writer.write(b'{"type":"pong"}')
            elif msg['type']=='task':
                from tasks.executor import execute_task
                result = execute_task(msg['payload'])
                writer.write(json.dumps({"result": str(result)}).encode())
        except Exception as e:
            writer.write(json.dumps({"error": str(e)}).encode())
        await writer.drain()
        writer.close()