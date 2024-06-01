import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QTextEdit, QFileDialog, QLineEdit
import os
import re

class TextFileReader(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.date_pattern = '\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}'
        self.tag_pattern = ': \w{4,5}: '
        self.row_pattern = f'({self.date_pattern})({self.tag_pattern})'
        self.ssh_path = ''
        self.path_to_log_file = ''
        self.scp_down_command = f'{self.ssh_path}:{self.path_to_log_file}'
        self.toggle_buttons()

    def initUI(self):
        self.setWindowTitle('Log File Reader')
        self.setGeometry(200, 200, 600, 600)

        self.text_edit = QTextEdit()
        self.text_tag = QLabel()
        self.text_date = QLabel()
        self.button_down = QPushButton('Download(ssh) file to "Documents/ssh_downloads"', self)
        self.down_lable = QLabel('Scp command: ', self)
        self.ssh_conn_line_edit = QLineEdit('SSH CONN', self)
        self.path_to_log_file_line_edit = QLineEdit('PATH TO LOG FILE', self)
        self.button_open = QPushButton('Open File', self)
        self.button_start = QPushButton('Go to begins of file', self)
        self.button_next = QPushButton('Next message', self)
        self.button_prev = QPushButton('Previous message', self)
        self.button_end = QPushButton('Go to end of file', self)
        self.button_exit = QPushButton('Exit', self)
        self.date_pattern_lable = QLabel('Date pattern: ', self)
        self.date_pattern_line_edit = QLineEdit('\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}', self)
        self.tag_pattern_lable = QLabel('Tag pattern: ', self)
        self.tag_pattern_line_edit = QLineEdit(': \w{4,5}: ', self)
        self.text_info = QLabel()
        
        layout = QVBoxLayout()
        layout.addWidget(self.down_lable)
        layout.addWidget(self.ssh_conn_line_edit)
        layout.addWidget(self.path_to_log_file_line_edit)
        layout.addWidget(self.button_down)
        layout.addWidget(self.button_open)
        layout.addWidget(self.date_pattern_lable)
        layout.addWidget(self.date_pattern_line_edit)
        layout.addWidget(self.tag_pattern_lable)
        layout.addWidget(self.tag_pattern_line_edit)
        layout.addWidget(self.text_tag)
        layout.addWidget(self.text_edit)
        layout.addWidget(self.text_date)
        layout.addWidget(self.button_start)
        layout.addWidget(self.button_next)
        layout.addWidget(self.button_prev)
        layout.addWidget(self.button_end)
        layout.addWidget(self.button_exit)
        layout.addWidget(self.text_info)
    
        self.setLayout(layout)
        self.text_tag.setText('Open the log file to read logs')

        self.button_down.clicked.connect(self.downloadFile)
        self.button_open.clicked.connect(self.openFile)
        self.button_start.clicked.connect(self.startPar)
        self.button_next.clicked.connect(self.nextPar)
        self.button_prev.clicked.connect(self.prevPar)
        self.button_end.clicked.connect(self.endPar)
        self.button_exit.clicked.connect(self.close)
        
        self.ssh_conn_line_edit.textChanged.connect(self.save_ssh_conn)
        self.path_to_log_file_line_edit.textChanged.connect(self.save_path_to_log_file)
        
        self.date_pattern_line_edit.textChanged.connect(self.save_date_pattern)
        self.tag_pattern_line_edit.textChanged.connect(self.save_tag_pattern)
        
        self.buttons_enable = True
        
    def toggle_buttons(self):
        self.buttons_enable = not(self.buttons_enable)
        self.button_start.setEnabled(self.buttons_enable)
        self.button_next.setEnabled(self.buttons_enable)
        self.button_prev.setEnabled(self.buttons_enable)
        self.button_end.setEnabled(self.buttons_enable)
        self.date_pattern_line_edit.setEnabled(self.buttons_enable)
        self.tag_pattern_line_edit.setEnabled(self.buttons_enable)
    
    def save_ssh_conn(self, text):
        self.ssh_path = text
        self.scp_down_command = f'{self.ssh_path}:{self.path_to_log_file}'
        print(self.scp_down_command)
        
    def save_path_to_log_file(self, text):
        self.path_to_log_file = text
        self.scp_down_command = f'{self.ssh_path}:{self.path_to_log_file}'
        print(self.scp_down_command) 
    
    def save_date_pattern(self, text):
        self.date_pattern = text
        self.row_pattern = f'({self.date_pattern})({self.tag_pattern})'
        print(self.row_pattern)
        
    def save_tag_pattern(self, text):
        self.tag_pattern = text
        self.row_pattern = f'({self.date_pattern})({self.tag_pattern})'
        print(self.row_pattern)
    
    def downloadFile(self):
        os.system('rm -rf ~/Documents/ssh_downloads')
        os.system('mkdir ~/Documents/ssh_downloads')
        os.system(f'scp {self.scp_down_command} ~/Documents/ssh_downloads')
        print(self.scp_down_command)
    
    def openFile(self):
        try:
            fname = QFileDialog.getOpenFileName(self, 'Open log file', '', '(*.log || *.txt)')[0]
            if fname:
                with open(fname, 'r') as file:
                    text = file.read()
                    self.lines = text.split('\n')
                    self.saved_pars = []
                    start_row = 0
                    for idx, row in enumerate(self.lines):
                        if idx > 0:
                            if re.search(self.row_pattern, row):
                                end_row = idx
                                self.saved_pars.append([start_row, end_row])
                                start_row = idx
                    self.toggle_buttons()
                            
                    self.current_par = 0
                    self.showCurrentPar()
                    
        except Exception as e:
            self.text_date.setText(f'{e}')
            print(e)

    def nextPar(self):
        try:
            if self.current_par < len(self.saved_pars) - 1:
                self.button_next.setText(f'Next message')
                self.button_prev.setText(f'Previous message')
                self.current_par += 1
                self.showCurrentPar()
            else:
                
                self.button_next.setText(f'You are reached the end of file')
        except Exception as e:
            self.text_info.setText(f'{e}')
            print(e)

    def prevPar(self):
        try:
            if self.current_par > 0:
                self.button_prev.setText(f'Previous message')
                self.button_next.setText(f'Next message')
                self.current_par -= 1
                self.showCurrentPar()
            else:
                self.button_prev.setText(f'You are reached the begins of file')
        except Exception as e:
            self.text_info.setText(f'{e}')
            print(e)
    
    def startPar(self):
        try:
            self.current_par = 0
            self.showCurrentPar()
            self.button_prev.setText(f'Previous message')
            self.button_next.setText(f'Next message')
        except Exception as e:
            self.text_info.setText(f'{e}')
            print(e)
            
    def endPar(self):
        try:
            self.current_par = len(self.saved_pars) - 1
            self.showCurrentPar()
            self.button_prev.setText(f'Previous message')
            self.button_next.setText(f'Next message')
        except Exception as e:
            self.text_info.setText(f'{e}')
            print(e)
            
    def showCurrentPar(self):
        try:
            if self.saved_pars:
                par = self.saved_pars[self.current_par]
                mes = ''.join(self.lines[par[0]:par[1]])
                tag = re.findall(self.row_pattern, mes)[0][1].replace(':', '')
                date = re.findall(self.row_pattern, mes)[0][0].replace(':', '')
                payload = list(filter(None,re.split(self.row_pattern, mes)))[2]
                self.text_edit.setPlainText(payload)
                self.text_tag.setText(tag)
                self.text_date.setText(date)
            else: 
                self.text_date.setText(f'No information for pattern found') 
        except Exception as e:
            self.text_info.setText(f'{e}')
            print(e)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TextFileReader()
    window.show()
    sys.exit(app.exec_())