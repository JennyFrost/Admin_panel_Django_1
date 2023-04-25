from dotenv import load_dotenv
from split_settings.tools import include

load_dotenv()

include(
    'components/installed_apps.py',
)

include(
    'components/middleware.py',
)

include(
    'components/templates.py',
)

include(
    'components/database.py',
)

include(
    'components/auth_password_validators.py',
)

include(
    'components/constants.py',
)
