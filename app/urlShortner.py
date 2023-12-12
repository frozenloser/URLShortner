from random import randint
from this import s
from fastapi import APIRouter, HTTPException
from tortoise import Tortoise
from fastapi.responses import RedirectResponse
from models import URLShortner

route = APIRouter()
Tortoise.init_models(["models"], "models")

# shorten url


@route.post('/shortenUrl')
async def shortenUrl(url: str):
    # check if valid url
    if not url.startswith("http://") and not url.startswith("https://"):
        raise HTTPException(status_code=400, detail="Invalid URL")
    # check if url already exists
    urlExists = await URLShortner.filter(url=url).exists()
    if urlExists:
        # get the short url
        obj = await URLShortner.get(url=url)
        shortURL = "http://localhost:8000/getURL/" + obj.shortUrl
        # return the short url
        return {"url": url, "shortURL": shortURL}
    else:
        # Generate unique hash of 6 characters from url
        # check if hash exists
        # if exists, generate new hash
        # else, save url and hash
        charList = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        hash = ""
        for i in range(6):
            hash += charList[randint(0, len(charList)-1)]
        hashExists = await URLShortner.filter(shortUrl=hash).exists()
        if hashExists:
            return await shortenUrl(url)
        else:
            shortURL = "http://localhost:8000/getURL/" + hash
            await URLShortner.create(url=url, shortUrl=hash, status=1, updatedBy=1, createdBy=1, createdIP="")
            return {"url": url, "shortUrl": shortURL}


# get url
@route.get('/getURL/{hash}')
async def getUrl(hash: str):
    # check if hash exists
    isExist = await URLShortner.filter(shortUrl=hash).exists()
    if isExist:
        # get the url
        obj = await URLShortner.get(shortUrl=hash)
        # return the url
        return RedirectResponse(url=obj.url)
    else:
        raise HTTPException(status_code=404, detail="URL not found")

# get all URLS

@route.get("/getAllURLs")
async def getAllURLs():
    isExist = await URLShortner.all().exists()
    if isExist:
        obj = await URLShortner.all().values('url', 'shortUrl')
        return(obj)
    else:
        raise HTTPException(status_code=404, detail="No URLs Found")
