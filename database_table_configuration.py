from loguru import logger


def configure_and_fill_database_tables() -> None:
    from database import Creator, Filler
    import asyncio
    creator = Creator()
    filler = Filler()
    asyncio.run(creator.recreate_all_tables())
    asyncio.run(filler.fill_necessarily_tables())


if __name__ == '__main__':
    configure_and_fill_database_tables()
