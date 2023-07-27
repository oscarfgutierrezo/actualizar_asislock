# Importaciones de terceros
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
# Importaciones locales
from helpers.pathsConstructor import pathsConstructor

class Reporte(QMainWindow):
    def __init__(self, actualizados, error):
        super().__init__()
        # Crear path absoluto para archivo .ui y cargarlo en Reporte
        menuPrincipalSoporte = pathsConstructor('reporte/reporte.ui')
        loadUi(menuPrincipalSoporte, self)

        # Mostrar resultado de Actualizados
        equiposActualizados = [str(equipo) for equipo in actualizados]
        equiposActualizadosReporte = ', '.join(equiposActualizados)
        self.equiposActualizadosLista.setText(equiposActualizadosReporte)

        # Mostrar resultado de Errores
        equiposError = [str(equipo) for equipo in error]
        equiposErrorReporte = ', '.join(equiposError)
        self.equiposNoActualizadosLista.setText(equiposErrorReporte)

if __name__ == "__main__":
    reporte = Reporte()
    reporte.show()

        

    