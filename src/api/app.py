import uvicorn
from fastapi import FastAPI
from fastapi_healthcheck import HealthCheckFactory, healthCheckRoute

from api.v1 import get_v1_routers
from core.dependency_injection import Container
from core.settings import get_settings

settings = get_settings()
print(settings.API_PORT)


def create_app() -> FastAPI:
    container = Container()
    fast_api = FastAPI(
        openapi_url="/api/openapi.json",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        root_path=settings.ROOT_PATH,
    )
    fast_api.add_api_route(
        "/health", endpoint=healthCheckRoute(factory=HealthCheckFactory())
    )
    fast_api.include_router(get_v1_routers())
    fast_api.container = container
    return fast_api


def create_health_route():
    # Add Health Checks
    health_checks = HealthCheckFactory()
    app.add_api_route(
        "/health", endpoint=healthCheckRoute(factory=health_checks)
    )


def create_routes():
    app.include_router(get_v1_routers())


def start():
    create_health_route()
    create_routes()
    uvicorn.run(app, host="0.0.0.0", port=settings.API_PORT)


app = create_app()

if __name__ == "__main__":
    start()
