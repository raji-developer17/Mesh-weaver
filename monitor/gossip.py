import asyncio, psutil, json
class GossipProtocol:
    def __init__(self, node): self.node=node; self.cluster_info={}
    async def start(self):
        while True:
            await asyncio.sleep(5)
            stats = {"cpu": psutil.cpu_percent(), "ram": psutil.virtual_memory().percent, "id": self.node.id}
            # print(f"Gossip: {stats}")
    async def get_best_node(self):
    
        if not self.cluster_info: return None
        return min(self.cluster_info.values(), key=lambda x: x['cpu'])