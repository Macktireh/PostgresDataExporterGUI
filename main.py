from dependency_injector.wiring import Provide, inject
from dotenv import load_dotenv

from app import App
from containers import Container
from interface import IServiceDataProcessor


load_dotenv(".env")


@inject
def main(serviceDataProcessor: IServiceDataProcessor = Provide[Container.serviceDataProcessor]) -> None:
    App(serviceDataProcessor).start()


if __name__ == "__main__":
    container = Container()
    container.config.database.from_env("POSTGRES_DB", required=True)
    container.config.user.from_env("POSTGRES_USER", required=True)
    container.config.password.from_env("POSTGRES_PASSWORD", required=True)
    container.config.host.from_env("POSTGRES_HOST", required=True)
    container.config.port.from_env("POSTGRES_PORT", required=True)
    container.wire(modules=[__name__])

    main()
