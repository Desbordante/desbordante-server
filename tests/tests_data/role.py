from app.db.models.user.role import RoleType

role_data = [
    {
        "user_id": "5e5c3c27-c39f-4fe5-a1f2-be23271e62f1",
        "type": RoleType.ANONYMOUS,
        "permission_indices": "some indices",
        "id": "54e660d5-daa0-4946-9050-a68c6dd5f0db",
    },
    {
        "user_id": "8cb69c83-a2c6-4bce-a20c-a615d1d3f8dd",
        "type": RoleType.ADMIN,
        "permission_indices": "some indices",
        "id": "dc658aeb-c0ba-45fe-aceb-6ccf327c35de",
    },
    {
        "user_id": "6d6d3c27-c39f-4fe5-a1f2-be23271e62f1",
        "type": RoleType.USER,
        "permission_indices": "some indices",
        "id": "b43234ec-086f-47e9-aade-3d17a8f589cc",
    },
]
