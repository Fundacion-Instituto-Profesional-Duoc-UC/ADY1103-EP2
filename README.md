# 🚀 Evaluación Parcial 2 (EP2)

## Implementación del Stack Open Source de Observabilidad

---

## 📖 Descripción

En esta evaluación asumirás nuevamente el rol de **Consultor SRE (Site Reliability Engineer)** para dar continuidad a la organización ficticia creada durante la Evaluación Parcial 1.

Para simular el entorno operativo de la empresa, se proporciona una aplicación desarrollada en Python que representa el sistema transaccional principal del negocio, generando métricas continuamente.

Tu objetivo será implementar una arquitectura de observabilidad basada completamente en herramientas Open Source, utilizando:

* Prometheus como sistema de monitoreo y almacenamiento de métricas.
* Grafana como plataforma de visualización.
* Contenedores Docker para el despliegue de la solución.

---

## 📑 Contenido

* [Prerrequisitos](#-prerrequisitos)
* [Configuración del Entorno](#️-configuración-del-entorno)
* [Ejecución del Simulador](#-ejecución-del-simulador)
* [Métricas Disponibles](#-métricas-disponibles)
* [Limpieza del Entorno AWS](#-limpieza-del-entorno-aws)

---

# 📋 Prerrequisitos

Antes de comenzar, verifica que dispones de:

| Requisito         | Versión                             |
| ----------------- | ----------------------------------- |
| Sistema Operativo | Linux (Ubuntu o Debian recomendado) |
| Python            | 3.10 o superior                     |
| Docker            | Última versión estable              |
| Docker Compose    | Última versión estable              |
| Git               | Última versión estable              |

---

## 💻 Instancia Recomendada

Para garantizar un funcionamiento fluido del laboratorio y del stack de observabilidad, se recomienda utilizar una instancia:

| Tipo | vCPU | Memoria |
|--------|------|----------|
| t3.small | 2 vCPU | 2 GiB RAM |

---

## 🌐 Configuración de Red y Firewall

La instancia utilizada para el laboratorio debe contar con las reglas de firewall necesarias para permitir la comunicación entre los distintos componentes de observabilidad.

> ⚠️ Importante: Si los puertos no se encuentran habilitados correctamente, Prometheus, Grafana y otros servicios no podrán ser accedidos o monitoreados.


Verifica tu instalación:

```bash
python3 --version
docker --version
docker compose version
git --version
```

---

# ⚙️ Configuración del Entorno

## 1️⃣ Clonar el repositorio

```bash
git clone https://github.com/Fco-Quiroga/ADY1103-Monitoreo-Observabilidad.git

cd ADY1103-Monitoreo-Observabilidad/04_Ev_Parcial_2-Stack_Open_Source
```

---

## 2️⃣ Crear y activar el entorno virtual

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## 3️⃣ Instalar dependencias

```bash
pip install --upgrade pip

pip install -r requirements.txt
```

---

## 4️⃣ Ejecutar el simulador

```bash
python3 app.py
```

---

# 🎮 Ejecución del Simulador

Al iniciar la aplicación se mostrará un menú con distintos rubros de negocio:

1. Banco
2. Clínica
3. Fintech
4. E-commerce
5. Contabilidad

### Procedimiento

1. Selecciona el rubro asignado.
2. Ingresa el número correspondiente.
3. Presiona **Enter**.
4. El simulador iniciará un servidor web en el puerto **8000**.
5. Comenzará a generar tráfico y métricas de forma continua.
6. Mantén la aplicación en ejecución mientras configuras Prometheus y Grafana.

---

# 🔍 Verificación de Métricas

Puedes comprobar que el simulador está exponiendo métricas correctamente ejecutando:

```bash
curl http://localhost:8000/metrics
```

También puedes acceder desde tu navegador:

```text
http://localhost:8000/metrics
```

---

## ⏳ Acumulación de Métricas para las Evidencias

> ⚠️ Importante: Una vez iniciado el simulador, debes dejarlo ejecutándose durante un período suficiente para que Prometheus pueda recopilar datos históricos y Grafana disponga de información representativa para visualizar.

Antes de capturar las evidencias finales, asegúrate de contar con **al menos 30 minutos de métricas continuas** almacenadas en Prometheus.


# 📈 Métricas Disponibles

El endpoint `/metrics` expone telemetría en formato Prometheus.

A continuación se describen los principales indicadores disponibles:

## 🌐 Disponibilidad y Tráfico

| Métrica                         | Descripción                                                   |
| ------------------------------- | ------------------------------------------------------------- |
| `http_requests_total`           | Total de peticiones HTTP clasificadas por código de respuesta |
| `http_request_duration_seconds` | Histograma de latencia de las solicitudes                     |

---

## 💼 Negocio

| Métrica                       | Descripción                                             |
| ----------------------------- | ------------------------------------------------------- |
| `business_transactions_total` | Operaciones intentadas, exitosas y fallidas del negocio |

---

## 🖥️ Recursos del Sistema

| Métrica                      | Descripción                      |
| ---------------------------- | -------------------------------- |
| `process_cpu_usage_percent`  | Consumo de CPU                   |
| `process_memory_usage_bytes` | Consumo de memoria RAM           |
| `process_threads`            | Cantidad de hilos activos        |
| `process_fds_open`           | Descriptores de archivo abiertos |
| `process_uptime_seconds`     | Tiempo de ejecución continuo     |

---

## 💾 Infraestructura

| Métrica                      | Descripción                          |
| ---------------------------- | ------------------------------------ |
| `node_disk_read_bytes_total` | Lecturas acumuladas de disco         |
| `network_dns_resolution_ms`  | Latencia de resolución DNS           |
| `kafka_consumer_group_lag`   | Mensajes pendientes de procesamiento |

---

# 🧹 Limpieza del Entorno AWS

> ⚠️ Importante: Una vez finalizada la actividad y obtenidas todas las evidencias, elimina los recursos utilizados para evitar consumo innecesario de créditos en AWS Academy Learner Lab.

## Paso 1: Detener y eliminar contenedores

Si utilizaste Docker Compose:

```bash
docker compose down
```

Verifica que no existan contenedores ejecutándose:

```bash
docker ps
```

---

## Paso 2: Terminar la instancia EC2

1. Accede al servicio EC2.
2. Selecciona la instancia utilizada.
3. Haz clic en:

```text
Instance State → Terminate Instance
```

4. Confirma la acción.

---

## Paso 3: Finalizar el Learner Lab

1. Regresa a AWS Academy.
2. Haz clic en:

```text
End Lab
```

3. Espera la confirmación de cierre.

---

> ✅ Completar estos pasos garantiza que no continúe el consumo de créditos asociados al laboratorio.

---

## 👨‍💻 Autor

**ADY1103 - Monitoreo y Observabilidad**

Evaluación Parcial 2 — Implementación del Stack Open Source de Observabilidad.
