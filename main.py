from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.database.connect import get_db
from src.config.settings import messages

app = FastAPI(title='PhotoShareAPI')


@app.get('/')
def root_path():
    return {'message': messages.app_welcome}


@app.get('/healthchecker')
def health_checker(db: Session = Depends(get_db)):
    try:
        result = db.execute(text('SELECT 1')).fetchone()
        if result is None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=messages.db_error_config)
        return {'message': messages.app_welcome}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=messages.db_connect_error)
