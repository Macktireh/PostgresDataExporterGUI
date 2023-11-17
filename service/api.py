import base64
import csv
import os

# from pathlib import Path
from typing import List, Tuple

import psycopg2
# from dotenv import load_dotenv

from interface import IPostgreSQLConnection, IServiceDataProcessor, ParamsConnection


class PostgreSQLConnection(IPostgreSQLConnection):
    def __init__(self, params: ParamsConnection = None) -> None:
        # self.load_env()
        self.params = params

    # def load_env(self) -> None:
    #     BASE_DIR: Path = Path(__file__).resolve().parent
    #     load_dotenv(os.path.join(BASE_DIR, ".env"))

    def connect(self) -> psycopg2.extensions.connection:
        return psycopg2.connect(**self.params)


class ServiceDataProcessor(IServiceDataProcessor):
    def __init__(self, connection: PostgreSQLConnection) -> None:
        self.connection = connection

    def fetchData(self, query: str) -> Tuple[List[Tuple], List[str]]:
        with self.connection.connect() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                return cur.fetchall()[:100], [col[0] for col in cur.description]

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

        with open(f"{baseDirectory}/output.csv", "w", newline="") as f:
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

    def exportToCSV2(self, row: Tuple, pathImages: str, writer: csv.writer, indexImage: int, indexName: int) -> None:
        row = list(row)
        filename = self.saveImage(row[indexImage], pathImages, str(row[indexName]))
        row[-1] = filename
        writer.writerow(row)

    def saveImage(self, base64_image: bytes, path: str, name: str) -> str:
        filename: str = f"{path}/{name}".replace(" ", "_") + ".png"
        base64_img: bytes = base64.b64encode(base64_image)
        img_data: bytes = base64.b64decode(base64_img)
        with open(filename, "wb") as f:
            f.write(img_data)
        return f"images/{name}".replace(" ", "_") + ".png"


def main() -> None:
    postgres_connection: PostgreSQLConnection = PostgreSQLConnection()
    data_processor: ServiceDataProcessor = ServiceDataProcessor(postgres_connection)

    data, column_names = data_processor.fetch_data()
    data_processor.export_to_csv(column_names, data)


if __name__ == "__main__":
    main()
