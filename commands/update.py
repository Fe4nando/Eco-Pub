import discord 
from discord.ext import commands 
import json 

class Update(commands.Cog):
    def __init__(self,client):
     self.client=client
     
    @commands.command()
    async def update(self,ctx):
     await open_account(ctx.author)
     user=ctx.author
     users=await get_bank_data()
     wallet_amt=users[str(user.id)]["Wallet"]
     bank_amt=users[str(user.id)]["Bank"]
     net_amt=users[str(user.id)]["Net"]
     daily_count=users[str(user.id)]['daily count']
     #update 
     users[str(user.id)]["Wallet"]=wallet_amt
     users[str(user.id)]["Bank"]=bank_amt
     users[str(user.id)]["Net"]=net_amt
     users[str(user.id)]["daily count"]=daily_count
     users[str(user.id)]["Job"]=0
     users[str(user.id)]["Hours"]=0
     users[str(user.id)]["Tree"]=0
     with open(r"./data/mainbank.json","w") as f:
        json.dump(users,f)
     await ctx.send("Update Complete!")
     
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
     
     
async def setup(client):
    await  client.add_cog(Update(client))