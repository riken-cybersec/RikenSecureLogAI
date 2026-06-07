from email.mime import message
import subprocess
import json
import time
from colorama import Fore, Style, init
import smtplib
from email.mime.text import MIMEText

EMAIL_SENDER = "rikenpatidar17@gmail.com"
EMAIL_PASSWORD = "ldhp txew mbpo ouht"
EMAIL_RECEIVER = "rikenpatidar17@gmail.com"

WHITELIST = [
    "192.168.237.135"
]

source_counts = {}

init()

print(Fore.RED + """
██████╗ ██╗██╗  ██╗███████╗███╗   ██╗
██╔══██╗██║██║ ██╔╝██╔════╝████╗  ██║
██████╔╝██║█████╔╝ █████╗  ██╔██╗ ██║
██╔══██╗██║██╔═██╗ ██╔══╝  ██║╚██╗██║
██║  ██║██║██║  ██╗███████╗██║ ╚████║
╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝
""" + Style.RESET_ALL)

print("=" * 60)
print(Fore.GREEN + "Riken SecureLog AI Pro v1.0" + Style.RESET_ALL)
print("       Created by Riken Patel")
print("=" * 60)

try:

    command = "journalctl | grep -Ei 'failure|FAILED SU|password check failed|Accepted password|session opened'"

    output = subprocess.check_output(command, shell=True, text=True)

    failed_attempts = output.strip().split("\n")
    total = len(failed_attempts)

    live_counter = total 

    ip_attempts = {}

    print(Fore.YELLOW + f"[INFO] Total Failed Attempts Detected: {total}" + Style.RESET_ALL)

    if total >= 5:

        if "rhost=" in output:

            failed_attempts = []

    for line in output.strip().split("\n"):

        if (
            "failure" in line.lower()
            or "failed" in line.lower()
            or "password check failed" in line.lower()
     ):

                failed_attempts.append(line)

    print("\nRecent Failed Attempts:\n")

    for attempt in failed_attempts[-5:]:
        print(Fore.YELLOW + attempt + Style.RESET_ALL)

    print("\nSuspicious Sources:\n")

    sources = []

    for line in failed_attempts:

        if "rhost=" in line:
            try:
                source = line.split("rhost=")[1].split()[0]
                sources.append(source)
            except:
                pass

        elif "user=" in line:
            try:
                source = line.split("user=")[1].split()[0]
                sources.append("user=" + source)
            except:
                pass

    unique_sources = set(sources)

    for source in unique_sources:

        count = sources.count(source)

        if count >= 10:
            print(Fore.RED + f"{source} --> {count} failed attempts" + Style.RESET_ALL)

        else:
            print(Fore.YELLOW + f"{source} --> {count} failed attempts" + Style.RESET_ALL)

    if total >= 20:
        print(Fore.RED + "\n[TOTAL_THREAT_LEVEL] CRITICAL" + Style.RESET_ALL)

    elif total >= 10:
        print(Fore.MAGENTA + "\n[THREAT LEVEL] HIGH" + Style.RESET_ALL)

    elif total >= 5:
        print(Fore.YELLOW + "\n[THREAT LEVEL] MEDIUM" + Style.RESET_ALL)

    else:
        print(Fore.GREEN + "\n[THREAT LEVEL] LOW" + Style.RESET_ALL)

    def send_email_alert(subject, message):
        try:
            msg = MIMEText(message)

            msg["Subject"] = subject
            msg["From"] = EMAIL_SENDER
            msg["To"] = EMAIL_RECEIVER

            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)

            server.sendmail(
                EMAIL_SENDER,
                EMAIL_RECEIVER,
                msg.as_string()
            )

            server.quit()

            print("[EMAIL ALERT SENT]")

        except Exception as e:
            print(f"Email failed: {e}")


    blocked_ips = set()

    def block_ip(ip):

        if ip in blocked_ips:
            return

        try:
            subprocess.run(
                ["iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"],
                check=True
            )

            blocked_ips.add(ip)

            with open("blocked_ips.log", "a") as f:
                f.write(ip + "\n")

            print(f"\n[AUTO BLOCKED] {ip}")

            send_email_alert(
                "🚨 AUTO BLOCK ALERT - RikenSecureLogAI",
                f"Suspicious IP blocked:\n\nIP: {ip}\nReason: More than 10 failed login attempts."
            )

        except Exception as e:
            print(f"Block failed: {e}")

    print("\n" + "="*40)
    print("BLOCKED IPS LIST")
    print("="*40)

   

    try:
        with open("blocked_ips.log", "r") as f:
            ips = set(line.strip() for line in f if line.strip())

        if ips:
            for ip in ips:
                print(f"[BLOCKED] {ip}")
        else:
            print("No blocked IPs found.")

    except FileNotFoundError:
        print("No blocked IPs found.")

    print("="*40 + "\n")

    print("\n" + "="*40)
    print("WHITELISTED IPS")
    print("="*40)

    for ip in WHITELIST:
        print(f"[TRUSTED] {ip}")

    print("="*40)   
        

    print("\nRecommended Actions:")
    print("- Enable MFA")
    print("- Monitor suspicious login attempts")
    print("- Block suspicious IP addresses")

    print() 

except subprocess.CalledProcessError:

    print("\n[INFO] No failed login attempts found.")

    print("\n" + "=" * 60)

# TXT REPORT

report = open("security_report.txt", "w")

report.write("===== Riken SecureLog AI Report =====\n\n")
report.write(f"Total Failed Attempts: {total}\n\n")

report.write("Detected Sources:\n")

for source in unique_sources:

    count = sources.count(source)

    report.write(f"{source} --> {count} failed attempts\n")

report.write("\nThreat Level: ")

if total >= 20:
    report.write("CRITICAL\n")

elif total >= 10:
    report.write("HIGH\n")

elif total >= 5:
    report.write("MEDIUM\n")

else:
    report.write("LOW\n")

report.write("\nRecommended Actions:\n")
report.write("- Enable MFA\n")
report.write("- Block suspicious IPs\n")
report.write("- Monitor authentication logs\n")

report.close()



# JSON REPORT

report_data = {

    "total_failed_attempts": total,

    "threat_level":
        "CRITICAL" if total >= 20 else
        "HIGH" if total >= 10 else
        "MEDIUM" if total >= 5 else
        "LOW",

    "suspicious_sources": list(unique_sources),

    "sources": {}

}

for source in unique_sources:

    report_data["sources"][source] = sources.count(source)

with open("security_report.json", "w") as json_file:

    json.dump(report_data, json_file, indent=4)

print(Fore.CYAN + "[+] JSON report exported successfully!" + Style.RESET_ALL)

print(Fore.GREEN + "\n[+] Report saved as security_report.txt" + Style.RESET_ALL)

print(Fore.CYAN + "\n[+] Live Monitoring Started..." + Style.RESET_ALL)

#print("\n" + "=" * 60)
#print(Fore.GREEN + "[LIVE MONITORING]" + Style.RESET_ALL)
#print("=" * 60)

live_failed_attempts = 0
current_live_threat = "LOW"

# LIVE MONITORING


try:

    command = "journalctl -n 0 -f"

    process = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        text=True
    )

    print(Fore.CYAN + "\n[LIVE MONITORING ACTIVE]\n" + Style.RESET_ALL)
    
    print(Fore.CYAN +
      f"\n[LIVE THREAT LEVEL] {current_live_threat}"
      + Style.RESET_ALL)

    for line in process.stdout:

        line = line.strip()
        print(line)

        # FAILED LOGINS

        if (
            "failure" in line.lower()
            or "failed" in line.lower()
            or "password check failed" in line.lower()
            or "incorrect password attempt" in line.lower()
        ):
            
            live_counter += 1 

    
            if "from" in line:
                try:
                    ip = line.split("from")[1].split()[0]

                    ip_attempts[ip] = ip_attempts.get(ip, 0) + 1

                    print(f"IP COUNT: {ip} -> {ip_attempts[ip]}")

                    if ip_attempts[ip] >= 10:

                        if ip in WHITELIST:
                            print(Fore.GREEN + f"\n[WHITELISTED IP] {ip} - Skipping block" + Style.RESET_ALL)

                        else:
                            print(Fore.RED + f"\n[AUTO BLOCK CANDIDATE] {ip}" + Style.RESET_ALL)
                            block_ip(ip)

                except:
                 pass
            
            live_failed_attempts += 1

            if live_failed_attempts >= 20:
                new_threat = "CRITICAL"
            elif live_failed_attempts >= 10:
                new_threat = "HIGH"
            elif live_failed_attempts >= 5:
                new_threat = "MEDIUM"
            else:
                new_threat = "LOW"

            if new_threat != current_live_threat:
                current_live_threat = new_threat

                print(Fore.CYAN +
                        f"\n[LIVE THREAT LEVEL] {current_live_threat}"
                        + Style.RESET_ALL)    

            print(Fore.RED + "\n[FAILED LOGIN DETECTED]" + Style.RESET_ALL)
            print(Fore.YELLOW + line + Style.RESET_ALL)

        # SUCCESS LOGINS
        
        elif (
            "session opened for user" in line.lower()
            or "accepted password" in line.lower()
           and "cron" not in line.lower()
           and "systemd" not in line.lower()
        ):

            print(Fore.GREEN + "\n[SUCCESS LOGIN DETECTED]" + Style.RESET_ALL)
            print(Fore.GREEN + line + Style.RESET_ALL)

            if "accepted password for root" in line.lower():
                print(Fore.RED + "[CRITICAL] ROOT ACCESS GAINED!" + Style.RESET_ALL)

                send_email_alert(
                    "🚨 CRITICAL ROOT ACCESS ALERT",
                    f"Root access detected!\n\nLog:\n{line}"
                )
    
except KeyboardInterrupt:

    print(Fore.CYAN + "\nMonitoring stopped." + Style.RESET_ALL)