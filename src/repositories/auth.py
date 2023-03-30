from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from libgravatar import Gravatar

from src.database.models import User
from src.schemas import UserModel, UserUpdateModel
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
    db.refresh(new_user)
    return new_user


async def update_user(email: str, body: UserUpdateModel, db: Session) -> User:
    """
    The update_user function updates a user's information in the database.
        Args:
            email (str): The email of the user to update.
            body (UserUpdateModel): A UserUpdateModel object containing updated information for the user.
            db (Session): An open connection to a database session, used by SQLAlchemy ORM to communicate with said DBMS.

    :param email: str: Find the user by email
    :param body: UserUpdateModel: Pass the user's updated information to the database
    :param db: Session: Access the database
    :return: The user object that was updated
    :doc-author: Trelent
    """
    user = await get_user_by_email(email, db)
    if user:
        if body.username:
            user.username = body.username
        if body.firstname:
            user.firstname = body.firstname
        if body.lastname:
            user.lastname = body.lastname
        db.commit()
    return user


async def update_avatar(email: str, avatar_url: str, db: Session) -> User:
    """
    The update_avatar function updates the avatar of a user.

    :param email: str: Identify the user
    :param avatar_url: str: Update the avatar url of a user
    :param db: Session: Pass in the database session
    :return: The user object with the updated avatar url
    :doc-author: Trelent
    """
    user = await get_user_by_email(email, db)
    if user:
        user.avatar = avatar_url
        db.commit()
    return user


async def update_password(email: str, password:str, db: Session) -> User:
    """
    The update_password function updates the password of a user in the database.
        Args:
            email (str): The email address of the user to update.
            password (str): The new password for this user.

    :param email: str: Identify the user in the database
    :param password:str: Update the password of a user
    :param db: Session: Access the database
    :return: The user object
    :doc-author: Trelent
    """
    user = await get_user_by_email(email, db)
    if user:
        user.password = password
        db.commit()
    return user


async def change_active(email: str, is_active: bool, db: Session) -> User:
    """
    The change_active function takes in an email and a boolean value,
    and changes the is_active field of the user with that email to be equal to the boolean.


    :param email: str: Get the user by email
    :param is_active: bool: Set the user's is_active status to true or false
    :param db: Session: Pass in the database session to the function
    :return: The user object
    :doc-author: Trelent
    """
    user = await get_user_by_email(email, db)
    if user:
        user.is_active = is_active
        db.commit()
    return user
