from datetime import datetime
from app.db.models.user.code import CodeType

code_data = [
    {
        "id": "a3637c76-3e67-4009-8d52-a7456c1c5218",
        "type": CodeType.EMAIL_VERIFICATION_REQUIRED,
        "value": 45445,
        "expiring_date": datetime.now(),
        "user_id": "5e5c3c27-c39f-4fe5-a1f2-be23271e62f1",
        "device_id": "3939939393",
    },
    {
        "id": "2f3c6ddd-eb6c-4bfd-bdf4-413401d48136",
        "type": CodeType.EMAIL_VERIFICATION_REQUIRED,
        "value": 45445,
        "expiring_date": datetime.now(),
        "user_id": "8cb69c83-a2c6-4bce-a20c-a615d1d3f8dd",
        "device_id": "393449939393",
    },
]
