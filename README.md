# wazuh_active_responses

## Overview

`wazuh_active_responses` is a collection of active response scripts for the Wazuh security platform.
Each script resides in its own subfolder and implements a specific action that can be triggered by Wazuh alerts.

---

## Repository Structure

```
├── install_velociraptor
│   ├── install_velo.py          
│   └── README.md                
└── README.md                    
```

## How It Works

1. **Alert Generation**
   When a rule matches an event, Wazuh generates an alert in JSON format.

2. **Active Response Trigger**
   The `install_velociraptor` script is registered as an active response for the rule(s) that require installing Velociraptor.

3. **Execution Flow**
   - The script validates the incoming JSON and ensures the command is `add`.
   - It downloads a specified MSI file from a URL.
   - Installs the MSI silently using `msiexec`.
   - Logs all actions to an active‑response log file.
   - Writes a brief result record to `ar-test-result.txt`.


## Contributing

Feel free to fork this repository, add new active responses, or improve existing ones.
When adding a new script:

1. Create a subfolder under the root directory.
2. Add the Python (or other language) file(s).
3. Include a `README.md` explaining its purpose and usage.
