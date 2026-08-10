from rich.console import Console
from rich.table import Table
from rich.live import Live
import time, random
console = Console()
def render_dashboard(nodes):
    table = Table(title="MeshWeaver Live Dashboard")
    table.add_column("Node ID"); table.add_column("CPU"); table.add_column("RAM"); table.add_column("Status")
    for n in nodes: table.add_row(n['id'], f"{n['cpu']}%", f"{n['ram']}%", n['status'])
    return table