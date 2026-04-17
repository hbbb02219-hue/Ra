import os
import re
import random

import aiofiles
import aiohttp
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont
from py_yt import VideosSearch

from config import YOUTUBE_IMG_URL

# 🔥 RANDOM THUMBNAILS LIST
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


def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    return image.resize((newWidth, newHeight))


async def get_thumb(videoid=None):
    global _last_thumb

    # 🔥 50% chance random thumbnail
    if random.choice([True, False]) or not videoid:
        try:
            choice = random.choice(RANDOM_THUMBS)

            while choice == _last_thumb and len(RANDOM_THUMBS) > 1:
                choice = random.choice(RANDOM_THUMBS)

            _last_thumb = choice
            return choice
        except Exception as e:
            print(f"Random Thumb Error: {e}")
            return RANDOM_THUMBS[0]

    # 🔥 ORIGINAL YOUTUBE THUMB LOGIC
    try:
        if os.path.isfile(f"cache/{videoid}.png"):
            return f"cache/{videoid}.png"

        url = f"https://www.youtube.com/watch?v={videoid}"
        results = VideosSearch(url, limit=1)

        for result in (await results.next())["result"]:
            title = re.sub(r"\W+", " ", result.get("title", "Unsupported Title")).title()
            duration = result.get("duration", "Unknown")
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
            views = result.get("viewCount", {}).get("short", "Unknown Views")

        async with aiohttp.ClientSession() as session:
            async with session.get(thumbnail) as resp:
                if resp.status == 200:
                    f = await aiofiles.open(f"cache/thumb{videoid}.png", mode="wb")
                    await f.write(await resp.read())
                    await f.close()

        youtube = Image.open(f"cache/thumb{videoid}.png")

        image1 = changeImageSize(1280, 720, youtube)
        image1 = image1.filter(ImageFilter.GaussianBlur(20))
        image1 = ImageEnhance.Brightness(image1).enhance(0.4)

        youtube_thumb = youtube.resize((840, 460))
        image1.paste(youtube_thumb, (220, 70))

        draw = ImageDraw.Draw(image1)

        try:
            font = ImageFont.truetype("arial.ttf", 40)
        except:
            font = ImageFont.load_default()

        draw.text((50, 550), title[:40], fill="white", font=font)

        try:
            os.remove(f"cache/thumb{videoid}.png")
        except:
            pass

        file_name = f"cache/{videoid}.png"
        image1.save(file_name)

        return file_name

    except Exception as e:
        print(f"YT Thumb Error: {e}")
        return YOUTUBE_IMG_URL


async def get_qthumb(vidid):
    try:
        url = f"https://www.youtube.com/watch?v={vidid}"
        results = VideosSearch(url, limit=1)
        for result in (await results.next())["result"]:
            return result["thumbnails"][0]["url"].split("?")[0]
    except Exception as e:
        print(e)
        return YOUTUBE_IMG_URL