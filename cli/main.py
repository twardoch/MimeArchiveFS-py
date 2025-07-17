#!/usr/bin/env python3
"""
Command line interface for my_package.
this_file: cli/main.py
"""
import argparse
import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from my_package.main import add, hello


def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="My Package CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s hello World
  %(prog)s add 5 3
        """,
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 1.0.0",
        help="Show version and exit",
    )
    
    subparsers = parser.add_subparsers(
        dest="command",
        help="Available commands",
        metavar="COMMAND",
    )
    
    # Hello command
    hello_parser = subparsers.add_parser(
        "hello",
        help="Say hello to someone",
        description="Greet someone with a friendly hello message",
    )
    hello_parser.add_argument(
        "name",
        help="Name to greet",
    )
    
    # Add command
    add_parser = subparsers.add_parser(
        "add",
        help="Add two numbers",
        description="Add two integers and display the result",
    )
    add_parser.add_argument(
        "a",
        type=int,
        help="First number",
    )
    add_parser.add_argument(
        "b",
        type=int,
        help="Second number",
    )
    
    args = parser.parse_args()
    
    if args.command == "hello":
        result = hello(args.name)
        print(result)
    elif args.command == "add":
        try:
            result = add(args.a, args.b)
            print(f"{args.a} + {args.b} = {result}")
        except TypeError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()