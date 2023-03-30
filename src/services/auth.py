import redis
import pickle
from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status, Depends
from jose import jwt, JWTError
from typing import Optional

from sqlalchemy.orm import Session

from src.database.connect import get_db
from src.config.config import settings
from src.config.settings import messages
from src.repositories.auth import get_user_by_email


class Auth:
    algorithm = settings.algorithm
    secret_key = settings.secret_key
    pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')
    auth_redis = redis.Redis(host=settings.redis_host, port=settings.redis_port, db=settings.redis_db)

    def create_hash_password(self, password: str):
        """
        The create_hash_password function takes a password as an argument and returns the hashed version of that
        password. The hashing algorithm used is PBKDF2 with SHA256, which is considered to be cryptographically secure.

        :param self: Represent the instance of the class
        :param password: str: Create a hash password
        :return: A hash of the password
        :doc-author: Trelent
        """
        return self.pwd_context.hash(password)

    def verify_password(self, password: str, hashed_password: str):
        """
        The verify_password function takes a plain-text password and hashed password as arguments.
        It then uses the verify method of the pwd_context object to check if they match.

        :param self: Represent the instance of the class
        :param password: str: Verify the password that is entered by the user
        :param hashed_password: str: Pass in the hashed password from the database
        :return: A boolean value
        :doc-author: Trelent
        """
        return self.pwd_context.verify(password, hashed_password)

    def create_access_token(self, data: dict, expires_delta: Optional[float] = None):
        """
        The create_access_token function creates a JWT token that contains the data passed to it. The function also
        takes an optional expires_delta parameter, which is a datetime.timedelta object that indicates for how long
        the token will be valid.

        :param self: Refer to the current class instance
        :param data: dict: Pass the data that will be encoded into the jwt
        :param expires_delta: Optional[float]: Set the expiration time of the token
        :return: An encoded jwt token
        :doc-author: Trelent
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(minutes=10)
        to_encode.update({'exp': expire, 'iat': datetime.utcnow(), 'scope': 'access_token'})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    def create_refresh_token(self, data: dict, expires_delta: Optional[float] = None):
        """
        The create_refresh_token function creates a refresh token. Args: data (dict): A dictionary containing the
        user's id and username. expires_delta (Optional[float]): The time in seconds until the token expires.
        Defaults to None, which sets it to 1 day from now.

        :param self: Represent the instance of the class
        :param data: dict: Pass the data that will be encoded into the token
        :param expires_delta: Optional[float]: Set the expiration time of the refresh token
        :return: A refresh token that is encoded with the user's id, email, and username
        :doc-author: Trelent
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(days=1)
        to_encode.update({'exp': expire, 'iat': datetime.utcnow(), 'scope': 'refresh_token'})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    def decode_refresh_token(self, token: str):
        """
        The decode_refresh_token function is used to decode the refresh token.
            The function takes in a token as an argument and returns the payload of that token.
            If there is an error decoding or if the scope of the payload does not equal 'refresh_token',
            then it will raise a HTTPException with status code 401 Unauthorized.

        :param self: Represent the instance of the class
        :param token: str: Pass in the token that is to be decoded
        :return: A payload, which is a dictionary containing the user's id
        :doc-author: Trelent
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            if payload['scope'] == 'refresh_token':
                return payload['sub']
            else:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=messages.user_error_token_scope)
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=messages.user_error_decode_r_token)

    async def get_current_user(self, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db())):
        """
        The get_current_user function is a dependency that can be injected into any endpoint function.
        It will decode the JWT token and return the user object if it exists, otherwise it will raise an exception.

        :param self: Access the class attributes and methods
        :param token: str: Get the token from the request header
        :param db: Session: Get a database session
        :return: The user object
        :doc-author: Trelent
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=messages.user_error_decode_r_token,
            headers={'WWW_Authenticate': 'Bearer'}
        )
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            if payload['scope'] == 'access_token':
                email = payload['sub']
                if email is None:
                    raise credentials_exception
            else:
                raise credentials_exception
        except JWTError:
            raise credentials_exception

        user = self.auth_redis.get(f'user:{email}')
        if user is None:
            user = await get_user_by_email(email, db)
            if user is None:
                raise credentials_exception
            self.auth_redis.set(f'user:{email}', pickle.dumps(user))
            self.auth_redis.expire(f'user:{email}', 10000)
        else:
            user = pickle.loads(user)

        return user


auth_service: Auth = Auth()
