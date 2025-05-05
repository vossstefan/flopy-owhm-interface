import pytest
from flopy_owhm_interface.chd_writer import write_chd_input

def mock_chd_package():
    class MockChd:
        pass
    chd = MockChd()
    chd.stress_period_data = {
        0: [
            {'k': 1, 'i': 1, 'j': 1, 'shead': 100.0, 'ehead': 90.0},
            {'k': 1, 'i': 2, 'j': 2, 'shead': 110.0, 'ehead': 95.0},
        ]
    }
    return chd

def test_write_chd_input(tmp_path):
    chd = mock_chd_package()
    output_file = tmp_path / 'CHD.dat'
    write_chd_input(chd, str(output_file))
    with open(output_file, 'r') as f:
        content = f.read()
    assert 'CHD' in content or 'BEGIN CHD' in content
    assert '100.0' in content
    assert '110.0' in content 