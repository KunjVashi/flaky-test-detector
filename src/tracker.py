import sqlite3
import time
from datetime import datetime
from pathlib import Path

class TestResultTracker:
    """Tracks test execution results and stores them in a database."""
    
    def __init__(self, db_path="database/test_results.db"):
        """Initialize the tracker and create database if needed."""
        self.db_path = db_path
        
        # Create database directory if it doesn't exist
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize database
        self._init_database()
    
    def _init_database(self):
        """Create the database table if it doesn't exist."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS test_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                test_name TEXT NOT NULL,
                result TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                duration REAL,
                error_message TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_result(self, test_name, result, duration, error_message=None):
        """Add a test result to the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO test_results (test_name, result, timestamp, duration, error_message)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            test_name,
            result,
            datetime.now().isoformat(),
            duration,
            error_message
        ))
        
        conn.commit()
        conn.close()
    
    def get_flake_rate(self, test_name):
        """Calculate the flake rate for a specific test."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get total runs
        cursor.execute('SELECT COUNT(*) FROM test_results WHERE test_name = ?', (test_name,))
        total_runs = cursor.fetchone()[0]
        
        if total_runs == 0:
            return 0.0
        
        # Get failed runs
        cursor.execute('SELECT COUNT(*) FROM test_results WHERE test_name = ? AND result = "FAILED"', (test_name,))
        failed_runs = cursor.fetchone()[0]
        
        conn.close()
        
        # Calculate flake rate
        flake_rate = (failed_runs / total_runs) * 100
        return round(flake_rate, 2)
    
    def get_all_tests(self):
        """Get a list of all unique test names in the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT DISTINCT test_name FROM test_results')
        tests = [row[0] for row in cursor.fetchall()]
        
        conn.close()
        return tests
    
    def get_summary(self):
        """Generate a summary report of all tests."""
        tests = self.get_all_tests()
        
        summary = []
        for test in tests:
            flake_rate = self.get_flake_rate(test)
            
            # Classify flakiness
            if flake_rate == 0:
                classification = "✅ STABLE"
            elif flake_rate <= 10:
                classification = "⚠️  SLIGHTLY FLAKY"
            elif flake_rate <= 40:
                classification = "🟡 MODERATELY FLAKY"
            elif flake_rate <= 60:
                classification = "🟠 HIGHLY FLAKY"
            elif flake_rate < 100:
                classification = "🔴 SEVERELY FLAKY"
            else:
                classification = "💀 BROKEN"
            
            summary.append({
                'test_name': test,
                'flake_rate': flake_rate,
                'classification': classification
            })
        
        # Sort by flake rate (highest first)
        summary.sort(key=lambda x: x['flake_rate'], reverse=True)
        
        return summary
    
    def clear_database(self):
        """Clear all test results from the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM test_results')
        conn.commit()
        conn.close()