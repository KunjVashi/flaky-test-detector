# This is a comment - Python ignores these lines
# They're just notes for humans

# This is a function definition
# Functions are reusable blocks of code
# "test_" at the start tells pytest this is a test
def test_simple_addition():
    """
    This is a docstring - describes what the function does
    Three quotes allow multi-line descriptions
    """
    # This line does 2 + 2 and stores the result in a variable called 'result'
    result = 2 + 2
    
    # 'assert' checks if something is True
    # If result equals 4, test passes ✅
    # If result does NOT equal 4, test fails ❌
    assert result == 4
    
    # Print statement (you'll see this when test runs)
    print("✅ Addition test passed!")


def test_string_operations():
    """Testing string manipulations"""
    # Create a variable called 'name' with value "Python"
    name = "Python"
    
    # .upper() converts string to uppercase
    # This checks if "Python".upper() equals "PYTHON"
    assert name.upper() == "PYTHON"
    
    # len() returns the length (number of characters)
    # "Python" has 6 letters
    assert len(name) == 6
    
    print("✅ String test passed!")


def test_list_operations():
    """Testing list manipulations"""
    # Create a list (like an array) with 3 numbers
    my_list = [1, 2, 3]
    
    # .append() adds an item to the end of the list
    my_list.append(4)
    # Now my_list is [1, 2, 3, 4]
    
    # Check if the list now has 4 items
    assert len(my_list) == 4
    
    # Check if 4 is in the list
    # 'in' operator checks if an item exists in a list
    assert 4 in my_list
    
    print("✅ List test passed!")

def test_intentional_failure():
    result = 2 + 2
    # This assertion is WRONG (2+2 does not equal 5)
    assert result == 5, "Two plus two should equal four, not five!"