import subprocess

import hikari
import tanjun

component = tanjun.Component()


@component.with_slash_command
@tanjun.as_slash_command("build", "Build a new docker image")
async def nsfw_command(ctx: tanjun.abc.Context) -> None:
    await ctx.respond("Building a new image... This may take some time.")
    subprocess.run(["docker", "build", "--pull", "--no-cache", "-t", "porth", "."])
    await ctx.respond("Done! Check your console for any errors.")


load_slash = component.make_loader()
