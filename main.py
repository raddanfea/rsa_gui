import sys
import qdarkstyle as qdarkstyle
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QListWidget, QPushButton, QGridLayout, QPlainTextEdit, QProgressBar, \
    QLineEdit
import my_rsa


def key_to_tuple(key):
    try:
        # key = bytearray.fromhex(key)
        # key = ''.join(chr(x) for x in key)[1:-1]
        arr = key.split(' ')
        key_tuple = int(arr[0]), int(arr[1])
    except Exception as e:
        print("Invalid key values!")
    return key_tuple


class Decoder(QWidget):

    def mousePressEvent(self, event):
        self.offset = event.pos()

    def mouseMoveEvent(self, event):
        x = event.globalX()
        y = event.globalY()
        x_w = self.offset.x()
        y_w = self.offset.y()
        self.move(x - x_w, y - y_w)

    def __init__(self, parent=None):
        super(Decoder, self).__init__(parent)
        self.setWindowTitle('Crypt v1')
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setGeometry(100, 100, 800, 500)
        self.listFile = QListWidget()
        self.encodeBtn = QPushButton('Encode')
        self.decodeBtn = QPushButton('Decode')
        self.rsaPubKey = QLineEdit('Public Key')
        self.rsaPubKey.setWhatsThis('Public Key')
        self.rsaPrvKey = QLineEdit('Private Key')
        self.inputLabel = QPlainTextEdit('Text Message')
        self.outputLabel = QPlainTextEdit('Encrypted Message')
        self.genRsaBtn = QPushButton('Generate')
        self.load_bar = QProgressBar()
        self.q_btn = QPushButton('Exit')
        self.repeat = 0
        self.coding = 1
        self.coded = ''

        layout = QGridLayout()

        layout.addWidget(self.genRsaBtn, 0, 4, 1, 2)
        layout.addWidget(self.rsaPubKey, 1, 3, 1, 4)
        layout.addWidget(self.rsaPrvKey, 2, 3, 1, 4)
        layout.addWidget(self.q_btn, 0, 9, 1, 1)
        layout.addWidget(self.encodeBtn, 3, 3, 1, 2)
        layout.addWidget(self.decodeBtn, 3, 5, 1, 2)
        layout.addWidget(self.inputLabel, 7, 0, 10, 5)
        layout.addWidget(self.outputLabel, 7, 5, 10, 5)

        self.encodeBtn.clicked.connect(self.encode)
        self.decodeBtn.clicked.connect(self.decode)
        self.genRsaBtn.clicked.connect(self.gen_rsa_keypair)
        self.q_btn.clicked.connect(self.close)
        self.setLayout(layout)

    def gen_rsa_keypair(self):
        public, private = my_rsa.generate_keypair()
        # public, private = str(public).encode('utf-8').hex(), str(private).encode('utf-8').hex()
        public, private = str(public)[1:-1].replace(',', ''), str(private)[1:-1].replace(',', '')
        self.rsaPrvKey.setText(str(private))
        self.rsaPubKey.setText(str(public))

    def encode(self):
        try:
            pubkey = key_to_tuple(self.rsaPubKey.text())
            text = self.inputLabel.toPlainText()
            encrypted_msg = my_rsa.encrypt(pubkey, text)
            msg = str(encrypted_msg)[1:-1].replace(',', '')
            self.outputLabel.setPlainText(msg)
        except Exception as e:
            print(str(e))

    def decode(self):
        try:
            prvkey = key_to_tuple(self.rsaPrvKey.text())
            text = self.outputLabel.toPlainText()
            list = [int(x) for x in text.split(' ')]
            decrypted_msg = my_rsa.decrypt(prvkey, list)
            self.inputLabel.setPlainText(decrypted_msg)
        except Exception as e:
            print(str(e))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet())
    window = Decoder()
    window.show()
    app.exec()
