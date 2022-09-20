from aiohttp import web
import logging
import handlers
import cli
import dotenv


def get_app(args):
    app = web.Application()
    app["settings"] = args
    app.add_routes([
        web.get('/', handlers.index_page_handler),
        web.get('/archive/{archive_hash}/', handlers.archive_handler),
    ])
    return app


def main():
    dotenv.load_dotenv()
    args = cli.get_args()
    logging.basicConfig(level=args.log)
    app = get_app(args)
    web.run_app(app)


if __name__ == "__main__":
    main()
