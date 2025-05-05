import pytest
from flopy_owhm_interface.gage_writer import write_gage_input

def mock_gage_package():
    class MockGage:
        pass
    gage = MockGage()
    gage.stress_period_data = {
        0: [
            {'unit': 1, 'outtype': 0},
            {'unit': 2, 'outtype': 1},
        ]
    }
    return gage

def test_write_gage_input(tmp_path):
    gage = mock_gage_package()
    output_file = tmp_path / 'GAGE.dat'
    write_gage_input(gage, str(output_file))
    with open(output_file, 'r') as f:
        content = f.read()
    assert 'GAGE' in content or 'BEGIN GAGE' in content
    assert '1' in content
    assert '2' in content 