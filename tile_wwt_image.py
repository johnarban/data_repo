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


potm2208a = {
    "image_name": "potm2208a.tif",
    "url": "http://www.worldwidetelescope.org/wwtweb/ShowImage.aspx?ra=24.1734885223478&dec=15.782739448056697&x=639.6762771876581&y=365.8067779463834&scale=0.1714914904015271&rotation=69.92000000000002&name=M+74&imageurl=http%3A%2F%2Fesawebb.org%2Fmedia%2Farchives%2Fimages%2Fscreen%2Fpotm2208a.jpg&thumb=http%3A%2F%2Fesawebb.org%2Fmedia%2Farchives%2Fimages%2Fthumbs%2Fpotm2208a.jpg&credits=&creditsUrl=http%3A%2F%2Fesawebb.org%2Fimages%2Fpotm2208a%2F",
    "name": "Mid-Infrared (JWST)",
    "avm-source": "potm2208a.jpg",
}

weic2403c = {
    "image_name": "weic2403c.tif",
    "url": "http://www.worldwidetelescope.org/wwtweb/ShowImage.aspx?ra=24.17437150224632&dec=15.780613507831623&x=640.0&y=400.7170294494238&scale=0.1539673612143702&rotation=250.5199999999998&name=NGC+628&imageurl=http%3A%2F%2Fesawebb.org%2Fmedia%2Farchives%2Fimages%2Fscreen%2Fweic2403c.jpg&thumb=http%3A%2F%2Fesawebb.org%2Fmedia%2Farchives%2Fimages%2Fthumbs%2Fweic2403c.jpg&credits=&creditsUrl=http%3A%2F%2Fesawebb.org%2Fimages%2Fweic2403c%2F",
    "name": "Infrared (JWST)",
    "avm-source": "weic2403c.jpg",
}

noao_m74mortfieldw = {
    "image_name": "noao-m74mortfieldw.tif",
    "url": "http://www.worldwidetelescope.org/wwtweb/ShowImage.aspx?ra=24.1712825361&dec=15.7868634046&x=625.3509928384001&y=458.01199544248897&scale=0.5356910135480624&rotation=186.8582146259037&name=M74&imageurl=http%3A%2F%2Fnoirlab.edu%2Fpublic%2Fmedia%2Farchives%2Fimages%2Fscreen%2Fnoao-m74mortfieldw.jpg&thumb=http%3A%2F%2Fnoirlab.edu%2Fpublic%2Fmedia%2Farchives%2Fimages%2Fthumbs%2Fnoao-m74mortfieldw.jpg&credits=&creditsUrl=http%3A%2F%2Fnoirlab.edu%2Fpublic%2Fimages%2Fnoao-m74mortfieldw%2F",
    "name": "Optical (NOAO)",
    "outdir": "noao_ngc628",
    "avm-source": "noao-m74mortfieldw.jpg",
}

hubble_has_avm = {
    "image_name": "./ngc 628 Hubble Full Res (For Display).png",
    "url": None,
    "name": "Optical (Hubble)",
   "outdir": "hubble_ngc628"
}


image_def = potm2208a

for image_def in [potm2208a, weic2403c, noao_m74mortfieldw, hubble_has_avm]:

    image_name = image_def["image_name"]
    image_base = os.path.splitext(image_name)[0]
    wcs_path = image_base + ".wcs"
    outdir = image_def.get("outdir", image_base)
    layer_name = image_def["name"]
    url = image_def["url"]


    if url is not None:
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
    elif "avm-source" in image_def:
        # toasty tile-study --outdir noao_ngc628 --name "Optical (NOAO)" --avm noao-m74mortfieldw.jpg
        tile_output = get_output(
            [
                "toasty",
                "tile-study",
                "--from-avm",
                image_def["avm-source"],
                "--outdir",
                outdir,
                "--name",
                layer_name,
                image_name,
            ]
        )
    else:
        # toasty tile-study --outdir hubble_ngc628 --name "Optical (Hubble)" --avm ngc\ 628\ Hubble\ Full\ Res\ \(For\ Display\).png
        tile_output = get_output(
            [
                "toasty",
                "tile-study",
                "--outdir",
                outdir,
                "--name",
                layer_name,
                "--avm",
                image_name,
            ]
        )

    lines = tile_output.strip().splitlines()
    if not lines:
        raise RuntimeError("Could not find the suggested toasty cascade command in tile-study output.")

    cascade_command = lines[-1].strip()
    run(cascade_command)

    # Add the wwtdatatool command at the end, using the output folder name
    run([
        "wwtdatatool",
        "wtml",
        "rewrite-urls",
        f"{outdir}/index_rel.wtml",
        f"https://raw.githubusercontent.com/johnarban/data_repo/main/{outdir}/",
        f"{outdir}/index.wtml",
    ])
