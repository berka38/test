import ast
import re
from typing import List, Tuple

class SecurityChecker:
    """
    Security checker for command installations.
    Checks Python code for potentially dangerous operations.
    """
    
    DANGEROUS_IMPORTS = [
        'os', 'sys', 'subprocess', 'shutil', 'pathlib',
        'pickle', 'marshal', 'shelve',
        'socket', 'requests', 'urllib',
    ]
    
    DANGEROUS_FUNCTIONS = [
        'eval', 'exec', 'compile', '__import__',
        'open', 'file', 'input', 'raw_input'
    ]
    
    def __init__(self, code: str):
        self.code = code
        self.warnings: List[str] = []
        
    def check_code(self) -> Tuple[bool, List[str]]:
        """
        Check code for potential security issues.
        Returns (is_safe, warnings)
        """
        try:
            tree = ast.parse(self.code)
            
            # Check imports
            self._check_imports(tree)
            
            # Check function calls
            self._check_calls(tree)
            
            # Check string patterns
            self._check_patterns()
            
            return len(self.warnings) == 0, self.warnings
            
        except SyntaxError:
            self.warnings.append("❌ Code contains syntax errors")
            return False, self.warnings
            
    def _check_imports(self, tree: ast.AST):
        """Check for dangerous imports"""
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for name in node.names:
                    if any(name.name.startswith(imp) for imp in self.DANGEROUS_IMPORTS):
                        self.warnings.append(f"⚠️ Dangerous import: {name.name}")
            
            elif isinstance(node, ast.ImportFrom):
                if any(node.module.startswith(imp) for imp in self.DANGEROUS_IMPORTS):
                    self.warnings.append(f"⚠️ Dangerous import: {node.module}")
    
    def _check_calls(self, tree: ast.AST):
        """Check for dangerous function calls"""
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    if node.func.id in self.DANGEROUS_FUNCTIONS:
                        self.warnings.append(f"⚠️ Dangerous function call: {node.func.id}()")
                elif isinstance(node.func, ast.Attribute):
                    if node.func.attr in self.DANGEROUS_FUNCTIONS:
                        self.warnings.append(f"⚠️ Dangerous method call: {node.func.attr}()")
    
    def _check_patterns(self):
        """Check for suspicious patterns in code"""
        patterns = [
            (r'subprocess\.', "subprocess usage"),
            (r'os\.system', "system command execution"),
            (r'__[a-zA-Z]+__', "magic method usage"),
            (r'lambda', "lambda function"),
            (r'globals\(\)', "globals() access"),
            (r'locals\(\)', "locals() access"),
        ]
        
        for pattern, warning in patterns:
            if re.search(pattern, self.code):
                self.warnings.append(f"⚠️ Suspicious pattern: {warning}")

    def format_warnings(self) -> str:
        """Format warnings into a readable message"""
        return "\n".join(self.warnings)
