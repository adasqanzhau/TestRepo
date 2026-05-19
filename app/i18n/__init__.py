"""Internationalization for MediPlatform (kk, ru, en)."""

from flask import session, request

from app.i18n.translations import TRANSLATIONS

SUPPORTED_LOCALES = {
    'kk': 'Қазақша',
    'ru': 'Русский',
    'en': 'English',
}
DEFAULT_LOCALE = 'ru'
LOCALE_COOKIE = 'mp_locale'


def get_locale():
    loc = session.get('locale')
    if loc in SUPPORTED_LOCALES:
        return loc
    loc = request.cookies.get(LOCALE_COOKIE)
    if loc in SUPPORTED_LOCALES:
        return loc
    accept = request.accept_languages.best_match(SUPPORTED_LOCALES.keys())
    return accept or DEFAULT_LOCALE


def set_locale(locale):
    if locale in SUPPORTED_LOCALES:
        session['locale'] = locale
        session.modified = True


def translate(key, **kwargs):
    """Resolve dotted key, e.g. nav.dashboard."""
    locale = get_locale()
    data = TRANSLATIONS.get(locale) or TRANSLATIONS[DEFAULT_LOCALE]
    node = data
    for part in key.split('.'):
        if isinstance(node, dict) and part in node:
            node = node[part]
        else:
            fallback = TRANSLATIONS[DEFAULT_LOCALE]
            node = fallback
            for p in key.split('.'):
                if isinstance(node, dict) and p in node:
                    node = node[p]
                else:
                    return key
            break
    if not isinstance(node, str):
        return key
    if kwargs:
        try:
            return node.format(**kwargs)
        except (KeyError, ValueError):
            return node
    return node


def init_app(app):
    @app.context_processor
    def inject_i18n():
        locale = get_locale()
        return {
            '_': translate,
            'current_locale': locale,
            'supported_locales': SUPPORTED_LOCALES,
            'locale_names': SUPPORTED_LOCALES,
        }
