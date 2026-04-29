# ls frames/frame_*.png | sort -V | awk '{print "file \047" $0 "\047"}' > frames.txt
import os
import glob
from pathlib import Path

frames_dir = Path("frames")
frame_files = sorted(frames_dir.glob("frame_*.png"), key=lambda x: int(x.stem.split("_")[1]))
with open("frames.txt", "w") as f:
    for frame_file in frame_files[::5]:
        f.write(f"file '{frame_file}'\n")