# type: ignore
from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd

from ..base import BaseQuery

__all__ = ("AverageRentalDurationsQuery",)


class AverageRentalDurationsQuery(BaseQuery):
    """Query to analyze the average rental durations."""

    QUERY = """
    SELECT
      CONCAT(c.first_name, ' ', c.last_name) AS customer_name,

      AVG(
        TIMESTAMPDIFF(
          HOUR, r.rental_date, r.return_date
        )
      )
      AS avg_rental_hours,

      COUNT(r.rental_id) AS rental_count,
      COUNT(r.return_date) AS returned_rentals
    FROM
      customer c
      JOIN rental r ON c.customer_id = r.customer_id
    WHERE
      r.return_date IS NOT NULL
    GROUP BY
      customer_name
    HAVING
      returned_rentals >= 1
    ORDER BY
      avg_rental_hours DESC
    """

    def plot(self, data: pd.DataFrame) -> None:
        """Plot the average rental durations as a scatter plot.

        :param data: The data to plot.
        :type data: :class:`pd.DataFrame`
        """

        # Convert average rental hours to days for better readability.
        data["avg_rental_days"] = data["avg_rental_hours"] / 24

        ax = data.plot(
            kind="scatter",
            x="returned_rentals",
            y="avg_rental_days",
            c="avg_rental_days",
            s=data["rental_count"] * 2,
            edgecolor="black",
            colormap="viridis",
            colorbar=True,
        )

        ax.set_title(
            "Average Rental Durations",
            fontsize=12,
            fontweight="bold",
        )

        ax.set_xlabel("Returned Rentals", fontsize=12)
        ax.set_ylabel("Average Rental Days", fontsize=12)

        plt.savefig("plots/one/average_rental_duration.png", dpi=200)
