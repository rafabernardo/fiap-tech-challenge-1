import uvicorn
from fastapi import FastAPI
from fastapi_healthcheck import HealthCheckFactory, healthCheckRoute

from src.adapters.driver.entrypoints.v1.v1 import router as v1_router
from src.config.settings import get_settings

settings = get_settings()
print(settings.API_PORT)


def create_app() -> FastAPI:
    fast_api = FastAPI()
    fast_api.add_api_route(
        "/health", endpoint=healthCheckRoute(factory=HealthCheckFactory())
    )
    return fast_api


def create_health_route():
    # Add Health Checks
    health_checks = HealthCheckFactory()
    app.add_api_route("/health", endpoint=healthCheckRoute(factory=health_checks))


def create_routes():
    app.include_router(v1_router, prefix="/v1")


def start():
    create_health_route()
    create_routes()
    uvicorn.run(app, host="0.0.0.0", port=settings.API_PORT)


app = create_app()

if __name__ == "__main__":
    start()
