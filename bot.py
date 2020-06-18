# Work with Python 3.6
import discord
from random import * 
from discord.utils import get
import os.path 
import json 
import datetime  
import time 
TOKEN = 'Njk1ODk1NDU5NjkyMTUwODQ1.XohEwg.ufQKWbb8dw4DdmUoPqoZBaCcADY'
default_time = 1586016335
MONTH = 60 * 60 * 24 * 30
WEEK = 60 * 60 * 24 * 7 
client = discord.Client()
monthly = ["2020-05-01 00:00:00", 
    "2020-06-01 00:00:00", "2020-04-22 00:00:00", 
    "2020-07-01 00:00:00", "2020-05-22 00:00:00", 
    "2020-08-01 00:00:00", "2020-06-22 00:00:00", 
    "2020-09-01 00:00:00", "2020-07-22 00:00:00", 
    "2020-10-01 00:00:00", "2020-08-22 00:00:00", 
    "2020-11-01 00:00:00", "2020-09-22 00:00:00", 
    "2020-12-01 00:00:00", "2020-10-22 00:00:00", 
    "2020-12-01 00:00:00", "2020-11-22 00:00:00", 
    "2020-04-15 00:00:00", "2020-05-15 00:00:00",
    "2020-06-15 00:00:00", "2020-07-15 00:00:00",
    "2020-08-15 00:00:00", "2020-09-15 00:00:00",
    "2020-10-15 00:00:00", "2020-11-15 00:00:00",
    "2020-12-15 00:00:00", "2020-04-07 00:00:00",
    "2020-05-07 00:00:00", "2020-06-07 00:00:00",
    "2020-07-07 00:00:00", "2020-08-07 00:00:00",
    "2020-09-07 00:00:00", "2020-10-07 00:00:00",
    "2020-11-07 00:00:00", "2020-12-07 00:00:00",
    "2020-04-22 00:00:00"
]
RULES = """group này có các channel chia theo các mảng: web, pwn, crypto, re, misc,...
các e nghiên cứu mảng nào có thắc mắc có thể đặt câu hỏi ở channel tương ứng, ae nào biết sẽ giải đáp thắc mắc của các e :v
Bên cạnh đó, cuối tuần nếu rảnh bọn a sẽ đăng kí tham gia các giải CTF online. Các em có thể xem lịch của các giải đó ở đây 
https://ctftime.org/ 
Sau khi đăng kí bọn a sẽ tạo channel tương ứng với giải đó và nhắn user/pass. Các e có thể tham gia chơi cùng :v
"""
isCheck = True 

def getChannelCategory(channel) : 
    category_id = channel.category_id 
    parent = get(client.get_all_channels(), id = category_id)
    return parent 

def checkDate() : 
    global isCheck
    date = str(datetime.datetime.today().replace(hour=0, minute=0, second=0)).split(".")[0] 
    if isCheck == True and date in monthly : 
        isCheck = False 
        return True
    if datetime.datetime.now().day in [2, 8, 16, 23] : 
        isCheck = True 
    return False 

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return
    
    if message.content.startswith("!help") : 
        msg = """
            Chào bạn. Mình là đệ của hắc mão. Mình có thể làm một vài công việc như sau :    
            \t 1. `!hello` : chào bot dễ thương bot sẽ chào lại.  
            \t 2. `!create <name-channel>` : tạo channel các challenge khi chơi ctf. Tạo trong channel `notify` của kì CTF tương ứng với.  
                    VD : picoCTF2020 - challenge warmup tên sẽ là : pico2020-warmup   
            \t 3. `!list` : liệt kê tất cả channel trong thư mục hiện tại.  
            \t 4. `join <name-channel>` : tham gia vào một channel ctf. Thông thường nó sẽ được ẩn đi.  
            \t 5. `!solve` : sau khi hoàn thành một challenge, vào channel của challenge đó và gõ `!solve` để log lại kết quả.  
            \t 6. `!status` : gõ `!status` ở channel `notify` để biết bài nào đã solve, chưa solve, ai solve để hỏi đáp cho dễ.  
            \t 7. `!rules` : hiện luật.  
        """ 
        await message.channel.send(msg)

    if message.content.startswith('!hello'):
        print(message.author)
        if "Lan" in str(message.author) : 
            msg = 'Hello {0.author.mention} xinh gái.'.format(message)
        elif "quan" in str(message.author) : 
            msg = '{0.author.mention} Lo con k'.format(message)
        elif "hac_mao" in str(message.author) : 
            msg = 'Hello đại ca {0.author.mention}.Chúc đại ca ngày mới tốt lành.Tu tiên tới bất diệt truyền thuyết.'.format(message)
        else : 
            msg = 'Hello {0.author.mention}'.format(message)
        await message.channel.send(msg)
    
    if message.author.name == "hac_mao" and "hi" in message.content : 
        await message.channel.send("Chào bạn mình là đệ hắc mão! Chào lại bằng cách gõ `!hello`. Gõ `!help` để nhận sự giúp đỡ.") 

    if  message.content.startswith("!rule") : 
        await message.channel.send(RULES) 
    
    if message.content.startswith("!join") : 
        argv = message.content.split(' ') 
        if len(argv) != 2 : 
            await message.channel.send("`USAGE : join <channel-name>`")
            return 
        else : 
            guild = client.guilds[0] 
            channel = get(guild.channels, name=argv[1]) 
            override = discord.PermissionOverwrite()
            override.send_messages = True
            override.read_messages = True
            if channel == None : 
                return 
            await channel.send("Hacmao_bot has add {0.author.name} to the channel.".format(message)) 
            await channel.set_permissions(message.author, overwrite=override) 
        
    if message.content.startswith('!create') :
        argv = message.content.split(" ") 
        if len(argv) != 2 : 
            await message.channel.send("USAGE : `!create <name-channel>`") 
            return 
        
        if "notify" not in message.channel.name : 
            await message.channel.send("You must create new channel in notify channel. Go to CTF channel.")   
            return 

        guild = client.guilds[0]
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False)
        }
        category = get(client.get_all_channels(), name="testctf") 
        channel = await guild.create_text_channel(argv[1], overwrites=overwrites, category=category) 

        # add creator to secret channel
        override = discord.PermissionOverwrite()
        override.send_messages = True
        override.read_messages = True
        await channel.set_permissions(message.author, overwrite=override)
        await channel.send("Hacmao_bot has add {0.author.name} to the channel.".format(message)) 

        ctf_name = category.name + "_unsolved"
        challenge_name = argv[1]
        if os.path.isfile(ctf_name) : 
            f = open(ctf_name , "a") 
        else : 
            f = open(ctf_name , "w") 
        f.write(challenge_name + "\n") 
        f.close() 

    if message.content.startswith("!list") : 
        if "notify" not in message.channel.name : 
            await message.channel.send("You must list channel in notify channel. Go to CTF channel.")   
            return
        category = getChannelCategory(message.channel) 
        channels = client.get_all_channels() 
        msg = "```🎇🎇🎇Channel list : \n"
        for channel in channels : 
            if category == getChannelCategory(channel) : 
                msg += "  🔑 {0.name}\n".format(channel) 
        msg += "```\n" 
        await message.channel.send(msg)  

    if message.content.startswith("!solve") : 
        category = getChannelCategory(message.channel) 
        if category == None or "ctf" not in category.name or "notify" in message.channel.name : 
            await message.channel.send("Nhầm channel bạn eii!!!") 
            return 
        ctf_name = category.name + "_solved" 
        unsolve_challenge = open(category.name + "_unsolved", "r").read() 
        if message.channel.name not in unsolve_challenge : 
            await message.channel.send("Challenge đã được giải thành công!") 
            return 
        if os.path.isfile(ctf_name) : 
            f = open(ctf_name , "a") 
        else : 
            f = open(ctf_name , "w") 
        msg = "\t [*] {0.channel.name} : {1.author.name}\n".format(message, message) 
        f.write(msg) 
        f.close()

        unsolve_challenge = unsolve_challenge.replace(message.channel.name + "\n", "")  # delete solved challenge from unsolved challenge 
        f = open(category.name + "_unsolved", "w") 
        f.write(unsolve_challenge)
        f.close()
        await message.channel.send("[****] @here {0.author.name} make BKSEC greate again. ".format(message)) 

    if message.content.startswith("!status") : 
        channel_name = message.channel.name 
        category = getChannelCategory(message.channel) 
        if category == None or "ctf" not in category.name : 
            await message.channel.send("Nhầm channel bạn eii!!!") 
            return 
        ctf_name = category.name 
        try : 
            solved_challenge = open(ctf_name + "_solved", "r").read() 
            solved_challenge = solved_challenge.replace("[*]", "✅")
        except : 
            solved_challenge = ""
        unsolve_challenge = open(ctf_name + "_unsolved", "r").read().split("\n") 
        
        msg = "```💥💥💥 SOLVED : \n" + solved_challenge  + "\n"
        msg += "💥💥💥 UNSOLVED : \n" 
        for c in unsolve_challenge[:-1] : 
            msg += "\t ❌ " + c + "\n" 
        msg += "```\n"
        await message.channel.send(msg)   

    # log data and check user 
    current_time = int(time.time())
    username = message.author.name 
    users = json.load(open("users.json", "r"))  
    users[username] = current_time
    """
    if checkDate() : 
        channel = get(client.get_all_channels(), name="bot-nhac-nho")
        for user in users.keys() :  
            if current_time - users[user] > 2*WEEK : 
                user_ = get(client.get_all_members(), name=user) 
                await channel.send("{0.mention} ơi! Ping lần 2 !!!".format(user_)) 
            elif current_time - users[user] > WEEK : 
                user_ = get(client.get_all_members(), name=user) 
                await channel.send("{0.mention} ơi! Bạn đâu rồi !!!".format(user_)) 
            if current_time - users[user] > WEEK * 4 : 
                await channel.send("Hacmao_bot lost his patient with {0}".format(user_.name)) 
                #await client.kick(user_)  
    """        

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


client.run(TOKEN)
