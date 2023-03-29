from src.schemas import Role

DEFAULT_ROLE = Role.user


class Messages:
    user_created = 'User successfully created'
    user_error_decode_r_token = 'Could not validate credentials'
    user_error_token_scope = 'Invalid scope for token'


messages = Messages()