"""
Backup management for the Memory Optimizer tool.
"""

import shutil
from pathlib import Path
from datetime import datetime
from typing import Optional

class BackupManager:
    """Manages backup creation and restoration."""
    
    def __init__(self, backup_dir: Optional[str] = None):
        self.backup_dir = Path(backup_dir) if backup_dir else None
    
    def create_backup(self, file_path: Path) -> Path:
        """Create a backup of the given file."""
        # Create backup filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{file_path.stem}.{timestamp}.bak.py"
        
        # Determine backup location
        if self.backup_dir:
            backup_path = self.backup_dir / backup_name
            self.backup_dir.mkdir(parents=True, exist_ok=True)
        else:
            backup_path = file_path.parent / backup_name
        
        # Copy file
        shutil.copy2(file_path, backup_path)
        return backup_path
    
    def restore_backup(self, original_path: Path, backup_path: Path) -> None:
        """Restore a file from backup."""
        shutil.copy2(backup_path, original_path)
    
    def find_latest_backup(self, original_path: Path) -> Optional[Path]:
        """Find the most recent backup for a file."""
        pattern = f"{original_path.stem}.*.bak.py"
        
        # Search in backup directory or original directory
        search_dir = self.backup_dir if self.backup_dir else original_path.parent
        backups = list(search_dir.glob(pattern))
        
        if not backups:
            return None
        
        # Return most recent backup
        return max(backups, key=lambda p: p.stat().st_mtime)