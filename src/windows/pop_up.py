from src.setup_checks import SetupCheckBase
from PyQt5 import QtWidgets

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, checks: list[SetupCheckBase]):
        super().__init__()

        self.setWindowTitle("iMessage GPT Bot")
        self.setGeometry(100, 100, 500, 400)
        
        central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QtWidgets.QVBoxLayout()
        central_widget.setLayout(layout)

        message_label = QtWidgets.QLabel("<h2>It looks like GPT iMessage Bot is being ran without being fully set up.</h2>"
                                         "<h3>Make sure you have completed all the installation instructions below:</h3>", self)
        layout.addWidget(message_label)
        for check in checks:
            if check.success:
                check_name = f"✅ {check.check_name}"
            else:
                check_name = f"🚫 {check.check_name}"

            label = QtWidgets.QLabel(f"<h3>{check_name}</h3>", self)
            layout.addWidget(label)

            if not check.success:
                error_reason = QtWidgets.QLabel(f"<h3>{check.error_reason}</h3>", self)
                layout.addWidget(error_reason)

                for i, instruction in enumerate(check.instructions):
                    instruction_widget = QtWidgets.QLabel(f"<h4>{i}. {instruction}</h4>", self)
                    layout.addWidget(instruction_widget)

        close_button = QtWidgets.QPushButton("Close Window", self)
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.show()

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())