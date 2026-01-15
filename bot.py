import os
import discord
from discord.ext import commands, tasks

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

GUILD_ID = 1461395635763806250  # COLOQUE O ID DO SEU SERVIDOR
PROTECTED_CHANNELS = ["regras", "anuncios"]

@bot.event
async def on_ready():
    print(f"Bot online como {bot.user}")
    if not nuke_loop.is_running():
        nuke_loop.start()

@tasks.loop(hours=3)
async def nuke_loop():
    guild = bot.get_guild(GUILD_ID)
    if not guild:
        print("Servidor não encontrado.")
        return

    print("Executando nuke automático...")

    for channel in guild.text_channels:
        if channel.name.lower() not in PROTECTED_CHANNELS:
            try:
                await channel.delete()
            except Exception as e:
                print(f"Erro ao deletar {channel.name}: {e}")

    await guild.create_text_channel("geral")
    await guild.create_text_channel("chat")

    print("Nuke automático finalizado.")

@bot.command()
@commands.has_permissions(administrator=True)
async def nuke(ctx):
    await ctx.send("💣 Executando nuke manual...")

    for channel in ctx.guild.text_channels:
        if channel.name.lower() not in PROTECTED_CHANNELS:
            try:
                await channel.delete()
            except Exception as e:
                print(f"Erro ao deletar {channel.name}: {e}")

    await ctx.guild.create_text_channel("geral")
    await ctx.guild.create_text_channel("chat")

    await ctx.send("✅ Nuke concluído.")

bot.run(os.getenv("DISCORD_TOKEN"))
