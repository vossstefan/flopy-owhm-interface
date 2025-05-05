import pytest
from flopy_owhm_interface.drt_writer import write_drt_input

def mock_drt_package():
    class MockDrt:
        pass
    drt = MockDrt()
    drt.stress_period_data = {
        0: [
            {'k': 1, 'i': 1, 'j': 1, 'elev': 10.0, 'cond': 100.0, 'return_fraction': 0.5},
            {'k': 1, 'i': 2, 'j': 2, 'elev': 12.0, 'cond': 200.0, 'return_fraction': 0.6},
        ]
    }
    return drt

def test_write_drt_input(tmp_path):
    drt = mock_drt_package()
    output_file = tmp_path / 'DRT.dat'
    write_drt_input(drt, str(output_file))
    with open(output_file, 'r') as f:
        content = f.read()
    assert 'DRT' in content or 'BEGIN DRT' in content
    assert '0.5' in content
    assert '0.6' in content 