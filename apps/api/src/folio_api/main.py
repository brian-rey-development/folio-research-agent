from fastapi import FastAPI

HEALTH_PATH = "/health"
HEALTH_BODY = {"status": "ok"}


def create_app() -> FastAPI:
    app = FastAPI(title="Folio API")

    @app.get(HEALTH_PATH)
    def health() -> dict[str, str]:
        return HEALTH_BODY

    return app


app = create_app()
