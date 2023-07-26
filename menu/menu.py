# Importaciones módulos Python
import threading
import time
# Importaciones de terceros
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.uic import loadUi
# Importaciones locales
from helpers.pathsConstructor import pathsConstructor
from actualizarLibs import actualizarLibs

class Menu(QMainWindow):
    def __init__(self):
        super().__init__()
        # Crear path absoluto para archivo .ui y cargarlo en MenuPrincipalAgente
        menuPrincipalSoporte = pathsConstructor('menu/menu.ui')
        loadUi(menuPrincipalSoporte, self)

        # Limitar los inputs de equipos a 3 caracteres numéricos
        rx  = QRegExp("[0-9]{3}")
        val = QRegExpValidator(rx)
        self.rangoMin_Input.setValidator(val)
        self.rangoMax_Input.setValidator(val)

        # Asociar método validarFormulario a Boton Actualizar
        self.actualizar_btn.clicked.connect(self.validarFormulario)

        # Programas seleccionadas
        self.programas = []

    def onCheckBoxChange(self):
        if self.asislock_check.isChecked():
            self.programas.append('asislock')
        if self.desktop_check.isChecked():
            self.programas.append('asislockDesktop')
        if self.chrome_check.isChecked():
            self.programas.append('chromeDriver')
        if self.edge_check.isChecked():
            self.programas.append('edgeDriver')
        if self.explorer_check.isChecked():
            self.programas.append('explorerDriver')
        if self.rr_check.isChecked():
            self.programas.append('rr')

    def validarFormulario(self):
        # Capturar datos del formulario
        self.rangoMin = int( self.rangoMin_Input.text() )
        self.rangoMax = int( self.rangoMax_Input.text() )

        if not self.rangoMin or not self.rangoMax:
            self.formMessages.setText('Los dos números de equipo son requeridos')
            delay = threading.Timer(3, self.limpiarMensaje)
            delay.start()
            return

        if self.rangoMin > self.rangoMax:
            self.formMessages.setText('El equipo inicial debe ser menor al equipo final')
            delay = threading.Timer(3, self.limpiarMensaje)
            delay.start()
            return

        self.onCheckBoxChange()

        if not self.programas:
            self.formMessages.setText('Selecciona al menos un programa')
            delay = threading.Timer(3, self.limpiarMensaje)
            delay.start()
            return
        
        self.formMessages.setText('Actualizando equipos. Por favor no cierre el programa')
        QApplication.processEvents()
        self.actualizarEquipos()
        self.limpiarFormulario()

    def actualizarEquipos(self):
        actualizador = actualizarLibs(self.rangoMin, self.rangoMax, self.programas)
        equipos_actualizados, equipos_error = actualizador.actualizarEquipos()
        print("Equipos actualizados:", equipos_actualizados)
        print("Equipos con error:", equipos_error)

    def limpiarMensaje(self):
        self.formMessages.clear()

    def limpiarFormulario(self):
        self.formMessages.clear()
        self.rangoMin_Input.clear()
        self.rangoMax_Input.clear()
        self.asislock_check.setChecked(False)
        self.desktop_check.setChecked(False)
        self.chrome_check.setChecked(False)
        self.edge_check.setChecked(False)
        self.explorer_check.setChecked(False)
        self.rr_check.setChecked(False)

