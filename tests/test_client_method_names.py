import importlib
import inspect
import pkgutil
import sys

import nltk
import pytest
import spacy

try:
    nlp = spacy.load("en_core_web_trf")
except:
    pass

ALLOWED_CALLABLE_NAMES = {'current_usage', 'public_key'}  # add here client method names if you feel test gives you true negative results


def _get_all_methods(package_name):
    """Get all ``*Client`` methods."""
    ignored_items = {'API_RESOURCE', 'RESPONSE_MODEL', 'ROOT_NAME'}
    package = importlib.import_module(package_name)
    for loader, name, is_pkg in pkgutil.walk_packages(package.__path__):
        module = importlib.import_module(package_name + '.' + name)
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and obj.__name__ != 'BaseClient' and obj.__name__.endswith('Client'):
                for method_name, method_obj in inspect.getmembers(obj):
                    if not method_name.startswith('_') and method_name not in ignored_items:
                        yield method_name


def _check_first_word_is_verb(phrase) -> bool:
    """Check first word in given phrase is verb."""
    to_phrase: str = 'to {phrase}'.format(phrase=phrase)
    spacy_opinion: bool = any(token.pos_ == "VERB" for token in nlp(to_phrase))
    nltk_opinion: bool = any((tagged_token[1].startswith('V') for tagged_token in nltk.pos_tag(nltk.word_tokenize(to_phrase))))
    return nltk_opinion or spacy_opinion


@pytest.mark.skipif(sys.version_info < (3, 11), reason="requires python3.11 or higher")
def test_client_method_names():
    """Check *Client method names, must contain verb."""
    actions = set([action.replace('_', ' ') for action in _get_all_methods('lago_python_client.clients') if action not in ALLOWED_CALLABLE_NAMES])
    for action in actions:
        assert _check_first_word_is_verb(action) is True
