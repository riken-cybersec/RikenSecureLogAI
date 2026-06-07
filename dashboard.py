import tkinter as tk
from tkinter import ttk
from datetime import datetime
import subprocess

def show_graph():
    attempts = [5, 12, 20, 35, 50]
    times = ["1PM", "2PM", "3PM", "4PM", "5PM"]

    plt.plot(times, attempts, marker="o")
    plt.title("Login Attempt Graph")
    plt.xlabel("Time")
    plt.ylabel("Attempts")
    plt.grid(True)
    plt.show()

import matplotlib.pyplot as plt

root = tk.Tk()

root.title("Riken SecureLog AI Pro")
root.geometry("900x600")
root.configure(bg="black")

title = tk.Label(
    root,
    text="RIKEN SECURELOG AI PRO",
    font=("Arial", 24, "bold"),
    fg="cyan",
    bg="black"
)

title.pack(pady=20)

status_label = tk.Label(
    root,
    text="Monitoring Active...",
    font=("Arial", 14),
    fg="lime",
    bg="black"
)

status_label.pack()

attack_counter = tk.Label(
    root,
    text="Total Attacks Detected: 0",
    font=("Arial", 14, "bold"),
    fg="red",
    bg="black"
)

attack_counter.pack()

info_frame = tk.Frame(
    root,
    bg="black",
    highlightbackground="cyan",
    highlightthickness=2
)

info_frame.pack(pady=10)

threat_info = tk.Label(
    info_frame,
    text="Threat Level: LOW",
    font=("Arial", 12, "bold"),
    fg="yellow",
    bg="black"
)

threat_info.pack(anchor="w", padx=20, pady=5)

attempt_info = tk.Label(
    info_frame,
    text="Failed Attempts: 0",
    font=("Arial", 12),
    fg="lime",
    bg="black"
)

attempt_info.pack(anchor="w", padx=20, pady=5)

attacker_info = tk.Label(
    info_frame,
    text="Top Attacker: None",
    font=("Arial", 12),
    fg="orange",
    bg="black"
)

attacker_info.pack(anchor="w", padx=20, pady=5)

remote_info = tk.Label(
    info_frame,
    text="Remote Alerts: INACTIVE",
    font=("Arial", 12),
    fg="red",
    bg="black"
)

remote_info.pack(anchor="w", padx=20, pady=5)

log_box = tk.Text(
    root,
    height=20,
    width=100,
    bg="black",
    fg="lime",
    insertbackground="white"
)

log_box.pack(pady=20)

graph_button = tk.Button(
    root,
    text="Show Attack Graph",
    command=show_graph,
    font=("Arial", 12, "bold"),
    bg="red",
    fg="white"
)

graph_button.pack(pady=10)

def show_graph():

    labels = ["Low", "Medium", "High", "Critical"]

    values = [2, 5, 8, 12]

    plt.figure(figsize=(8,5))

    plt.bar(labels, values)

    plt.title("Attack Severity Graph")

    plt.xlabel("Threat Level")

    plt.ylabel("Attack Count")

    plt.show()

def monitor_logs():


    current_time = datetime.now().strftime("%H:%M:%S")

    status_label.config(
        text=f"Monitoring Active | {current_time}"
    )

    root.after(1000, monitor_logs)

    command = "journalctl -n 10 | grep -Ei 'failure|FAILED SU|password check failed'"

    try:

        output = subprocess.check_output(
            command,
            shell=True,
            text=True
        )

        logs = output.strip().split("\n")

        top_attacker = "user=kali"

        attacker_info.config(
            text=f"Top Attacker: {top_attacker}"
)

        log_box.delete("1.0", tk.END)

        for line in logs:
            log_box.insert(tk.END, line + "\n")

        total = len(logs)

        attempt_info.config(
    text=f"Failed Attempts: {total}"
)

        attack_counter.config(
    text=f"Total Attacks Detected: {total}"
)

        attack_counter.config(text=f"Total Attacks Detected: {total}")

        if total >= 10:

             threat_info.config(
                text="Threat Level: CRITICAL",
                fg="red"
    )

             remote_info.config(
                text="Remote Alerts: ACTIVE",
                fg="red"
    )

             threat_label.config(
                text="Threat Level: CRITICAL",
                fg="red"
    )
        elif total >= 5:

            threat_info.config(
                text="Threat Level: HIGH",
                fg="orange"
    )

            threat_label.config(
                text="Threat Level: HIGH",
                fg="orange"
    )

        else:

            threat_info.config(
                text="Threat Level: LOW",
                fg="lime"
)

            remote_info.config(
                text="Remote Alerts: INACTIVE",
                fg="lime"
)
  
            threat_label.config(
                text="Threat Level: LOW",
                fg="lime"
    )

    except:

        pass

current_time = datetime.now().strftime("%H:%M:%S")

status_label.config(
        text=f"Monitoring Active | {current_time}"
    )

root.after(5000, monitor_logs)

monitor_logs()

root.mainloop()