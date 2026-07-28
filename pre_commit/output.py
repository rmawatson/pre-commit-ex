from __future__ import annotations

import contextlib
import sys
from typing import Any
from typing import IO
from threading import Lock


write_lock = Lock()

def write(s: str, stream: IO[bytes] = sys.stdout.buffer) -> None:
    with write_lock:
        stream.write(s.encode())
        stream.flush()


def write_line_b(
        s: bytes | None = None,
        stream: IO[bytes] | None = None,
        logfile_name: str | None = None,
) -> None:
    resolved: IO[bytes] = stream if stream is not None else sys.stdout.buffer

    with write_lock, contextlib.ExitStack() as exit_stack:
        output_streams = [resolved]
        if logfile_name:
            output_streams.append(exit_stack.enter_context(open(logfile_name, 'ab')))

        for output_stream in output_streams:
            if s is not None:
                output_stream.write(s)
            output_stream.write(b'\n')
            output_stream.flush()


def write_line(s: str | None = None, **kwargs: Any) -> None:
    write_line_b(s.encode() if s is not None else s, **kwargs)
