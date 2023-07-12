import sys
from math import pow
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from pytestqt.qtbot import QtBot


class FunctionPlotter(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize the GUI elements
        self.title = QLabel("Function Plotter")
        self.textbox_label = QLabel("Function:")
        self.textbox = QLineEdit()

        self.xmin_textbox_label = QLabel("Min X:")
        self.xmin_textbox = QLineEdit()
        
        self.xmax_textbox_label = QLabel("Max X:")
        self.xmax_textbox = QLineEdit()
        
        self.plot_button = QPushButton("Plot the Function")
        self.plot_button.clicked.connect(self.plot_function)
        
        # Set the validators for the text boxes
        self.double_validator = QDoubleValidator()
        self.xmin_textbox.setValidator(self.double_validator)
        self.xmax_textbox.setValidator(self.double_validator)

        # Initialize the plot widget
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        # Set the layout
        vbox = QVBoxLayout()
        vbox.addWidget(self.title)
        
        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.textbox_label)
        hbox1.addWidget(self.textbox)
        
        vbox.addLayout(hbox1)
        
        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.xmin_textbox_label)
        hbox2.addWidget(self.xmin_textbox)
        hbox2.addWidget(self.xmax_textbox_label)
        hbox2.addWidget(self.xmax_textbox)
        
        vbox.addLayout(hbox2)
        vbox.addWidget(self.plot_button)
        vbox.addWidget(self.canvas)
        
        self.setLayout(vbox)

        # Set the window properties
        self.setWindowTitle("Function Plotter")
        self.setGeometry(100, 100, 800, 600)
        self.show()

        
    def plot_function(self):
        # Get the input values from the text boxes
        function_str = self.textbox.text()
        xmin_str = self.xmin_textbox.text()
        xmax_str = self.xmax_textbox.text()

        # validate that the function is not empty
        if function_str == "":
            self.canvas.figure.clf()
            self.canvas.draw()
            self.show_error("Function cannot be empty.")
            return
        
        # validate that xmin and xmax are not empty
        if xmin_str == "" or xmax_str == "":
            self.canvas.figure.clf()
            self.canvas.draw()
            self.show_error("Min X and Max X cannot be empty.")
            return
        
        # Validate that the function has only the following characters in it: 0-9, x, +, -, *, /, (, ), and ^
        valid_chars = "0123456789x+-*/()^"
        for char in function_str:
            if char not in valid_chars:
                self.canvas.figure.clf()
                self.canvas.draw()
                self.show_error("Invalid function syntax.")
                return
        # ocnvert ^ in function to ** for python
        function_str = function_str.replace("^", "**")

        try:
            xmin = float(xmin_str)
            xmax = float(xmax_str)
            if xmin >= xmax:
                self.canvas.figure.clf()
                self.canvas.draw()
                self.show_error("Min X must be less than Max X.")
                return
        except ValueError:
            self.canvas.figure.clf()
            self.canvas.draw()
            self.show_error("Min X and Max X must be numbers.")
            return

        # Create the x and y data for the plot
        x_data = []
        y_data = []
        try:
            for x in range(int(xmin), int(xmax) + 1):
                x_val = x
                y_val = eval(function_str)
                x_data.append(x_val)
                y_data.append(y_val)
        except SyntaxError:
            self.canvas.figure.clf()
            self.canvas.draw()
            self.show_error("Invalid function syntax.")
            return

        # Clear the plot and plot the data
        self.canvas.figure.clf()
        ax = self.canvas.figure.add_subplot(111)
        ax.plot(x_data, y_data)

        # Set the plot properties
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_title(function_str)
        self.canvas.draw()

    def show_error(self, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowTitle("Error")
        msg_box.setText(message)
        msg_box.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = FunctionPlotter()
    sys.exit(app.exec_())

