import random
import re

def parse(accomplishment):
    matches = re.findall('(?:&#[0-9]+;)+', accomplishment)
    if not matches:
        matches = [_get_random()]

    # TODO: trim off emoji at the start/end, since they probably don't have
    # semantic meaning.
    return {
        'emoji' : matches,
        'a' : accomplishment,
    }

def _get_random():
    return random.choice(emoji.unicode_codes.UNICODE_EMOJI_ALIAS.keys())
