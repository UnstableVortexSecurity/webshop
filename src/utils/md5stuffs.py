import hashlib


def write_file_from_stream_to_file_like_while_calculating_md5(stream, f, maxsize: int = 536870912,
                                                              chunksize: int = 4096) -> str:
    m = hashlib.md5()  # nosec: md5 is used only for integrity checking here

    total_recieved = 0

    # Begin receiving the file

    while True:  # This is where uploading happens
        chunk = stream.read(chunksize)
        if len(chunk) == 0:
            break

        total_recieved += len(chunk)
        if total_recieved > maxsize:
            raise OverflowError("File too big")

        m.update(chunk)
        f.write(chunk)

    return m.hexdigest()


def calculate_md5_sum_for_file(fname) -> str:
    m = hashlib.md5()  # nosec: md5 is used only for integrity checking here

    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            m.update(chunk)

    return m.hexdigest()
