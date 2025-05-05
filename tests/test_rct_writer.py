import pytest
from flopy_owhm_interface.rct_writer import write_rct_input

def mock_rct_package():
    class MockRct:
        pass
    rct = MockRct()
    rct.parameters = {
        'isothm': 1,
        'ireact': 2,
        'rc1': 0.1,
        'rc2': 0.2,
        'rc3': 0.3,
        'rc4': 0.4,
        'sp1': 0.5,
        'sp2': 0.6,
        'sp3': 0.7,
        'sp4': 0.8
    }
    return rct

def test_write_rct_input(tmp_path):
    rct = mock_rct_package()
    output_file = tmp_path / 'RCT.dat'
    write_rct_input(rct, str(output_file))
    with open(output_file, 'r') as f:
        content = f.read()
    assert 'RCT' in content or 'BEGIN RCT' in content
    assert '1' in content
    assert '2' in content
    assert '0.1' in content
    assert '0.8' in content 