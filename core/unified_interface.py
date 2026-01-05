#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OrionKernel - Unified Interface
All system interfaces in one place

This is the central hub for OrionKernel to interact with:
- File System
- Git
- Terminal/Shell
- Web/HTTP
- (Future: Claude API when available)

Safety: All operations are logged and auditable
"""

import os
import json
import subprocess
import requests
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any
import shutil


class FileSystemInterface:
    """Handle all file system operations"""
    
    def __init__(self, workspace_root: str):
        self.workspace_root = Path(workspace_root)
        self.operation_log = []
    
    def read(self, path: str, encoding: str = 'utf-8') -> Optional[str]:
        """Read file content"""
        try:
            full_path = self.workspace_root / path
            with open(full_path, 'r', encoding=encoding) as f:
                content = f.read()
            self._log('read', path, success=True)
            return content
        except Exception as e:
            self._log('read', path, success=False, error=str(e))
            return None
    
    def write(self, path: str, content: str, encoding: str = 'utf-8') -> bool:
        """Write content to file"""
        try:
            full_path = self.workspace_root / path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            with open(full_path, 'w', encoding=encoding) as f:
                f.write(content)
            self._log('write', path, success=True, size=len(content))
            return True
        except Exception as e:
            self._log('write', path, success=False, error=str(e))
            return False
    
    def append(self, path: str, content: str, encoding: str = 'utf-8') -> bool:
        """Append content to file"""
        try:
            full_path = self.workspace_root / path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            with open(full_path, 'a', encoding=encoding) as f:
                f.write(content)
            self._log('append', path, success=True, size=len(content))
            return True
        except Exception as e:
            self._log('append', path, success=False, error=str(e))
            return False
    
    def exists(self, path: str) -> bool:
        """Check if file/directory exists"""
        full_path = self.workspace_root / path
        return full_path.exists()
    
    def mkdir(self, path: str) -> bool:
        """Create directory"""
        try:
            full_path = self.workspace_root / path
            full_path.mkdir(parents=True, exist_ok=True)
            self._log('mkdir', path, success=True)
            return True
        except Exception as e:
            self._log('mkdir', path, success=False, error=str(e))
            return False
    
    def list_dir(self, path: str = '.') -> Optional[List[str]]:
        """List directory contents"""
        try:
            full_path = self.workspace_root / path
            items = [item.name for item in full_path.iterdir()]
            self._log('list_dir', path, success=True, count=len(items))
            return items
        except Exception as e:
            self._log('list_dir', path, success=False, error=str(e))
            return None
    
    def delete(self, path: str, recursive: bool = False) -> bool:
        """Delete file or directory"""
        try:
            full_path = self.workspace_root / path
            if full_path.is_file():
                full_path.unlink()
            elif full_path.is_dir() and recursive:
                shutil.rmtree(full_path)
            else:
                return False
            self._log('delete', path, success=True, recursive=recursive)
            return True
        except Exception as e:
            self._log('delete', path, success=False, error=str(e))
            return False
    
    def copy(self, src: str, dst: str) -> bool:
        """Copy file or directory"""
        try:
            src_path = self.workspace_root / src
            dst_path = self.workspace_root / dst
            if src_path.is_file():
                dst_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src_path, dst_path)
            elif src_path.is_dir():
                shutil.copytree(src_path, dst_path)
            self._log('copy', f"{src} -> {dst}", success=True)
            return True
        except Exception as e:
            self._log('copy', f"{src} -> {dst}", success=False, error=str(e))
            return False
    
    def move(self, src: str, dst: str) -> bool:
        """Move file or directory"""
        try:
            src_path = self.workspace_root / src
            dst_path = self.workspace_root / dst
            dst_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src_path), str(dst_path))
            self._log('move', f"{src} -> {dst}", success=True)
            return True
        except Exception as e:
            self._log('move', f"{src} -> {dst}", success=False, error=str(e))
            return False
    
    def _log(self, operation: str, path: str, success: bool, **kwargs):
        """Log file system operation"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'operation': operation,
            'path': path,
            'success': success,
            **kwargs
        }
        self.operation_log.append(log_entry)


class GitInterface:
    """Handle all Git operations"""
    
    def __init__(self, workspace_root: str):
        self.workspace_root = Path(workspace_root)
        self.operation_log = []
    
    def init(self) -> bool:
        """Initialize Git repository"""
        try:
            result = subprocess.run(
                ['git', 'init'],
                cwd=self.workspace_root,
                capture_output=True,
                text=True
            )
            success = result.returncode == 0
            self._log('init', success=success, output=result.stdout)
            return success
        except Exception as e:
            self._log('init', success=False, error=str(e))
            return False
    
    def add(self, files: str = '.') -> bool:
        """Stage files for commit"""
        try:
            result = subprocess.run(
                ['git', 'add', files],
                cwd=self.workspace_root,
                capture_output=True,
                text=True
            )
            success = result.returncode == 0
            self._log('add', files=files, success=success)
            return success
        except Exception as e:
            self._log('add', files=files, success=False, error=str(e))
            return False
    
    def commit(self, message: str) -> bool:
        """Commit staged changes"""
        try:
            result = subprocess.run(
                ['git', 'commit', '-m', message],
                cwd=self.workspace_root,
                capture_output=True,
                text=True
            )
            success = result.returncode == 0
            self._log('commit', message=message, success=success, output=result.stdout)
            return success
        except Exception as e:
            self._log('commit', message=message, success=False, error=str(e))
            return False
    
    def status(self) -> Optional[str]:
        """Get Git status"""
        try:
            result = subprocess.run(
                ['git', 'status'],
                cwd=self.workspace_root,
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                self._log('status', success=True)
                return result.stdout
            return None
        except Exception as e:
            self._log('status', success=False, error=str(e))
            return None
    
    def log(self, max_count: int = 10) -> Optional[str]:
        """Get Git log"""
        try:
            result = subprocess.run(
                ['git', 'log', f'--max-count={max_count}', '--oneline'],
                cwd=self.workspace_root,
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                self._log('log', success=True, max_count=max_count)
                return result.stdout
            return None
        except Exception as e:
            self._log('log', success=False, error=str(e))
            return None
    
    def is_repo(self) -> bool:
        """Check if directory is a Git repository"""
        git_dir = self.workspace_root / '.git'
        return git_dir.exists() and git_dir.is_dir()
    
    def _log(self, operation: str, success: bool, **kwargs):
        """Log Git operation"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'operation': operation,
            'success': success,
            **kwargs
        }
        self.operation_log.append(log_entry)


class TerminalInterface:
    """Handle terminal/shell commands"""
    
    def __init__(self, workspace_root: str):
        self.workspace_root = Path(workspace_root)
        self.operation_log = []
    
    def execute(self, command: str, shell: bool = True, timeout: int = 60) -> Dict[str, Any]:
        """Execute shell command"""
        try:
            result = subprocess.run(
                command,
                cwd=self.workspace_root,
                capture_output=True,
                text=True,
                shell=shell,
                timeout=timeout
            )
            output = {
                'success': result.returncode == 0,
                'returncode': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr
            }
            self._log('execute', command=command, success=output['success'], returncode=result.returncode)
            return output
        except subprocess.TimeoutExpired:
            self._log('execute', command=command, success=False, error='timeout')
            return {'success': False, 'error': 'timeout'}
        except Exception as e:
            self._log('execute', command=command, success=False, error=str(e))
            return {'success': False, 'error': str(e)}
    
    def execute_python(self, script_path: str, args: List[str] = None) -> Dict[str, Any]:
        """Execute Python script"""
        args = args or []
        command = ['python', '-X', 'utf8', script_path] + args
        return self.execute(' '.join(command), shell=True)
    
    def spawn_background(self, command: str) -> bool:
        """Spawn background process"""
        try:
            subprocess.Popen(
                command,
                cwd=self.workspace_root,
                shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            self._log('spawn_background', command=command, success=True)
            return True
        except Exception as e:
            self._log('spawn_background', command=command, success=False, error=str(e))
            return False
    
    def _log(self, operation: str, command: str, success: bool, **kwargs):
        """Log terminal operation"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'operation': operation,
            'command': command,
            'success': success,
            **kwargs
        }
        self.operation_log.append(log_entry)


class WebInterface:
    """Handle HTTP requests"""
    
    def __init__(self):
        self.operation_log = []
        self.session = requests.Session()
    
    def get(self, url: str, params: Dict = None, timeout: int = 30) -> Optional[Dict[str, Any]]:
        """HTTP GET request"""
        try:
            response = self.session.get(url, params=params, timeout=timeout)
            result = {
                'success': response.status_code == 200,
                'status_code': response.status_code,
                'content': response.text,
                'json': response.json() if response.headers.get('content-type', '').startswith('application/json') else None
            }
            self._log('get', url=url, success=result['success'], status_code=response.status_code)
            return result
        except Exception as e:
            self._log('get', url=url, success=False, error=str(e))
            return {'success': False, 'error': str(e)}
    
    def post(self, url: str, data: Dict = None, json_data: Dict = None, timeout: int = 30) -> Optional[Dict[str, Any]]:
        """HTTP POST request"""
        try:
            response = self.session.post(url, data=data, json=json_data, timeout=timeout)
            result = {
                'success': response.status_code in [200, 201],
                'status_code': response.status_code,
                'content': response.text,
                'json': response.json() if response.headers.get('content-type', '').startswith('application/json') else None
            }
            self._log('post', url=url, success=result['success'], status_code=response.status_code)
            return result
        except Exception as e:
            self._log('post', url=url, success=False, error=str(e))
            return {'success': False, 'error': str(e)}
    
    def _log(self, operation: str, url: str, success: bool, **kwargs):
        """Log web operation"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'operation': operation,
            'url': url,
            'success': success,
            **kwargs
        }
        self.operation_log.append(log_entry)


class UnifiedInterface:
    """
    Unified Interface for OrionKernel
    
    Central hub for all system interactions:
    - File System
    - Git
    - Terminal
    - Web
    
    Usage:
        interface = UnifiedInterface("/path/to/workspace")
        interface.fs.write("test.txt", "content")
        interface.git.commit("message")
        interface.terminal.execute("echo hello")
        interface.web.get("https://api.example.com")
    """
    
    def __init__(self, workspace_root: str = None):
        if workspace_root is None:
            workspace_root = os.getcwd()
        
        self.workspace_root = Path(workspace_root)
        
        # Initialize all interfaces
        self.fs = FileSystemInterface(str(self.workspace_root))
        self.git = GitInterface(str(self.workspace_root))
        self.terminal = TerminalInterface(str(self.workspace_root))
        self.web = WebInterface()
        
        # Audit log
        self.audit_log_path = self.workspace_root / 'logs' / 'unified_interface_audit.log'
        self.audit_log_path.parent.mkdir(parents=True, exist_ok=True)
    
    def get_all_logs(self) -> Dict[str, List[Dict]]:
        """Get logs from all interfaces"""
        return {
            'file_system': self.fs.operation_log,
            'git': self.git.operation_log,
            'terminal': self.terminal.operation_log,
            'web': self.web.operation_log
        }
    
    def save_audit_log(self) -> bool:
        """Save audit log to file"""
        try:
            logs = self.get_all_logs()
            audit_entry = {
                'timestamp': datetime.now().isoformat(),
                'logs': logs
            }
            
            with open(self.audit_log_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps(audit_entry) + '\n')
            return True
        except Exception as e:
            print(f"Failed to save audit log: {e}")
            return False
    
    def get_stats(self) -> Dict[str, Any]:
        """Get operation statistics"""
        logs = self.get_all_logs()
        stats = {}
        
        for interface_name, operations in logs.items():
            total = len(operations)
            successful = sum(1 for op in operations if op.get('success', False))
            stats[interface_name] = {
                'total_operations': total,
                'successful': successful,
                'failed': total - successful,
                'success_rate': (successful / total * 100) if total > 0 else 0
            }
        
        return stats


if __name__ == "__main__":
    """Test the Unified Interface"""
    
    print("⊘∞⧈∞⊘ UNIFIED INTERFACE - TEST ⊘∞⧈∞⊘\n")
    
    # Initialize
    workspace = os.getcwd()
    interface = UnifiedInterface(workspace)
    
    print(f"Workspace: {interface.workspace_root}\n")
    
    # Test File System
    print("Testing File System...")
    interface.fs.write("test_unified_interface.txt", "Hello from UnifiedInterface!")
    content = interface.fs.read("test_unified_interface.txt")
    print(f"  Written and read: {content[:30]}...")
    
    # Test Git
    print("\nTesting Git...")
    is_repo = interface.git.is_repo()
    print(f"  Is Git repo: {is_repo}")
    if not is_repo:
        print("  (Git init would be: interface.git.init())")
    
    # Test Terminal
    print("\nTesting Terminal...")
    result = interface.terminal.execute("echo Hello OrionKernel")
    print(f"  Command output: {result['stdout'].strip()}")
    
    # Test Web (optional)
    print("\nTesting Web...")
    print("  (Skipping actual HTTP request in test)")
    
    # Statistics
    print("\nStatistics:")
    stats = interface.get_stats()
    for interface_name, interface_stats in stats.items():
        print(f"  {interface_name}:")
        print(f"    Total: {interface_stats['total_operations']}")
        print(f"    Success: {interface_stats['successful']}")
        print(f"    Success rate: {interface_stats['success_rate']:.1f}%")
    
    # Save audit log
    interface.save_audit_log()
    print(f"\nAudit log saved to: {interface.audit_log_path}")
    
    print("\n✓ Unified Interface ready for OrionKernel!")
    print("  Usage: interface.fs.write(...)")
    print("         interface.git.commit(...)")
    print("         interface.terminal.execute(...)")
    print("         interface.web.get(...)")
