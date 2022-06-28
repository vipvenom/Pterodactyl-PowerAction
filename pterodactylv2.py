import discord
from discord.ext import commands
import aiohttp
import random
import requests
import asyncio
import discord.ui
from discord.ui import Button, View
from pydactyl import PterodactylClient

# EDIT THESE
api = PterodactylClient('PANEL_URL', 'API_KEY')
pteroserverid = "SERVER_ID"

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
    embed = discord.Embed(title="Please select a power action",color=0x00ff00)
    embed.set_footer(text="Buttons will timeout in 1 minute")
    await ctx.send(embed=embed,view=view)
    print(f'{ctx.author.name} executeed the command panel')
  
  @panelweb.error
  async def panelweb_error(self,ctx, error):
    if isinstance(error, commands.NotOwner):
      embed = discord.Embed(title='⚠️ Restricted',description='Only the bot owner may execute this command!')
      await ctx.send(embed=embed)

class panelbuttons(View):
  def __init__(self,ctx):
    self.ctx = ctx
    super().__init__(timeout=60)

  @discord.ui.button(label="Start", style = discord.ButtonStyle.green)
  async def panelstart(self,interaction,button):
    if interaction.user == self.ctx.author:
      response = api.client.servers.send_power_action(pteroserverid, 'start')  
      embed = discord.Embed(title="Start signal sent successfully",color=0xff3336)
      embed.set_footer(text=f"Started by {interaction.user}")
      self.clear_items()
      await interaction.response.edit_message(embed=embed, view=self)

  @discord.ui.button(label="Stop", style = discord.ButtonStyle.red)
  async def panelstop(self,interaction,button):
    if interaction.user == self.ctx.author:
      response = api.client.servers.send_power_action(pteroserverid, 'stop')  
      embed = discord.Embed(description=f"Stop signal sent successfully",color=0xff3336)
      embed.set_footer(text=f"Stopped by {interaction.user}")
      self.clear_items()
      await interaction.response.edit_message(embed=embed,view=self)

  @discord.ui.button(label="Restart", style = discord.ButtonStyle.blurple)
  async def panelrestart(self,interaction,button):
    if interaction.user == self.ctx.author:
      response = api.client.servers.send_power_action(pteroserverid, 'restart')  
      embed = discord.Embed(description=f"Restart signal sent successfully",color=0xff3336)
      embed.set_footer(text=f"Restarted by {interaction.user}")
      self.clear_items()
      await interaction.response.edit_message(embed=embed,view=self)

  @discord.ui.button(label="Cancel", style = discord.ButtonStyle.grey)
  async def panelcancel(self,interaction,button):
    if interaction.user == self.ctx.author:
      embed = discord.Embed(description=f"Cancelled server power action",color=0xff3336)
      embed.set_footer(text=f"Cancelled by {interaction.user}")
      self.clear_items()
      await interaction.response.edit_message(embed=embed,view=self)

async def setup(client):
  await client.add_cog(ptero(client))
