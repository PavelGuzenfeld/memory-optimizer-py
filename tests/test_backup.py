"""
Tests for the backup functionality.
"""

import unittest
import tempfile
import shutil
import time
from pathlib import Path

from memory_optimizer.backup import BackupManager

class TestBackupManager(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.backup_manager = BackupManager()
        
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
        
    def test_create_backup(self):
        """Test backup creation."""
        # Create a test file
        test_file = Path(self.temp_dir) / "test.py"
        test_file.write_text("print('hello')")
        
        # Create backup
        backup_path = self.backup_manager.create_backup(test_file)
        
        # Check backup exists
        self.assertTrue(backup_path.exists())
        self.assertEqual(backup_path.read_text(), "print('hello')")
        
    def test_restore_backup(self):
        """Test backup restoration."""
        # Create test file and backup
        test_file = Path(self.temp_dir) / "test.py"
        test_file.write_text("print('hello')")
        backup_path = self.backup_manager.create_backup(test_file)
        
        # Modify original file
        test_file.write_text("print('modified')")
        
        # Restore from backup
        self.backup_manager.restore_backup(test_file, backup_path)
        
        # Check file is restored
        self.assertEqual(test_file.read_text(), "print('hello')")
        
    def test_find_latest_backup(self):
        """Test finding the latest backup."""
        # Create test file
        test_file = Path(self.temp_dir) / "test.py"
        test_file.write_text("print('hello')")
        
        # Create multiple backups
        backup1 = self.backup_manager.create_backup(test_file)
        time.sleep(0.1)  # Ensure different timestamps
        backup2 = self.backup_manager.create_backup(test_file)
        
        # Find latest backup
        latest = self.backup_manager.find_latest_backup(test_file)
        
        # Check correct backup is found
        self.assertEqual(latest, backup2)