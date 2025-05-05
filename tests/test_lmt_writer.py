import pytest
from flopy_owhm_interface.lmt_writer import write_lmt_input

def mock_lmt_package():
    class MockLmt:
        pass
    lmt = MockLmt()
    lmt.parameters = {
        'output_file': 'MT3D001.UCN',
        'output_format': 1
    }
    return lmt

def test_write_lmt_input(tmp_path):
    lmt = mock_lmt_package()
    output_file = tmp_path / 'LMT.dat'
    write_lmt_input(lmt, str(output_file))
    with open(output_file, 'r') as f:
        content = f.read()
    assert 'LMT' in content or 'BEGIN LMT' in content
    assert 'MT3D001.UCN' in content
    assert '1' in content 