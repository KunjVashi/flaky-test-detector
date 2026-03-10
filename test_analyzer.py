from src.analyzer import FlakyTestAnalyzer

# Create analyzer
analyzer = FlakyTestAnalyzer(test_directory="tests")

# Analyze all test files
print("🔍 Analyzing test files for flakiness patterns...\n")
print("=" * 70)

results = analyzer.analyze_all_tests()

for filepath, patterns in results.items():
    print(f"\n📄 File: {filepath}")
    print("-" * 70)
    
    total_issues = sum(len(issues) for issues in patterns.values())
    
    if total_issues == 0:
        print("✅ No flakiness patterns detected!")
        continue
    
    for category, issues in patterns.items():
        if issues:
            print(f"\n🔴 {category.replace('_', ' ').upper()}:")
            for issue in issues:
                print(f"  Line {issue['line']}: {issue['pattern']}")
                print(f"  └─ {issue['description']}")
                print(f"  └─ Fix: {issue['suggestion']}\n")

print("\n" + "=" * 70)