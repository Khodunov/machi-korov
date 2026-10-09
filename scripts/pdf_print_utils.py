"""Lossless stream compaction for print PDFs."""
import base64

from pypdf.generic import ArrayObject, NameObject


def compact_image_streams(writer):
    """Remove redundant ASCII85 wrappers, retaining original image encoding."""
    seen = set()
    for page in writer.pages:
        for reference in page.get('/Resources', {}).get('/XObject', {}).values():
            image = reference.get_object()
            if id(image) in seen:
                continue
            seen.add(id(image))
            filters = image.get('/Filter')
            if isinstance(filters, ArrayObject) and filters[0] == '/ASCII85Decode':
                image._data = base64.a85decode(image._data, adobe=True)
                image[NameObject('/Filter')] = ArrayObject(filters[1:])
