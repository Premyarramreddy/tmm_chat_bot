from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from config.settings import settings

DB_URL = (
    f"postgresql+asyncpg://{settings.DB_USER}:"
    f"{settings.DB_PASS}@{settings.DB_HOST}:"
    f"{settings.DB_PORT}/{settings.DB_NAME}"
)

# Async Engine with connection pooling
engine = create_async_engine(
    DB_URL,
    echo=False,         # set True for debugging SQL
    pool_size=10,       # number of persistent connections in the pool
    max_overflow=20,    # extra connections beyond pool_size
    pool_timeout=30,    # seconds to wait for a free connection
    pool_recycle=1800,  # recycle connections every 30 min
)

# Async Session factory
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Dependency for FastAPI
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
