from abc import ABC, abstractmethod
import csv
from typing import List, Tuple, TypedDict

import psycopg2


class ParamsConnection(TypedDict):
    database: str
    user: str
    password: str
    host: str
    port: str


class IPostgreSQLConnection(ABC):
    params: ParamsConnection

    # def load_env(self) -> None:
    #     pass

    @abstractmethod
    def connect(self) -> psycopg2.extensions.connection:
        pass


class IServiceDataProcessor:
    connection: IPostgreSQLConnection

    @abstractmethod
    def fetchData(self, query: str) -> Tuple[List[Tuple], List[str]]:
        pass

    @abstractmethod
    def exportToCSV(
        self,
        baseDirectory: str,
        colNames: List[str],
        record: List[Tuple],
        indexImage: int,
        indexName: int,
    ) -> None:
        pass

    @abstractmethod
    def exportToCSV2(self, row: Tuple, pathImages: str, writer: csv.writer, indexImage: int, indexName: int) -> None:
        pass

    @abstractmethod
    def saveImage(self, base64_image: bytes, path: str, name: str) -> str:
        pass
