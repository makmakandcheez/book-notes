from uuid import uuid4

import pytest

from app.api.v1.dependencies import get_current_user
from app.core.security import create_access_token
from app.models.user import User
from app.services.auth_service import UserNotFoundError


# token: Annotated[str, Depends(oauth2_scheme)],
# oauth2_scheme only extracts from HTTP request.
# We can just pass a token directly
@pytest.mark.asyncio
async def test_get_current_user(user_repo, auth_service):
    user = await user_repo.create_user(
        User(
            username="Johnny",
            email="1@test.com",
            hashed_password="123"
            )
        )
    token = create_access_token(user.id)
    result = await get_current_user(
        token = token,
        auth_service=auth_service
    )

    assert result.id == user.id


@pytest.mark.asyncio
async def test_get_current_user_wrong_id(auth_service):
    random_id = uuid4()
    token = create_access_token(random_id)
    with pytest.raises(UserNotFoundError):
        await get_current_user(
            token = token,
            auth_service=auth_service
        )
