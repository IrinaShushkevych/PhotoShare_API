from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from libgravatar import Gravatar

from src.database.models import User
from src.schemas import UserModel
from src.config.settings import messages


async def get_user_by_email(email: str, db: Session) -> User:
    """
    The get_user_by_email function takes in an email and a database session,
    and returns the user associated with that email. If no such user exists,
    it will return None.

    :param email: str: Specify the type of data that is expected to be passed into the function
    :param db: Session: Pass a database session to the function
    :return: The first user in the database with the given email
    :doc-author: Trelent
    """
    return db.query(User).filter(User.email == email).first()


async def create_user(body: UserModel, db: Session) -> User:
    """
    The create_user function creates a new user in the database.
        Args:
            body (UserModel): The UserModel object containing the data to be inserted into the database.
            db (Session): The SQLAlchemy Session object used to interact with our PostgreSQL database.

    :param body: UserModel: Create a new user object from the request body
    :param db: Session: Access the database
    :return: A user object
    :doc-author: Trelent
    """
    user = db.query(User).filter(User.email == body.email).first()
    if user is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=messages.user_exists)
    new_user = User(**body.dict())
    if new_user.avatar is None:
        try:
            g = Gravatar(body.email)
            new_user.avatar = g.get_image()
        except Exception as e:
            print(e)
    db.add(new_user)
    db.commit()
    db.refresh()
    return new_user
