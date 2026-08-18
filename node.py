import asyncio, psutil, json, uuid, time
from tasks.serializer import serialize_task, deserialize_task
from network.server import MeshServer
from network.client import MeshClient
from monitor.gossip import GossipProtocol
from monitor.heartbeat import HeartbeatMonitor
from monitor.system import get_system_stats
class MeshNode:
    def __init__(self, node_id, host='127.0.0.1', port=9001, peers=None):
        self.id = node_id
        self.host = host
        self.port = port
        self.peers = peers or []
        self.server = MeshServer(self)
        self.client = MeshClient(self)
        self.gossip = GossipProtocol(self)
        self.heartbeat = HeartbeatMonitor(self)
        self.tasks = {}

    async def start(self):
        print(f"[{self.id}] Starting on {self.host}:{self.port}")
        await asyncio.gather(
            self.server.start(),
            self.client.connect_to_peers(),
            self.gossip.start(),
            self.heartbeat.start()
        )

    async def submit_task(self, func, *args, **kwargs):
        task_id = str(uuid.uuid4())
        payload = serialize_task(func, args, kwargs, task_id)
        # Find best node (lowest CPU)
        best_peer = await self.gossip.get_best_node()
        target = best_peer if best_peer else self
        print(f"[{self.id}] Routing task {task_id} to {target.id if hasattr(target,'id') else target}")
        result = await self.client.send_task(target, payload)
        return result

if __name__ == "__main__":
    import sys
    port = int(sys.argv[1]) if len(sys.argv)>1 else 9001
    node = MeshNode(f"node-{port}", port=port)
    asyncio.run(node.start())