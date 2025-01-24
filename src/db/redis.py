import redis
from src.config import Config

JTI_EXPIRY = 3600

token_block_list = redis.Redis(host=Config.REDIS_HOST, port=Config.REDIS_PORT, db=0)


async def add_jti_to_block_list(jti: str) -> None:
    token_block_list.set(name=jti, value="", ex=JTI_EXPIRY)


async def token_in_blocklist(jti: str) -> bool:
    result = token_block_list.get(jti)

    return result is not None
