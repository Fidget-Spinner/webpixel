"""
Logic for index landing page.
"""

from aiohttp import web
from .common import parse_file, read_file

#import logging

#logging.basicConfig(level=logging.WARNING)


class IndexView(web.View):
    """ Router resource entry for index.html """

    async def get(self) -> web.Response:
        template = {"head_boilerplate": await read_file("./boilerplates/head_boilerplate.html")}
        if contents := await parse_file("index.html", template):
            return web.Response(text=contents, content_type="text/html")
        return web.Response(text="Could not load the page")

    # async def post(self) -> web.Response:
    #     return await self.get()



