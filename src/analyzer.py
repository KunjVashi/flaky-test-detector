import ast
import code
import os
from pathlib import Path

class FlakyTestAnalyzer:
    """Analyzes test code to detect potential flakiness root causes."""
    
    def __init__(self, test_directory="tests"):
        self.test_directory = test_directory
        self.patterns = {
            'timing_issues': [],
            'external_dependencies': [],
            'race_conditions': [],
            'shared_state': [],
            'resource_issues': []
        }
    
    def analyze_test_file(self, filepath):
        """Analyze a single test file for flakiness patterns."""
        with open(filepath, 'r') as f:
            code = f.read()
        
        try:
            tree = ast.parse(code)
            results = {
                'timing_issues': self._detect_timing_issues(tree, filepath),
                'external_dependencies': self._detect_external_deps(tree, filepath),
                'race_conditions': self._detect_race_conditions(tree, filepath),
                'shared_state': self._detect_shared_state(tree, filepath),
                'resource_issues': self._detect_resource_issues(tree, filepath)
            }
            return results
        except SyntaxError:
            return None
    
    def _detect_timing_issues(self, tree, filepath):
        """Detect time.sleep() and fixed waits."""
        issues = []
        
        for node in ast.walk(tree):
            # Detect time.sleep()
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute):
                    if (isinstance(node.func.value, ast.Name) and 
                        node.func.value.id == 'time' and 
                        node.func.attr == 'sleep'):
                        
                        # Get the sleep duration if it's a constant
                        duration = "unknown"
                        if node.args and isinstance(node.args[0], ast.Constant):
                            duration = node.args[0].value
                        
                        issues.append({
                            'type': 'fixed_wait',
                            'pattern': f'time.sleep({duration})',
                            'line': node.lineno,
                            'severity': 'HIGH',
                            'description': f'Fixed wait of {duration} seconds - should use explicit waits',
                            'suggestion': 'Replace with WebDriverWait or dynamic polling'
                        })
        
        return issues
    
    def _detect_external_deps(self, tree, filepath):
        """Detect external API calls and network operations."""
        issues = []
        
        external_modules = ['requests', 'urllib', 'http', 'httpx', 'aiohttp']
        
        for node in ast.walk(tree):
            # Detect requests.get/post etc
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute):
                    if isinstance(node.func.value, ast.Name):
                        if node.func.value.id in external_modules:
                            issues.append({
                                'type': 'external_api',
                                'pattern': f'{node.func.value.id}.{node.func.attr}()',
                                'line': node.lineno,
                                'severity': 'MEDIUM',
                                'description': 'External API call detected - network dependent',
                                'suggestion': 'Mock external calls or add retry logic with timeouts'
                            })
        
        return issues
    
    def _detect_race_conditions(self, tree, filepath):
        """Detect threading and async operations."""
        issues = []
        
        for node in ast.walk(tree):
            # Detect threading
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if 'threading' in alias.name or 'asyncio' in alias.name:
                        issues.append({
                            'type': 'async_operation',
                            'pattern': f'import {alias.name}',
                            'line': node.lineno,
                            'severity': 'HIGH',
                            'description': 'Async/threading operations can cause race conditions',
                            'suggestion': 'Use synchronization primitives or avoid shared state'
                        })
            
            # Detect random module usage
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute):
                    if (isinstance(node.func.value, ast.Name) and 
                        node.func.value.id == 'random'):
                        issues.append({
                            'type': 'random_behavior',
                            'pattern': f'random.{node.func.attr}()',
                            'line': node.lineno,
                            'severity': 'MEDIUM',
                            'description': 'Random values make tests non-deterministic',
                            'suggestion': 'Seed random for reproducibility or use fixed test data'
                        })
        
        return issues
    
    def _detect_shared_state(self, tree, filepath):
        """Detect global variables and class attributes."""
        issues = []
        
        for node in ast.walk(tree):
            # Detect global keyword
            if isinstance(node, ast.Global):
                issues.append({
                    'type': 'global_state',
                    'pattern': f'global {", ".join(node.names)}',
                    'line': node.lineno,
                    'severity': 'MEDIUM',
                    'description': 'Global variables can cause test interdependence',
                    'suggestion': 'Use fixtures or fresh instances for each test'
                })
        
        return issues
    
    def _detect_resource_issues(self, tree, filepath):
        """Detect file operations and resource handling."""
        issues = []
        
        for node in ast.walk(tree):
            # Detect file operations
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    if node.func.id == 'open':
                        issues.append({
                            'type': 'file_operation',
                            'pattern': 'open()',
                            'line': node.lineno,
                            'severity': 'LOW',
                            'description': 'File operations can fail due to permissions or state',
                            'suggestion': 'Use context managers (with statement) and cleanup fixtures'
                        })
        
        return issues
    
    def analyze_all_tests(self):
        """Analyze all test files in the test directory."""
        all_results = {}
        
        test_path = Path(self.test_directory)
        
        for test_file in test_path.glob('test_*.py'):
            results = self.analyze_test_file(test_file)
            if results:
                all_results[str(test_file)] = results
        
        return all_results
    
    def get_test_root_causes(self, test_name, test_file_path):
        """Get potential root causes for a specific test function."""
        with open(test_file_path, 'r') as f:
            code = f.read()
    
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return []
    
        # Find the specific test function
        test_function = None
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if node.name == test_name:
                    test_function = node
                    break
    
        if not test_function:
            return []
    
        # Analyze only this function
        all_issues = []
    
        # Detect patterns within this specific function
        for node in ast.walk(test_function):
            # Timing issues
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute):
                    # time.sleep()
                    if (isinstance(node.func.value, ast.Name) and 
                        node.func.value.id == 'time' and 
                        node.func.attr == 'sleep'):
                    
                        duration = "unknown"
                        if node.args and isinstance(node.args[0], ast.Constant):
                            duration = node.args[0].value
                    
                        all_issues.append({
                            'category': 'timing_issues',
                            'type': 'fixed_wait',
                            'pattern': f'time.sleep({duration})',
                            'line': node.lineno,
                            'severity': 'HIGH',
                            'description': f'Fixed wait of {duration} seconds',
                            'suggestion': 'Replace with WebDriverWait or dynamic polling'
                        })
                
                    # random calls
                    if isinstance(node.func.value, ast.Name) and node.func.value.id == 'random':
                        all_issues.append({
                            'category': 'race_conditions',
                            'type': 'random_behavior',
                            'pattern': f'random.{node.func.attr}()',
                            'line': node.lineno,
                            'severity': 'MEDIUM',
                            'description': 'Random values make tests non-deterministic',
                            'suggestion': 'Seed random for reproducibility or use fixed test data'
                        })
                
                    # External API calls
                    external_modules = ['requests', 'urllib', 'http', 'httpx', 'aiohttp']
                    if isinstance(node.func.value, ast.Name) and node.func.value.id in external_modules:
                        all_issues.append({
                            'category': 'external_dependencies',
                            'type': 'external_api',
                            'pattern': f'{node.func.value.id}.{node.func.attr}()',
                            'line': node.lineno,
                            'severity': 'MEDIUM',
                            'description': 'External API call detected',
                            'suggestion': 'Mock external calls or add retry logic'
                        })
        
            # Global variables
            if isinstance(node, ast.Global):
                all_issues.append({
                    'category': 'shared_state',
                    'type': 'global_state',
                    'pattern': f'global {", ".join(node.names)}',
                    'line': node.lineno,
                    'severity': 'MEDIUM',
                    'description': 'Global variables can cause test interdependence',
                    'suggestion': 'Use fixtures or fresh instances for each test'
                })
        
            # File operations
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id == 'open':
                    all_issues.append({
                        'category': 'resource_issues',
                        'type': 'file_operation',
                        'pattern': 'open()',
                        'line': node.lineno,
                        'severity': 'LOW',
                        'description': 'File operations can fail',
                        'suggestion': 'Use context managers and cleanup fixtures'
                    })
    
        # Check for threading/async imports (function-level imports)
        for node in ast.walk(test_function):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if 'threading' in alias.name or 'asyncio' in alias.name:
                        all_issues.append({
                            'category': 'race_conditions',
                            'type': 'async_operation',
                            'pattern': f'import {alias.name}',
                            'line': node.lineno,
                            'severity': 'HIGH',
                            'description': 'Async/threading can cause race conditions',
                            'suggestion': 'Use synchronization primitives'
                        })
    
        return all_issues
    
    def generate_analysis_report(self, flaky_tests):
        """Generate a comprehensive analysis report for flaky tests."""
        report = []
        
        for test_info in flaky_tests:
            test_name = test_info['test_name']
            flake_rate = test_info['flake_rate']
            
            # Find the test file
            test_file = self._find_test_file(test_name)
            
            if test_file:
                root_causes = self.get_test_root_causes(test_name, test_file)
                
                report.append({
                    'test_name': test_name,
                    'flake_rate': flake_rate,
                    'classification': test_info['classification'],
                    'root_causes': root_causes,
                    'file': str(test_file)
                })
            else:
                report.append({
                    'test_name': test_name,
                    'flake_rate': flake_rate,
                    'classification': test_info['classification'],
                    'root_causes': [],
                    'file': 'Not found'
                })
        
        return report
    
    def _find_test_file(self, test_name):
        """Find which file contains a specific test."""
        test_path = Path(self.test_directory)
        
        for test_file in test_path.glob('test_*.py'):
            with open(test_file, 'r') as f:
                content = f.read()
                if f'def {test_name}' in content:
                    return test_file
        
        return None
    