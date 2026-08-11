# MeshWeaver - Zero-Dependency P2P Async Task Broker

Decentralized Task Queue without Redis/RabbitMQ.

## Architecture
- asyncio + sockets for transport
- Kademlia DHT for discovery
- Gossip Protocol for CPU/RAM sharing
- cloudpickle for function serialization
- Fault Tolerance via Heartbeat + Reassignment
- Flask + SocketIO Dashboard

## Run
pip install -r requirements.txt
python run_nodes.py  -> will start 5 nodes + dashboard

Dashboard: http://localhost:5000

## Demo
1. Dashboard shows 5 online nodes
2. Submit factorial(100) -> goes to lowest CPU node
3. Click Offline on a node -> task reassigns