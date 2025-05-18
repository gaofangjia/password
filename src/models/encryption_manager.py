from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from base64 import b64encode, b64decode
from pathlib import Path
from typing import Optional
import os

class EncryptionManager:
    def __init__(self):
        # 确保数据目录存在
        self.data_dir = Path.home() / '.password_generator'
        self.data_dir.mkdir(exist_ok=True)
        
        # 密钥文件路径
        self.key_file = self.data_dir / 'master.key'
        
        # 初始化或加载密钥
        self._init_key()
        
    def _init_key(self):
        """初始化或加载主密钥"""
        if not self.key_file.exists():
            # 生成新的密钥
            key = Fernet.generate_key()
            # 保存密钥
            with open(self.key_file, 'wb') as f:
                f.write(key)
        else:
            # 加载现有密钥
            with open(self.key_file, 'rb') as f:
                key = f.read()
                
        self.fernet = Fernet(key)
    
    def encrypt_password(self, password: str) -> str:
        """加密密码"""
        try:
            encrypted = self.fernet.encrypt(password.encode())
            return b64encode(encrypted).decode()
        except Exception as e:
            raise ValueError(f"加密失败：{str(e)}")
    
    def decrypt_password(self, encrypted_password: str) -> str:
        """解密密码"""
        try:
            decrypted = self.fernet.decrypt(b64decode(encrypted_password))
            return decrypted.decode()
        except Exception as e:
            raise ValueError(f"解密失败：{str(e)}")
    
    def save_password_to_file(self, 
                             password: str, 
                             file_path: str, 
                             master_password: Optional[str] = None) -> bool:
        """将密码保存到加密文件"""
        try:
            # 如果提供了主密码，使用它来生成新的加密密钥
            if master_password:
                salt = os.urandom(16)
                kdf = PBKDF2HMAC(
                    algorithm=hashes.SHA256(),
                    length=32,
                    salt=salt,
                    iterations=100000,
                )
                key = b64encode(kdf.derive(master_password.encode()))
                fernet = Fernet(key)
                encrypted = fernet.encrypt(password.encode())
            else:
                # 使用默认密钥
                encrypted = self.fernet.encrypt(password.encode())
            
            # 保存加密后的密码
            with open(file_path, 'wb') as f:
                if master_password:
                    # 如果使用主密码，需要保存salt
                    f.write(salt)
                f.write(encrypted)
                
            return True
        except Exception:
            return False
    
    def load_password_from_file(self, 
                               file_path: str, 
                               master_password: Optional[str] = None) -> Optional[str]:
        """从加密文件加载密码"""
        try:
            with open(file_path, 'rb') as f:
                if master_password:
                    # 读取salt
                    salt = f.read(16)
                    # 重新生成密钥
                    kdf = PBKDF2HMAC(
                        algorithm=hashes.SHA256(),
                        length=32,
                        salt=salt,
                        iterations=100000,
                    )
                    key = b64encode(kdf.derive(master_password.encode()))
                    fernet = Fernet(key)
                    encrypted = f.read()
                    decrypted = fernet.decrypt(encrypted)
                else:
                    # 使用默认密钥
                    encrypted = f.read()
                    decrypted = self.fernet.decrypt(encrypted)
                
                return decrypted.decode()
        except Exception:
            return None