from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

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

    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
 
    @app.middleware("http")
    async def db_session_middleware(request: Request, call_next):
        request.state.db = db
        request.state.odoo = odoo_service
        request.state.settings = settings
        response = await call_next(request)
        return response
    
    # api routes
    api_app = FastAPI(title="apis")
    api_app.include_router(api.router)
    app.mount('/api', api_app)

    # static files
    app.mount("/", StaticFiles(directory=staticdir), name="static")

    return app
