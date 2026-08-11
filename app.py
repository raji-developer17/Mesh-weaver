from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO
import asyncio, threading, time, random, uuid
from collections import deque


app = Flask(__name__)
app.config['SECRET_KEY'] = 'meshweaver-secret'
socketio = SocketIO(app, cors_allowed_origins="*")

# In-memory state for demo
nodes_state = {
    f"node-{i}": {"id": f"node-{i}", "ip": "127.0.0.1", "port": 9000+i, "status": "online", "cpu": random.randint(10,70), "ram": random.randint(20,60), "last_heartbeat": time.time(), "tasks_completed": random.randint(5,50)}
    for i in range(1,6)
}
tasks_log = deque(maxlen=100)
tasks_stats = {"total": 185, "running": 0, "completed": 0, "failed": 0, "pending": 0}
cpu_history = {f"node-{i}": deque([random.randint(10,70) for _ in range(20)], maxlen=20) for i in range(1,6)}

def background_updater():
    while True:
        time.sleep(2)
        for nid, n in nodes_state.items():
            if n["status"] == "online":
                n["cpu"] = max(5, min(95, n["cpu"] + random.randint(-8,8)))
                n["ram"] = max(10, min(90, n["ram"] + random.randint(-5,5)))
                n["last_heartbeat"] = time.time()
                cpu_history[nid].append(n["cpu"])
        socketio.emit('update', {'nodes': list(nodes_state.values()), 'cpu_history': {k:list(v) for k,v in cpu_history.items()}, 'stats': tasks_stats, 'logs': list(tasks_log)})

threading.Thread(target=background_updater, daemon=True).start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/nodes')
def api_nodes():
    return jsonify(list(nodes_state.values()))
@app.route('/api/logs')
def api_logs():
    return jsonify({
        "logs": list(tasks_log)[::-1],
        "stats": tasks_stats,
        "cpu_history": {k:list(v) for k,v in cpu_history.items()}
    })

@app.route('/api/submit_task', methods=['POST'])
def submit_task():
    data = request.json
    func_code = data.get('code', 'def task(): return 42')
    
    task_id = str(uuid.uuid4())[:8]
    # Find best node - lowest CPU
    online_nodes = [n for n in nodes_state.values() if n["status"]=="online"]
    best = min(online_nodes, key=lambda x: x["cpu"]) if online_nodes else None
    if not best:
        return jsonify({"error": "No nodes online"}), 500

    tasks_stats["total"]+=1
    tasks_stats["running"]+=1

    log_entry = {"time": time.strftime("%H:%M:%S"), "msg": f"Task {task_id} submitted -> Finding best node... Best: {best['id']} (CPU {best['cpu']}%)", "type": "info"}
    tasks_log.append(log_entry)
    socketio.emit('log', log_entry)

    def execute():
        time.sleep(1)
        tasks_log.append({"time": time.strftime("%H:%M:%S"), "msg": f"Task {task_id} assigned to {best['id']}", "type": "assign"})
        time.sleep(random.uniform(1,3))
        # Simulate 90% success
        if random.random() > 0.3:
            tasks_stats["running"]-=1
            tasks_stats["completed"]+=1
            nodes_state[best["id"]]["tasks_completed"]+=1
            tasks_log.append({"time": time.strftime("%H:%M:%S"), "msg": f"Task {task_id} completed on {best['id']} -> Result: Success", "type": "success"})
        else:
            
            tasks_log.append({"time": time.strftime("%H:%M:%S"), "msg": f"Task {task_id} failed on {best['id']} -> Reassigning...", "type": "error"})
            time.sleep(1.5)
            # Reassign
            second_best = min([n for n in online_nodes if n["id"]!=best["id"]], key=lambda x: x["cpu"], default=best)
            tasks_log.append({"time": time.strftime("%H:%M:%S"), "msg": f"Task {task_id} reassigned to {second_best['id']} -> Completed", "type": "success"})
            time.sleep(2,4)
            tasks_stats["failed"]-=1
            tasks_stats["completed"]+=1
            nodes_state[second_best["id"]]["tasks_completed"]+=1
            tasks_log.append({"time": time.strftime("%H:%M:%S"), "msg": f"Task {task_id} completed on {second_best['id']} after retry -> Success", "type": "success"})

    threading.Thread(target=execute, daemon=True).start()
    return jsonify({"task_id": task_id, "assigned_to": best["id"]})

@app.route('/api/toggle_node/<node_id>', methods=['POST'])
def toggle_node(node_id):
    if node_id in nodes_state:
        nodes_state[node_id]["status"] = "offline" if nodes_state[node_id]["status"]=="online" else "online"
        msg = f"Node {node_id} {'disconnected - Heartbeat lost!' if nodes_state[node_id]['status']=='offline' else 'joined - Discovery via DHT'}"
        tasks_log.append({"time": time.strftime("%H:%M:%S"), "msg": msg, "type": "warn"})
        return jsonify(nodes_state[node_id])
    return jsonify({"error": "not found"}), 404

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
