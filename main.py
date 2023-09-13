import asyncio
import datetime

import aiohttp
from more_itertools import chunked

from models import Base, Session, SwapiPeople, engine


MAX_REQUESTS_CHUNK = 5


async def insert_people(people_list):
    async with Session() as session:
        for people in people_list:
            if people is None:
                break
            new_people = SwapiPeople(
                name=people.get('name'),
                birth_year=people.get('birth_year'),
                eye_color=people.get('eye_color'),
                films=people.get('films'),
                gender=people.get('gender'),
                hair_color=people.get('hair_color'),
                height=people.get('height'),
                homeworld=people.get('homeworld'),
                mass=people.get('mass'),
                skin_color=people.get('skin_color'),
                species=people.get('species'),
                starships=people.get('starships'),
                vehicles=people.get('vehicles')
            )
            session.add(new_people)
            await session.commit()


async def get_inf_people(url, field):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                result = data.get(field)
                return result
            else:
                return None


async def get_people(people_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://swapi.dev/api/people/{people_id}") as response:
            if response.status == 200:
                json_data = await response.json()
                films = [await get_inf_people(url, 'title') for url in json_data.get('films')]
                species = [await get_inf_people(url, 'name') for url in json_data.get('species')]
                starships = [await get_inf_people(url, 'name') for url in json_data.get('starships')]
                vehicles = [await get_inf_people(url, 'name') for url in json_data.get('vehicles')]
                people_inf = {
                    'name': json_data.get('name'),
                    'birth_year': json_data.get('birth_year'),
                    'eye_color': json_data.get('eye_color'),
                    'films': ', '.join(films),
                    'gender': json_data.get('gender'),
                    'hair_color': json_data.get('hair_color'),
                    'height': json_data.get('height'),
                    'homeworld': json_data.get('homeword'),
                    'mass': json_data.get('mass'),
                    'skin_color': json_data.get('skin_color'),
                    'species': ', '.join(species),
                    'starships': ', '.join(starships),
                    'vehicles': ', '.join(vehicles),
                }
                return people_inf
            else:
                return None


async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    for person_ids_chunk in chunked(range(1, 100), MAX_REQUESTS_CHUNK):
        person_coros = [get_people(person_id) for person_id in person_ids_chunk]
        people = await asyncio.gather(*person_coros)
        insert_people_coro = insert_people(people)
        asyncio.create_task(insert_people_coro)

    main_task = asyncio.current_task()
    insets_tasks = asyncio.all_tasks() - {main_task}
    await asyncio.gather(*insets_tasks)

if __name__ == '__main__':
    start = datetime.datetime.now()
    asyncio.run(main())
    print(datetime.datetime.now() - start)
