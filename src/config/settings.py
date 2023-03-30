from src.schemas import Role

DEFAULT_ROLE = Role.user


class Messages:
    app_welcome = 'Welcome!'
    db_connect_error = 'Connect to DB failed'
    db_error_config = 'DB configuration is wrong'
    user_created = 'User successfully created'
    user_error_decode_r_token = 'Could not validate credentials'
    user_error_token_scope = 'Invalid scope for token'
    user_exists = 'User already exist'


messages = Messages()
