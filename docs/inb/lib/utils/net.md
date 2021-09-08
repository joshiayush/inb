# Net Service

This service provides a way to check the network status on your system.

This document contains the following section:

- [System Call Interface](#system-call-interface)

## System Call Interface

- **Method ping():**

  > ```python
  > def ping(host: str = None) -> bool:
  > ```
  >
  > This method pings the given host name and returns `True` if the host respond.
  >
  > This function takes in an argument called `host` which is the host to send request to. This function internally uses a function
  > called `subprocess.call()` so to avoid the shell injection or command injection vulnerability.
  >
  > This method is compatible for both `posix` and `windows` operating systems.
