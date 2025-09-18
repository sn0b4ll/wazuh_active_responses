# install_velo.py

## Overview

`install-velo.py` is an Active Response script for Wazuh agents that automatically downloads and installs a Velociraptor MSI package when triggered by a specific rule ID. The script is written in Python 3 and follows the Wazuh active response conventions.

- **Author**: sn0b4ll (modified from original Wazuh Inc.)
- **Date**: 2025‑09‑18
- **License**: GPL‑2.0

## Features

| Feature | Description |
|---------|-------------|
| **JSON parsing** | Reads the alert JSON from stdin, validates it, and extracts the `command` field. |
| **Command handling** | Supports only the `"add"` command to trigger installation. |
| **MSI download & install** | Downloads a specified MSI file via HTTP(S) and installs it silently using `msiexec`. |
| **Logging** | Writes detailed debug logs to `C:\Program Files (x86)\ossec-agent\active-response\active-responses.log` with timestamps. |
| **Result file** | Appends the triggered rule ID to `ar-test-result.txt` for audit purposes. |

## Usage

The script is intended to be called by Wazuh’s active response system. No manual execution is required.


### Customizing MSI URL

Edit the `VELO_MSI_URL` variable at the top of the script:

```python
VELO_MSI_URL="<replace with VELO-MSI>"
```

Use your own Velociraptor MSI location or a local file path. If you don't have an MSI yet, you can look here: https://docs.velociraptor.app/docs/deployment/clients/

### Example Configuration in `ossec.conf`

```xml
  <command>
    <name>windows-install-velo</name>
    <executable>install-velo.exe</executable>
    <timeout_allowed>no</timeout_allowed>
  </command>

  <active-response>
    <disabled>no</disabled>
    <command>windows-install-velo</command>
    <location>local</location>
    <rules_id>62123</rules_id>
  </active-response>
```

## Logging

All actions are appended to:

```
C:\Program Files (x86)\ossec-agent\active-response\active-responses.log
```

Each log entry includes:

- Timestamp (`YYYY/MM/DD HH:MM:SS`)
- Script name
- Log message

Example log line:

```
2025/08/15 12:34:56 install_velo.py: Successfully downloaded and installed velo_install.msi
```

## Dependencies

- Python 3.x (bundled with Windows)
- `urllib` (standard library) for downloading files.
- `subprocess` (standard library) to invoke `msiexec`.
- `ossec-agent` must be running on a Windows machine.

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| MSI download fails | Network blocked or URL incorrect | Verify the URL and network connectivity. |
| `msiexec` not found | Path to `msiexec.exe` missing from PATH | Add `C:\Windows\System32` to the system PATH or provide full path in the script. |
| Script exits with `OS_INVALID` | JSON input malformed or command not `"add"` | Ensure Wazuh sends correct JSON and that the rule uses `-a add`. |

## Extending

To add additional actions (e.g., uninstall, reconfigure), extend the `setup_and_check_message()` function to recognize new commands and implement corresponding logic in the `main()` branch.

---

**Author:** sn0b4ll
**License:** GPL‑2.0
