# 🌐 Acceso Público - Sistema de Gestión Educativa

Este documento explica cómo hacer tu aplicación accesible desde internet para que otros puedan verla mientras la ejecutas localmente.

## 🚀 **Métodos Disponibles**

### **Opción 1: Script Automático (Recomendado)**

#### **Windows - PowerShell:**
```powershell
# Ejecutar desde la carpeta del proyecto
.\public_access.ps1
```

#### **Windows - Batch:**
```cmd
# Ejecutar desde la carpeta del proyecto
start_public.bat
```

### **Opción 2: Manual con Ngrok**

#### **1. Instalar Ngrok:**
- Ve a [https://ngrok.com/download](https://ngrok.com/download)
- Descarga ngrok para Windows
- Descomprime y agrega a PATH

#### **2. Ejecutar aplicación:**
```bash
python run.py
```

#### **3. Crear túnel público:**
```bash
# En otra terminal
ngrok http 5000
```

#### **4. Compartir URL:**
Ngrok te dará una URL como: `https://abc123.ngrok.io`

### **Opción 3: Acceso en Red Local**

Tu aplicación ya está configurada con `host='0.0.0.0'`, así que puedes acceder desde cualquier dispositivo en tu red WiFi usando:

```
http://TU_IP_LOCAL:5000
```

Para encontrar tu IP local:
```cmd
ipconfig | findstr IPv4
```

## 🔐 **Usuarios de Prueba**

Una vez que la aplicación esté accesible, puedes usar estos usuarios:

### **Administrador:**
- **Usuario:** `admin`
- **Contraseña:** `admin123`

### **Docentes:**
- **Usuario:** `docente1` | **Contraseña:** `123456`
- **Usuario:** `docente2` | **Contraseña:** `123456`

### **Padres de Familia:**
- **Usuario:** `padre_test_1` | **Contraseña:** `123456`
- **Usuario:** `padre_test_2` | **Contraseña:** `123456`

## ⚠️ **Consideraciones de Seguridad**

- 🔒 **Solo para demostración:** No uses esto en producción
- 🔒 **Datos de prueba:** Usa solo datos ficticios
- 🔒 **Sesiones temporales:** Cierra la conexión cuando termines
- 🔒 **URLs temporales:** Las URLs de ngrok cambian cada vez

## 🛠️ **Solución de Problemas**

### **Error: "ngrok not found"**
```bash
# Instalar con Chocolatey
choco install ngrok

# O con Scoop
scoop install ngrok
```

### **Error: "Port already in use"**
```bash
# Cerrar procesos en puerto 5000
netstat -ano | findstr :5000
taskkill /PID [NUMERO_PID] /F
```

### **Error: "Permission denied"**
```bash
# Ejecutar PowerShell como administrador
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 📊 **Monitoreo en Tiempo Real**

Con ngrok puedes monitorear el tráfico en:
```
http://localhost:4040
```

## 🎯 **Casos de Uso**

- ✅ **Demostración a clientes**
- ✅ **Pruebas con usuarios remotos**
- ✅ **Presentaciones en vivo**
- ✅ **Testing en dispositivos móviles**
- ✅ **Colaboración en tiempo real**

## 📞 **Soporte**

Si tienes problemas:
1. Verifica que Python esté en PATH
2. Confirma que la aplicación funciona localmente primero
3. Asegúrate de tener permisos de firewall
4. Revisa que no hay otros servicios en puerto 5000

---

**¡Tu Sistema de Gestión Educativa listo para ser compartido! 🎉** 