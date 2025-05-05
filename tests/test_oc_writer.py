import pytest
from flopy_owhm_interface.oc_writer import write_oc_input

def mock_oc_package():
    class MockOc:
        pass
    oc = MockOc()
    oc.parameters = {
        'csv_output': True,
        'listing_output': False,
        'custom_blocks': ['CUSTOM1', 'CUSTOM2']
    }
    return oc

def test_write_oc_input(tmp_path):
    oc = mock_oc_package()
    output_file = tmp_path / 'OC.dat'
    write_oc_input(oc, str(output_file))
    with open(output_file, 'r') as f:
        content = f.read()
    assert 'OC' in content or 'BEGIN OC' in content
    assert 'CSV_OUTPUT' in content
    assert '1' in content  # True as int
    assert 'LISTING_OUTPUT' in content
    assert '0' in content  # False as int
    assert 'CUSTOM1' in content
    assert 'CUSTOM2' in content 