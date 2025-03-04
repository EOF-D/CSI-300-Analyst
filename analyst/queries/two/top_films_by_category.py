# type: ignore
from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd

from ..base import BaseQuery

__all__ = ("TopFilmsByCategoryQuery",)


class TopFilmsByCategoryQuery(BaseQuery):
    """Query to analyze top 5 most rented films within a specific category."""

    CATEGORY = "Sports"
    QUERY = f"""
    SELECT
      f.title AS film_title,
      COUNT(r.rental_id) AS rental_count,
      f.rental_rate AS rental_rate,
      f.rating AS rating
    FROM
      film f
      JOIN film_category fc ON f.film_id = fc.film_id
      JOIN category c ON fc.category_id = c.category_id
      JOIN inventory i ON f.film_id = i.film_id
      JOIN rental r ON i.inventory_id = r.inventory_id
    WHERE
      c.name = '{CATEGORY}'
    GROUP BY
      f.title,
      f.rental_rate,
      f.rating
    ORDER BY
      rental_count DESC
    LIMIT
      5
    """

    def plot(self, data: pd.DataFrame) -> None:
        """Plot the top rented films within the specified category.

        :param data: The data to plot.
        :type data: :class:`pd.DataFrame`
        """
        ax = data.plot(
            kind="barh",
            x="film_title",
            y="rental_count",
            legend=False,
            color="steelblue",
            edgecolor="black",
        )

        ax.set_title(
            f"Top 5 Rented Films in {__class__.CATEGORY} Category",
            fontsize=12,
            fontweight="bold",
        )

        ax.set_xlabel("Number of Rentals", fontsize=12)
        ax.set_ylabel("Title", fontsize=12)

        # Add data labels.
        rental_count = data["rental_count"]
        rental_rate = data["rental_rate"]

        for idx, (value, rate) in enumerate(zip(rental_count, rental_rate)):
            ax.text(
                value + 0.3,
                idx,
                f"{value} (${rate:.2f})",
                va="center",
                fontsize=10,
            )

        # Remove top and right spines.
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        plt.savefig(
            "plots/two/top_films_by_category.png", bbox_inches="tight", dpi=200
        )
