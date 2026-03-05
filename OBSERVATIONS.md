# Flaky Test Observations

## Date: 16/02/2026

## Test Run Results

### Run 1
- test_stable_always_passes: PASSED ✅
- test_stable_string: PASSED ✅
- test_flaky_random: PASSED ✅
- test_flaky_timing: FAILED ❌
- test_flaky_external_api: PASSED ✅
- test_slightly_flaky: PASSED ✅
- test_very_flaky: FAILED ❌ 
- test_flaky_race_condition: PASSED ✅

### Run 2
- test_stable_always_passes: PASSED ✅
- test_stable_string: PASSED ✅
- test_flaky_random: FAILED ❌
- test_flaky_timing: PASSED ✅
- test_flaky_external_api: PASSED ✅
- test_slightly_flaky: PASSED ✅
- test_very_flaky: FAILED ❌ 
- test_flaky_race_condition: PASSED ✅

### Run 3
- test_stable_always_passes: PASSED ✅
- test_stable_string: PASSED ✅
- test_flaky_random: FAILED ❌
- test_flaky_timing: PASSED ✅
- test_flaky_external_api: FAILED ❌
- test_slightly_flaky: PASSED ✅
- test_very_flaky: PASSED ✅
- test_flaky_race_condition: FAILED ❌

### Run 4
- test_stable_always_passes: PASSED ✅
- test_stable_string: PASSED ✅
- test_flaky_random: FAILED ❌
- test_flaky_timing: PASSED ✅
- test_flaky_external_api: PASSED ✅
- test_slightly_flaky: PASSED ✅
- test_very_flaky: FAILED ❌ 
- test_flaky_race_condition: PASSED ✅

### Run 5
- test_stable_always_passes: PASSED ✅
- test_stable_string: PASSED ✅
- test_flaky_random: PASSED ✅
- test_flaky_timing: FAILED ❌
- test_flaky_external_api: FAILED ❌
- test_slightly_flaky: PASSED ✅
- test_very_flaky: FAILED ❌ 
- test_flaky_race_condition: FAILED ❌

---

## My Analysis

### Questions to Answer:

1. **Which tests ALWAYS passed in all 5 runs?**
   Answer: test_stable_always_passes, test_stable_string, test_slightly_flaky ALWAYS passed in all 5 runs.

2. **Which test failed MOST often?**
   Answer: test_very_flaky failed MOST often.

3. **Which test failed LEAST often (or rarely)?**
   Answer: test_stable_always_passes, test_stable_string, test_slightly_flaky these 3 tests never failed and test_flaky_timing, test_exteral_api, test_flaky_race_condition failed 2 times.

4. **Did the stable tests ever fail?**
   Answer: No

5. **What pattern do you notice?**
   Answer: I noticed that timing can be a crucial factor.

6. **In real life, why would test_flaky_timing be a problem?**
   Answer: test_flaky_timing would be a problem because sometimes a particular thing on internet may take longer to appear than expected.

---

## Calculate Flake Rates

For each flaky test, calculate:
Flake Rate = (Number of failures / Total runs) × 100

Example: If test_flaky_random failed 3 times out of 5:
Flake Rate = (3 / 5) × 100 = 60%

**test_stable_always_passes:**
- Total runs: 5
- Failures: 0
- Flake rate: 0%

**test_stable_string:**
- Total runs: 5
- Failures: 0
- Flake rate: 0%

**test_flaky_random:**
- Total runs: 5
- Failures: 3
- Flake rate: 60%

**test_flaky_timing:**
- Total runs: 5
- Failures: 2
- Flake rate: 40%

**test_flaky_external_api:**
- Total runs: 5
- Failures: 2
- Flake rate: 40%

**test_slightly_flaky:**
- Total runs: 5
- Failures: 0
- Flake rate: 0%

**test_very_flaky:**
- Total runs: 5
- Failures: 5
- Flake rate: 100%

**test_flaky_race_condition:**
- Total runs: 5
- Failures: 2
- Flake rate: 40%

## Real-World Connection

Imagine you're testing a login button on a website.

If your test is like `test_flaky_timing`, what could go wrong?

Answer: There is a possibility that sometimes the login button takes longer to appear than expected. In this case the test will fail.

---

---

## Real-World Web Testing Results

### Test Run Results (5 runs with actual websites)

### Run 1
- test_flaky_dynamic_loading: FAILED ❌
- test_flaky_add_remove_elements: PASSED ✅
- test_flaky_form_authentication: PASSED ✅
- test_flaky_dropdown: PASSED ✅
- test_stable_page_title: PASSED ✅
- test_fixed_dynamic_loading: PASSED ✅

### Run 2
- test_flaky_dynamic_loading: FAILED ❌
- test_flaky_add_remove_elements: PASSED ✅
- test_flaky_form_authentication: PASSED ✅
- test_flaky_dropdown: PASSED ✅
- test_stable_page_title: PASSED ✅
- test_fixed_dynamic_loading: PASSED ✅

### Run 3
- test_flaky_dynamic_loading: FAILED ❌
- test_flaky_add_remove_elements: PASSED ✅
- test_flaky_form_authentication: PASSED ✅
- test_flaky_dropdown: PASSED ✅
- test_stable_page_title: PASSED ✅
- test_fixed_dynamic_loading: PASSED ✅

### Run 4
- test_flaky_dynamic_loading: FAILED ❌
- test_flaky_add_remove_elements: PASSED ✅
- test_flaky_form_authentication: PASSED ✅
- test_flaky_dropdown: PASSED ✅
- test_stable_page_title: PASSED ✅
- test_fixed_dynamic_loading: PASSED ✅

### Run 5
- test_flaky_dynamic_loading: FAILED ❌
- test_flaky_add_remove_elements: PASSED ✅
- test_flaky_form_authentication: PASSED ✅
- test_flaky_dropdown: PASSED ✅
- test_stable_page_title: PASSED ✅
- test_fixed_dynamic_loading: PASSED ✅


### Real-World Analysis

1. **Which real-world test was most flaky?**
   Answer: test_flaky_dynamic_loading

2. **What's the difference between test_flaky_dynamic_loading and test_fixed_dynamic_loading?**
   Answer: flaky dynamic loading uses implicit wait and fixed dynamic loading uses explicit wait.

3. **Why did test_stable_page_title never fail?**
   Answer: because it only checks page title. so its fast and reliable.

4. **In your own words, explain why time.sleep() causes flakiness:**
   Answer: because it is implicit wait and it waits for only fixed seconds.

5. **What's a better approach than time.sleep()?**
   Answer: explicit wait is better approach than time.sleep().