from django.conf import settings
from django.shortcuts import redirect
from django.utils import translation

def cycle_language(request):
    languages = [lang[0] for lang in settings.LANGUAGES]

    current_lang = translation.get_language()
    try:
        next_lang = languages[(languages.index(current_lang) + 1) % len(languages)]
    except ValueError:
        next_lang = settings.LANGUAGE_CODE

    response = redirect(request.META.get('HTTP_REFERER','/'))
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME,next_lang)
    translation.activate(next_lang)
    return response