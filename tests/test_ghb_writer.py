import pytest
from flopy_owhm_interface.ghb_writer import write_ghb_input

def mock_ghb_package():
    class MockGhb:
        pass
    ghb = MockGhb()
    ghb.boundaries = [
        {'k': 1, 'i': 1, 'j': 1, 'bhead': 100.0, 'cond': 500.0},
        {'k': 1, 'i': 2, 'j': 2, 'bhead': 101.0, 'cond': 600.0},
    ]
    return ghb

def test_write_ghb_input(tmp_path):
    ghb = mock_ghb_package()
    output_file = tmp_path / 'GHB.dat'
    write_ghb_input(ghb, str(output_file))
    with open(output_file, 'r') as f:
        content = f.read()
    assert 'GHB' in content or 'BEGIN GHB' in content
    assert '1' in content
    assert '2' in content 