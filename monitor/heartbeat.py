import asyncio, time
class HeartbeatMonitor:
    def __init__(self, node): self.node=node; self.last_seen={}
    async def start(self):
        while True:
            await asyncio.sleep(2)
            # Check if any peer missed heartbeat
            now = time.time()
            for peer_id, last in list(self.last_seen.items()):
                if now - last > 10:
                    print(f"[{self.node.id}] Peer {peer_id} OFFLINE - Reassigning its tasks")
    def beat(self, peer_id): self.last_seen[peer_id]=time.time()