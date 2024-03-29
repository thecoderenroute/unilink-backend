from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from src.twitter.utils import TwitterWrapper

from pprint import pprint

# from ...main import twitter_service as twtsrvc

twitter_router = APIRouter(prefix="/twitter")


@twitter_router.get("/")
async def get_twitter():
    return "twitter app created!"


@twitter_router.get("/user/{username}")
async def get_user(username: str, twitter_service: TwitterWrapper = Depends()):
    user_data = twitter_service.get_user_data_from_username(username)
    pprint(user_data)
    # print(user_data)
    print(type(user_data))
    json_compatible_item_data = jsonable_encoder(user_data)
    return JSONResponse(content=json_compatible_item_data)


@twitter_router.get("/tweets/{username}")
async def get_user_tweets(username: str, twitter_service: TwitterWrapper = Depends()):
    user_data = twitter_service.get_users_recent_tweets(username)
    json_compatible_item_data = jsonable_encoder(user_data)
    return JSONResponse(content=json_compatible_item_data)


@twitter_router.get("/create_tweet")
async def create_twitter_tweet(text: str, twitter_service: TwitterWrapper = Depends()):
    res = twitter_service.create_tweet(text)
    json_compatible_item_data = jsonable_encoder(res)
    return JSONResponse(content=json_compatible_item_data)


@twitter_router.get("/delete_tweet")
async def delete_tweet_by_id(
    tweet_id: int, twitter_service: TwitterWrapper = Depends()
):
    res = twitter_service.delete_tweet(tweet_id)
    json_compatible_item_data = jsonable_encoder(res)
    return JSONResponse(content=json_compatible_item_data)
