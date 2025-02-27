from __future__ import annotations

from typing import Any, ClassVar

import mysql.connector as connector
import pandas as pd  # type: ignore

from ..config import Config

__all__ = ("BaseQuery",)


class BaseQuery:
    QUERY: ClassVar[str]

    def __init__(self, config: Config) -> None:
        """Initialize the query object.

        :param config: The configuration object.
        :type config: :class:`Config`
        """
        self.config = config
        self.conn = None

    def __enter__(self) -> BaseQuery:
        if self.conn is None:
            self.conn = connector.connect(**self.config)

        return self

    def __exit__(self, *_: Any) -> None:
        if self.conn is not None:
            self.conn.close()

    def _query(self) -> pd.DataFrame:
        """Runs the query."""
        if not hasattr(self.__class__, "QUERY"):
            raise NotImplementedError("Query not implemented.")

        if self.conn is None:
            raise RuntimeError("Connection not established.")

        cursor = self.conn.cursor(dictionary=True)
        cursor.execute(self.QUERY)

        data = cursor.fetchall()
        return pd.DataFrame(data)

    def plot(self, data: pd.DataFrame) -> None:
        """Plots the data.

        :param data: The data to plot.
        :type data: :class:`pd.DataFrame

        :raises NotImplementedError: If the plot method is not implemented.
        """
        raise NotImplementedError("Plot not implemented.")

    def run(self) -> None:
        """Runs the query."""
        self.plot(self._query())
