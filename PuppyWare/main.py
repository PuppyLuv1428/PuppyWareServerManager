import tkinter as tk
from mcrcon import MCRcon
import threading

# RCON configuration
RCON_HOST = "localhost"
RCON_PORT = 25575
RCON_PASSWORD = "YourStrongPassword"

# Trusted players
TRUSTED = ["ExampleUser1", "ExampleUser2"]

# RCON command execution
def run_command(cmd):
    try:
        with MCRcon(RCON_HOST, RCON_PASSWORD, port=RCON_PORT) as mcr:
            response = mcr.command(cmd)
            print(f"> {cmd}\n{response}")
    except Exception as e:
        print(f"Command failed: {e}")

# Get online players from /list
def get_online_players():
    try:
        with MCRcon(RCON_HOST, RCON_PASSWORD, port=RCON_PORT) as mcr:
            response = mcr.command("list")
            if ":" in response:
                names = response.split(":")[1].strip().split(", ")
                return [name.strip() for name in names if name]
            return []
    except Exception as e:
        print(f"Failed to get players: {e}")
        return []

# Emergency actions
def deop_all():
    for player in get_online_players():
        if player not in TRUSTED:
            run_command(f"deop {player}")

def kick_all():
    for player in get_online_players():
        if player not in TRUSTED:
            run_command(f"kick {player} Emergency action")

def ipban_all():
    for player in get_online_players():
        if player not in TRUSTED:
            run_command(f"ban-ip {player}")

# GUI setup
def launch_gui():
    root = tk.Tk()
    root.title("PuppyWare Server Manager")
    root.geometry("900x700")
    root.configure(bg="#1e1e1e")

    # Console log viewer
    log_box = tk.Text(root, height=20, bg="black", fg="lime", font=("Courier", 10))
    log_box.pack(fill="x", padx=10, pady=10)

    def refresh_log():
        try:
            with open("logs/latest.log", "r") as f:
                log_box.delete("1.0", tk.END)
                log_box.insert(tk.END, f.read()[-5000:])
        except:
            log_box.delete("1.0", tk.END)
            log_box.insert(tk.END, "Log not found.")
        root.after(1000, refresh_log)

    refresh_log()

    # Command input
    cmd_frame = tk.Frame(root, bg="#1e1e1e")
    cmd_frame.pack(fill="x", padx=10)

    cmd_entry = tk.Entry(cmd_frame, font=("Courier", 12), bg="#2e2e2e", fg="white")
    cmd_entry.pack(side="left", fill="x", expand=True)

    def send_cmd():
        cmd = cmd_entry.get()
        run_command(cmd)
        cmd_entry.delete(0, tk.END)

    tk.Button(cmd_frame, text="Send", command=send_cmd, bg="#444", fg="white").pack(side="right")

    # Panic buttons
    panic_frame = tk.Frame(root, bg="#1e1e1e")
    panic_frame.pack(pady=20)

    tk.Button(panic_frame, text="Deop All (Emergency)", command=deop_all, bg="red", fg="white", width=25).pack(pady=5)
    tk.Button(panic_frame, text="Kick All (Emergency)", command=kick_all, bg="orange", fg="white", width=25).pack(pady=5)
    tk.Button(panic_frame, text="IP-Ban All (Emergency)", command=ipban_all, bg="darkred", fg="white", width=25).pack(pady=5)

    # Placeholder for future graphs
    tk.Label(root, text="Performance Graphs Coming Soon...", bg="#1e1e1e", fg="gray", font=("Courier", 12)).pack(pady=20)

    root.mainloop()

# Launch the GUI
if __name__ == "__main__":
    launch_gui()
