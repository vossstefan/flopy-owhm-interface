import pytest
from flopy_owhm_interface.rch_writer import write_rch_input

def mock_rch_package():
    class MockRch:
        pass
    rch = MockRch()
    rch.stress_period_data = {
        0: [
            {'k': 1, 'i': 1, 'j': 1, 'recharge': 0.01},
            {'k': 1, 'i': 2, 'j': 2, 'recharge': 0.02},
        ]
    }
    return rch

def test_write_rch_input(tmp_path):
    rch = mock_rch_package()
    output_file = tmp_path / 'RCH.dat'
    write_rch_input(rch, str(output_file))
    with open(output_file, 'r') as f:
        content = f.read()
    assert 'RCH' in content or 'BEGIN RCH' in content
    assert '0.01' in content
    assert '0.02' in content 