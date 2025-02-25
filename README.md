<div align="center">
    <h1>CSI-300 Project 2</h1>
</div>

## Installing

To setup your environment for running, please follow this step by step.

```bash
python -m pip install poetry            # If you don't have poetry.
python -m poetry install                # Installs the dependencies of the project.
```

## Running

To run the tool use poetry:

```
poetry run python -m analyst --config <config_path> --query=<QueryClass>
```

## Creating new queries

### Setup namespace.

```py
# queries/__init__.py
# add this
from .actor_name_length import *
```

Example class.

```py
# queries/actor_name_length.py
from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd  # type: ignore

from .base import BaseQuery
from ..config import Config

__all__ = ("ActorNameLength",)


class ActorNameLength(BaseQuery):
    # MUST PUT.
    QUERY = """
    SELECT CHAR_LENGTH(first_name) as Characters FROM actor;
    """

    # MUST PUT.
    def __init__(self, config: Config) -> None:
        super().__init__(config)

    def _plot(self, data: pd.DataFrame) -> None:
        # Customize your plot.
        data.plot(kind="hist", title="Actor Name Length", bins=20)
        plt.savefig("actor_name_length.png")
```
