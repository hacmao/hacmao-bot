# Work with Python 3.6
import discord
from random import * 
from discord.utils import get
import os.path 
import json 
import datetime  
import time 
from upcomming import upcomming_events, getCtfInfo
from writeup import * 


TOKEN = 'Njk1ODk1NDU5NjkyMTUwODQ1.XohEwg.ufQKWbb8dw4DdmUoPqoZBaCcADY'
default_time = int(time.time())
MONTH = 60 * 60 * 24 * 30
WEEK = 60 * 60 * 24 
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
    "2020-12-15 00:00:00", "2020-04-06 00:00:00",
    "2020-05-07 00:00:00", "2020-06-07 00:00:00",
    "2020-07-07 00:00:00", "2020-08-07 00:00:00",
    "2020-09-07 00:00:00", "2020-10-07 00:00:00",
    "2020-11-07 00:00:00", "2020-12-07 00:00:00",
    "2020-04-22 00:00:00"
]
RULES = """Có một trưởng lão từng nói  
```group này có các channel chia theo các mảng: web, pwn, crypto, re, misc,...
các e nghiên cứu mảng nào có thắc mắc có thể đặt câu hỏi ở channel tương ứng, ae nào biết sẽ giải đáp thắc mắc của các e :v
Bên cạnh đó, cuối tuần nếu rảnh bọn a sẽ đăng kí tham gia các giải CTF online. Các em có thể xem lịch của các giải đó ở đây 
https://ctftime.org/ 
Sau khi đăng kí bọn a sẽ tạo channel tương ứng với giải đó và nhắn user/pass. Các e có thể tham gia chơi cùng :v```
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

async def createChannelInCategory(message, name, category) :  
    guild = client.guilds[0]
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False)
    }
    channel = await guild.create_text_channel(name, overwrites=overwrites, category=category) 

    # add creator to secret channel
    override = discord.PermissionOverwrite()
    override.send_messages = True
    override.read_messages = True
    await channel.set_permissions(message.author, overwrite=override)
    await channel.send("Hacmao_bot has add {0.author.name} to the channel.".format(message)) 
    return channel 

async def createCTF(message, name) :  
    guild = client.guilds[0]
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False)
    }
    channel = await guild.create_category(name) 
    return channel

def getCTF(message) : 
    ctf_name = getChannelCategory(message.channel).name
    ctf_list = json.load(open("ctf.json", "r"))
    current_ctf = ctf_list[ctf_name] 
    return current_ctf 

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return
    
    content = message.content.strip()
    if content.startswith("!help") : 
        msg = """
            Chào bạn. Mình là đệ của hắc mão. Mình có thể làm một vài công việc như sau :    
            \t 1. `!hello` : chào bot dễ thương bot sẽ chào lại.  
            \t 2. `!create <name-channel>` : tạo channel các challenge khi chơi ctf. Tạo trong channel `notify` của kì CTF tương ứng với.  
                    VD : picoCTF2020 - challenge warmup tên sẽ là : pico2020-warmup   
            \t 3. `!list` : liệt kê tất cả channel trong thư mục hiện tại.  
            \t 4. `!join <name-channel>` : tham gia vào một channel ctf. Thông thường nó sẽ được ẩn đi.  
            \t 5. `!solve` : sau khi hoàn thành một challenge, vào channel của challenge đó và gõ `!solve` để log lại kết quả.  
            \t 6. `!status` : gõ `!status` ở channel `notify` để biết bài nào đã solve, chưa solve, ai solve để hỏi đáp cho dễ.  
            \t 8. `!info` : xem thông tin chi tiết về kì CTF đang chơi tại channel `notify` 
            \t 9. `!upcoming` : xem thông tin về các kì CTF sắp tới 
            \t 10. `!writeup <category>` : search các writeup về kì CTF hiện tại trên ctfd
            \t 11. `!rank` : hiển thị rank hiện tại trong group bksec 
            \t 12. `!rules` : hiện luật.  
            Admin : 
            \t 1. `!addctf` <ctf-name> <ctfd-url> : lưu ý ctfd-url là url được đăng trên trang ctftime, ko phải trang chơi ctf.
        """ 

        await message.channel.send(msg)

    if content.startswith('!hello'):
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
    
    if message.author.name == "hac_mao" and "!bot" in message.content : 
        await message.channel.send("Chuẩn rồi đại ca.") 

    if  content.startswith("!rule") : 
        await message.channel.send(RULES) 
    
    if content.startswith("!join") : 
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
        
    if content.startswith('!create') :
        if "notify" not in message.channel.name : 
            await message.channel.send("You must create new channel in notify channel. Go to CTF channel.")   
            return 
        argv = content.split(" ") 
        if len(argv) != 2 : 
            await message.channel.send("USAGE : !create <channel-name>") 
            return 

        ctf_name = getChannelCategory(message.channel)
        await createChannelInCategory(message, argv[1], ctf_name) 
        ctf_list = json.load(open("ctf.json", "r")) 
        current_ctf = ctf_list[ctf_name.name] 
        if "challenge" not in current_ctf.keys() : 
            current_ctf["challenge"] = {}
        current_ctf["challenge"][argv[1]] = None 
        json.dump(ctf_list, open("ctf.json", "w")) 

    if content.startswith("!list") : 
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

    if content.startswith("!solve") : 
        author = message.author.name
        category = getChannelCategory(message.channel) 
        if category == None  or "notify" in message.channel.name : 
            await message.channel.send("Nhầm channel bạn eii!!!") 
            return 
        ctf_name = getChannelCategory(message.channel).name
        ctf_list = json.load(open("ctf.json", "r"))
        current_ctf = ctf_list[ctf_name] 
        challenge_name = message.channel.name
        if  current_ctf["challenge"][challenge_name] != None : 
            await message.channel.send("Challenge đã được giải thành công!") 
            return 
        else : 
            current_ctf["challenge"][challenge_name] = message.author.name
            json.dump(ctf_list, open("ctf.json", "w"))
            users = json.load(open("users.json", "r")) 
            if author not in users.keys() : 
                users[author] = {}
                users[author]["last_access"] = int(time.time()) 
                users[author]['points'] = 0
            users[author]['points'] += 1
            json.dump(users, open("users.json", "w"))
            await message.channel.send("[****] @here {0.author.name} make BKSEC greate again. ".format(message)) 

    if content.startswith("!status") : 
        channel_name = message.channel.name 
        category = getChannelCategory(message.channel) 
        if category == None or "ctf" not in category.name or "notify" not in channel_name: 
            await message.channel.send("Nhầm channel bạn eii!!!") 
            return 
        
        current_ctf = getCTF(message) 
        challenges = current_ctf['challenge']
        solved = [] 
        unsolved = [] 
        for _ in challenges.keys() : 
            if challenges[_] == None : 
                unsolved.append(_) 
            else : 
                solved.append([_, challenges[_]]) 
 
        msg = "```💥💥💥 SOLVED : \n" 
        for _ in solved : 
            msg += "\t✅ {0[0]} : {0[1]}".format(_) + "\n"
        msg += "```\n```"
        msg += "💥💥💥 UNSOLVED : \n" 
        for c in unsolved : 
            msg += "\t ❌ " + c + "\n" 
        msg += "```\n"
        await message.channel.send(msg)   

    if content.startswith("!upcoming") : 
        msgs = await upcomming_events() 
        for msg in msgs : 
            await message.channel.send(msg)

    if content.startswith("!addctf") : 
        if message.author.top_role.name == "admin" : 
            args = content.split(" ") 
            if len(args) != 3 : 
                await message.channel.send("USAGE : !addctf <ctf-name> <ctfd-url>")
                return 
            ctf_name, ctf_url = args[1].lower(), args[2]  
            ctf_list = json.load(open("ctf.json", "r"))  
            if ctf_name not in ctf_list.keys() : 
                ctf_list[ctf_name] = {} 
            ctf_list[ctf_name]["ctfd_link"] = args[2].lower()
            json.dump(ctf_list, open("ctf.json", "w")) 
            ctf_channel = await createCTF(message, ctf_name) 
            # notify_channel = await createChannelInCategory(message, "notify", ctf_channel) 
            guild = client.guilds[0]
            notify_channel = await guild.create_text_channel("notify", category=ctf_channel) 

            author = message.author
            msg = "@here "
            if "Lan" in author.name : 
                msg += "{0.mention} sư tỉ nay có nhã hứng chơi {1}".format(author, ctf_name) 
            elif "hac_mao" in author.name : 
                msg += "Đại ca đã tạo {0}".format(ctf_name) 
            else : 
                msg += "{0.mention} sư huynh đã điều động chư vị huynh đệ cùng thảo phạt {1}".format(author, ctf_name) 
            await notify_channel.send(msg)
        else : 
            await message.channel.send("Chỉ có sư huynh, sư tỉ mới được làm điều này.(*￣3￣)╭")
    
    if content.startswith("!info") : 
        if message.channel.name != "notify" : 
            return 
        
        current_ctf = getCTF(message)
        ctfd_url = current_ctf["ctfd_link"] 
        msg = await getCtfInfo(ctfd_url) 
        await message.channel.send(msg)

    if content.startswith("!writeup") : 
        ctf_name = getChannelCategory(message.channel).name
        ctf_list = json.load(open("ctf.json", "r")) 
        if ctf_name not in ctf_list.keys() : 
            return 
        current_ctf = ctf_list[ctf_name]
        ctfd_link_wu = current_ctf["ctfd_link"] + "/tasks/" 
        argv = message.content.split(" ") 
        if len(argv) > 2 : 
            await message.channel.send("`USAGE : !writeup <category>?`") 
            return 
        elif len(argv) == 2 : 
            msgs = await original_writeups_tag(ctfd_link_wu, argv[1])
            for msg in msgs : 
                await message.channel.send(msg)
        else : 
            msgs =  await original_writeups(ctfd_link_wu)
            for msg in msgs : 
                await message.channel.send(msg)

    if content.startswith("!addp") : 
        author = message.author 
        if author.top_role.name != "admin" : 
            await message.channel.send("Chỉ có sư huynh, sư tỉ mới được quyền cộng điểm. ¯\_(ツ)_/¯") 
            return 
        
        args = content.split(" ") 
        if len(args) != 2 : 
            await message.channel.send("`USAGE : !addp <points>") 
            return 
        
        points = args[1] 
        if not points.isdigit() :  
            await message.channel.send("Điểm phải là số") 
            return 
        ctf_name = getChannelCategory(message.channel).name 
        ctf_list = json.load(open("ctf.json", "r")) 
        challenge_name = message.channel.name 
        if ctf_name not in ctf_list.keys() : 
            await message.channel.send("Sai kênh rồi biểu huynh :))")  
            return 
        
        current_ctf = ctf_list[ctf_name] 
        if current_ctf['challenge'][challenge_name] == None : 
            await message.channel.send('Challenge phải được giải trước khi cộng điểm.')
            return   
        user_solve = current_ctf['challenge'][challenge_name] 
        if "scoreboard" not in current_ctf.keys() : 
            current_ctf['scoreboard'] = {} 
        if user_solve not in current_ctf['scoreboard'].keys() : 
            current_ctf['scoreboard'][user_solve] = 0 
        current_ctf['scoreboard'][user_solve] += int(points)  
        json.dump(ctf_list, open("ctf.json", "w")) 
    
    if content.startswith("!sc") : 
        headers = ["TOP", "Username", "Points"] 
        info = []
        msgs = []
        ctf_name = getChannelCategory(message.channel).name 
        ctf_list = json.load(open("ctf.json", "r")) 
        challenge_name = message.channel.name 
        if ctf_name not in ctf_list.keys() : 
            await message.channel.send("Sai kênh rồi biểu huynh :))")  
            return 
        current_ctf = ctf_list[ctf_name] 

        if "scoreboard" not in current_ctf.keys() :  
            await message.channel.send("No solved yet") 
            return 
        
        scoreboard = current_ctf['scoreboard'] 
        scoreboard = sorted(scoreboard.items(), key = lambda kv:(kv[0], kv[1]))
        for ind, user in enumerate(scoreboard, start=1) : 
            username, points = user
            info.append([ind, username, points]) 
            tmp = tabulate(info, headers, tablefmt="fancy_grid") 
            if len(tmp) >= 1994 : 
                tmp = tabulate(info[:-1], headers, tablefmt="fancy_grid") 
                msgs.append("```" + tmp + "```") 
                info = [info[-1]] 
        table = tabulate(info, headers, tablefmt="fancy_grid") 
        msgs.append("```" + table + "```" )
        for msg in msgs : 
            await message.channel.send(msg) 

    if content.startswith("!rank") :  
        headers = ["TOP", "Name", "Points"] 
        users = json.load(open("users.json", "r")) 
        top_users = sorted(users.items(), key = lambda kv:(kv[1]['points'], kv[1]['points']))[::-1][:5]
        info = [] 
        for i in range(len(top_users)) : 
            user = top_users[i]
            info.append([i+1, user[0], user[1]['points']]) 
        
        msg = "```" 
        msg += tabulate(info, headers, tablefmt="fancy_grid") + "```"

        await message.channel.send(msg)

    if content.startswith("!addwu") : 
        args = content.split(" ") 
        user_id = int(args[1][3:-1])
        user = get(client.get_all_members(), id=user_id).name
        users_list = json.load(open("users.json", "r")) 
        users_list[user]['points'] += 3
        json.dump(users_list, open("users.json", "w"))
        

    # log data and check user 
    current_time = int(time.time())
    username = message.author.name 
    users = json.load(open("users.json", "r"))  
    if username not in users.keys() : 
        users[username] = {"last_access" : current_time}
    users[username]["last_access"] = current_time
    json.dump(users, open("users.json", "w"))
    if checkDate() : 
        channel = get(client.get_all_channels(), name="bot-nhac-nho")
        for user in users.keys() :  
            if current_time - users[user]["last_access"] > 2 * WEEK : 
                user_ = get(client.get_all_members(), name=user) 
                await channel.send("{0.mention} ơi! Ping lần 2 !!!".format(user_)) 
            elif current_time - users[user]["last_access"] > WEEK : 
                user_ = get(client.get_all_members(), name=user) 
                await channel.send("{0.mention} ơi! Bạn đâu rồi !!!".format(user_)) 
            
            guild = client.guilds[0]
            if current_time - users[user]["last_access"] > WEEK * 4 : 
                await channel.send("Hacmao_bot lost his patient with {0}".format(user_.name)) 
                await guild.kick(user_)  
            break
        

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    # get all users 
    guild = client.guilds[0] 
    members = guild.members 
    users = json.load(open("users.json", "r"))
    current_username = users.keys()
    for member in members : 
        name = member.name
        if name not in current_username : 
            users[name] = {} 
            users[name]["last_access"] = int(time.time())
            users[name]["points"] = 0 
    json.dump(users, open("users.json", "w"))
    print('------')


client.run(TOKEN)
