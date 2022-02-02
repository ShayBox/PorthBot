import os
import subprocess

import hikari

bot = hikari.GatewayBot(os.environ["DISCORD_TOKEN"])


@bot.listen()
async def message_create(event: hikari.MessageCreateEvent) -> None:
    if event.is_bot:
        return

    content = event.message.content
    if content is None or "```porth" not in content:
        return

    # Extract the code from the message content and codeblock
    blocks = content.split("```")
    block = filter(lambda b: b.startswith("porth\n"), blocks)
    block = map(lambda b: b.replace("porth\n", ""), block)
    code = "\n".join(block)

    # Run the code and get the output
    result = subprocess.run(["docker", "run", "-t", "porth", code], capture_output=True)

    # Send the output to the channel
    await event.message.respond(
        embed=hikari.Embed(
            color="fbe9d8",
            title="Standard Output",
            description=f"```{result.stdout.decode('utf-8')}```",
            timestamp=event.message.timestamp,
        )
    )


def main() -> None:
    bot.run(
        activity=hikari.Activity(
            name="for codeblocks", type=hikari.ActivityType.WATCHING
        ),
        asyncio_debug=True,
        coroutine_tracking_depth=20,
        propagate_interrupts=True,
    )
