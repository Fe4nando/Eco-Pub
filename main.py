
import discord 
import json
import random
from discord.ext import commands 
from Assets.embeds import help1
import asyncio
import os
import time



intents = discord.Intents.all()
discord.member = True
token="OTY0MTE2MDE3MzkzNTg2MjE2.Ylf9Ag._XMlnU0TrzXT60Ux28tPfFnH1WY"
cilent=commands.Bot (command_prefix=commands.when_mentioned_or('$'),intents = intents)
cilent.remove_command('help')
status="online"
client=cilent
@cilent.event
async def on_ready():
    await cilent.change_presence(status=discord.Status.dnd,activity=discord.Game('$help'))
    print('Client online')

@cilent.command()
async def help(ctx):
  await ctx.send(embed=help1)

investments=[{"name":"Tesla","des":"Car Maker"},
            {"name":"Airbus","des":"Plane Maker"},
            {"name":"SpaceX","des":"Doge Coin!"},
            {"name":"Boeing","des":"Plane Maker"},
            {"name":"Ford","des":"Car maker"},
            {"name":"Mojang","des":"Game Developer"},
            {"name":"Roit","des":"Game Developer"}]


@cilent.command()
@commands.cooldown(1,36000,commands.cooldowns.BucketType.user)
async def invest(ctx,comp=None,amount=None):
    if comp==None and amount==None:
        em=discord.Embed(title="Investment options!",color=discord.Color.from_rgb(0,255,255))
        for item in investments:
            name = item["name"]
            description = item["des"]
            em.add_field(name=name,value=description)
        await ctx.send(embed=em)
    else:
      await open_account(ctx.author)
      user=ctx.author
      users=await get_bank_data()
      wallet_amt=users[str(user.id)]["Wallet"]
      if wallet_amt<=24999:
          await ctx.send("please Enter a Value 25k and above")
      if amount==None:
          await ctx.send("Please Enter The Amount!")
          return 
      amount=int(amount)
      if amount>wallet_amt:
          await ctx.send("You Dont Have That Much Of Money In Wallet!")
      if amount<0:
          await ctx.send("Please Enter A Positive Value!")
      market=random.randrange(2)
      if market==1:
          status="+"
      if market==0:
          data=["Due to a Pandemic the market has crashed","The Company went bankrupt","The due to war the market has crashed"]
          info=random.choice(data)
          status=f"{info} -"
      else:  
       number=random.randrange(251)
       decimal=random.randrange(100)/100
       precentage=number+decimal
       final=amount/100*precentage
       final=round(final)
       em=discord.Embed(title="Investement Summary",description=f"Investment Summary of **{ctx.author.display_name}** to **{comp}**",color=discord.Color.from_rgb(65,65,65))
       em.add_field(name="💰 **Amount Invested**",value=f"**{amount}**",inline=False)
       em.add_field(name="▶ **Status**",value=f"**{status}{precentage}%**",inline=False)
       em.add_field(name="✅ **Final**",value=f"**{status}{final}**")
       if status=="+":
          users[str(user.id)]["Wallet"]-=amount
          users[str(user.id)]["Net"]+=final
          with open(r"./data/mainbank.json","w") as f:
             json.dump(users,f)

       if status=="-":
          users[str(user.id)]["Wallet"]-=amount
          with open(r"./data/mainbank.json","w") as f:
             json.dump(users,f)
        
       await ctx.send(embed=em)
        
        
    
        
 

@cilent.command(aliases = ["lb"])
async def leaderboard(ctx,x = 5):
    users = await get_bank_data()
    leader_board = {}
    total = []
    for user in users:
        name = int(user)
        total_amount = users[user]["Net"]+users[user]["Wallet"]+users[user]["Bank"]
        leader_board[total_amount] = name
        total.append(total_amount)
    total = sorted(total,reverse=True)   
    em = discord.Embed(title = f"Top {x} Richest People" , description = "This is decided on the basis of Net Value",color = discord.Color.from_rgb(255,255,0))
    index = 1
    for amt in total:
        id_ = leader_board[amt]
        member = cilent.get_user(id_)
        name = member.name
        em.add_field(name = f"{index}. {name}" , value = f"**Net Value**:{amt}",  inline = False)
        if index == x:
            break
        else:
            index += 1
    await ctx.send(embed = em)

@cilent.command()
async def withdraw(ctx,amount=None):
    await open_account(ctx.author)
    if amount==None:
        await ctx.send("Please enter the amount")
        return
    bal = await update_bank(ctx.author)
    amount=int(amount)
    if amount>bal[1]:
        await ctx.send("You dont have that much money")
        return
    if amount<0:
        await ctx.send("Please Enter a Positive Value")
        return
    await update_bank(ctx.author,amount)
    await update_bank(ctx.author,-1*amount,"Bank")
    await ctx.send(f"{amount} has been withdrew from your account")
@cilent.command()
async def dep(ctx,amount=None):
    await open_account(ctx.author)
    if amount==None:
        await ctx.send("Please enter the amount")
        return
    bal = await update_bank(ctx.author)
    amount=int(amount)
    if amount>bal[0]:
        await ctx.send("You dont have that much money")
        return
    if amount<0:
        await ctx.send("Please Enter a Positive Value")
        return
    await update_bank(ctx.author,-1*amount)
    await update_bank(ctx.author,amount,"Bank")
    await ctx.send(f"{amount} has been deposited to your account")
        

@cilent.command()
@commands.cooldown(1,120,commands.cooldowns.BucketType.user)
async def beg(ctx):
    await open_account(ctx.author)
    users=await get_bank_data()
    user=ctx.author
    earnings=random.randrange(251)
    await ctx.send(f"Someone gave you {earnings} money!")
    users[str(user.id)]["Wallet"]+=earnings
    with open(r"./data/mainbank.json","w") as f:
        json.dump(users,f)
        
@cilent.command()
@commands.cooldown(1,72000,commands.cooldowns.BucketType.user)
async def daily(ctx):
    await open_account(ctx.author)
    users=await get_bank_data()
    user=ctx.author
    users[str(user.id)]["daily count"]+=1
    daily_check=users[str(user.id)]["daily count"]
    daily=5000
    if daily_check>9:
        daily=10000
    if daily_check>49:
        daily=25000
    if daily_check>99:
        daily=50000
    
    earning=daily
    users[str(user.id)]["Wallet"]+=earning
    await ctx.send(f"Your Daily Amount:{daily} has been given to you! Day Count:{daily_check}")
    
    with open(r"./data/mainbank.json","w") as f:
        json.dump(users,f)
        
@daily.error
async def error(ctx,error):
    if isinstance(error,commands.CommandOnCooldown):
        msg="Looks like you hit a roadblock! Try again <t:{}:R>".format(int(time.time() + error.retry_after))
        await ctx.send(msg)
@beg.error
async def error(ctx,error):
    if isinstance(error,commands.CommandOnCooldown):
        msg="Oops! Try again <t:{}:R>".format(int(time.time() + error.retry_after))
        await ctx.send(msg)
        
@invest.error
async def error(ctx,error):
    if isinstance(error,commands.CommandOnCooldown):
        msg="We have a issue at the bank try again <t:{}:R>".format(int(time.time() + error.retry_after))
        await ctx.send(msg)
        

        
@cilent.command()
async def balance(ctx):
    await open_account(ctx.author)
    user=ctx.author
    users=await get_bank_data()
    wallet_amt=users[str(user.id)]["Wallet"]
    bank_amt=users[str(user.id)]["Bank"]
    net_amt=users[str(user.id)]["Net"]
    net_amt=net_amt+wallet_amt+bank_amt
    em=discord.Embed(title=f"{ctx.author.display_name}'s balance",color=discord.Color.from_rgb(65,65,65))
    em.add_field(name="💴 **Wallet**:",value=f"{wallet_amt}",inline=True)
    em.add_field(name="💳 **Bank**:",value=f"{bank_amt}",inline=True)
    em.add_field(name="💰 **Net Worth**:",value=f"{net_amt}",inline=False)
    await ctx.send(embed=em)

async def open_account(user):
    users=await get_bank_data()
    if str(user.id) in users:
        return False
    else:
        users[str(user.id)]={}
        users[str(user.id)]["Wallet"]=0
        users[str(user.id)]["Bank"]=0
        users[str(user.id)]["Net"]=0
        users[str(user.id)]["daily count"]=0
        users[str(user.id)]["Job"]=0
        users[str(user.id)]["Hours"]=0
        users[str(user.id)]["Tree"]=0
        
        
       

    with open(r"./data/mainbank.json","w") as f:
        json.dump(users,f)
       
        
    return True

async def get_bank_data():
    with open (r"./data/mainbank.json","r") as f:
        users=json.load(f)

        return users 

async def update_bank(user,change=0,mode="Wallet"):
    users=await get_bank_data()
    users[str(user.id)][mode]+=change
    with open(r"./data/mainbank.json","w") as f:
        json.dump(users,f)
    bal=[users[str(user.id)]["Wallet"],users[str(user.id)]["Bank"]]
    return bal

@client.command()
async def download(ctx):
    if ctx.author.id==738243110949355672:
     await ctx.send(file=discord.File(r'./data/mainbank.json'))
    else:
        await ctx.send("You Cant Download the Data unless your Fernando.")
    

@client.command()
async def load_extensions(ctx,extension):
    client.load_extension(f"cogs.{extension}")

@client.command()
async def unload_extensions(ctx,extension):
    client.unload_extension(f"cogs.{extension}")
    
async def load_extensions():
 for filename in os.listdir('./commands'):
    if filename.endswith('.py'):
        await client.load_extension(f'commands.{filename[:-3]}')
    
async def main():
    async with client:
        await load_extensions()
        await client.start(token)

asyncio.run(main())