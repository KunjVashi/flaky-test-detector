# 🔍 Flaky Test Detector

> Intelligent tool to automatically detect, analyze, and diagnose flaky tests in automated test suites

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![pytest](https://img.shields.io/badge/pytest-latest-green.svg)
![Status](https://img.shields.io/badge/Status-Phase%201%20Complete-green.svg)

---

## 📋 Problem Statement

Flaky tests are automated tests that exhibit non-deterministic behavior - sometimes passing, sometimes failing without any code changes. They:
- Waste **50-70% of CI/CD reruns**
- Cost companies **millions in lost productivity**
- Erode trust in test automation
- Make it impossible to distinguish real bugs from false positives

**73% of test failures in large projects are caused by flaky tests, not actual bugs.**

---

## 💡 Solution

An intelligent tool that:
1. **Detects** flaky tests by running them 100+ times
2. **Calculates** statistical flake rates with precision
3. **Analyzes** root causes (timing issues, race conditions, external dependencies)
4. **Reports** actionable insights with fix recommendations
5. **Prioritizes** which tests need attention first

---

## 🚀 Current Progress

### ✅ Phase 1: Automated Detection (COMPLETE)
- Automated test execution runner
- SQLite database for result tracking
- Statistical flake rate calculation
- Classification system (Stable → Broken)
- Professional reporting dashboard

### 🔄 Coming Next
- Phase 2: Root cause analyzer
- Phase 3: Pattern recognition
- Phase 4: Web dashboard with Streamlit

---

## 🛠️ Tech Stack

- **Python 3.8+** - Core language
- **pytest** - Testing framework
- **Selenium** - Web automation testing
- **SQLite** - Data persistence
- **Streamlit** - Dashboard (upcoming)

---

## 📊 Example Output
```
============================================================
📊 FLAKINESS DETECTION REPORT
============================================================

🔴 SEVERELY FLAKY
Test: test_very_flaky
Flake Rate: 80.95%

🟠 HIGHLY FLAKY
Test: test_flaky_external_api
Flake Rate: 43.75%

✅ STABLE
Test: test_stable_always_passes
Flake Rate: 0.0%
============================================================
```

---

## 🎯 Key Features

### Flakiness Classification
- **0%** - ✅ Stable
- **1-10%** - ⚠️ Slightly Flaky
- **11-40%** - 🟡 Moderately Flaky
- **41-60%** - 🟠 Highly Flaky
- **61-99%** - 🔴 Severely Flaky
- **100%** - 💀 Broken

### Root Cause Categories (Planned)
1. **Timing Issues** (~40%) - Fixed waits, async operations
2. **Race Conditions** (~25%) - Unpredictable execution order
3. **External Dependencies** (~20%) - API calls, network issues
4. **Shared State** (~10%) - Tests affecting each other
5. **Resource Constraints** (~5%) - Disk, memory, permissions

---

## 🏃 Quick Start

### Prerequisites
```bash
python3 --version  # Python 3.8+
```

### Installation
```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/flaky-test-detector.git
cd flaky-test-detector

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install pytest selenium webdriver-manager
```

### Run Detection
```bash
# Run the flaky test detection
python run_flaky_detection.py

# View results in terminal
```

---

## 📁 Project Structure
```
flaky-test-detector/
├── src/
│   ├── __init__.py
│   └── tracker.py           # Core tracking logic
├── tests/
│   ├── test_basics.py       # Basic pytest examples
│   ├── test_flaky_suite.py  # Intentionally flaky tests
│   └── test_real_world_flaky.py  # Selenium-based tests
├── run_flaky_detection.py   # Main runner script
├── OBSERVATIONS.md          # Manual test observations
└── README.md
```

---

## 🎓 Academic Context

**Final Year Project | Computer Engineering | 2025**

This project explores:
- Statistical analysis of test behavior
- Pattern recognition in automation code
- Data-driven quality assurance
- Real-world industry problem solving

---

## 📈 Impact

### For QA Teams
- Identify problematic tests automatically
- Prioritize fixes based on severity
- Save hours of manual debugging
- Improve CI/CD reliability

### For Development Teams
- Reduce wasted rerun time
- Increase confidence in test results
- Enable faster deployment cycles
- Lower infrastructure costs

---

## 📝 License

This project is developed for academic purposes.

---

## 👤 Author

**Kunj Vashi**  
Computer Engineering Student  
[GitHub](https://github.com/KunjVashi) | [LinkedIn](https://www.linkedin.com/in/kunj-vashi-7a900537a/)

---

**⭐ Star this repo if you find it useful!**
