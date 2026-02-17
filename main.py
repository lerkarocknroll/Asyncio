import asyncio
from datetime import datetime

from aiohttp import ClientSession
from more_itertools import chunked

from db import Session, PersonModel, engine, Base

CHUNK_SIZE = 10

async def get_total_people(session: ClientSession) -> int:
    async with session.get('https://www.swapi.tech/api/people') as resp:
        data = await resp.json()
        return data['total_records']

async def get_person(person_id: int, session: ClientSession):
    print(f'begin {person_id}')
    url = f'https://www.swapi.tech/api/people/{person_id}'
    async with session.get(url) as response:
        if response.status == 404:
            print(f'end {person_id} (not found)')
            return None
        data = await response.json()
        props = data['result']['properties']
        uid = data['result']['uid']
        print(f'end {person_id}')
        return {
            'person_id': uid,
            'birth_year': props.get('birth_year'),
            'eye_color': props.get('eye_color'),
            'gender': props.get('gender'),
            'hair_color': props.get('hair_color'),
            'mass': props.get('mass'),
            'name': props.get('name'),
            'skin_color': props.get('skin_color'),
            'homeworld': props.get('homeworld'),   # сохраняем URL
        }

async def insert_people(people_chunk):
    if not people_chunk:
        return
    async with Session() as session:
        people_models = [PersonModel(**person_data) for person_data in people_chunk]
        session.add_all(people_models)
        await session.commit()

async def get_people(total: int):
    async with ClientSession() as session:
        for id_chunk in chunked(range(1, total + 1), CHUNK_SIZE):
            coroutines = [get_person(i, session=session) for i in id_chunk]
            results = await asyncio.gather(*coroutines)
            valid_people = [r for r in results if r is not None]
            if valid_people:
                await insert_people(valid_people)

async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with ClientSession() as session:
        total = await get_total_people(session)
        print(f'Всего персонажей: {total}')
        await get_people(total)

if __name__ == '__main__':
    start = datetime.now()
    asyncio.run(main())
    print(f'Время выполнения: {datetime.now() - start}')