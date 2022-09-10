#!/usr/bin/python3

from pprint import pprint
import aiohttp
import asyncio
import json
from my_key import SpotifyClient
import random
import re
import sys
import time

offset = random.randint(1, 1000)
real_offset = str(offset)

# key = os.getenv('RAPID_API_KEY')
# client_id = os.getenv('UNSPLASH_KEY')

async def get_weather(client):
    weather_url = "https://weatherapi-com.p.rapidapi.com/current.json"
    querystring = {
        'q': 'ibadan'
    }
    headers = {
        "X-RapidAPI-Key": SpotifyClient.rapid_key(),
	    "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
    }
    async with client.get(url=weather_url, params=querystring, headers=headers) as response:
        assert response.status == 200
        location_data = await response.json()
        return location_data

async def image(client):
    client_id = SpotifyClient.unsplash_id()
    unspalsh_url = f'https://api.unsplash.com/photos/random/?client_id={client_id}'
    querystring = {
        'Accept-Version': 'v1',
        'orientation': 'squarish',
        'content_filter': 'low',
        'query': 'weather'
    }
    
    async with client.get(url=unspalsh_url, params=querystring) as response:
        assert response.status == 200
        image_data = await response.json()
        return image_data

async def tracks(client):
    track_url = "https://spotify81.p.rapidapi.com/search"

    querystring = {
        "q":"weather",
        "type":"tracks",
        "offset": real_offset,
        "limit":"1",
        "numberOfTopResults":"1"
    }

    headers = {
	"X-RapidAPI-Key": SpotifyClient.rapid_key(),
	"X-RapidAPI-Host": "spotify81.p.rapidapi.com"
}
    async with client.get(url=track_url, params=querystring, headers=headers) as response:
        assert response.status == 200
        track_data = await response.json()
        return track_data


async def main1():
    async with aiohttp.ClientSession() as session:
        data1 = await get_weather(session)
        name = data1['location']['name']
        cloud = data1['current']['cloud']
        temp_c = data1['current']['temp_c']
        weather_info = {
            'location_name': name,
            'cloud': cloud,
            'temp_c': temp_c
        }
        return (weather_info)

async def main2():
    async with aiohttp.ClientSession() as session:
        data2 = await image(session)
        image_link = data2['urls']['small']
        alt_desc = data2['alt_description']
        firstname_of_owner = data2['user']['first_name']
        lastname_of_owner = data2['user']['last_name']
        image_info = {
            'image_link': image_link,
            'alt_desc': alt_desc,
            'first_name': firstname_of_owner,
            'lastname': lastname_of_owner
        }
        return (image_info)

async def main3():
    async with aiohttp.ClientSession() as session:
        album_info_dict = {}
        data3 = await tracks(session)
        # pprint (data3)
        album_info_list = data3['tracks']
        album_info_dict = album_info_list[0]
        track_name = album_info_dict['data']['name']
        track_id = album_info_dict['data']['id']
        track_url = "https://open.spotify.com/embed/track/" + track_id + "?utm_source=generator"
        track_info = {
            'track_id': track_id,
            'name': track_name,
            'url': track_url
        }
        # pprint(track_info)
        return (track_info)
    
#         album_info_list = data3['tracks']
#         album_info_dict = album_info_list[0]
#         name = album_info_dict['album']['name']
#         track_url = album_info_dict['external_urls']['spotify']
#         url_split = re.sub('.com/', '.com/embed/', track_url)
#         real_track_url = url_split + "?utm_source=generator"
#         track_info = {
#             'track_name': name,
#             "url": real_track_url 
#         }
#     return (track_info)


async def all_calls():
    """ Schedule three calls *concurrently*:"""
    dict_all_three_data = {}
    # print(f"started at {time.strftime('%X')}")
    all_three_data = await asyncio.gather(
        main1(),
        main2(),
        main3(),
    )
    dict_weather = all_three_data[0]
    dict_image = all_three_data[1]
    dict_music = all_three_data[2]
    dict_all_three_data = {**dict_weather, **dict_image, **dict_music}
    pprint (dict_all_three_data)
    return (dict_all_three_data)
    # print(f"ended at {time.strftime('%X')}")

# asyncio.run(main3())