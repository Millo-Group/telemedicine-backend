from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

from os.path import abspath
from dotenv import load_dotenv

from .routes import api, jitsi
from .services.database import init_db
from .services.oddo_service import OdooService
from .config import Settings


def create_app():
    staticdir = abspath('app/static')

    app = FastAPI()

    load_dotenv()

    # settings
    settings = Settings()

    # init database here
    db = init_db()



    odoo_service = OdooService(
        url='https://infinityclinic.co',
        username='lbansal.75way@gmail.com',
        password='123'
    )

    @app.middleware("http")
    async def db_session_middleware(request: Request, call_next):
        request.state.db = db
        request.state.odoo = odoo_service
        request.state.settings = settings
        response = await call_next(request)
        return response
    
    # routes
    app.include_router(api.router,  prefix="/api")
    app.mount("", StaticFiles(directory=staticdir), name="static")
    app.include_router(jitsi.router)

 
    return app
