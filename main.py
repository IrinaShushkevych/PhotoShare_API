from fastapi import FastAPI

app = FastAPI(title='PhotoShareAPI')


@app.get('/')
def root_path():
    return {'message': 'Hello!'}
