# Installation

1. `python -m venv venv`
2. `source venv/bin/activate` (for mac)
3. `pip install -r requirements.txt`
4. `python services/sqlite.py`

# App Settings

You need to add your credentials to the `config.json` file in the root.

```json
// config.json
{
    "assistant_id" : "",
    "open_api_key" : "",
    "app_secret" : ""
}
```