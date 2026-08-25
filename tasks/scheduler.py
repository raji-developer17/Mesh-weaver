
class Scheduler:
    def __init__(self, gossip):
        self.gossip = gossip
    async def select_node(self, nodes):
        return min(nodes, key=lambda n: n.cpu_usage)