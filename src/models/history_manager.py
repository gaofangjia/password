import sqlite3
from datetime import datetime
from typing import List, Dict
from pathlib import Path

class HistoryManager:
    def __init__(self):
        # 确保数据目录存在
        data_dir = Path.home() / '.password_generator'
        data_dir.mkdir(exist_ok=True)
        
        # 数据库文件路径
        self.db_path = data_dir / 'history.db'
        
        # 初始化数据库
        self._init_database()
    
    def _init_database(self):
        """初始化数据库表结构"""
        with sqlite3.connect(str(self.db_path)) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS password_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    password TEXT NOT NULL,
                    length INTEGER NOT NULL,
                    strength INTEGER NOT NULL,
                    entropy REAL NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expiry_date TIMESTAMP
                )
            """)
            conn.commit()
    
    def add_record(self, 
                   password: str, 
                   length: int, 
                   strength: int, 
                   entropy: float,
                   expiry_date: datetime = None) -> bool:
        """添加新的密码记录"""
        try:
            with sqlite3.connect(str(self.db_path)) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO password_history 
                    (password, length, strength, entropy, expiry_date)
                    VALUES (?, ?, ?, ?, ?)
                """, (password, length, strength, entropy, expiry_date))
                conn.commit()
                return True
        except sqlite3.Error:
            return False

if __name__ == "__main__":
    # 测试 HistoryManager 类
    manager = HistoryManager()

    print("初始化 HistoryManager 完成.")
    print(f"数据库文件位于: {manager.db_path}")

    # 添加一些记录
    print("\n添加测试记录...")
    manager.add_record("test_password1", 12, 3, 80.5)
    manager.add_record("securepass123", 10, 4, 95.1, datetime(2024, 12, 31))
    print("测试记录添加完成.")

    # 获取最近的记录
    print("\n获取最近的10条记录:")
    recent_records = manager.get_recent_records(10)
    if recent_records:
        for record in recent_records:
            print(record)
    else:
        print("没有找到记录.")

    # 获取一条记录的 ID 用于删除测试 (假设第一条是我们刚添加的)
    if recent_records:
        record_to_delete_id = recent_records[0]['id']
        print(f"\n尝试删除记录 ID: {record_to_delete_id}...")
        if manager.delete_record(record_to_delete_id):
            print(f"记录 ID: {record_to_delete_id} 删除成功.")
        else:
            print(f"记录 ID: {record_to_delete_id} 删除失败.")
        
        print("\n再次获取最近的10条记录 (删除后):")
        updated_records = manager.get_recent_records(10)
        if updated_records:
            for record in updated_records:
                print(record)
        else:
            print("没有找到记录.")

    # 清空历史记录 (可选，如果需要保持数据则注释掉)
    # print("\n清空所有历史记录...")
    # if manager.clear_history():
    #     print("历史记录已清空.")
    # else:
    #     print("清空历史记录失败.")

    # print("\n再次获取记录 (清空后):")
    # final_records = manager.get_recent_records()
    # if not final_records:
    #     print("历史记录为空.")
    # else:
    #     for record in final_records:
    #         print(record)

    print("\n测试完成.")

    
    def get_recent_records(self, limit: int = 10) -> List[Dict]:
        """获取最近的密码记录"""
        with sqlite3.connect(str(self.db_path)) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM password_history
                ORDER BY created_at DESC
                LIMIT ?
            """, (limit,))
            
            records = []
            for row in cursor.fetchall():
                record = dict(row)
                records.append(record)
            
            return records
    
    def clear_history(self) -> bool:
        """清空历史记录"""
        try:
            with sqlite3.connect(str(self.db_path)) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM password_history")
                conn.commit()
                return True
        except sqlite3.Error:
            return False

if __name__ == "__main__":
    # 测试 HistoryManager 类
    manager = HistoryManager()

    print("初始化 HistoryManager 完成.")
    print(f"数据库文件位于: {manager.db_path}")

    # 添加一些记录
    print("\n添加测试记录...")
    manager.add_record("test_password1", 12, 3, 80.5)
    manager.add_record("securepass123", 10, 4, 95.1, datetime(2024, 12, 31))
    print("测试记录添加完成.")

    # 获取最近的记录
    print("\n获取最近的10条记录:")
    recent_records = manager.get_recent_records(10)
    if recent_records:
        for record in recent_records:
            print(record)
    else:
        print("没有找到记录.")

    # 获取一条记录的 ID 用于删除测试 (假设第一条是我们刚添加的)
    if recent_records:
        record_to_delete_id = recent_records[0]['id']
        print(f"\n尝试删除记录 ID: {record_to_delete_id}...")
        if manager.delete_record(record_to_delete_id):
            print(f"记录 ID: {record_to_delete_id} 删除成功.")
        else:
            print(f"记录 ID: {record_to_delete_id} 删除失败.")
        
        print("\n再次获取最近的10条记录 (删除后):")
        updated_records = manager.get_recent_records(10)
        if updated_records:
            for record in updated_records:
                print(record)
        else:
            print("没有找到记录.")

    # 清空历史记录 (可选，如果需要保持数据则注释掉)
    # print("\n清空所有历史记录...")
    # if manager.clear_history():
    #     print("历史记录已清空.")
    # else:
    #     print("清空历史记录失败.")

    # print("\n再次获取记录 (清空后):")
    # final_records = manager.get_recent_records()
    # if not final_records:
    #     print("历史记录为空.")
    # else:
    #     for record in final_records:
    #         print(record)

    print("\n测试完成.")

    
    def delete_record(self, record_id: int) -> bool:
        """删除指定的密码记录"""
        try:
            with sqlite3.connect(str(self.db_path)) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    DELETE FROM password_history
                    WHERE id = ?
                """, (record_id,))
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error:
            return False

if __name__ == "__main__":
    # 测试 HistoryManager 类
    manager = HistoryManager()

    print("初始化 HistoryManager 完成.")
    print(f"数据库文件位于: {manager.db_path}")

    # 添加一些记录
    print("\n添加测试记录...")
    manager.add_record("test_password1", 12, 3, 80.5)
    manager.add_record("securepass123", 10, 4, 95.1, datetime(2024, 12, 31))
    print("测试记录添加完成.")

    # 获取最近的记录
    print("\n获取最近的10条记录:")
    recent_records = manager.get_recent_records(10)
    if recent_records:
        for record in recent_records:
            print(record)
    else:
        print("没有找到记录.")

    # 获取一条记录的 ID 用于删除测试 (假设第一条是我们刚添加的)
    if recent_records:
        record_to_delete_id = recent_records[0]['id']
        print(f"\n尝试删除记录 ID: {record_to_delete_id}...")
        if manager.delete_record(record_to_delete_id):
            print(f"记录 ID: {record_to_delete_id} 删除成功.")
        else:
            print(f"记录 ID: {record_to_delete_id} 删除失败.")
        
        print("\n再次获取最近的10条记录 (删除后):")
        updated_records = manager.get_recent_records(10)
        if updated_records:
            for record in updated_records:
                print(record)
        else:
            print("没有找到记录.")

    # 清空历史记录 (可选，如果需要保持数据则注释掉)
    # print("\n清空所有历史记录...")
    # if manager.clear_history():
    #     print("历史记录已清空.")
    # else:
    #     print("清空历史记录失败.")

    # print("\n再次获取记录 (清空后):")
    # final_records = manager.get_recent_records()
    # if not final_records:
    #     print("历史记录为空.")
    # else:
    #     for record in final_records:
    #         print(record)

    print("\n测试完成.")