import discord
from discord.ext import commands
import aiohttp
import random
import requests
import asyncio
from pydactyl import PterodactylClient
api = PterodactylClient('Your panel domain or ip', 'your user API ')

client = commands.Bot(command_prefix="!", case_insensitive=True)







@client.command()
@commands.is_owner() 
async def panel(ctx):
  serverid = "Your Server ID"
  embed = discord.Embed(title="Server Status",description=f"{api.client.servers.get_server_utilization(serverid)['current_state']}",color=0x00ff00)
  await ctx.send(embed=embed)
  embed1 = discord.Embed(title="What Power Action Do You Want To Send?",description="*start , stop , restart , kill*\n\n`cancel` To Cancel The Power-Action",color=0x00ff00)
  await ctx.send(embed=embed1)


  def check(m):
          return m.channel == ctx.channel and m.author == ctx.author

  action = await client.wait_for('message', check=check) 
  if action.content == "start":
      response = api.client.servers.send_power_action(serverid, 'start')  
      embed3 = discord.Embed(description=f"Power-Action `start` Done",color=0x842899)
      embed3.set_footer(text=f"started By {ctx.author}")
  if action.content == "stop":
      response = api.client.servers.send_power_action(serverid, 'stop')  
      embed3 = discord.Embed(description=f"Power-Action `stop` Done",color=0x842899)
      embed3.set_footer(text=f"Stopped By {ctx.author}")
  if action.content == "restart":
      response = api.client.servers.send_power_action(serverid, 'restart')  
      embed3 = discord.Embed(description=f"Power-Action `restart` Done",color=0x842899)
      embed3.set_footer(text=f"restarted By {ctx.author}")
  if action.content == "kill":
      response = api.client.servers.send_power_action(serverid, 'kill')  
      embed3 = discord.Embed(description=f"Power-Action `kill` Done",color=0x842899)
      embed3.set_footer(text=f"killed By {ctx.author}")
  if action.content == "cancel":
      embed3 = discord.Embed(description=f"Action Canceled",color=0x842899)
  await ctx.send(embed=embed3)

  print(f'{ctx.author.name} Used The Command panelweb')


  @panel.error
  async def panel_error(ctx, error):
    if isinstance(error, commands.NotOwner):
      embed = discord.Embed(title='⚠️ Restricted',description='Only Bot Owner Can Execute This Command')
      await ctx.send(embed=embed)




client.run('bot Token')
