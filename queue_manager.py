import asyncio

QUEUE = asyncio.Queue()

async def worker():
    while True:
        task = await QUEUE.get()
        try:
            await task()
        except Exception as e:
            print("Worker Error:", e)
        QUEUE.task_done()