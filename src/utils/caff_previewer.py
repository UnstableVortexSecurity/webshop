import tempfile
import os
import os.path
import shutil
import requests
from flask import current_app
from .md5stuffs import calculate_md5_sum_for_file, write_file_from_stream_to_file_like_while_calculating_md5
from .exceptions import FileIntegrityError
import magic

EXPECTED_PREVIEW_MIMETYPE = 'image/png'

# The response is validated for
# - integrity (2-way)
# - mime type (both header and file identifying)
# - size (handled by md5sum saver, generator thingy)

def create_caff_preview(src_file: str) -> str:  # hopefully returns a file path

    # Send file for previewing
    uploaded_caff_md5sum = calculate_md5_sum_for_file(src_file)

    with open(src_file, 'rb') as f:
        r = requests.post(current_app.config['CAFF_PREVIEWER_ENDPOINT'], data=f, stream=True)

    r.raise_for_status()

    # Verify the results while saving the file
    if r.headers.get("Content-type") != EXPECTED_PREVIEW_MIMETYPE:
        raise ValueError(f"Converter output (reported by header) is not {EXPECTED_PREVIEW_MIMETYPE}")

    if r.headers.get("X-request-checksum") != uploaded_caff_md5sum:
        # This really is the most pointless check in the world
        # But it was fun to implement
        raise FileIntegrityError("File sent for previewing and received by previewer differ")

    converted_png_fd, converted_png_path = tempfile.mkstemp(
        prefix=os.path.basename(src_file).split('.')[0],
        suffix='.png'
    )

    with open(converted_png_fd, "wb") as f:
        converted_png_md5sum = write_file_from_stream_to_file_like_while_calculating_md5(r.raw, f)

    if r.headers.get("X-response-checksum") != converted_png_md5sum:
        # This does not have much point either
        raise FileIntegrityError("File sent by previewer and received by the app differ")

    with magic.Magic(flags=magic.MAGIC_MIME_TYPE) as m:
        calculated_mimetype = m.id_filename(converted_png_path)

    if calculated_mimetype != EXPECTED_PREVIEW_MIMETYPE:
        raise ValueError(f"Converter output (calculated from file) is not {EXPECTED_PREVIEW_MIMETYPE}")

    del r
    return converted_png_path
