from app.db.models.user.permission import AllPermissions

permission_data = [
    {"id": "1", "permission": AllPermissions.CAN_MANAGE_APP_CONFIG},
    {"id": "2", "permission": AllPermissions.CAN_USE_USERS_DATASETS},
    {"id": "3", "permission": AllPermissions.CAN_USE_BUILTIN_DATASETS},
    {"id": "4", "permission": AllPermissions.CAN_USE_OWN_DATASETS},
    {"id": "5", "permission": AllPermissions.CAN_MANAGE_USERS_SESSIONS},
    {"id": "6", "permission": AllPermissions.CAN_VIEW_ADMIN_INFO},
]
