import subprocess
import shutil
import os

class actualizarLibs:
    def __init__(self, equipoInicial, equipoFinal, programas):
        # Paths
        self.libsCompartida = r"\\10.255.255.10\tecnologia\COMUN\DESARROLLO\asislock\Despliegue\libs"
        self.libsLocal = r"\c$\libs"

        # Rango de equipos
        self.equipoInicial = int(equipoInicial)
        self.equipoFinal = int(equipoFinal)

        # Credenciales
        self.usuario = "david.lopez"
        self.usuarioDominio = "ASISTEBOG\david.lopez"
        self.password = "23Falcon23*"

        # Archivos
        self.asislock = r"\app.exe"
        self.asislockDesktop = r"\asislock.exe"
        self.chromeDriver = r"\chromedriver.exe"
        self.explorerDriver = r"\IEDriverServer.exe"
        self.edgeDriver = r"\msedgedriver.exe"
        self.rr = r"\R.R.hod"
        self.archivosCopiar = []

        # Identificar programas enviados desde formulario
        for programa in programas:
            if programa == 'asislock':
                self.archivosCopiar.append(self.asislock)
            if programa == 'asislockDesktop':
                self.archivosCopiar.append(self.asislockDesktop)
            if programa == 'chromeDriver':
                self.archivosCopiar.append(self.chromeDriver)
            if programa == 'explorerDriver':
                self.archivosCopiar.append(self.explorerDriver)
            if programa == 'edgeDriver':
                self.archivosCopiar.append(self.edgeDriver)
            if programa == 'rr':
                self.archivosCopiar.append(self.rr)

        # Resultados
        self.equiposActualizados = []
        self.equiposError = []

    def conectarEquipo(self, equipo):
        # Conexion con credenciales sin dominio
        try:
            comando_net_use = f"net use {equipo} /user:{self.usuario} {self.password}"
            subprocess.run(comando_net_use, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        except subprocess.CalledProcessError:
            # Conexion con credenciales con dominio
            try:
                comando_net_use = f"net use {equipo} /user:{self.usuarioDominio} {self.password}"
                subprocess.run(comando_net_use, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            except subprocess.CalledProcessError:
                return False
        
        return True

    def eliminarArchivo(self, archivo):
        try:
            os.remove(archivo)
            return True
        except PermissionError:
            return False
        except OSError:
            return False
        
    def eliminarContenidoCarpeta(self, carpeta):
        archivosLista = os.listdir(carpeta)

        for archivo in archivosLista:
            rutaArchivo = os.path.join(carpeta, archivo)
            if os.path.isfile(rutaArchivo):
                archivoEliminado = self.eliminarArchivo(rutaArchivo)
                if not archivoEliminado:
                    return False
            else:
                archivoEliminado = self.eliminarContenidoCarpeta(rutaArchivo)
                if not archivoEliminado:
                    return False
                try:
                    os.rmdir(rutaArchivo)
                except OSError as e:
                    return False

        return True
    
    def copiarArchivo(self, equipo, archivo):
        origenPath = self.libsCompartida +  archivo
        destinoPath = equipo + self.libsLocal + archivo
        
        try:
            shutil.copy(origenPath, destinoPath)
            return True
        except FileNotFoundError:
            return False
        except PermissionError:
            return False
    
    def actualizarEquipos(self):
        for numero in range(self.equipoInicial, self.equipoFinal + 1):
            # Construir nombre equipo y ruta libs local
            equipo = fr"\\EQUIPOP4-{numero}.ASISTEBOG.local"

            # Conectar a equipo
            conexion = self.conectarEquipo(equipo)
            if not conexion:
                self.equiposError.append(numero)
                continue

            # Copiar Archivos
            for archivo in self.archivosCopiar:
                copiaExitosa = self.copiarArchivo(equipo, archivo)
                if not copiaExitosa:
                    self.equiposError.append(numero)
                    break
            
            else:
                self.equiposActualizados.append(numero)

        return self.equiposActualizados, self.equiposError
    
    def limpiarLibs(self):
        for numero in range(self.equipoInicial, self.equipoFinal + 1):
            # Construir nombre equipo y ruta libs local
            equipo = fr"\\EQUIPOP4-{numero}.ASISTEBOG.local"
            libsPath = equipo + self.libsLocal

            # Conectar a equipo
            conexion = self.conectarEquipo(equipo)
            if not conexion:
                self.equiposError.append(numero)
                continue
            
            # Limpiar carpeta libs local
            carpetaLimpia = self.eliminarContenidoCarpeta(libsPath)
            if not carpetaLimpia:
                self.equiposError.append(numero)
                continue
