import uvicorn
from fastapi import FastAPI
from fastapi_healthcheck import HealthCheckFactory, healthCheckRoute
# from src.adapters.driver.entrypoints.v1.register import register as register_router
from src.adapters.driver.entrypoints.v1.v1 import router as v1_router

# from src.adapters.entrypoints.v1.settings import router as settings_router
# from src.configs.depency_injection import Container


def create_app() -> FastAPI:
    # container = Container()
    fast_api = FastAPI()
    # fast_api.container = container
    return fast_api


def create_health_route():
    # Add Health Checks
    _healthChecks = HealthCheckFactory()
    app.add_api_route("/health", endpoint=healthCheckRoute(factory=_healthChecks))


def create_routes():
    app.include_router(v1_router, prefix="/v1")
    # app.include_router(settings_router)


def start():
    create_health_route()
    create_routes()
    uvicorn.run(app, host="0.0.0.0", port=8383)


app = create_app()

if __name__ == "__main__":
    start()
