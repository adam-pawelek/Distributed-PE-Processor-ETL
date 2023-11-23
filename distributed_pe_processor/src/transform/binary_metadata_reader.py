import pefile

from distributed_pe_processor.database.models.file_metadata_model import FileMetadataModel


def get_file_size(content: str) -> int:
    return len(content)


def get_file_type(path: str) -> str:
    return path[-3:].lower()


def get_file_architecture(pe: pefile.PE) -> str:
    architecture = "x32"
    if hasattr(pe, 'FILE_HEADER') and pe.FILE_HEADER.Machine == pefile.MACHINE_TYPE['IMAGE_FILE_MACHINE_AMD64']:
        architecture = "x64"
    return architecture


def get_file_imports(pe: pefile.PE) -> int:
    return len(pe.DIRECTORY_ENTRY_IMPORT) if hasattr(pe, 'DIRECTORY_ENTRY_IMPORT') else 0


def get_file_exports(pe: pefile.PE) -> int:
    return len(pe.DIRECTORY_ENTRY_EXPORT.symbols) if hasattr(pe, 'DIRECTORY_ENTRY_EXPORT') else 0


def get_metadata(path_content_tuple: tuple[str, str]) -> tuple:
    path, content = path_content_tuple
    try:
        pe = pefile.PE(data=content)
        metadata_file = FileMetadataModel(
            file_path=path,
            file_size=get_file_size(content),
            file_type=get_file_type(path),
            architecture=get_file_architecture(pe),
            num_imports=get_file_imports(pe),
            num_exports=get_file_exports(pe)
        )
        print(metadata_file.get_metadata_values_tuple())

    except:
        metadata_file = FileMetadataModel(
            file_path=path,
            file_size=get_file_size(content),
            file_type=get_file_type(path),
            architecture="",
            num_imports=None,
            num_exports=None
        )
    return metadata_file.get_metadata_values_tuple()
