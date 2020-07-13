import asyncio, time
from timeloop import Timeloop
from datetime import timedelta
from core.database import db

timer = Timeloop()

# defining how often our threads will run
leaderboardUpdate = 86400
leaderboardPrune = 2628288

class Thread():

    @staticmethod
    def start(block=False):
        try:
            #Thread.set_format()
            timer.start(block)
        except Exception as e:
            print(e)

    @staticmethod
    def stop():
        try:
            timer.stop()
        except Exception as e:
            print(e)


async def update():
    try:
        db.scoreboardCompile()

    except Exception as e:
        print(f"[THREAD] Update Error! {e}!")


async def prune():
    try:
        db.scoreboardTrim()

    except Exception as e:
        print(f"[THREAD] Pruning Error! {e}!")


@timer.job(interval=timedelta(seconds = leaderboardUpdate))
def runUpdate():
    #"""Run the process asynchronously on a timer."""
    asyncio.run(update())


@timer.job(interval=timedelta(seconds = leaderboardPrune))
def runPrune():
    #"""Run the process asynchronously on a timer."""
    asyncio.run(prune())
