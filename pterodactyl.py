import discord, asyncio
from discord.ext import commands
from pydactyl import PterodactylClient

api = PterodactylClient('Your panel domain or ip', 'your user API ')
bot = commands.Bot(command_prefix="!", case_insensitive=True)
actions = ['start', 'stop', 'restart', 'kill']

@bot.command()
@commands.is_owner() 
async def panel(ctx):
  serverid = "Your Server ID"
  embed = discord.Embed(title="Server Status",description=f"{api.client.servers.get_server_utilization(serverid)['current_state']}",color=0x00ff00)
  await ctx.send(embed=embed)
  embed1 = discord.Embed(title="What Power Action Do You Want To Send?",description="*start , stop , restart , kill*\n\n`cancel` To Cancel The Power-Action",color=0x00ff00)
  await ctx.send(embed=embed1)
  

  def check(m):
          return m.channel == ctx.channel and m.author == ctx.author
  try:
    action = await bot.wait_for('message', check=check, timeout=30)
  except asyncio.TimeoutError:
    await ctx.reply(embed=discord.Embed(title='You didn\'t respond in time.'))
    return
  command = action.content.lower()
  if command not in actions:
    await ctx.reply(embed=discord.Embed(title='Choose a valid option.', description='Please choose one of the following.\n'+', '.join(actions)))
    

  api.client.servers.send_power_action(serverid, command)
  responseEmbed = discord.Embed(title=f'{command.capitalize()}ed by {ctx.author.name}#{ctx.author.discriminator}.', description=f"Power-Action `{command}` completed.", color=0x842899)
  await ctx.send(embed=responseEmbed)

  print(f'{ctx.author.name} Used The Command panelweb')


  @panel.error
  async def panel_error(ctx, error):
    if isinstance(error, commands.NotOwner):
      embed = discord.Embed(title='⚠️ Restricted',description='Only Bot Owner Can Execute This Command')
      await ctx.send(embed=embed)
    



bot.run('bot Token')
