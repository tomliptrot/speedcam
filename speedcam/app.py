# an API to access the video stream?
# see here https://stribny.name/blog/fastapi-video/
# and here https://stackoverflow.com/questions/65971081/stream-video-to-web-browser-with-fastapi
# and here https://fastapi.tiangolo.com/advanced/custom-response/#streamingresponse
# and here https://github.com/mpimentel04/rtsp_fastapi

from pathlib import Path
from typing import Optional

import typer

from speedcam.video import Video, calibrate_distance, detect_movement

cli = typer.Typer()


@cli.command()
def scan(file: Path):
    typer.echo(f"Scanning {file}")
    vid = Video.load(file)
    movement, video_with_rect, grays, threshs = detect_movement(vid)
    print(movement.x.diff())
    print((movement.x + movement.w).diff())
    video_with_rect.save("test.mp4")


@cli.command()
def calib(file: Path):
    typer.echo("calibrating")
    vid = Video.load(file)
    calibrate_distance(vid)
