import time
import random
from prometheus_client import start_http_server, Counter, Histogram, Gauge

# ==========================================
# 1. MÉTRICAS CORE, DE PROCESO E INFRAESTRUCTURA
# ==========================================
HTTP_REQUESTS = Counter('http_requests_total', 'Total de peticiones HTTP procesadas', ['rubro', 'endpoint', 'status_code'])
HTTP_LATENCY = Histogram('http_request_duration_seconds', 'Latencia de peticiones HTTP', ['rubro', 'endpoint'], buckets=[0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0])
BIZ_TRANSACTIONS = Counter('business_transactions_total', 'Métricas de impacto comercial', ['rubro', 'status'])
CPU_USAGE = Gauge('process_cpu_usage_percent', 'Uso de CPU del proceso', ['rubro'])
MEM_USAGE = Gauge('process_memory_usage_bytes', 'Uso de Memoria (Bytes)', ['rubro'])
PROCESS_UPTIME = Gauge('process_uptime_seconds', 'Tiempo de actividad del proceso', ['rubro'])
PROCESS_FDS = Gauge('process_fds_open', 'Descriptores de archivo abiertos (Sockets/Archivos)', ['rubro'])
PROCESS_THREADS = Gauge('process_threads', 'Cantidad de hilos (threads) activos', ['rubro'])
DISK_IO_READ = Counter('node_disk_read_bytes_total', 'Bytes leídos del disco local', ['rubro', 'device'])
DNS_RESOLUTION_TIME = Gauge('network_dns_resolution_ms', 'Tiempo de resolución DNS', ['rubro'])
KAFKA_LAG = Gauge('kafka_consumer_group_lag', 'Mensajes atrasados en auditoría', ['rubro'])

# Configuración Global
START_TIME = time.time()
SECTORS = {
    "1": {"rubro": "banco", "endpoints": ["/api/login", "/api/transfer"]},
    "2": {"rubro": "clinica", "endpoints": ["/api/auth", "/api/triage"]},
    "3": {"rubro": "fintech", "endpoints": ["/api/trade", "/api/settle"]},
    "4": {"rubro": "ecommerce", "endpoints": ["/api/checkout", "/api/invoice"]},
    "5": {"rubro": "contabilidad", "endpoints": ["/api/ledger", "/api/audit"]}
}

def simulate_traffic(rubro_name, endpoints):
    """Simulación integral de tráfico, procesos y ruido."""
    
    # --- SIMULACIÓN CORE ---
    endpoint = random.choice(endpoints)
    dice_roll = random.random()
    if dice_roll < 0.80: latency = random.uniform(0.05, 0.30)
    elif dice_roll < 0.95: latency = random.uniform(0.50, 1.50)
    else: latency = random.uniform(2.00, 5.00)

    status_roll = random.random()
    if status_roll < 0.02: status = str(random.choice([500, 502, 503, 504]))
    elif status_roll < 0.07: status = str(random.choice([400, 401, 403, 404]))
    else: status = str(random.choice([200, 201]))

    HTTP_REQUESTS.labels(rubro=rubro_name, endpoint=endpoint, status_code=status).inc()
    HTTP_LATENCY.labels(rubro=rubro_name, endpoint=endpoint).observe(latency)

    if random.random() < 0.25:
        BIZ_TRANSACTIONS.labels(rubro=rubro_name, status="intentadas").inc()
        if random.random() < 0.85: BIZ_TRANSACTIONS.labels(rubro=rubro_name, status="exitosas").inc()
        else: BIZ_TRANSACTIONS.labels(rubro=rubro_name, status="mermas").inc()

    # --- SIMULACIÓN DE PROCESO (NUEVO) ---
    uptime_seconds = time.time() - START_TIME
    PROCESS_UPTIME.labels(rubro=rubro_name).set(uptime_seconds)
    
    CPU_USAGE.labels(rubro=rubro_name).set(random.uniform(30.0, 85.0))
    MEM_USAGE.labels(rubro=rubro_name).set(random.uniform(250.0, 1024.0) * 1024 * 1024)
    
    # Hilos: fluctúan levemente según la carga, típicamente entre 15 y 25
    PROCESS_THREADS.labels(rubro=rubro_name).set(random.randint(15, 25))
    
    # Descriptores de archivo: Base de 150-200. Si hay errores 5xx, simulamos que los sockets
    # se quedan pegados y los FDs suben drásticamente (fuga de descriptores).
    base_fds = random.randint(150, 200)
    if status.startswith('5'):
        PROCESS_FDS.labels(rubro=rubro_name).set(base_fds + random.randint(300, 600))
    else:
        PROCESS_FDS.labels(rubro=rubro_name).set(base_fds)

    DISK_IO_READ.labels(rubro=rubro_name, device="nvme0n1").inc(random.randint(1024, 1048576))
    DNS_RESOLUTION_TIME.labels(rubro=rubro_name).set(random.uniform(1.0, 15.0))
    KAFKA_LAG.labels(rubro=rubro_name).set(max(0, random.randint(-50, 150)))

def main():
    print("=== SRE LAB 2.1: PROMETHEUS + PROCESS METRICS ===")
    for key, val in SECTORS.items():
        print(f"[{key}] {val['rubro'].upper()}")
    
    choice = input("\nSelecciona el rubro (1-5): ").strip()
    if choice not in SECTORS:
        print("Opción inválida.")
        return

    rubro_data = SECTORS[choice]
    rubro_name = rubro_data["rubro"]
    endpoints = rubro_data["endpoints"]

    print(f"\nIniciando servidor de métricas para '{rubro_name}'...")
    start_http_server(8000)
    print("✅ Servidor Prometheus escuchando en http://localhost:8000/metrics")
    print("Generando tráfico y métricas OS en tiempo real... (Presiona Ctrl+C para detener)")

    try:
        while True:
            simulate_traffic(rubro_name, endpoints)
            time.sleep(random.uniform(0.1, 0.5))
    except KeyboardInterrupt:
        print("\nServidor detenido.")

if __name__ == "__main__":
    main()