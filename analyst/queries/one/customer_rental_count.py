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
        CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
        COUNT(r.rental_id) as rental_count
    FROM
        customer c JOIN rental r ON c.customer_id = r.customer_id
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
        # Take the top 10 customers by rental count.
        customers = data.head(10)

        ax = customers.plot(
            kind="bar",
            x="customer_name",
            y="rental_count",
            width=0.8,
            color="steelblue",
            edgecolor="black",
            legend=False,
        )

        ax.set_title(
            "Top 10 Customers by Rental Count",
            fontsize=12,
            fontweight="bold",
        )

        ax.set_xlabel("Name", fontsize=12)
        ax.set_ylabel("Rentals", fontsize=12)
        plt.savefig("plots/one/rentals_count.png", bbox_inches="tight")
