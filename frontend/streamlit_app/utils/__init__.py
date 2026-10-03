from .api_client import client, APIClient
from .auth import (
    is_authenticated,
    get_current_user,
    login,
    quick_login,
    logout,
    render_sidebar_brand,
    DEMO_USERS,
    LOGO_PATH
)
from .config import USE_LIVE_API, get_dataset_metadata
from .i18n import (
    t,
    get_current_lang,
    set_lang,
    render_language_toggle,
    TRANSLATIONS
)
from .gov_theme import (
    apply_gov_theme,
    hide_default_sidebar_nav,
    render_top_navbar,
    render_citizen_navbar,
    render_split_login_header,
    render_role_selection_landing,
    render_gov_header,
    render_breadcrumb,
    status_pill,
    render_gov_footer,
    NAV_ITEMS
)

__all__ = [
    "client",
    "APIClient",
    "is_authenticated",
    "get_current_user",
    "login",
    "quick_login",
    "logout",
    "render_sidebar_brand",
    "DEMO_USERS",
    "LOGO_PATH",
    "USE_LIVE_API",
    "get_dataset_metadata",
    "t",
    "get_current_lang",
    "set_lang",
    "render_language_toggle",
    "TRANSLATIONS",
    "apply_gov_theme",
    "hide_default_sidebar_nav",
    "render_top_navbar",
    "render_citizen_navbar",
    "render_split_login_header",
    "render_role_selection_landing",
    "render_gov_header",
    "render_breadcrumb",
    "status_pill",
    "render_gov_footer",
    "NAV_ITEMS",
]
