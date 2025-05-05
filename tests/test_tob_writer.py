import pytest
from flopy_owhm_interface.tob_writer import write_tob_input

def mock_tob_package():
    class MockTob:
        pass
    tob = MockTob()
    tob.observation_data = [
        {'k': 1, 'i': 1, 'j': 1, 'obsname': 'OBS1', 'obstype': 'CONC'},
        {'k': 1, 'i': 2, 'j': 2, 'obsname': 'OBS2', 'obstype': 'CONC'},
    ]
    return tob

def test_write_tob_input(tmp_path):
    tob = mock_tob_package()
    output_file = tmp_path / 'TOB.dat'
    write_tob_input(tob, str(output_file))
    with open(output_file, 'r') as f:
        content = f.read()
    assert 'TOB' in content or 'BEGIN TOB' in content
    assert 'OBS1' in content
    assert 'OBS2' in content 