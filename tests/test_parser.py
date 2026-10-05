"""Тесты парсера метаданных."""

from pathlib import Path

from erp_audit.parser import iter_objects, parse_metadata

FIXTURES = Path(__file__).parent / "fixtures" / "config_sample"


def test_parse_metadata_catalog():
    xml_path = FIXTURES / "Catalogs" / "Контрагенты.xml"
    obj = parse_metadata(xml_path)

    assert obj is not None
    assert obj.name == "Контрагенты"
    assert obj.type == "Catalog"


def test_parse_metadata_document():
    xml_path = FIXTURES / "Documents" / "РеализацияТоваров.xml"
    obj = parse_metadata(xml_path)

    assert obj is not None
    assert obj.name == "РеализацияТоваров"
    assert obj.type == "Document"


def test_parse_metadata_invalid_file(tmp_path: Path):
    bad_xml = tmp_path / "bad.xml"
    bad_xml.write_text("not valid xml <<<")

    obj = parse_metadata(bad_xml)
    assert obj is None


def test_parse_metadata_non_mdo_file(tmp_path: Path):
    xml = tmp_path / "other.xml"
    xml.write_text('<?xml version="1.0"?><Root name="X"></Root>')

    obj = parse_metadata(xml)
    assert obj is None


def test_iter_objects_finds_all():
    objects = list(iter_objects(FIXTURES))
    names = {o.name for o in objects}

    assert "Контрагенты" in names
    assert "РеализацияТоваров" in names
    assert len(objects) >= 2
