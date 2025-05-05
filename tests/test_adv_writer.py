import pytest
from flopy_owhm_interface.adv_writer import write_adv_input

def mock_adv_package():
    class MockAdv:
        pass
    adv = MockAdv()
    adv.parameters = {
        'mixelm': 1,
        'percel': 0.75,
        'nadvfd': 2
    }
    return adv

def test_write_adv_input(tmp_path):
    adv = mock_adv_package()
    output_file = tmp_path / 'ADV.dat'
    write_adv_input(adv, str(output_file))
    with open(output_file, 'r') as f:
        content = f.read()
    assert 'ADV' in content or 'BEGIN ADV' in content
    assert '1' in content
    assert '0.75' in content
    assert '2' in content 