"""make.fun entry: copy the pre-built news image to the output directory.

The judging sandbox provides only the Python standard library, so this
program does exactly one thing: copy entry.png (which lives next to this
file) into the output directory as entry.png.
"""

import os
import shutil

OUTPUT_NAME = "entry.png"


def main() -> None:
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, OUTPUT_NAME)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, OUTPUT_NAME)
    shutil.copyfile(src, dst)


if __name__ == "__main__":
    main()
