# Importaciones módulos Python
import sys
# Importaciones de terceros
from PyQt5.QtWidgets import QApplication
# Importaciones locales
from menu.menu import Menu
from recursos.recursos_rc import qt_resource_data

class App():
  def __init__(self):
    # Instanciar QApplication: Inicia app según configuración del escritorio del usuario y define su apariencia; maneja los eventos.
    app = QApplication(sys.argv)
    # Instanciar y mostrar LoginPrincipal
    menu = Menu()
    menu.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    app = App()