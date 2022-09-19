from re import A
from aiohttp import web
import aiofiles
import asyncio
import os


async def archive_handler(request: web.Request):
    
    response = web.StreamResponse()

    response.headers['Content-Type'] = 'text/html'
    response.headers['Content-Disposition'] = 'attachment;'\
                                              'filename="archive.zip"'

    await response.prepare(request)
    archive_hash = request.match_info['archive_hash']
    cmd = f"zip -r - ./"
    proc = await asyncio.create_subprocess_shell(
        cmd=cmd,
        cwd = f'{os.getcwd()}/test_photos/{archive_hash}',
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    # 512 kbytes = 524288 bytes
    while True:
        if proc.stdout.at_eof():
            break
        stdout = await proc.stdout.read(n=300)
        await response.write(stdout)
        
    return response


async def index_page_handler(request):
    async with aiofiles.open('index.html', mode='r') as index_file:
        index_contents = await index_file.read()
    return web.Response(text=index_contents, content_type='text/html')


if __name__ == '__main__':
    print(os.getcwd())
    app = web.Application()
    app.add_routes([
        web.get('/', index_page_handler),
        web.get('/archive/{archive_hash}/', archive_handler),
    ])
    web.run_app(app)
