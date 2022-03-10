from app.logger import get_logger
from app.schemas.user import User
from app.services.user import user_service


log = get_logger(__name__)


async def create_default_user() -> None:
    try:
        user = User(username="guest", password="guest")
        user_in_db = await user_service.find(payload={"username": user.username})
        if user_in_db:
            raise Exception("Default user already exists. Skipping creation")
        created_user = await user_service.create(payload=user)
        log.info("Default user created successfully with ID=", created_user.id)
    except Exception as e:
        log.error(f"{e}")
