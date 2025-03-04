# type: ignore
from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd

from ..base import BaseQuery

__all__ = ("CategoryAvgRentalRatesQuery",)


class CategoryAvgRentalRatesQuery(BaseQuery):
    """Query to analyze average rental rates for all categories."""

    QUERY = """
    SELECT
      c.name AS category_name,
      AVG(f.rental_rate) AS avg_rental_rate,
      COUNT(f.film_id) AS film_count
    FROM
      category c
      JOIN film_category fc ON c.category_id = fc.category_id
      JOIN film f ON fc.film_id = f.film_id
    GROUP BY
      c.name
    ORDER BY
      avg_rental_rate DESC
    """

    def plot(self, data: pd.DataFrame) -> None:
        """Plot the average rental rates for each film category.

        :param data: The data to plot.
        :type data: :class:`pd.DataFrame`
        """
        # Cast to numeric type.
        data["avg_rental_rate"] = pd.to_numeric(data["avg_rental_rate"])

        ax = data.plot(
            kind="barh",
            x="category_name",
            y="avg_rental_rate",
            legend=False,
            color="steelblue",
            edgecolor="black",
        )

        ax.set_title(
            "Average Rental Rate per Category",
            fontsize=12,
            fontweight="bold",
        )

        ax.set_xlabel("Average Rental Rate", fontsize=12)
        ax.set_ylabel("Category", fontsize=12)

        # Add data labels.
        for idx, value in enumerate(data["avg_rental_rate"]):
            ax.text(
                value + 0.1,
                idx,
                f"${value:.2f}",
                va="center",
                fontsize=10,
            )

        # Remove top and right spines.
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        plt.tight_layout()
        plt.savefig("plots/two/category_avg_rental_rates.png", dpi=200)
