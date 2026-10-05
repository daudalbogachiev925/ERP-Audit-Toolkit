"""Парсинг выгрузки конфигурации 1С (XML-файлы метаданных)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

from lxml import etree


@dataclass(frozen=True)
class MetadataObject:
    """Объект метаданных 1С."""

    name: str
    uuid: str
    type: str
    path: Path

    def __repr__(self) -> str:
        return f"<{self.type} {self.name}>"


def parse_metadata(xml_path: Path) -> MetadataObject | None:
    """Парсит один XML-файл метаданных.

    Args:
        xml_path: путь к XML-файлу выгрузки.

    Returns:
        MetadataObject или None, если файл не содержит метаданных.
    """
    try:
        tree = etree.parse(str(xml_path))
        root = tree.getroot()
    except (etree.XMLSyntaxError, OSError):
        return None

    tag = root.tag
    if "}" in tag:
        tag = tag.split("}", 1)[1]

    if tag != "MetaDataObject":
        return None

    name = root.get("name")
    uuid = root.get("uuid", "")

    if not name:
        return None

    inner = root[0] if len(root) > 0 else None
    if inner is None:
        return None

    inner_tag = inner.tag
    if "}" in inner_tag:
        inner_tag = inner_tag.split("}", 1)[1]

    return MetadataObject(
        name=name,
        uuid=uuid,
        type=inner_tag,
        path=xml_path,
    )


def iter_objects(config_dir: Path) -> Iterator[MetadataObject]:
    """Итерирует по всем объектам метаданных в директории.

    Args:
        config_dir: корень выгрузки конфигурации.

    Yields:
        MetadataObject для каждого найденного объекта.
    """
    for xml_path in config_dir.rglob("*.xml"):
        obj = parse_metadata(xml_path)
        if obj is not None:
            yield obj
