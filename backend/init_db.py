import os
import asyncio
from datetime import datetime, timezone

from src.db import init_db
from src.security.password import hash_password
from src.models.users import UserDocument


DUMMY_ADMIN_EMAIL: str = 'admin@example.com'
DUMMY_ADMIN_PASSWORD: str = 'admin123'
IS_DEV: bool = os.getenv('IS_DEV', 'false').lower() == 'true'


async def ensure_dummy_admin_user() -> None:
    if not IS_DEV:
        print('⚠ Skipping dummy admin user creation.')
        return

    print('👤 Ensuring dummy admin user exists...')

    existing = await UserDocument.find_one(UserDocument.email == DUMMY_ADMIN_EMAIL)
    if existing:
        print(f'ℹ Dummy admin {DUMMY_ADMIN_EMAIL} already exists, skipping')
        return

    user: UserDocument = UserDocument(
        email=DUMMY_ADMIN_EMAIL,
        password=hash_password(DUMMY_ADMIN_PASSWORD),
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    await user.insert()
    print(f'✔ Inserted dummy admin user: {DUMMY_ADMIN_EMAIL}')


async def main_async() -> None:
    print('🔗 Connecting DB and initializing Beanie...')
    await init_db()
    print('✔ Beanie initialized.')
    await ensure_dummy_admin_user()
    print('🎉 DB initialization done.')


if __name__ == '__main__':
    asyncio.run(main_async())
