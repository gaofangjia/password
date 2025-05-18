from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QSpinBox, QCheckBox,
    QLineEdit, QProgressBar, QTextEdit, QScrollArea,
    QFrame, QSlider, QDateTimeEdit, QFileDialog, QMessageBox
)
from PySide6.QtCore import Qt, QSize, QDateTime
from PySide6.QtGui import QColor, QPalette, QClipboard
from ..models.password_generator import PasswordGenerator
from ..models.history_manager import HistoryManager
from ..models.encryption_manager import EncryptionManager
from PySide6.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QHeaderView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # 初始化模型
        self.password_generator = PasswordGenerator()
        self.history_manager = HistoryManager()
        self.encryption_manager = EncryptionManager()
        
        # 当前选中的密码
        self.current_password = ""
        
        # 设置窗口属性
        self.setWindowTitle("密码生成器 - 作者：高芳嘉 2025年3月1日")
        self.setMinimumSize(800, 600)
        
        # 设置主窗口样式
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2D2D2D;
            }
            QLabel {
                color: #ECF0F1;
                font-size: 14px;
            }
            QPushButton {
                background-color: #3498DB;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2980B9;
            }
            QSpinBox, QLineEdit {
                background-color: #34495E;
                color: #ECF0F1;
                border: none;
                padding: 5px;
                border-radius: 4px;
            }
            QCheckBox {
                color: #ECF0F1;
            }
            QProgressBar {
                border: none;
                border-radius: 4px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #27AE60;
                border-radius: 4px;
            }
            QTextEdit {
                background-color: #34495E;
                color: #ECF0F1;
                border: none;
                border-radius: 4px;
            }
        """)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QHBoxLayout(central_widget)
        
        # 创建左侧控制面板
        control_panel = self._create_control_panel()
        control_panel.setMaximumWidth(int(self.width() * 0.3))
        
        # 创建右侧显示区域
        display_area = self._create_display_area()
        
        # 添加到主布局
        main_layout.addWidget(control_panel)
        main_layout.addWidget(display_area)
        main_layout.setStretch(0, 3)  # 左侧占30%
        main_layout.setStretch(1, 7)  # 右侧占70%
    
    def _create_control_panel(self) -> QWidget:
        """创建左侧控制面板"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # 密码长度设置
        length_label = QLabel("密码长度：")
        self.length_spinbox = QSpinBox()
        self.length_spinbox.setRange(12, 64)
        self.length_spinbox.setValue(16)
        
        # 密码数量设置
        count_label = QLabel("生成数量：")
        self.count_spinbox = QSpinBox()
        self.count_spinbox.setRange(1, 10)
        self.count_spinbox.setValue(3)
        
        # 字符类型选项
        self.uppercase_check = QCheckBox("大写字母")
        self.uppercase_check.setChecked(True)
        self.lowercase_check = QCheckBox("小写字母")
        self.lowercase_check.setChecked(True)
        self.digits_check = QCheckBox("数字")
        self.digits_check.setChecked(True)
        self.special_check = QCheckBox("特殊字符")
        self.special_check.setChecked(True)
        
        # 生成按钮
        generate_btn = QPushButton("生成密码")
        generate_btn.clicked.connect(self._generate_passwords)
        
        # 添加到布局
        layout.addWidget(length_label)
        layout.addWidget(self.length_spinbox)
        layout.addWidget(count_label)
        layout.addWidget(self.count_spinbox)
        layout.addWidget(self.uppercase_check)
        layout.addWidget(self.lowercase_check)
        layout.addWidget(self.digits_check)
        layout.addWidget(self.special_check)
        layout.addWidget(generate_btn)
        layout.addStretch()
        
        return panel
    
    def _create_display_area(self) -> QWidget:
        """创建右侧显示区域"""
        display = QWidget()
        layout = QVBoxLayout(display)
        
        # 密码显示区域
        self.password_display = QTextEdit()
        self.password_display.setReadOnly(True)
        self.password_display.textChanged.connect(self._on_password_selected)
        
        # 密码强度进度条
        strength_layout = QHBoxLayout()
        strength_label = QLabel("密码强度：")
        self.strength_progress = QProgressBar()
        self.strength_progress.setRange(0, 100)
        strength_layout.addWidget(strength_label)
        strength_layout.addWidget(self.strength_progress)
        
        # 密码熵值显示
        self.entropy_label = QLabel("密码熵值：0 bits")
        
        # 功能按钮区域
        buttons_layout = QHBoxLayout()
        copy_btn = QPushButton("复制到剪贴板")
        copy_btn.clicked.connect(self._copy_to_clipboard)
        history_btn = QPushButton("历史记录")
        history_btn.clicked.connect(self._show_history)
        
        buttons_layout.addWidget(copy_btn)
        buttons_layout.addWidget(history_btn)
        
        # 添加到布局
        layout.addWidget(self.password_display)
        layout.addLayout(strength_layout)
        layout.addWidget(self.entropy_label)
        layout.addLayout(buttons_layout)
        
        return display
    
    def _on_password_selected(self):
        """当用户选择密码时更新当前密码"""
        cursor = self.password_display.textCursor()
        if cursor.hasSelection():
            self.current_password = cursor.selectedText()
        else:
            # 尝试获取当前行的密码
            cursor.select(QTextEdit.LineUnderCursor)
            line = cursor.selectedText()
            if line.startswith("密码："):
                self.current_password = line[3:]
    
    def _generate_passwords(self):
        """生成密码"""
        try:
            passwords = self.password_generator.generate_passwords(
                length=self.length_spinbox.value(),
                count=self.count_spinbox.value(),
                use_uppercase=self.uppercase_check.isChecked(),
                use_lowercase=self.lowercase_check.isChecked(),
                use_digits=self.digits_check.isChecked(),
                use_special=self.special_check.isChecked()
            )
            
            # 显示生成的密码
            self.password_display.clear()
            for password in passwords:
                # 检查密码强度
                strength_result = self.password_generator.check_password_strength(password)
                score = strength_result['score'] * 25  # 转换为0-100的范围
                
                # 计算熵值
                entropy = self.password_generator.calculate_entropy(password)
                
                # 更新显示
                self.password_display.append(f"密码：{password}")
                self.password_display.append(f"强度：{score}%")
                self.password_display.append(f"熵值：{entropy} bits")
                self.password_display.append("")
                
                # 添加到历史记录
                self.history_manager.add_record(
                    password=password,
                    length=len(password),
                    strength=score,
                    entropy=entropy
                )
            
            # 设置第一个密码为当前密码
            if passwords:
                self.current_password = passwords[0]
                # 更新强度和熵值显示
                strength_result = self.password_generator.check_password_strength(self.current_password)
                score = strength_result['score'] * 25
                self.strength_progress.setValue(int(score))
                entropy = self.password_generator.calculate_entropy(self.current_password)
                self.entropy_label.setText(f"密码熵值：{entropy} bits")
                
        except ValueError as e:
            self.password_display.setText(f"错误：{str(e)}")
    
    def _copy_to_clipboard(self):
        """复制密码到剪贴板"""
        if not self.current_password:
            QMessageBox.warning(self, "警告", "请先选择一个密码")
            return
            
        clipboard = QApplication.clipboard()
        clipboard.setText(self.current_password)
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("提示")
        msg.setText("密码已复制到剪贴板")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.button(QMessageBox.Ok).setText("确定")
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #2D2D2D;
            }
            QMessageBox QLabel {
                color: #ECF0F1;
                font-size: 14px;
            }
            QPushButton {
                background-color: #3498DB;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 14px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #2980B9;
            }
        """)
        msg.exec_()

    def _show_history(self):
        """显示历史记录"""
        dialog = QDialog(self)
        dialog.setWindowTitle("历史记录")
        dialog.setMinimumSize(600, 400)
        
        layout = QVBoxLayout(dialog)
        
        # 创建表格
        table = QTableWidget()
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(["密码", "长度", "强度", "熵值", "生成时间"])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # 设置右键菜单
        table.setContextMenuPolicy(Qt.CustomContextMenu)
        def show_context_menu(pos):
            menu = QMenu()
            copy_action = menu.addAction("复制密码")
            delete_action = menu.addAction("删除")
            
            action = menu.exec_(table.mapToGlobal(pos))
            if action == copy_action:
                current_item = table.item(table.currentRow(), 0)
                if current_item:
                    clipboard = QApplication.clipboard()
                    clipboard.setText(current_item.text())
                    msg = QMessageBox(dialog)
                    msg.setIcon(QMessageBox.Information)
                    msg.setWindowTitle("提示")
                    msg.setText("密码已复制到剪贴板")
                    msg.setStandardButtons(QMessageBox.Ok)
                    msg.button(QMessageBox.Ok).setText("确定")
                    msg.setStyleSheet("""
                        QMessageBox {
                            background-color: #2D2D2D;
                        }
                        QMessageBox QLabel {
                            color: #ECF0F1;
                            font-size: 14px;
                        }
                        QPushButton {
                            background-color: #3498DB;
                            color: white;
                            border: none;
                            padding: 8px 16px;
                            border-radius: 4px;
                            font-size: 14px;
                            min-width: 80px;
                        }
                        QPushButton:hover {
                            background-color: #2980B9;
                        }
                    """)
                    msg.exec_()
            elif action == delete_action:
                current_row = table.currentRow()
                if current_row >= 0:
                    record_id = records[current_row]['id']
                    if self.history_manager.delete_record(record_id):
                        table.removeRow(current_row)
                        records.pop(current_row)
        
        table.customContextMenuRequested.connect(show_context_menu)
        # 获取历史记录
        records = self.history_manager.get_recent_records(limit=50)
        table.setRowCount(len(records))
        
        # 填充数据
        for i, record in enumerate(records):
            table.setItem(i, 0, QTableWidgetItem(record['password']))
            table.setItem(i, 1, QTableWidgetItem(str(record['length'])))
            table.setItem(i, 2, QTableWidgetItem(f"{record['strength']}%"))
            table.setItem(i, 3, QTableWidgetItem(f"{record['entropy']} bits"))
            table.setItem(i, 4, QTableWidgetItem(record['created_at']))
        
        # 按钮区域
        buttons_layout = QHBoxLayout()
        delete_btn = QPushButton("删除选中")
        clear_btn = QPushButton("清空记录")
        
        def delete_selected():
            selected_rows = set(item.row() for item in table.selectedItems())
            for row in sorted(selected_rows, reverse=True):
                record_id = records[row]['id']
                if self.history_manager.delete_record(record_id):
                    table.removeRow(row)
                    records.pop(row)
        
        def clear_all():
            if QMessageBox.question(dialog, "确认", "确定要清空所有历史记录吗？") == QMessageBox.Yes:
                for record in records:
                    self.history_manager.delete_record(record['id'])
                table.setRowCount(0)
                records.clear()
        
        delete_btn.clicked.connect(delete_selected)
        clear_btn.clicked.connect(clear_all)
        
        buttons_layout.addWidget(delete_btn)
        buttons_layout.addWidget(clear_btn)
        
        layout.addWidget(table)
        layout.addLayout(buttons_layout)
        
        dialog.exec_()