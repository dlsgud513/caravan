from typing import Optional, Dict
from src.models.user import User
from src.repositories.base_repository import BaseRepository

class UserRepository(BaseRepository[User]):
    """
    User-specific repository providing additional query methods.
    """
    def __init__(self):
        super().__init__()
        # Add an index for finding users by email efficiently.
        self._email_to_id: Dict[str, int] = {}

    def save(self, entity: User) -> User:
        """
        Saves a user entity and updates the email index.
        """
        # If the user already has an ID, it might be an update.
        # Remove the old email from the index if it's being changed.
        if entity.user_id and entity.user_id in self._data:
            old_user = self._data[entity.user_id]
            if old_user.email != entity.email:
                self._email_to_id.pop(old_user.email, None)

        saved_entity = super().save(entity)
        self._email_to_id[saved_entity.email] = saved_entity.user_id
        return saved_entity

    def find_by_email(self, email: str) -> Optional[User]:
        """
        Finds a user by their email address.
        """
        user_id = self._email_to_id.get(email)
        if user_id is not None:
            return self.find_by_id(user_id)
        return None

    def delete(self, entity_id: int) -> bool:
        """
        Deletes a user and removes them from the email index.
        """
        user = self.find_by_id(entity_id)
        if user:
            self._email_to_id.pop(user.email, None)
        return super().delete(entity_id)

    def clear(self):
        """Clears all user data and indices."""
        super().clear()
        self._email_to_id.clear()
