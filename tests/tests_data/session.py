from datetime import datetime
from app.db.models.user.session import SessionStatusType

session_data = [
    {
        "user_id": "8cb69c83-a2c6-4bce-a20c-a615d1d3f8dd",
        "device_id": "3939939393",
        "status": SessionStatusType.VALID,
        "id": "dd76f362-dc9f-4514-a923-c56fcc655d70",
        "access_token_iat": 4535434,
        "refresh_token_iat": None,
        "created_at": datetime.now(),
    },
    {
        "user_id": "5e5c3c27-c39f-4fe5-a1f2-be23271e62f1",
        "device_id": "393449939393",
        "status": SessionStatusType.INVALID,
        "id": "9a8fe773-3b41-49dc-a034-f491c0490ad4",
        "access_token_iat": 545334,
        "refresh_token_iat": 45554,
        "created_at": datetime.now(),
    },
    {
        # Without defined fields.
        "user_id": "6d6d3c27-c39f-4fe5-a1f2-be23271e62f1",
        "device_id": "3443434",
        "status": SessionStatusType.INVALID,
    },
]
