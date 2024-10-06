import pytest
import bytom as bt

# Dummy test
def test_one_plus_one():
    two = bt.one_plus_one(1, 1)
    assert two == 2

    # Note "match" is optional
    with pytest.raises(AssertionError, match="Inputs must be 1"):
        fail = bt.one_plus_one(3, 3)

    
