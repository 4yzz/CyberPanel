"""
CyberPanel — Single Page Edition
Author: 4yzz
Tech: Python 3.10+, PySide6, requests
"""

import sys, socket, subprocess
from datetime import datetime
from PySide6 import QtCore, QtGui, QtWidgets

try:
    import requests
except ImportError:
    requests = None

APP_TITLE = "CyberPanel by 4yzz"

# ---------- helpers ----------
def fw_font(size=10):
    f = QtGui.QFont("Consolas, FiraCode, Menlo, monospace")
    f.setStyleHint(QtGui.QFont.Monospace)
    f.setPointSize(size)
    return f

def ts():
    return datetime.now().strftime("%H:%M:%S")

# ---------- Main Panel ----------
class CyberPanel(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)

        # Command Runner
        layout.addWidget(QtWidgets.QLabel("💻 Command Runner"))
        self.cmd_inp = QtWidgets.QPlainTextEdit()
        self.cmd_inp.setFont(fw_font())
        self.cmd_inp.setPlaceholderText("Type a command, e.g. echo Hello or ipconfig")
        layout.addWidget(self.cmd_inp)

        self.cmd_out = QtWidgets.QPlainTextEdit(readOnly=True)
        self.cmd_out.setFont(fw_font())
        layout.addWidget(self.cmd_out)

        run_btn = QtWidgets.QPushButton("Run Command")
        run_btn.clicked.connect(self.run_command)
        layout.addWidget(run_btn)

        # Network Info
        layout.addWidget(QtWidgets.QLabel("🌐 Network Info"))
        self.local_ip = QtWidgets.QLineEdit(readOnly=True)
        self.public_ip = QtWidgets.QLineEdit(readOnly=True)
        self.local_ip.setFont(fw_font())
        self.public_ip.setFont(fw_font())

        form = QtWidgets.QFormLayout()
        form.addRow("Local IP:", self.local_ip)
        form.addRow("Public IP:", self.public_ip)
        layout.addLayout(form)

        refresh_btn = QtWidgets.QPushButton("Refresh IP Info")
        refresh_btn.clicked.connect(self.update_ip)
        layout.addWidget(refresh_btn)

        # VPN Connect (simplified)
        layout.addWidget(QtWidgets.QLabel("🔒 VPN Connect"))
        self.vpn_list = QtWidgets.QListWidget()
        for code, name in [
            ("UK", "United Kingdom"),
            ("FR", "France"),
            ("DE", "Germany"),
            ("BE", "Belgium"),
        ]:
            self.vpn_list.addItem(f"{code} — {name}")
        layout.addWidget(self.vpn_list)

        vpn_btn = QtWidgets.QPushButton("Connect")
        vpn_btn.clicked.connect(self.connect_vpn)
        layout.addWidget(vpn_btn)

        self.status = QtWidgets.QLabel("Status: Not connected")
        layout.addWidget(self.status)

        layout.addStretch(1)
        self.update_ip()

    # --- logic ---
    def run_command(self):
        cmd = self.cmd_inp.toPlainText().strip()
        if not cmd:
            return
        self.cmd_out.appendPlainText(f"[{ts()}] $ {cmd}")
        try:
            proc = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
            if proc.stdout:
                self.cmd_out.appendPlainText(proc.stdout.strip())
            if proc.stderr:
                self.cmd_out.appendPlainText("[stderr] " + proc.stderr.strip())
            self.cmd_out.appendPlainText(f"[exit code: {proc.returncode}]")
        except Exception as e:
            self.cmd_out.appendPlainText(f"❌ Error: {e}")

    def update_ip(self):
        try:
            self.local_ip.setText(socket.gethostbyname(socket.gethostname()))
        except:
            self.local_ip.setText("(unknown)")

        if requests:
            try:
                r = requests.get("https://api.ipify.org?format=json", timeout=5)
                self.public_ip.setText(r.json().get("ip", "(unknown)"))
            except:
                self.public_ip.setText("(failed)")
        else:
            self.public_ip.setText("Install requests")

    def connect_vpn(self):
        item = self.vpn_list.currentItem()
        if not item:
            self.status.setText("Status: choose a server first")
            return
        server = item.text()
        self.status.setText(f"Status: Connected to {server}")
        self.cmd_out.appendPlainText(f"[{ts()}] Connected to {server}")

# ---------- Run ----------
def main():
    app = QtWidgets.QApplication(sys.argv)
    win = QtWidgets.QMainWindow()
    win.setWindowTitle(APP_TITLE)
    panel = CyberPanel()
    win.setCentralWidget(panel)
    win.resize(800, 600)
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
