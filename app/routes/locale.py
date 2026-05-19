from flask import Blueprint, redirect, request, make_response, url_for

from app.i18n import LOCALE_COOKIE, SUPPORTED_LOCALES, set_locale

locale_bp = Blueprint('locale', __name__)


@locale_bp.route('/set-language/<lang>')
def set_language(lang):
    if lang not in SUPPORTED_LOCALES:
        lang = 'ru'
    set_locale(lang)
    next_url = request.args.get('next') or request.referrer or url_for('landing')
    resp = make_response(redirect(next_url))
    resp.set_cookie(
        LOCALE_COOKIE,
        lang,
        max_age=60 * 60 * 24 * 365,
        httponly=False,
        samesite='Lax',
    )
    return resp
