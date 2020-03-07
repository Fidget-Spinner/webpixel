"""
Main entry point, run this to start the web app.
"""
from aiohttp import web

import views
import signal
import asyncio
import logging
import os

logging.basicConfig(level=logging.DEBUG)

DIR_NAME = os.path.dirname(__file__)


def _add_static_routes(app: web.Application) -> None:
    app.add_routes([web.static("/js", os.path.join(DIR_NAME, "./views/js/")),
                    web.static("/css", os.path.join(DIR_NAME, "./views/css/")),
                    ])


def add_routes(app: web.Application) -> None:
    """ Route adding/resolving for resources and views"""
    _add_static_routes(app)  # add static routes first so that they will be at top of table and retrieved first
    app.add_routes([web.view("/", views.IndexView),
                    ])


async def setup(port: int = 8080) -> (web.AppRunner, web.TCPSite):
    """ Set up AppRunner and TCPSite"""
    app = web.Application()
    add_routes(app)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, None, port=port)
    await site.start()
    print(f"Started site on localhost:{port}")
    return runner, site


async def graceful_shutdown(sig, loop, runner: web.AppRunner, site: web.TCPSite) -> None:
    """ Gracefully terminate the sites and cleanup App runner, then finishes all pending coroutines and stops loop."""
    print(f'Received {sig.name}. Beginning graceful shutdown...', end="")
    await site.stop()
    print(f"Site stopped...", end="")
    await runner.cleanup()
    print(f"AppRunner cleaned up...", end="")
    # list of all other tasks except this coroutine
    tasks = [task for task in asyncio.all_tasks() if task is not asyncio.current_task()]
    list(map(lambda task: task.cancel(), tasks))    # cancel all the tasks
    results = await asyncio.gather(*tasks, return_exceptions=True)
    print(f'Finished awaiting cancelled tasks, results: {results}...', end="")
    await asyncio.sleep(0.07)  # to really make sure everything else has time to stop
    loop.stop()
    print(f"Done!")


async def entry() -> (web.AppRunner, web.TCPSite):
    runner, site = await setup()
    # Only on unix-like systems that support unix signals. Not implemented on windows
    # loop.add_signal_handler(signal.SIGTERM,
    #                         functools.partial(asyncio.ensure_future,
    #                                           graceful_shutdown(signal.SIGTERM, loop, runner, site)))
    return runner, site


def main():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    runner, site = loop.run_until_complete(loop.create_task(entry()))
    try:
        assert runner, "No app runner"
        assert site, "No site running"
        loop.run_forever()
    except AssertionError as error:
        logging.error(error.args)
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(graceful_shutdown(signal.SIGTERM, loop, runner, site))
        loop.close()


if __name__ == "__main__":
    main()


