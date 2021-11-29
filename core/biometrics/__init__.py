from modzy import ApiClient

from core.config import get_settings

API_URL = "https://app.modzy.com/api"
API_KEY = get_settings().modzy_api_key

modzy_client = ApiClient(base_url=API_URL, api_key=API_KEY)

models = {
    "face": {  # Facial embedding
        'id': '899doc921x'
    },
    "voice": {  # Voice fingerprint
        'id': '8bjq6tqvqv',
    },
}

for model in models:
    model_info = modzy_client.models.get(models[model]['id'])
    if models[model].get('version', None) is None:
        models[model]['version'] = model_info.latestActiveVersion
    models[model]['name'] = model_info.name
