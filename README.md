# Pulso 9 — Demo pública

Pulso 9 es un sistema de reporting automático para e-commerce.  
Esta versión pública es una **demo técnica** que muestra cómo se estructura el proyecto a nivel de arquitectura, configuración y pruebas.  
El objetivo es evidenciar buenas prácticas sin exponer integraciones privadas ni lógica de negocio sensible.

---

## Concepto

El sistema consolida información de **pedidos** e **inventario** desde distintas fuentes.  
En esta demo se incluyen:

- **CSV genérico**: lectura de pedidos e inventario desde archivos planos.  
- **Shopify (mock)**: un adapter simulado que reproduce la estructura de datos de Shopify a partir de CSV de ejemplo.  

En ambos casos, los datos se procesan y generan reportes diarios con métricas clave:  
- Total de pedidos  
- Ingresos confirmados  
- Pedidos pendientes y rechazados  
- Alertas de stock bajo según umbral configurable  

---

## Instalación

```bash
git clone https://github.com/MatiasFormoso/pulso9-public.git
cd pulso9-public

python -m venv .venv
# Windows: .venv\Scripts\activate
# Unix/Mac:
source .venv/bin/activate

pip install -r requirements.txt
cp .env.example .env   # completar credenciales SMTP si se desea envío por email
