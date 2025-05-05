import pytest
from flopy_owhm_interface.drn_writer import write_drn_input

def mock_drn_package():
    class MockDrn:
        pass
    drn = MockDrn()
    drn.drains = [
        {'drain_id': 1, 'row': 1, 'col': 1, 'elev': 5.0, 'cond': 100.0},
        {'drain_id': 2, 'row': 2, 'col': 2, 'elev': 6.0, 'cond': 200.0},
    ]
    return drn

def test_write_drn_input(tmp_path):
    drn = mock_drn_package()
    output_file = tmp_path / 'DRN.dat'
    write_drn_input(drn, str(output_file))
    with open(output_file, 'r') as f:
        content = f.read()
    assert 'DRN' in content or 'BEGIN DRN' in content
    assert '1' in content
    assert '2' in content 