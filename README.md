# wazuh_active_responses

## Overview

`wazuh_active_responses` is a collection of active response scripts for the Wazuh security platform.
Each script resides in its own subfolder and implements a specific action that can be triggered by Wazuh alerts.

For more information about active responses, please see here: [Wazuh Documentation](https://documentation.wazuh.com/current/user-manual/capabilities/active-response/index.html)

---

## Repository Structure

```
├── install_velociraptor
│   ├── install_velo.py          
│   └── README.md                
└── README.md                    
```

## Contributing

Feel free to fork this repository, add new active responses, or improve existing ones.
When adding a new script:

1. Create a subfolder under the root directory.
2. Add the Python (or other language) file(s).
3. Include a `README.md` explaining its purpose and usage.
