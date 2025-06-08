from .routes import router

def register_routes(app):
    app.include_router(router)
