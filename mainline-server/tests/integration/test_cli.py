import os
import socket
import subprocess

import httpx
from fastapi import status
from tenacity import retry, stop_after_delay, wait_fixed


def next_free_port(port=1024, max_port=65535):
    """Finds a free port"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while port <= max_port:
        try:
            sock.bind(("", port))
            sock.close()
            return port
        except OSError:
            port += 1
    raise IOError("no free ports")


@retry(wait=wait_fixed(0.3), stop=stop_after_delay(5), reraise=True)
def connect(port: int):
    result = httpx.get(f"http://127.0.0.1:{port}/health")
    assert result.status_code == status.HTTP_200_OK
    assert result.content.decode() == "pass", result.content.decode()


def test_api():
    expected_port = next_free_port()
    process = subprocess.Popen(
        ["mainline-server", "--port", str(expected_port)],
        stdout=None,
        stderr=None,
        stdin=None,
        close_fds=True,
        env=os.environ | {"COVERAGE_PROCESS_START": "pyproject.toml"},
    )
    connect(expected_port)
    process.kill()
