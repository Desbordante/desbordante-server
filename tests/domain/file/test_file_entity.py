from uuid import UUID

from internal.domain.file import File


def test_file_initialization():
    file = File()
    assert isinstance(file._name, UUID)
    assert isinstance(file.name, str)
    assert isinstance(file.name_as_uuid, UUID)


def test_file_name_properties():
    file = File()

    assert file.name == str(file._name)
    assert file.name_as_uuid == file._name
