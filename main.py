import random
import sys
import torch
from PyQt5.QtCore import Qt
from core import core_selection
from dataBase.database import *
from PyQt5.QtGui import QIntValidator, QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit, QGridLayout, QSizePolicy
from PyQt5.QtCore import QObject, pyqtSignal


class EmittingStream(QObject):
    text_written = pyqtSignal(str)

    def write(self, text):
        self.text_written.emit(str(text))
        QApplication.processEvents()
        self.flush()

    def flush(self):
        pass



class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.result_output = None
        self.button_run = None
        self.button_random = None
        self.edit_s = None
        self.edit_k = None
        self.edit_j = None
        self.edit_n = None
        self.edit_m = None
        self.Database = Database()

        # 设置 PyTorch 使用 GPU
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        print(f"Using device: {self.device}")

        # 设置窗口标题和大小
        self.setWindowTitle('最佳样本生成器v0.1')
        self.setGeometry(600, 360, 1000, 600)

        # 创建控件
        label_m = QLabel('样本总数  (45<=m<=54):')
        self.edit_m = QLineEdit()
        self.edit_m.setValidator(QIntValidator(45, 54))

        label_n = QLabel('样本选择数 (7<=n<=25):')
        self.edit_n = QLineEdit()
        self.edit_n.setValidator(QIntValidator(7, 25))

        label_k = QLabel('每组选择数 (4<=k<=7)k:')
        self.edit_k = QLineEdit()
        self.edit_k.setValidator(QIntValidator(4, 7))

        label_j = QLabel('每组选择最少数(s<=j<=k)j:')
        self.edit_j = QLineEdit()
        self.edit_j.setValidator(QIntValidator(3, 7))

        label_s = QLabel('选择的最少样本数(3<=s<=7)s:')
        self.edit_s = QLineEdit()
        self.edit_s.setValidator(QIntValidator(3, 7))

        self.edit_n.setText(str(0))
        self.edit_m.setText(str(0))
        self.edit_j.setText(str(0))
        self.edit_k.setText(str(0))
        self.edit_s.setText(str(0))

        self.button_random = QPushButton('随机请求')
        self.button_random.clicked.connect(self.randomInput)

        self.button_run = QPushButton('样本生成')
        self.button_run.clicked.connect(self.run)

        self.result_output = QTextEdit()
        self.result_output.setReadOnly(True)

        # self.result_output.textChanged.connect(self.run)
        self.result_output2 = QTextEdit(self)
        self.result_output2.setReadOnly(True)
        self.result_output2.setLineWrapMode(QTextEdit.NoWrap)
        # self.result_output2.setMinimumSize(150, 400)
        self.result_output2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.result_output2.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.result_output2.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.result_output2.ensureCursorVisible()

        grid = QGridLayout()
        grid.addWidget(label_m, 1, 0)
        grid.addWidget(self.edit_m, 1, 1)
        grid.addWidget(label_n, 2, 0)
        grid.addWidget(self.edit_n, 2, 1)
        grid.addWidget(label_k, 3, 0)
        grid.addWidget(self.edit_k, 3, 1)
        grid.addWidget(label_j, 4, 0)
        grid.addWidget(self.edit_j, 4, 1)
        grid.addWidget(label_s, 5, 0)
        grid.addWidget(self.edit_s, 5, 1)
        grid.addWidget(self.button_random, 6, 0)
        grid.addWidget(self.button_run, 6, 1)
        grid.addWidget(self.result_output, 7, 0, 1, 2)
        grid.addWidget(self.result_output2, 1, 2, 7, 2)

        # Set column widths
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)
        grid.setColumnStretch(2, 2)

        self.setLayout(grid)

        # 添加icon
        icon = QIcon("src/icon.png")
        self.setWindowIcon(icon)
        # 使用样式表设置控件的样式
        self.setStyleSheet('''
                QLabel {
                    color: black;
                    font-size: 14px;
                }
                QLineEdit {
                    background-color: #3a3a3a;
                    border: 1px solid #666666;
                    color: white;
                    font-size: 14px;
                }
                QPushButton {
                    background-color: #0072c6;
                    border: none;
                    color: white;
                    font-size: 16px;
                    padding: 5px 10px;
                }
                QPushButton :hover {
                    background-color: red;
                    border: none;
                    color: white;
                    font-size: 16px;
                    padding: 5px 10px;
                }
                QTextEdit {
                    background-color: #3a3a3a;
                    border: 1px solid #666666;
                    color: white;
                    font-size: 14px;
                }
            ''')
        # 创建一个 EmittingStream 对象
        stream = EmittingStream()

        # 将输出重定向到 QTextEdit 控件中
        stream.text_written.connect(self.result_output2.insertPlainText)
        sys.stdout = stream

    def randomInput(self):
        # 随机生成n, m, j, k, s的值
        self.edit_n.setText(str(random.randint(7, 25)))
        self.edit_m.setText(str(random.randint(45, 54)))
        self.edit_k.setText(str(random.randint(4, 7)))
        self.edit_j.setText(str(random.randint(3, int(self.edit_k.text()))))
        self.edit_s.setText(str(random.randint(3, int(self.edit_j.text()))))

    def clean_console(self):
        self.result_output.clear()
        self.result_output.setPlainText('computing...\n')
        QApplication.processEvents()

    # @pyqtSlot()
    def run(self):
        # 获取n, m, j, k, s的值
        n = int(self.edit_n.text())
        m = int(self.edit_m.text())
        k = int(self.edit_k.text())
        j = int(self.edit_j.text())
        s = int(self.edit_s.text())

        self.clean_console()
        # 在文本框中输出结果
        string = core_selection(self.device,self.Database, m, n, k, j, s)
        self.result_output.clear()
        self.result_output.setPlainText(string)


if __name__ == '__main__':
    app = QApplication([])
    widget = MyWidget()
    widget.show()
    app.exec_()
