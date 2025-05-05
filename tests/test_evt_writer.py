import pytest
import os
from flopy_owhm_interface.evt_writer import write_evt_input

def mock_evt_package():
    class MockEvt:
        pass
    evt = MockEvt()
    evt.stress_period_data = {
        0: [
            {'k': 1, 'i': 1, 'j': 1, 'surf': 100.0, 'evtr': 0.01},
            {'k': 1, 'i': 2, 'j': 2, 'surf': 99.0, 'evtr': 0.02},
        ]
    }
    return evt

def test_write_evt_input(tmp_path):
    evt = mock_evt_package()
    output_file = tmp_path / 'EVT.dat'
    write_evt_input(evt, str(output_file))
    with open(output_file, 'r') as f:
        content = f.read()
    assert 'BEGIN EVT' in content
    assert '1   1   1   100.0   0.01' in content
    assert '1   2   2   99.0   0.02' in content
    assert 'END EVT' in content 