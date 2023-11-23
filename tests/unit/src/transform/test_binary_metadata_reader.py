import pefile

from distributed_pe_processor.src.transform.binary_metadata_reader import get_file_size, get_file_type, \
    get_file_architecture, get_file_imports, get_file_exports
from tests.data.read_binary_files import get_binary_files


# Test get_file_size
def test_get_file_size():
    assert get_file_size(b"12345") == 5  # binary string
    assert get_file_size(b"") == 0


def test_get_file_type():
    assert get_file_type("file.Exe") == "exe"
    assert get_file_type("file.EXE") == "exe"
    assert get_file_type("file.dll") == "dll"


def test_get_file_architecture():
    binary_files = get_binary_files()
    pe = pefile.PE(data=binary_files["file1.exe"])
    assert get_file_architecture(pe) =="x32"
    pe = pefile.PE(data=binary_files["file2.exe"])
    assert get_file_architecture(pe) =="x64"


def test_get_file_imports():
    binary_files = get_binary_files()
    pe = pefile.PE(data=binary_files["file1.exe"])
    assert get_file_imports(pe) == 1
    pe = pefile.PE(data=binary_files["file2.exe"])
    assert get_file_imports(pe) == 8


def test_get_file_exports():
    binary_files = get_binary_files()
    pe = pefile.PE(data=binary_files["file1.exe"])
    assert get_file_exports(pe) == 0
    pe = pefile.PE(data=binary_files["file2.exe"])
    assert get_file_exports(pe) == 0



