['ls AloneMusic/utils/', 'cat AloneMusic/utils/thumbnails.py']
__init__.py
__pycache__
channelplay.py
database.py
decorators
errors.py
exceptions.py
extraction.py
formatters.py
inline
inlinequery.py
logger.py
pastebin.py
permissions.py
stream
sys.py
thumbnails
thumbnails (13).py
thumbnails.py
thumbnails.py#
['ls AloneMusic/utils/', 'cat AloneMusic/utils/thumbnails.py']
import random

# 🔥 Tumhare diye hue images
RANDOM_THUMBS = [
    "https://files.catbox.moe/ikxb96.jpg",
    "https://files.catbox.moe/dqxsjh.jpg",
    "https://files.catbox.moe/lnaqxk.jpg",
    "https://files.catbox.moe/0qzssp.jpg",
    "https://files.catbox.moe/lz57vi.jpg",
    "https://files.catbox.moe/x1fcb6.jpg",
    "https://files.catbox.moe/32ghsc.jpg",
    "https://files.catbox.moe/tm8vmd.jpg",
]

_last_thumb = None

async def get_thumb(videoid=None):  # videoid ignore
    global _last_thumb

    try:
        choice = random.choice(RANDOM_THUMBS)

        # ❌ same image repeat na ho
        while choice == _last_thumb and len(RANDOM_THUMBS) > 1:
            choice = random.choice(RANDOM_THUMBS)

        _last_thumb = choice
        return choice

    except Exception as e:
        print(e)
        return RANDOM_THUMBS[0]