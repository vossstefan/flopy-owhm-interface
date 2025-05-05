import pytest
import os
from flopy_owhm_interface.owhm_interface import OWHMInterface

def mock_flopy_model():
    class MockModel:
        pass
    m = MockModel()
    # Minimal mocks for a few packages
    class MockEvt: stress_period_data = {0: [{'k': 1, 'i': 1, 'j': 1, 'surf': 100.0, 'evtr': 0.01}]}
    class MockFmp: farms = [{'farm_id': 1, 'name': 'Farm1', 'area': 100.0}]; farm_dict = {1: 'Farm1'}
    class MockGhb: boundaries = [{'k': 1, 'i': 1, 'j': 1, 'bhead': 100.0, 'cond': 500.0}]
    class MockRch: stress_period_data = {0: [{'k': 1, 'i': 1, 'j': 1, 'recharge': 0.01}]}
    m.evt = MockEvt()
    m.fmp = MockFmp()
    m.ghb = MockGhb()
    m.rch = MockRch()
    return m

def test_write_input_files(tmp_path):
    model = mock_flopy_model()
    interface = OWHMInterface(owhm_exe_path='dummy_exe')
    interface.write_input_files(model, workspace=str(tmp_path))
    # Check that expected files are created
    for fname in ['EVT.dat', 'FMP.dat', 'GHB.dat', 'RCH.dat']:
        fpath = tmp_path / fname
        assert os.path.exists(fpath)
        with open(fpath, 'r') as f:
            content = f.read()
        assert fname.split('.')[0] in content or f'BEGIN {fname.split(".")[0]}' in content 