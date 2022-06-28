import discord
from discord.ext import commands
import aiohttp
import random
import requests
import asyncio
import discord.ui
from discord.ui import Button, View
from pydactyl import PterodactylClient


api = PterodactylClient('your panel link', 'your user api credentials from panel')
pteroserverid = "Get server id from settings of the server"

def convert_from_ms( milliseconds ): 
    seconds, milliseconds = divmod(milliseconds,1000) 
    minutes, seconds = divmod(seconds, 60) 
    hours, minutes = divmod(minutes, 60) 
    days, hours = divmod(hours, 24) 
    seconds = seconds + milliseconds/1000 
    return f"{days}d, {hours}h, {minutes}m"

class ptero(commands.Cog):

  def __init__(self, client):
    self.client = client





  @commands.command()
  @commands.is_owner()
  async def panel(self,ctx):
    pteroserverstatus = api.client.servers.get_server_utilization(pteroserverid)
    resources = pteroserverstatus['resources']
    uptime = resources['uptime']
    date = convert_from_ms(uptime)
    embed = discord.Embed(title="Server Status - " + pteroserverstatus['current_state'],description = f"**Uptime** - {date}",color=0x00ff00)
    await ctx.send(embed=embed)
    view = panelbuttons(ctx)
    embed1 = discord.Embed(title="What Power Action Do You Want To Send?",color=0x00ff00)
    embed1.set_footer(text="Button Will Timeout In 1 Minute")
    await ctx.send(embed=embed1,view=view)
    print(f'{ctx.author.name} Used The Command panel')
  


  @panelweb.error
  async def panelweb_error(self,ctx, error):
    if isinstance(error, commands.NotOwner):
      embed = discord.Embed(title='⚠️ Restricted',description='Only Bot Owner Can Execute This Command')
      await ctx.send(embed=embed)
    



 



class panelbuttons(View):
  def __init__(self,ctx):
    self.ctx = ctx
    super().__init__(timeout=60)

  
  @discord.ui.button(label="Start", style = discord.ButtonStyle.green)
  async def panelstart(self,interaction,button):
    if interaction.user != self.ctx.author:
      await interaction.response.send_message('This Gui Is Only Valid For The Author',ephemeral=True)
    else:
      response = api.client.servers.send_power_action(pteroserverid, 'start')  
      embed3 = discord.Embed(title="Power-Action `start` Done For Your Server",color=0xff3336)
      embed3.set_footer(text=f"started By {interaction.user}")
      self.clear_items()
      await interaction.response.edit_message(embed=embed3, view=self)
      
    
    
  @discord.ui.button(label="Stop", style = discord.ButtonStyle.red)
  async def panelstop(self,interaction,button):
    if interaction.user != self.ctx.author:
      await interaction.response.send_message('This Gui Is Only Valid For The Author',ephemeral=True)
    else:
      response = api.client.servers.send_power_action(pteroserverid, 'stop')  
      embed3 = discord.Embed(description=f"Power-Action `stop` Done For Your Server",color=0xff3336)
      embed3.set_footer(text=f"Stopped By {interaction.user}")
      self.clear_items()
      await interaction.response.edit_message(embed=embed3,view=self)

    
  @discord.ui.button(label="Restart", style = discord.ButtonStyle.blurple)
  async def panelrestart(self,interaction,button):
    if interaction.user != self.ctx.author:
      await interaction.response.send_message('This Gui Is Only Valid For The Author',ephemeral=True)
    else:
      response = api.client.servers.send_power_action(pteroserverid, 'restart')  
      embed3 = discord.Embed(description=f"Power-Action `restart` Done For Your Server",color=0xff3336)
      embed3.set_footer(text=f"Restarted By {interaction.user}")
      self.clear_items()
      await interaction.response.edit_message(embed=embed3,view=self)
      
    
  @discord.ui.button(label="Cancel", style = discord.ButtonStyle.grey)
  async def panelcancel(self,interaction,button):
    if interaction.user != self.ctx.author:
      await interaction.response.send_message('This Gui Is Only Valid For The Author',ephemeral=True)
    else:
      embed3 = discord.Embed(description=f"Power-Action Canceled For Your Server",color=0xff3336)
      embed3.set_footer(text=f"Canceled By {interaction.user}")
      self.clear_items()
      await interaction.response.edit_message(embed=embed3,view=self)










    
async def setup(client):
  await client.add_cog(ptero(client))