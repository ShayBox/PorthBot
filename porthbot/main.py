import os
import subprocess

import hikari

if os.name != "nt":
    import uvloop

    uvloop.install()

bot = hikari.GatewayBot(os.environ["DISCORD_TOKEN"])
messages: dict[int, hikari.Message] = {}


async def process_message(message: hikari.Message, update: bool) -> None:
    content = message.content
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
    embed = hikari.Embed(
        color="fbe9d8",
        title="Standard Output",
        description=f"```{result.stdout.decode('utf-8')}```",
        timestamp=message.timestamp,
    )
    if update:
        response = messages[message.id]
        response = await response.edit(embed=embed)
    else:
        response = await message.respond(embed=embed)

    # Keep track of messages and responses for edits
    messages[message.id] = response


@bot.listen()
async def message_create(event: hikari.MessageCreateEvent) -> None:
    if event.is_human:
        await process_message(event.message, update=False)


@bot.listen()
async def message_create(event: hikari.MessageUpdateEvent) -> None:
    if event.is_human:
        await process_message(event.message, update=True)


def main() -> None:
    bot.run(
        activity=hikari.Activity(
            name="for codeblocks", type=hikari.ActivityType.WATCHING
        ),
        asyncio_debug=True,
        coroutine_tracking_depth=20,
        propagate_interrupts=True,
    )
