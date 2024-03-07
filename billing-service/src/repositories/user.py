from sqlalchemy.orm import Session


class UserRepository:
    def __init__(
            self,
            session: Session,
    ):
        self._session = session

    def get_by_id(
        self, id_: int, lock: bool = False, **lock_params: Any
    ):
        query = self._session.query(User)

        if lock:
            query = query.with_for_update(**lock_params)

        return self(query.filter(User.id == id_).first())

    def get_by_public_id(
        self, public_id: str, lock: bool = False, **lock_params: Any
    ):
        query = self._session.query(User)
        if lock:
            query = query.with_for_update(**lock_params)

        return query.filter(User.public_id == public_id).first()

    def get_or_create(self, public_id: str) -> Task:
        user = self.get_by_public_id(public_id=public_id, lock=True)
        if not user:
            user = self._session.execute(
                insert(User)
                .values(public_id=public_id)
                .on_conflict_do_nothing(
                    index_elements=["public_id"],
                )
            )
        return user
