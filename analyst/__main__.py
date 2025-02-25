from __future__ import annotations

from argparse import ArgumentParser

from . import __version__
from .config import load_config


def gen_parser() -> ArgumentParser:
    """Creates the argument parser.

    :return: The argument parser.
    :rtype: :class:`argparse.ArgumentParser`
    """

    parser = ArgumentParser(prog="analyst")
    parser.add_argument("--version", action="version", version=f"Analyst {__version__}")

    # Add config argument.
    parser.add_argument(
        "--config",
        type=str,
        required=True,
        default="config.toml",
        help="Path to the config file.",
    )

    parser.add_argument(
        "--query",
        type=str,
        required=True,
        help="The query to run.",
    )

    return parser


def main() -> None:
    """The main entry point for the CLI."""

    parser = gen_parser()
    args = parser.parse_args()

    # Print help if no arguments are passed.
    if not vars(args):
        parser.print_help()

    config = load_config(args.config)
    try:
        queries = __import__("analyst.queries", fromlist=(args.query,))
        if not hasattr(queries, args.query):
            raise ImportError

        query = getattr(queries, args.query)
        with query(config) as q:
            print(q.run())

    except ImportError:
        raise ValueError(f"Query '{args.query}' not found.")


if __name__ == "__main__":
    main()
