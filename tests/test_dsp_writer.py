import pytest
from flopy_owhm_interface.dsp_writer import write_dsp_input

def mock_dsp_package():
    class MockDsp:
        pass
    dsp = MockDsp()
    dsp.parameters = {
        'al': 10.0,
        'trpt': 0.1,
        'trpv': 0.01,
        'dmcoef': 0.001
    }
    return dsp

def test_write_dsp_input(tmp_path):
    dsp = mock_dsp_package()
    output_file = tmp_path / 'DSP.dat'
    write_dsp_input(dsp, str(output_file))
    with open(output_file, 'r') as f:
        content = f.read()
    assert 'DSP' in content or 'BEGIN DSP' in content
    assert '10.0' in content
    assert '0.1' in content
    assert '0.01' in content
    assert '0.001' in content 