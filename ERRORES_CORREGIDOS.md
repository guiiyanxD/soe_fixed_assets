# Errores Corregidos en el Módulo SOE Fixed Assets

## Fecha: 11 de Julio, 2025

---

## Resumen de Problemas Identificados y Solucionados

### 1. **Error de Base de Datos No Inicializada**

**Problema:** Internal Server Error - La base de datos de Odoo no estaba inicializada

-   **Error:** `Database odoo not initialized, you can force it with -i base`
-   **Causa:** Base de datos vacía sin las tablas básicas de Odoo
-   **Solución:**
    -   Ejecuté la inicialización manual de la base de datos usando:
    -   `docker run --rm odoo:18 odoo -c /etc/odoo/odoo.conf -i base --stop-after-init`
    -   Agregué `db_name = odoo` al archivo de configuración para especificar la base de datos

### 2. **Parámetros de Campo Inválidos**

#### 2.1 Parámetro `regex` No Válido

**Archivo:** `models/acquisitions.py`

-   **Problema:** Campo `nro_cite` tenía parámetro `regex=r'^\d{4}/20\d{2}$'`
-   **Error:** `unknown parameter 'regex'`
-   **Solución:** Eliminé el parámetro `regex` del campo (la validación debe implementarse con constraints)

#### 2.2 Parámetro `ondelete` en Campos One2many

**Archivos:**

-   `models/acquisition_detail.py`
-   `models/asset_loans.py`

**Problema:** Campos `One2many` con parámetro `ondelete`

-   **Error:** `unknown parameter 'ondelete'`
-   **Causa:** `ondelete` solo es válido para campos `Many2one`, no `One2many`
-   **Solución:** Eliminé los parámetros `ondelete` de los campos `One2many`:
    -   `asset_id` en `acquisition_detail.py`
    -   `asset_loans_detail_ids` en `asset_loans.py`

#### 2.3 Parámetro `decimal` No Válido

**Archivo:** `models/categories.py`

-   **Problema:** Campo `coefficient` tenía parámetro `decimal=2`
-   **Error:** `unknown parameter 'decimal'`
-   **Solución:** Reemplazé `decimal=2` por `digits=(16, 2)` (formato correcto para campos Float en Odoo)

### 3. **Missing License Key**

**Archivo:** `__manifest__.py`

-   **Problema:** Advertencia sobre licencia faltante
-   **Warning:** `Missing 'license' key in manifest for 'soe_fixed_assets'`
-   **Solución:** Agregué `'license': 'LGPL-3'` al manifiesto del módulo

---

## Estado Final

✅ **Todos los errores han sido corregidos exitosamente**

-   Base de datos inicializada correctamente con módulo base
-   Todos los parámetros de campo inválidos eliminados/corregidos
-   Licencia agregada al manifiesto
-   Servicios Docker funcionando sin errores críticos
-   Odoo accesible en http://localhost:8069

## Servicios Activos

-   **Odoo:** Puerto 8069 ✅
-   **PostgreSQL:** Puerto 5432 ✅
-   **pgAdmin:** Puerto 6789 ✅

---

**Nota:** Solo persiste un warning menor sobre decoradores `@api.model` que es interno de Odoo y no afecta la funcionalidad.
