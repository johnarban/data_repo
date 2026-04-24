#!/usr/bin/env python
import argparse
import os
import shlex
import shutil
import sys


def command_string(command):
    if isinstance(command, str):
        return command

    return " ".join(shlex.quote(part) for part in command)


def run(command):
    command = command_string(command)
    print()
    print("> " + command)
    status = os.system(command)
    if status != 0:
        sys.exit(status)


def get_output(command):
    command = command_string(command)
    print()
    print("> " + command)
    output = os.popen(command).read()
    print(output, end="")
    return output




image_name = "weic2403c.tif"
image_base = os.path.splitext(image_name)[0]
wcs_path = image_base + ".wcs"
outdir = "weic2403c_test"
layer_name = "JWST_IMAGE"
url = "http://www.worldwidetelescope.org/wwtweb/ShowImage.aspx?ra=24.1734885223478&dec=15.782739448056697&x=639.6762771876581&y=365.8067779463834&scale=0.1714914904015271&rotation=69.92000000000002&name=M+74&imageurl=http%3A%2F%2Fesawebb.org%2Fmedia%2Farchives%2Fimages%2Fscreen%2Fpotm2208a.jpg&thumb=http%3A%2F%2Fesawebb.org%2Fmedia%2Farchives%2Fimages%2Fthumbs%2Fpotm2208a.jpg&credits=&creditsUrl=http%3A%2F%2Fesawebb.org%2Fimages%2Fpotm2208a%2F"

if os.path.isdir(outdir) :
    print(f"Removing existing output directory: {outdir}")
    shutil.rmtree(outdir)

run(["python", "wwt_url_to_fits_header.py", url, image_name])

tile_output = get_output(
    [
        "toasty",
        "tile-study",
        "--outdir",
        outdir,
        "--name",
        layer_name,
        "--fits-wcs",
        wcs_path,
        image_name,
    ]
)

lines = tile_output.strip().splitlines()
if not lines:
    raise RuntimeError("Could not find the suggested toasty cascade command in tile-study output.")

cascade_command = lines[-1].strip()
run(cascade_command)

