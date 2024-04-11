from rich.table import Table 
from rich.console import Console
from rich.progress import Progress
from rich.panel import Panel
from rich.live import Live 


privesc = [
    [1, "PwnKit"],
    [2, "linuxprivchecker.py"],
    [3, "linpeas.sh"],
    [4, "linux-exploit-suggester.sh"],
    [5, "lse.sh"]
    ]
privesc_tab = Table(title="Payloads", show_header=True)
privesc_tab.add_column("Number", style="cyan")
privesc_tab.add_column("Payload", style="magenta")

for payload in privesc:
    privesc_tab.add_row(str(payload[0]), payload[1]) 

