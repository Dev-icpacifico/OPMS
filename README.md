# OPMS

# Sistema de Gestión Operaciones Y recuperaciones Inmobiliarias
## Futuro Ventas y PostVenta

Este proyecto corresponde a una plataforma interna diseñada para gestionar el proceso completo de Operaciones y Recuperaciones de propiedades dentro de nuestros proyectos inmobiliarios.

## 🎯 Objetivo del Sistema

Centralizar y estructurar el ciclo completo de una venta de propiedad:

- Gestión de clientes (Básico)
- Registro y visualización de propiedades
- Asignación y seguimiento de etapas del proceso de venta
- Carga de documentación y validación de estados
- Generación de indicadores clave de seguimiento y avance (Futuro Power BI)

## 🧱 Arquitectura del Proyecto

- **Backend**: Django 5.x
- **Frontend Admin**: Django Admin personalizado + CoreUI (en vistas internas)
- **Base de datos**: PostgreSQL
- **Organización Modular**: Apps separadas por dominio funcional:
  - `gestion_clientes`
  - `gestion_propiedad`
  - `gestion_escrituracion`
  - `gestion_contable` (en construcción)

## 🧩 Estructura Funcional

### 1. Clientes
- Registro completo de datos personales y profesionales.
- Relación directa con cada venta.

### 2. Propiedades
- Jerarquía: Condominio → Etapa → Torre → Propiedad
- Datos técnicos y comerciales.
- Gestión de estados y condiciones comerciales.

### 3. Ventas
- Registro de venta con vínculo a propiedad y cliente.
- Seguimiento a través de etapas dinámicas.
- Carga de valores por etapa y control de flujo.

### 4. Etapas y Campos Dinámicos
- Configuración de etapas por negocio.
- Cada etapa tiene campos personalizables.
- Formulario inteligente con pestañas (CoreUI) para cargar información según etapa.

---

## 🔍 Características Destacadas

- Formulario de etapas con diseño tipo **wizard por pestañas**, adaptado a cada proceso.
- Validaciones de datos comerciales (gastos operacionales, UF/m2, descuentos).
- Admin extendido con filtros por etapa, ejecutivo, estado y propiedad.
- Base escalable para agregar reportes o dashboards en el futuro.

---

## 🛣️ Estado Actual

- Funcionalidad de clientes, propiedades, ventas y etapas operativa.
- Interfaz adaptada para visualización limpia.
- Pruebas internas realizadas en entorno de QA.

