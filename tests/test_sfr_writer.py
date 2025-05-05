import pytest
from flopy_owhm_interface.sfr_writer import write_sfr_input

def mock_sfr_package():
    class MockSfr:
        pass
    sfr = MockSfr()
    sfr.reaches = [
        {'reach_id': 1, 'cellid': (1, 1, 1), 'length': 100.0, 'width': 10.0, 'slope': 0.001},
        {'reach_id': 2, 'cellid': (1, 2, 2), 'length': 200.0, 'width': 20.0, 'slope': 0.002},
    ]
    return sfr

def test_write_sfr_input(tmp_path):
    sfr = mock_sfr_package()
    output_file = tmp_path / 'SFR.dat'
    write_sfr_input(sfr, str(output_file))
    with open(output_file, 'r') as f:
        content = f.read()
    assert 'SFR' in content or 'BEGIN SFR' in content
    assert '1' in content
    assert '2' in content 