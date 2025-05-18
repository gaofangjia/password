import secrets
import string
from typing import List, Set
from zxcvbn import zxcvbn

class PasswordGenerator:
    def __init__(self):
        self.uppercase_letters = string.ascii_uppercase
        self.lowercase_letters = string.ascii_lowercase
        self.digits = string.digits
        self.special_chars = '!@#$%^&*'
        
    def generate_passwords(self, 
                          length: int = 16, 
                          count: int = 3,
                          use_uppercase: bool = True,
                          use_lowercase: bool = True,
                          use_digits: bool = True,
                          use_special: bool = True) -> List[str]:
        # 验证参数
        if length < 12 or length > 64:
            raise ValueError("密码长度必须在12-64位之间")
        if count < 1 or count > 10:
            raise ValueError("密码数量必须在1-10个之间")
            
        # 确保至少选择两种字符类型
        char_types = [use_uppercase, use_lowercase, use_digits, use_special]
        if sum(char_types) < 2:
            raise ValueError("至少需要选择两种字符类型")
            
        # 构建字符集
        chars = ''
        if use_uppercase:
            chars += self.uppercase_letters
        if use_lowercase:
            chars += self.lowercase_letters
        if use_digits:
            chars += self.digits
        if use_special:
            chars += self.special_chars
            
        passwords = []
        for _ in range(count):
            while True:
                # 生成密码
                password = ''.join(secrets.choice(chars) for _ in range(length))
                # 确保密码包含所有选择的字符类型
                if self._validate_password(password, use_uppercase, use_lowercase, use_digits, use_special):
                    passwords.append(password)
                    break
                    
        return passwords
    
    def _validate_password(self, 
                          password: str,
                          use_uppercase: bool,
                          use_lowercase: bool,
                          use_digits: bool,
                          use_special: bool) -> bool:
        has_upper = any(c in self.uppercase_letters for c in password)
        has_lower = any(c in self.lowercase_letters for c in password)
        has_digit = any(c in self.digits for c in password)
        has_special = any(c in self.special_chars for c in password)
        
        if use_uppercase and not has_upper:
            return False
        if use_lowercase and not has_lower:
            return False
        if use_digits and not has_digit:
            return False
        if use_special and not has_special:
            return False
            
        return True
    
    def check_password_strength(self, password: str) -> dict:
        """使用zxcvbn检查密码强度"""
        return zxcvbn(password)
    
    def calculate_entropy(self, password: str) -> float:
        """计算密码熵值"""
        char_set: Set[str] = set(password)
        char_space = len(char_set)
        password_length = len(password)
        
        if char_space == 0 or password_length == 0:
            return 0.0
            
        # 使用信息熵公式：H = L * log2(N)
        # 其中L是密码长度，N是字符集大小
        import math
        entropy = password_length * math.log2(char_space)
        return round(entropy, 2)