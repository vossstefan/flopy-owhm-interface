import pandas as pd

def parse_sfr_output(path: str) -> pd.DataFrame:
    """
    Parse an SFR output file (CSV/TXT) and return as a Pandas DataFrame.
    Skips comment lines.
    """
    with open(path, 'r') as f:
        lines = [line for line in f if not line.strip().startswith(('#', '!'))]
    from io import StringIO
    data = StringIO(''.join(lines))
    return pd.read_csv(data)

def parse_swr_output(path: str) -> pd.DataFrame:
    """
    Parse an SWR output file (CSV/TXT) and return as a Pandas DataFrame.
    Skips comment lines.
    """
    with open(path, 'r') as f:
        lines = [line for line in f if not line.strip().startswith(('#', '!'))]
    from io import StringIO
    data = StringIO(''.join(lines))
    return pd.read_csv(data)

def parse_lak_output(path: str) -> pd.DataFrame:
    """
    Parse a LAK output file (CSV/TXT) and return as a Pandas DataFrame.
    Skips comment lines.
    """
    with open(path, 'r') as f:
        lines = [line for line in f if not line.strip().startswith(('#', '!'))]
    from io import StringIO
    data = StringIO(''.join(lines))
    return pd.read_csv(data)

def parse_drn_output(path: str) -> pd.DataFrame:
    """
    Parse a DRN output file (CSV/TXT) and return as a Pandas DataFrame.
    Skips comment lines.
    """
    with open(path, 'r') as f:
        lines = [line for line in f if not line.strip().startswith(('#', '!'))]
    from io import StringIO
    data = StringIO(''.join(lines))
    return pd.read_csv(data)

def parse_res_output(path: str) -> pd.DataFrame:
    """
    Parse a RES output file (CSV/TXT) and return as a Pandas DataFrame.
    Skips comment lines.
    """
    with open(path, 'r') as f:
        lines = [line for line in f if not line.strip().startswith(('#', '!'))]
    from io import StringIO
    data = StringIO(''.join(lines))
    return pd.read_csv(data)

def parse_accounting_output(path: str) -> pd.DataFrame:
    """
    Parse a water accounting output file (CSV/TXT) and return as a Pandas DataFrame.
    Skips comment lines.
    """
    with open(path, 'r') as f:
        lines = [line for line in f if not line.strip().startswith(('#', '!'))]
    from io import StringIO
    data = StringIO(''.join(lines))
    return pd.read_csv(data) 