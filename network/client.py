import asyncio, json
class MeshClient:
    def __init__(self, node): self.node=node
    async def connect_to_peers(self):
        while True:
            await asyncio.sleep(5) 
    async def send_task(self, target, payload):
        try:
            reader, writer = await asyncio.open_connection(target.host if hasattr(target,'host') else '127.0.0.1', target.port if hasattr(target,'port') else 9002)
            writer.write(json.dumps({"type":"task","payload":payload}).encode())
            await writer.drain()
            data = await reader.read(65536)
            writer.close()
            return json.loads(data.decode())
        except Exception as e:
            return {"error": str(e)}