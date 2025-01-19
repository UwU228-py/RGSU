import sqlite3
import aiosqlite

async def create_db():
    async with aiosqlite.connect('schedule.db') as conn:
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS schedule (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                day TEXT NOT NULL,
                subject TEXT NOT NULL
            )
        ''')
        await conn.commit()

async def add_schedule(day, subject):
    async with aiosqlite.connect('schedule.db') as conn:
        await conn.execute('INSERT INTO schedule (day, subject) VALUES (?, ?)', (day, subject))
        await conn.commit()

async def get_schedule(day):
    async with aiosqlite.connect('schedule.db') as conn:
        async with conn.execute('SELECT subject FROM schedule WHERE day = ?',(day,)) as cursor:
            subjects = await cursor.fetchall()
            return subjects
