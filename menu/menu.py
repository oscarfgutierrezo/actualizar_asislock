# Importaciones módulos Python
import threading
import time
# Importaciones de terceros
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import QRegExp, Qt
from PyQt5.QtGui import QRegExpValidator
from PyQt5.uic import loadUi
# Importaciones locales
from helpers.pathsConstructor import pathsConstructor
from actualizarLibs import actualizarLibs
from reporte.reporte import Reporte

class Menu(QMainWindow):
    def __init__(self):
        super().__init__()
        # Crear path absoluto para archivo .ui y cargarlo en Menu
        menu = pathsConstructor('menu/menu.ui')
        loadUi(menu, self)

        # Limitar los inputs de equipos a 3 caracteres numéricos
        rx  = QRegExp("[0-9]{4}")
        val = QRegExpValidator(rx)
        self.rangoMin_Input.setValidator(val)
        self.rangoMax_Input.setValidator(val)

        # Asociar método validarFormulario a Boton Actualizar
        self.actualizar_btn.clicked.connect(self.validarFormulario)

        # Checkbox seleccionar todos los programas
        self.limpiarLibs_check.stateChanged.connect(self.programasToggle)

        # Check buttons de programas con nombres
        self.checkboxs = {
            self.asislock_check: 'asislock',
            self.desktop_check: 'asislockDesktop',
            self.chrome_check: 'chromeDriver',
            self.edge_check: 'edgeDriver',
            self.explorer_check: 'explorerDriver',
            self.rr_check: 'rr'
        }

        # Programas seleccionadas
        self.programas = []

    # Agregar programas a lista en funcion de estado de checkbox
    def onCheckBoxChange(self):
        self.programas = [self.checkboxs[checkbox] for checkbox in self.checkboxs if checkbox.isChecked()]

    def validarFormulario(self):
        # Capturar datos del formulario
        self.rangoMin = self.rangoMin_Input.text()
        self.rangoMax = self.rangoMax_Input.text()

        # Validar datos de equipos
        if not self.rangoMin or not self.rangoMax:
            self.formMessages.setText('Los dos números de equipo son requeridos')
            delay = threading.Timer(3, self.limpiarMensaje)
            delay.start()
            return

        # Validar coherencia de rangos
        if self.rangoMin > self.rangoMax:
            self.formMessages.setText('El equipo inicial debe ser menor al equipo final')
            delay = threading.Timer(3, self.limpiarMensaje)
            delay.start()
            return

        # Agregar programas a lista
        self.onCheckBoxChange()

        # Validar programas seleccionados
        if not self.programas:
            self.formMessages.setText('Selecciona al menos un programa')
            delay = threading.Timer(3, self.limpiarMensaje)
            delay.start()
            return
        
        self.formMessages.setText('Actualizando equipos. Por favor no cierre el programa')
        QApplication.processEvents()

        # Limpiar libs en funcion de check
        if self.limpiarLibs_check.isChecked():
            self.limpiarLibs()

        # Actualizar libs
        self.actualizarEquipos()

        self.limpiarFormulario()

    def actualizarEquipos(self):
        actualizador = actualizarLibs(self.rangoMin, self.rangoMax, self.programas)
        equipos_actualizados, equipos_error = actualizador.actualizarEquipos()
        # Mostrar Resultados
        self.reporte = Reporte(equipos_actualizados, equipos_error)
        self.reporte.show()

    def limpiarLibs(self):
        actualizador = actualizarLibs(self.rangoMin, self.rangoMax, self.programas)
        actualizador.limpiarLibs()

    def limpiarMensaje(self):
        self.formMessages.clear()

    def limpiarFormulario(self):
        self.formMessages.clear()
        self.rangoMin_Input.clear()
        self.rangoMax_Input.clear()
        self.limpiarCheckboxes()
        self.limpiarLibs_check.setChecked(False)

    # Toggle a todos check programas segun estado de limpiar libs
    def programasToggle(self, state):
        if state == Qt.Checked:
            self.todosCheckboxes()

    # Deseleccionar todos los check de programas
    def limpiarCheckboxes(self):
        for checkbox in self.checkboxs:
            checkbox.setChecked(False)

    # Seleccionar todos los check de programas
    def todosCheckboxes(self):
        for checkbox in self.checkboxs:
            checkbox.setChecked(True)
