import logging
from datetime import datetime, date
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import BigInteger, String, Text, Integer, Date, DateTime, Boolean
from config import settings

logger = logging.getLogger(__name__)

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    pool_recycle=300,
    connect_args={"timeout": 30, "check_same_thread": False}
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    telegram_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str | None] = mapped_column(String(150), nullable=True)
    is_premium: Mapped[bool] = mapped_column(Boolean, default=False)
    registered_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class ScanHistory(Base):
    __tablename__ = "scan_history"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger)
    file_name: Mapped[str] = mapped_column(String(255), default="Text Input")
    ai_percent: Mapped[int] = mapped_column(Integer)
    human_percent: Mapped[int] = mapped_column(Integer)
    verdict: Mapped[str] = mapped_column(String(100))
    details: Mapped[str] = mapped_column(Text)
    scanned_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class DailyUsage(Base):
    __tablename__ = "daily_usage"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger)
    usage_date: Mapped[date] = mapped_column(Date, default=date.today)
    count: Mapped[int] = mapped_column(Integer, default=0)

async def init_db():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database initialized successfully.")
    except Exception as e:
        logger.critical(f"Database initialization failed: {e}")
        raise e
