# create mp4

```bash
ffmpeg -f concat -safe 0 -r 25 -i frames.txt -vf "drawtext=text='frame %{n}':x=30:y=30:fontsize=36:fontcolor=red:box=1:boxcolor=white@0.75:boxborderw=8" -c:v libx264 -crf 22 -pix_fmt yuv420p video.mp4
```

# create webm w/ transparency
```bash
ffmpeg -f concat -safe 0 -r 25 -i frames.txt -c:v libvpx-vp9 -pix_fmt yuva420p -b:v 0 -crf 30 -row-mt 1 -threads 8 video.webm
```


# processing original frames
```
magick mogrify -gravity center -crop 1024x1024+0+0 +repage -flop -path ./frames_small -colors 256 source/frame_*.png
```


# optimized processer
```
find ./source/ -name 'frame_*.png' -print0 | xargs -0 -n 1 -P 8 magick mogrify -monitor -gravity center -crop 1024x1024+0+0 +repage -colors 256 -flop -path ./frames_256
```