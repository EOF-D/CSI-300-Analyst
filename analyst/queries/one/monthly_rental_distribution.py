# type: ignore
from __future__ import annotations

from calendar import month_abbr

import matplotlib.pyplot as plt
import pandas as pd

from ..base import BaseQuery

__all__ = ("MonthlyRentalDistributionQuery",)


class MonthlyRentalDistributionQuery(BaseQuery):
    """Query to analyze the distribution of rental counts by month."""

    QUERY = """
    SELECT
      MONTH(rental_date) AS month,
      YEAR(rental_date) AS year,
      COUNT(rental_id) AS rental_count
    FROM
      rental
    GROUP BY
      month,
      year
    ORDER BY
      year,
      month
    """

    def plot(self, data: pd.DataFrame) -> None:
        """Plot the distribution of rental counts by month.

        :param data: The data to plot.
        :type data: :class:`pd.DataFrame`
        """

        # Add month names for better readability.
        data["month_name"] = data["month"].apply(lambda m: month_abbr[m])
        data["period"] = data.apply(
            lambda row: f"{row['month_name']} {row['year']}", axis=1
        )

        ax = data.plot(
            kind="bar",
            x="period",
            y="rental_count",
            width=0.8,
            legend=False,
            color="steelblue",
            edgecolor="black",
        )

        # Add the data labels to the bars.
        for idx, value in enumerate(data["rental_count"]):
            ax.text(
                idx,
                value + 10,
                str(value),
                ha="center",
                va="bottom",
                fontsize=10,
            )

        ax.set_title("Monthly Rental Distribution", fontsize=12, fontweight="bold")

        ax.set_xlabel("Month", fontsize=12)
        ax.set_ylabel("Number of Rentals", fontsize=12)

        # Rotate x-axis labels.
        plt.xticks(rotation=45, ha="right")
        plt.savefig(
            "plots/one/monthly_rental_distribution.png",
            bbox_inches="tight",
        )
