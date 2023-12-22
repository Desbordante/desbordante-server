from datetime import datetime
from uuid import uuid4

feedback_data = [
    {
        "user_id": "6d6d3c27-c39f-4fe5-a1f2-be23271e62f1",
        "rating": 5,
        "text": "some text",
        "id": uuid4(),
        "subject": "subject",
        "created_at": datetime.now(),
    },
    {
        # Without id, subject
        "user_id": "5e5c3c27-c39f-4fe5-a1f2-be23271e62f1",
        "rating": 3,
        "text": "some text",
        "created_at": datetime.now(),
    },
]
