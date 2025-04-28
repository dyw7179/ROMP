import sys
import subprocess
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, 
                           QFileDialog, QVBoxLayout, QWidget, QCheckBox, QLabel)

class RompGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('ROMP 이미지 처리기')
        self.setGeometry(100, 100, 400, 300)
        
        # 메인 위젯 설정
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()
        
        # 이미지 선택 버튼
        self.image_path_label = QLabel('선택된 이미지: 없음')
        self.select_button = QPushButton('이미지 선택')
        self.select_button.clicked.connect(self.select_image)
        
        # SMPL 옵션
        self.smpl_checkbox = QCheckBox('SMPL 계산 및 렌더링')
        self.smpl_checkbox.setChecked(True)
        
        # 실행 버튼
        self.run_button = QPushButton('실행')
        self.run_button.clicked.connect(self.run_romp)
        
        # 상태 표시
        self.status_label = QLabel('대기 중...')
        
        # 레이아웃에 위젯 추가
        layout.addWidget(self.image_path_label)
        layout.addWidget(self.select_button)
        layout.addWidget(self.smpl_checkbox)
        layout.addWidget(self.run_button)
        layout.addWidget(self.status_label)
        
        main_widget.setLayout(layout)
        
        self.image_path = None
        
    def select_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, '이미지 선택', '', 
                                                 'Images (*.png *.jpg *.jpeg)')
        if file_name:
            self.image_path = file_name
            self.image_path_label.setText(f'선택된 이미지: {file_name}')
            
    def run_romp(self):
        if not self.image_path:
            self.status_label.setText('이미지를 선택해주세요!')
            return
            
        self.status_label.setText('처리 중...')
        cmd = ['romp', '--mode=image']
        
        if self.smpl_checkbox.isChecked():
            cmd.extend(['--calc_smpl', '--render_mesh'])
            
        cmd.extend(['-i', self.image_path])
        cmd.extend(['--save_path', 'C:/Users/ADmiN/Documents/GitHub/ROMP/simple_romp/result_img'])
        
        try:
            subprocess.run(cmd, check=True)
            self.status_label.setText('처리 완료!')
        except subprocess.CalledProcessError:
            self.status_label.setText('오류가 발생했습니다!')

def main():
    app = QApplication(sys.argv)
    window = RompGUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main() 