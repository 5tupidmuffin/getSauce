import asyncio
from pysaucenao import SauceNao
import time
from utils import logit
import os


key = os.environ.get('API_KEY')  # required for api look up
sauce = SauceNao(api_key= key, min_similarity= 55.0)  # minimum similarity percentage


async def getUrlSauce(url):  # sauce from image url
    """
    Retrieves Source of Image

    url : Url pointing to Image
    """
    results = await sauce.from_url(url)
    time.sleep(0.5)  # to tackle "RuntimeError: Event loop is closed" bug
    print()
    logit(f"30 sec Limit: {results.short_remaining}")
    logit(f" daily Limit: {results.long_remaining}")
    print()
    return results

async def getImageSauce(filePath):  # sauce from image file
    """
    Retrieves Source of Iamge

    filePath : path to the image file 
    """
    results = await sauce.from_file(filePath)
    time.sleep(0.5)  # to tackle "RuntimeError: Event loop is closed" bug
    print()
    logit(f"30 sec Limit: {results.short_remaining}")
    logit(f" daily Limit: {results.long_remaining}")
    print()
    return results

