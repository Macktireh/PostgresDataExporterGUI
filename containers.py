from dependency_injector import containers, providers

from service.api import ServiceDataProcessor, ParamsConnection, PostgreSQLConnection


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    params = providers.Singleton(
        ParamsConnection,
        database=config.database,
        user=config.user,
        password=config.password,
        host=config.host,
        port=config.port,
    )

    connection = providers.Singleton(
        PostgreSQLConnection,
        params=params,
    )

    serviceDataProcessor = providers.Factory(
        ServiceDataProcessor,
        connection=connection,
    )
