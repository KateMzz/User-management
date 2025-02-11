from sqlalchemy.ext.asyncio import AsyncSession


class AsyncBase:
    """
    Define initialization method, which takes
    one argument - session to connect to database.
    """

    def __init__(self, session: AsyncSession):
        self.session = session
