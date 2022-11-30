import asyncio
import os
from aiohttp import web
import logging

class ZipContextManager:
    def __init__(self, path_to_photos: str, archive_hash: str):
        if path_to_photos[-1] == '/':
            self.path_to_photos = f'{path_to_photos}{archive_hash}'
        else:
            self.path_to_photos = f'{path_to_photos}/{archive_hash}'
        self.proc = None

    async def __aenter__(self):
        if not os.path.exists(self.path_to_photos):
            raise web.HTTPNotFound(
                text='Архив не существует или был удален'
            )
        self.proc = await asyncio.create_subprocess_exec(
            "zip", "-r - ./",
            cwd=self.path_to_photos,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        self.stdout = self.proc.stdout
        self.stderr = self.proc.stderr

        return self

    async def read_chunked_zip_stdout(self) -> bytes:
        if self.proc.stdout.at_eof():
            return None
        logging.info('Sending archive chunk ...')
        stdout = await self.proc.stdout.read(n=100)
        return stdout

    async def __aexit__(self, exc_type, exc, traceback):
        if exc:
            self.proc.terminate()
            if not asyncio.get_event_loop().is_closed():
                await self.proc.communicate()