from src.domain.authorization.entities import Actor, Task


class TaskPolicy:
    """Access policy for tasks."""

    def can_read(self, actor: Actor, task: Task) -> bool:
        if actor.is_admin:
            return True

        return task.is_public or task.owner_id == actor.user_id

    def can_create(self, actor: Actor, task: Task) -> bool:
        if actor.is_admin:
            return True

        is_anonymous = actor.user_id is None

        if is_anonymous and task.is_public:
            return True

        return task.owner_id == actor.user_id and not task.is_public
