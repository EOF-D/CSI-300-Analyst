# type: ignore
from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd

from ..base import BaseQuery

__all__ = ("CategoryRentalCountsQuery",)


class CategoryRentalCountsQuery(BaseQuery):
    """Query to analyze rental counts for all categories."""

    QUERY = """
    SELECT
      c.name AS category_name,
      COUNT(r.rental_id) AS rental_count
    FROM
      rental r
      JOIN inventory i ON r.inventory_id = i.inventory_id
      JOIN film_category fc ON i.film_id = fc.film_id
      JOIN category c ON fc.category_id = c.category_id
    GROUP BY
      category_name
    ORDER BY
      rental_count DESC
    """

    def plot(self, data: pd.DataFrame) -> None:
        """Plot the rental counts for each film category.

        :param data: The data to plot.
        :type data: :class:`pd.DataFrame`
        """
        ax = data.plot(
            kind="barh",
            x="category_name",
            y="rental_count",
            legend=False,
            color="steelblue",
            edgecolor="black",
        )

        ax.set_title(
            "Total Rentals per Category",
            fontsize=12,
            fontweight="bold",
        )

        ax.set_xlabel("Number of Rentals", fontsize=12)
        ax.set_ylabel("Category", fontsize=12)

        # Add data labels.
        for idx, value in enumerate(data["rental_count"]):
            ax.text(
                value + 10,
                idx,
                value,
                va="center",
                fontsize=10,
            )

        # Remove top and right spines.
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        plt.savefig("plots/two/category_rental_counts.png", dpi=200)
