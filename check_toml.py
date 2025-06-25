import tomllib
import sys

try:
    with open("pyproject.toml", "rb") as f:
        data = tomllib.load(f)
    print("pyproject.toml parsed successfully by tomllib!")
    # You could print parts of data here if needed for further verification
    # print(data.get("tool", {}).get("hatch", {}).get("envs", {}).get("lint"))
except tomllib.TOMLDecodeError as e:
    print(f"TOMLDecodeError: {e}", file=sys.stderr)
    sys.exit(1)
except Exception as e:
    print(f"An unexpected error occurred: {e}", file=sys.stderr)
    sys.exit(1)
