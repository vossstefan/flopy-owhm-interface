import pytest
from flopy_owhm_interface.riv_writer import write_riv_input

def mock_riv_package():
    class MockRiv:
        pass
    riv = MockRiv()
    riv.stress_period_data = {
        0: [
            {'k': 1, 'i': 1, 'j': 1, 'stage': 10.0, 'cond': 100.0, 'rbot': 5.0},
            {'k': 1, 'i': 2, 'j': 2, 'stage': 12.0, 'cond': 200.0, 'rbot': 6.0},
        ]
    }
    return riv

def test_write_riv_input(tmp_path):
    riv = mock_riv_package()
    output_file = tmp_path / 'RIV.dat'
    write_riv_input(riv, str(output_file))
    with open(output_file, 'r') as f:
        content = f.read()
    assert 'RIV' in content or 'BEGIN RIV' in content
    assert '10.0' in content
    assert '12.0' in content 