# type: ignore
from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd

from ..base import BaseQuery

__all__ = ("CustomerRentalCountsQuery",)


class CustomerRentalCountsQuery(BaseQuery):
    """Query to analyze the overall customer rental counts."""

    QUERY = """
    SELECT
      c.customer_id as customer_id,
      COUNT(r.rental_id) as rental_count
    FROM
      customer c
      JOIN rental r ON c.customer_id = r.customer_id
    GROUP BY
      c.customer_id
    ORDER BY
      rental_count DESC;
    """

    def plot(self, data: pd.DataFrame) -> None:
        """Plot the customer rental counts as a bar chart.

        :param data: The data to plot.
        :type data: :class:`pd.DataFrame`
        """

        ax = data.plot(
            kind="bar",
            x="customer_id",
            y="rental_count",
            width=1,
            legend=False,
            color="steelblue",
        )

        ax.set_title(
            "Total Rentals per Customer",
            fontsize=12,
            fontweight="bold",
        )

        ax.set_ylabel("Rental Count", fontsize=12)
        ax.get_xaxis().set_visible(False)

        plt.savefig("plots/one/customer_rental_count.png", dpi=200)
