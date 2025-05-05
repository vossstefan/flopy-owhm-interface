import pytest
from flopy_owhm_interface.maw_writer import write_maw_input

def mock_maw_package():
    class MockMaw:
        pass
    maw = MockMaw()
    maw.wells = [
        {'wellid': 1, 'row': 1, 'col': 1, 'radius': 0.5, 'rate': 100.0},
        {'wellid': 2, 'row': 2, 'col': 2, 'radius': 0.6, 'rate': 200.0},
    ]
    return maw

def test_write_maw_input(tmp_path):
    maw = mock_maw_package()
    output_file = tmp_path / 'MAW.dat'
    write_maw_input(maw, str(output_file))
    with open(output_file, 'r') as f:
        content = f.read()
    assert 'MAW' in content or 'BEGIN MAW' in content
    assert '1' in content
    assert '2' in content 