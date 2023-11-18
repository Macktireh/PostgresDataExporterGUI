import base64
import csv
import os
from typing import List, Tuple, TypedDict
from uuid import uuid4

import psycopg2

from service.exception import (
    DBConnectionException,
    DBQueryException,
    SaveImageException,
)


class ParamsConnection(TypedDict):
    database: str
    user: str
    password: str
    host: str
    port: str


class PostgreSQLConnection:
    def __init__(self, params: ParamsConnection = None) -> None:
        self.params = params

    def connect(self) -> psycopg2.extensions.connection:
        try:
            return psycopg2.connect(**self.params)
        except psycopg2.OperationalError as e:
            raise DBConnectionException(e)


class ServiceDataProcessor:
    def __init__(self, connection: PostgreSQLConnection) -> None:
        self.connection = connection

    def fetchData(self, query: str) -> Tuple[List[Tuple], List[str]]:
        try:
            with self.connection.connect() as conn:
                with conn.cursor() as cur:
                    cur.execute(query)
                    return cur.fetchall(), [col[0] for col in cur.description]
        except psycopg2.OperationalError as e:
            raise DBConnectionException(e)

        except Exception as e:
            raise DBQueryException(e)

    def exportToCSV(
        self,
        baseDirectory: str,
        colNames: List[str],
        record: List[Tuple],
        indexImage: int,
        indexName: int,
    ) -> None:
        pathImages = baseDirectory + "/images"
        if not os.path.exists(pathImages):
            os.makedirs(pathImages)

        with open(f"{baseDirectory}/data.csv", "w", newline="") as f:
            writer = csv.writer(f)
            colNames[-1] = "image"
            writer.writerow(colNames)
            for row in record:
                row = list(row)
                filename = self.saveImage(
                    row[indexImage], pathImages, str(row[indexName])
                )
                row[-1] = filename
                writer.writerow(row)

    def exportToCSV2(
        self,
        row: Tuple,
        writer: csv.writer,
        hasImage: bool = False,
        pathImages: str = None,
        indexImage: int = None,
    ) -> None:
        row = list(row)
        if hasImage:
            try:
                filename = self.saveImage(row[indexImage], pathImages)
            except Exception:
                raise SaveImageException(
                    "Quelque chose c'est mal passé lors de l'enregistrement de l'image. Veuillez bien l'index de la colonne image est correcte." # noqa
                )
            row[-1] = filename
        writer.writerow(row)

    def saveImage(self, base64_image: bytes, path: str) -> str | None:
        name = str(uuid4())
        filename: str = f"{path}/{name}.png"
        if not base64_image:
            return None
        base64_img: bytes = base64.b64encode(base64_image)
        img_data: bytes = base64.b64decode(base64_img)
        with open(filename, "wb") as f:
            f.write(img_data)
        return f"images/{name}".replace(" ", "_") + ".png"
