from __future__ import annotations

import argparse
import json
from pathlib import Path

from p1_c_adult_walk_density_experiment_v1 import write_results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    out = Path(args.output_dir)
    result = write_results(out)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
