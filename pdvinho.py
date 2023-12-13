import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
import asyncio
import os
import random

server_id = discord.Object(id=1174700277375438889)

intents = discord.Intents.all()
intents.members = True


class MeuClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents, application_id=1183904537375948971)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync(guild=server_id)

async def call_api_with_retry(func, *args, max_retries=3, **kwargs):
    delay = 1
    for i in range(max_retries):
        try:
            return await func(*args, **kwargs)
        except discord.errors.HTTPException as e:
            if e.status == 429:
                retry_after = int(e.headers.get('Retry-After', 1))
                adjusted_delay = retry_after + delay + random.uniform(0, 1)  # Adding jitter
                print(f"Rate limited. Retrying in {adjusted_delay} seconds.")
                await asyncio.sleep(adjusted_delay)
                delay *= 2
            else:
                raise

client = MeuClient(intents=discord.Intents.all())

# Cooldown decorator example
@commands.cooldown(1, 30, commands.BucketType.user)
@client.tree.command()
@app_commands.default_permissions(manage_messages=True)
async def limparchat(interaction: discord.Interaction, quantidade: int):
    await interaction.channel.purge(limit=quantidade)

# bot startup
@client.event
async def on_ready():
    print("O bot está funcionando 🚀")

async def minha_funcao_que_chama_api():
    await call_api_with_retry(client.tree.sync, guild=server_id)

@client.event
async def on_member_join(member):
    boasvindas = client.get_channel(1176508459676610571)
    regras = client.get_channel(1184283980997070918)

    mensagem = await boasvindas.send(f"Seja muito bem vindo ao servidor oficial do Projeto Desenvolve {member.mention}! Não esqueça de ler as regras em {regras.mention}")


@client.tree.command()
@app_commands.default_permissions(kick_members=True)
async def expulsar(interaction: discord.Interaction, usuario: discord.Member, motivo: str = "O usuário foi expulso por fazer spam."):
    try:
        await usuario.kick(reason=motivo)
    except:
        await interaction.response.send_message(f"O usuário {usuario} não pode ser expulso, pois não tenho permissões.")
    else:
        await interaction.response.send_message("O usuário foi expulso com sucesso.")


@client.tree.command()
@app_commands.default_permissions(ban_members=True)
async def banir(interaction: discord.Interaction, usuario: discord.Member, motivo: str = "O usuário foi banido por fazer spam."):
    try:
        await usuario.ban(delete_message_days=7, reason=motivo)
    except:
        await interaction.response.send_message(f"O usuário {usuario} não pode ser banido, pois não tenho permissões.")
    else:
        await interaction.response.send_message("O usuário foi banido com sucesso.")


@client.tree.command()
@app_commands.default_permissions(ban_members=True)
async def desbanir(interaction: discord.Interaction, usuario: discord.Member, motivo: str = "O usuário foi banido por fazer spam."):
    try:
        await usuario.unban(reason=motivo)
    except:
        await interaction.response.send_message(f"O usuário {usuario} não pode ser desbanido, pois não tenho permissões.")
    else:
        await interaction.response.send_message("O usuário foi desbanido com sucesso.")


@client.tree.command()
@app_commands.default_permissions(manage_guild=True)
async def embed_regras(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Fique atento às regras do servidor!",
        description="É um imenso prazer ter você aqui! Para nos mantermos fortes, unidos e organizados, é preciso que algumas regras e recomendações de comportamento sejam definidas (além do bom senso)",
        colour=14707394
    )

    embed.set_author(
        name="Projeto Desenvolve", icon_url="https://i.imgur.com/vxnDMZs.png")

    embed.set_footer(
        text="As regras estão sujeitas à alteração da moderação")

    embed.set_image(url="https://imgur.com/unTJHAW.png")

    embed.add_field(
        name="**Aqui está o que amamos ver (e queremos mais!):**", value="", inline=False)

    embed.add_field(
        name="", value="✅ Seja cordial, encorajador e apoie seus colegas. Isso faz toda a diferença! \n", inline=False)

    embed.add_field(
        name="", value="✅ Mensagens claras e objetivas ajudam a manter o nosso espaço organizado e compreensível. \n", inline=False)

    embed.add_field(
        name="", value="✅ Compartilhe materiais e insights que agregam ao aprendizado coletivo. \n", inline=False)

    embed.add_field(
        name="", value="✅ Interaja com educadores e colegas de forma construtiva. \n", inline=False)

    embed.add_field(
        name="", value="✅ Participe, contribua e colabore. Este é o seu espaço de crescimento! \n", inline=False)

    embed.add_field(
        name="", value="✅ Aproveite para expandir seus conhecimentos e estabelecer novas amizades. \n", inline=False)

    embed.add_field(
        name="**Aqui estão as práticas que precisamos evitar:** \n", value="", inline=False)
        
    embed.add_field( 
        name="", value="❌ Não é permitido nenhum tipo de discriminação e preconceito. \n", inline=False)

    embed.add_field( 
        name="", value="❌ Comunicação ofensiva não tem lugar entre nós. \n", inline=False)

    embed.add_field( 
        name="", value="❌ Spam e Flood (enviar propagandas e/ou mandar muitas mensagens de uma vez) \n", inline=False)

    embed.add_field( 
        name="", value="❌ Divulgação de Informações Pessoais: A segurança online é crucial, então nada de compartilhar dados sensíveis. \n", inline=False)

    embed.add_field( 
        name="", value="❌ Publicidade Não Autorizada: Mantenha o foco no propósito do nosso servidor - aprendizado e desenvolvimento. \n", inline=False)
        
    embed.add_field( 
        name="", value="❌ Desrespeito às Regras do Discord: Estamos aqui para usar essa ferramenta incrível com responsabilidade. \n", inline=False)

    await interaction.response.send_message(embed=embed)


@client.tree.command()
@app_commands.default_permissions(manage_messages=True)
async def limparchat(interaction: discord.Interaction, quantidade: int):
    await interaction.channel.purge(limit=quantidade)


@client.tree.command()
@app_commands.default_permissions(manage_messages=True)
async def pomo_message(interaction: discord.Interaction):
    await interaction.response.send_message("Olá! Neste canal você poderá acompanhar o seu tempo de estudo e de descanso.\nNão se preocupe, você será avisado(a) quando um desses tempos terminar 😄 ")


load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
client.run(TOKEN)
