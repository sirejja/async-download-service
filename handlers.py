from aiohttp import web
import aiofiles
import asyncio
import logging
from context_managers import ZipContextManager


async def archive_handler(request: web.Request) -> web.StreamResponse:
    if not(archive_hash := request.match_info['archive_hash']):
        raise web.HTTPNotFound(
                text='Архив не существует или был удален'
            )

    response = web.StreamResponse()
    response.enable_chunked_encoding()
    response.headers['Content-Type'] = 'text/html'
    response.headers['Content-Disposition'] = 'attachment;'\
                                              'filename="archive.zip"'
    await response.prepare(request)

    async with ZipContextManager(
        path_to_photos=request.app["settings"].storage,
        archive_hash=archive_hash) as proc:
        try :
            while True:
                await asyncio.sleep(request.app["settings"].delay)
                chunk = await proc.read_chunked_zip_stdout()
                if not chunk:
                    break
                await response.write(chunk)
        except ConnectionResetError:
            logging.info('Download was interrupted')

    return response


async def index_page_handler(request: web.Request) -> web.Response:
    async with aiofiles.open('index.html', mode='r') as index_file:
        index_contents = await index_file.read()
    return web.Response(text=index_contents, content_type='text/html')