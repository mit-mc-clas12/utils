# ****************************************************************
"""
 Download or copy lund files and return the name of 
    the target directory. 

    Inputs: 
    -------
    lund_location - A string containing the directory or path to lund file(s).

    Returns: 
    --------
    lund_download_dir - A string containing the name of the downloaded directory.

    A few cases can occur: 

    1) One local file, extension will be .txt, .dat, or .lund and the string 
       will not contain http. 
    2) Several local files, no extension will be given.  The string will not 
       contain http. 
    3) One web file, extension will be .txt, .dat, or .lund and the string 
       will contain http. 
    4) Many web files, no extension will be given.  The string will contain http. 

    Example values for lund_location:
    Online Directory - 'https://userweb.jlab.org/~ungaro/lund/'
    Online Directory typo - 'https://userweb.jlab.org/~ungaro/lund'
    
    Online file -   'https://userweb.jlab.org/~ungaro/lund/clasdis1.txt'

    Local Directory - /volatile/clas12/robertej/trans_test/
    Local Directory typo 1 - /volatile/clas12/robertej/trans_test/
    Local Directory typo 2 - volatile/clas12/robertej/trans_test/
    Local Directory typo 3 - volatile/clas12/robertej/trans_test

    Local File - /volatile/clas12/robertej/trans_test/rad.lund
    Local File typo - volatile/clas12/robertej/trans_test/rad.lund
"""
# ***************************************************************

import subprocess, os, sys


env = os.environ.copy()
env["XDG_RUNTIME_DIR"] = "/run/user/6635"
env["BEARER_TOKEN_FILE"] = "/var/run/user/6635/bt_u6635"


def to_pelican_path(lund_location):
    """
    Convert a /volatile/clas12/... path into the corresponding
    osdf:///jlab-osdf/clas12/volatile/... path for pelican.
    """
    if '/volatile/clas12/' not in lund_location:
        raise ValueError("lund_location must contain /volatile/clas12/")

    # Swap 'volatile' and 'clas12' → '/clas12/volatile/...'
    swapped = lund_location.replace('/volatile/clas12/', '/clas12/volatile/', 1)

    # Prefix OSDF
    return 'osdf:///jlab-osdf' + swapped


def Lund_Entry(lund_location, lund_files="lund_files"):
    valid_lund_extensions = ['.dat', '.txt', '.lund']

    # A case used to work around not downloading for types 1/3
    if lund_location == "no_download":
        print('Not downloading files due to SCard type.')
        return lund_location

    #######################################################
    # Use pelican to copy files from a jlab location to OSG
    #######################################################
    lund_pelican_path = to_pelican_path(lund_location)

    # Get listing from pelican
    result = subprocess.run(
        ['pelican', 'object', 'ls', lund_pelican_path],
        env=env,                     # assuming env is defined elsewhere
        stdout=subprocess.PIPE,
        universal_newlines=True,     # Python 3.6-compatible
        check=True,
    )

    allowed_ext = {'.txt', '.lund', '.dat'}

    lines = [
        line.strip()
        for line in result.stdout.splitlines()
        if line.strip()
    ]

    # Build full pelican paths for allowed files
    full_paths = []
    base = lund_pelican_path.rstrip('/')

    for name in lines:
        # If pelican already returns full OSDF paths, keep as-is
        if name.startswith('osdf:///'):
            path = name
        else:
            path = base + '/' + name.lstrip('/')

        if os.path.splitext(path)[1] in allowed_ext:
            full_paths.append(path)

    # Write full pelican paths to lund_files
    with open(lund_files, 'w') as f:
        if full_paths:
            f.write('\n'.join(full_paths) + '\n')

    return lund_files



def count_files(lund_location):
    """
    Use `pelican object ls` on the *OSDF* version of `lund_location`
    and return the number of entries ending in .txt, .lund, or .dat.
    """
    lund_pelican_path = to_pelican_path(lund_location)

    result = subprocess.run(
        ["pelican", "object", "ls", lund_pelican_path],
        stdout=subprocess.PIPE,
        universal_newlines=True,  # Python 3.6-compatible way to get str output
        check=True,
    )

    allowed_ext = {".txt", ".lund", ".dat"}

    # Split lines, strip whitespace, drop empties
    lines = [
        line.strip()
        for line in result.stdout.splitlines()
        if line.strip()
    ]

    # Keep only files with allowed extensions
    filtered = [
        line for line in lines
        if os.path.splitext(line)[1] in allowed_ext
    ]

    return len(filtered)
