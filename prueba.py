import subprocess
import shutil
import os

# Paths
libsCompartida = r"\\10.255.255.10\tecnologia\COMUN\DESARROLLO\asislock\Despliegue\libs"
libsLocal = r"\c$\libs"

#Rango de equipos
equipoInicial = 192
equipoFinal = 192

# Credenciales
usuario = "david.lopez"
usuarioDominio = "ASISTEBOG\david.lopez"
password = "23Falcon23*"

# Archivos
asislock = r"\app.exe"
asislockDesktop = r"\asislock.exe"
chromeDriver = r"\chromedriver.exe"
explorerDriver = r"\IEDriverServer.exe"
edgeDriver = r"\msedgedriver.exe"
rr = r"\R.R.hod"

archivosCopiar = [asislock, asislockDesktop, chromeDriver, explorerDriver, edgeDriver, rr]

# Resultados
equiposActualizados = []
equiposError = []

def conectarEquipo(equipo): 
    # Conexion con credenciales sin dominio
    try:
        comando_net_use = f"net use {equipo} /user:{usuario} {password}"
        subprocess.run(comando_net_use, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except subprocess.CalledProcessError:
        # Conexion con credenciales con dominio
        try:
            comando_net_use = f"net use {equipo} /user:{usuarioDominio} {password}"
            subprocess.run(comando_net_use, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        except subprocess.CalledProcessError:
            return False
    
    return True

def eliminarArchivo(archivo):
    try:
        os.remove(archivo)
        return True
    except PermissionError:
        return False
    except OSError:
        return False


def eliminarContenidoCarpeta(carpeta):
    archivosLista = os.listdir(carpeta)

    for archivo in archivosLista:
        rutaArchivo = os.path.join( carpeta, archivo)

        # Eliminar Archivos
        if os.path.isfile(rutaArchivo):
            archivoEliminado = eliminarArchivo(rutaArchivo)
            if not archivoEliminado:
                return False
            
        # Recursividad para carpetas
        else:
            archivoEliminado = eliminarContenidoCarpeta(rutaArchivo)
            if not archivoEliminado:
                return False
            try:
                os.rmdir(rutaArchivo)
            except OSError as e:
                return False

    return True

def copiarArchivo(equipo, archivo):
    origenPath = libsCompartida +  archivo
    destinoPath = equipo + libsLocal + archivo
    
    try:
        shutil.copy(origenPath, destinoPath)
        return True
    except FileNotFoundError:
        return False
    except PermissionError:
        return False

for numero in range(equipoInicial, equipoFinal + 1):
    # Construir nombre equipo y ruta libs local
    equipo = fr"\\EQUIPOP4-{numero}"
    libsPath = equipo + libsLocal

    # Conectar a equipo
    conexion = conectarEquipo(equipo)
    if not conexion:
        equiposError.append(numero)
        continue
    
    # Limpiar carpeta libs local
    carpetaLimpia = eliminarContenidoCarpeta(libsPath)
    if not carpetaLimpia:
        equiposError.append(numero)
        continue
        
    # Copiar Archivos
    for archivo in archivosCopiar:
        copiaExitosa = copiarArchivo(equipo, archivo)
        if not copiaExitosa:
            equiposError.append(numero)
            break
    
    else:
        equiposActualizados.append(numero)

print(equiposActualizados)
print(equiposError)

