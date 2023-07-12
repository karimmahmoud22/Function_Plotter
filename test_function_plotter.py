import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from pytestqt.qtbot import QtBot
import functionPlotter

def test_plot_function(qtbot: QtBot):
    # Create the application
    app = QApplication(sys.argv)

    # Create the widget
    widget = functionPlotter.FunctionPlotter()

    # Add the widget to the qtbot
    qtbot.addWidget(widget)

    # Test invalid function input
    qtbot.keyClicks(widget.textbox, "")
    qtbot.mouseClick(widget.plot_button, Qt.LeftButton)
    assert widget.canvas.figure.axes[0].lines == []

    # Test invalid xmin and/or xmax input
    qtbot.keyClicks(widget.textbox, "x**2")
    qtbot.keyClicks(widget.xmin_textbox, "5")
    qtbot.keyClicks(widget.xmax_textbox, "2")
    qtbot.mouseClick(widget.plot_button, Qt.LeftButton)
    assert widget.canvas.figure.axes[0].lines == []
    qtbot.keyClicks(widget.xmin_textbox, "a")
    qtbot.mouseClick(widget.plot_button, Qt.LeftButton)
    assert widget.canvas.figure.axes[0].lines == []

    # Test invalid function syntax
    qtbot.keyClicks(widget.textbox, "5*x^3+2*x")
    qtbot.keyClicks(widget.xmin_textbox, "-5")
    qtbot.keyClicks(widget.xmax_textbox, "5")
    qtbot.mouseClick(widget.plot_button, Qt.LeftButton)
    assert widget.canvas.figure.axes[0].lines == []

    # Test valid input
    qtbot.keyClicks(widget.textbox, "5*x**3+2*x")
    qtbot.mouseClick(widget.plot_button, Qt.LeftButton)
    assert widget.canvas.figure.axes[0].lines != []

    # Close the widget and application
    widget.close()
    app.quit()