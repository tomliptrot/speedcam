# an API to access the video stream?
# see here https://stribny.name/blog/fastapi-video/
# and here https://stackoverflow.com/questions/65971081/stream-video-to-web-browser-with-fastapi
# and here https://fastapi.tiangolo.com/advanced/custom-response/#streamingresponse
# and here https://github.com/mpimentel04/rtsp_fastapi

import typer


cli = typer.Typer()

@cli.command()
def start():
    """
    Start the server
    """
    typer.echo("Starting server")
    #uvicorn.run(app, host="0.0.0.0", port=HTTP_PORT, access_log=False)


@cli.command()
def stop():
    """
    Start the server
    """
    typer.echo("Stopping server")