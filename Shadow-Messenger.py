import socket
import threading
import ipaddress
import time
import os

print("Welcome to the Shadow-Messenger.")

def send_tcp_message(target_ip, message):
    retries = 3
    delay = 2
    while retries > 0:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            sock.connect((target_ip, 13377))
            message = message.encode().hex()
            message = bin(int(message, 16))[2:].zfill(8)
            message = message.encode().decode('unicode_escape').encode('latin1')
            sock.sendall(message)
            print("Message sent successfully!")
            break
        except Exception as e:
            print(f"Failed to send message: {str(e)}")
            retries -= 1
            if retries > 0:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
    else:
        print("Failed to send message after multiple retries.")
    sock.close()

def listen_tcp():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('0.0.0.0', 13377))
    sock.listen()
    print("Listening on port 13377...")
    while True:
        conn, addr = sock.accept()
        print(f"\nConnection received from {addr[0]}:{addr[1]}")
        data = b''
        while True:
            chunk = conn.recv(1024)
            if not chunk:
                break
            data += chunk
        message = data.decode()
        message = message.encode('latin1').decode('unicode_escape')
        message = int(message, 2)
        message = hex(message)[2:]
        message = bytes.fromhex(message).decode('utf-8')
        print(f"Received message: {message}")
        with open('received_messages.txt', 'a') as f:
            f.write(f"{addr[0]}:{addr[1]} - {message}\n")
        conn.close()

listen_thread = threading.Thread(target=listen_tcp)
listen_thread.start()

target_ip = None

while True:
    if target_ip is None:
        while True:
            username = input("Enter your username: ")
            if os.path.exists("ip.txt"):
                with open('ip.txt', 'r') as f:
                    saved_ip = f.read()
                    saved_username, saved_target_ip = saved_ip.split(':')
                    if saved_username == username:
                        target_ip = saved_target_ip
                        print(f"Using saved IP address: {target_ip}")
                        break
            target_ip = input("Enter the IP address of the target machine: ")
            try:
                ipaddress.ip_address(target_ip)
                with open('ip.txt', 'w') as f:
                    f.write(f"{username}:{target_ip}")
                break
            except ValueError:
                print("Invalid IP address. Please try again.")
    message = input("Enter the message you want to send: ")
    send_thread = threading.Thread(target=send_tcp_message, args=(target_ip, message))
    send_thread.start()
    print("Sending message...")
    input()
    send_thread.join()
