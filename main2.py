import requests
import json
import subprocess
from pyrogram import Client,filters
from pyrogram.types.messages_and_media import message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import FloodWait
from pyromod import listen
from pyrogram.types import Message
import pyrogram
import tgcrypto
import speedtest
from p_bar import progress_bar
from details import api_id, api_hash, bot_token, sudo_groups
from urllib.parse import parse_qs, urlparse
from subprocess import getstatusoutput
import helper
import logging
import time
import aiohttp
import asyncio
import aiofiles
from aiohttp import ClientSession
from pyrogram.types import User, Message
import sys ,io
import re
import os
from pyrogram.types import InputMediaDocument
import time
import random 
from psutil import disk_usage, cpu_percent, swap_memory, cpu_count, virtual_memory, net_io_counters, boot_time
import asyncio
from pyrogram import Client, filters
from pyrogram.errors.exceptions import MessageIdInvalid
import os
import yt_dlp
from bs4 import BeautifulSoup
from pyrogram.types import InputMediaDocument

botStartTime = time.time()
batch = []
bot = Client(
    "bot",
    api_id=api_id,
    api_hash=api_hash,
    bot_token=bot_token)
      
@bot.on_message(filters.command(["start"]) & filters.chat(sudo_groups))
async def start_handler(bot: Client, m: Message):
    menu_text = (
        "Welcome to XENOMORPH Downloader Bot!▄︻デ══━一💥 \n\n"
        "1. For All PDF /pdf\n"
        "2. For TXT /tor\n"
        "3. To Restart /restart\n"
        "4. Speedtest /speedtest\n"
    )
    
    await m.reply_text(menu_text)


@bot.on_message(filters.command(["restart"]))
async def restart_handler(bot: Client, m: Message):
 rcredit = "Bot Restarted by " + f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
 if (f'{m.from_user.id}' in batch or batch == []) or m.from_user.id == sudo_groups:
    await m.reply_text("Restarted ✅", True)
    os.execl(sys.executable, sys.executable, *sys.argv)
 else:
 	await m.reply_text("You are not started this batch 😶.")

@bot.on_message(filters.command(["pdf"])&(filters.chat(sudo_groups)))
async def c_pdf(bot: Client, m: Message):
    editable = await m.reply_text("**Hello I am All in one pdf DL Bot\n\nSend TXT file To Download.**")
    input99: Message = await bot.listen(editable.chat.id)
    x = await input99.download()
    await input99.delete(True)
    try:         
        with open(x, "r", encoding="utf-8") as f:
             content = f.read()
             content = content.split("\n")
        links = []
        for i in content:
           if i != '':
                 links.append(i.split(":", 1))
        os.remove(x)
    except Exception as e:
        logging.error(e)
        await m.reply_text("Invalid file input ❌.")
        os.remove(x)
        return
        
    editable = await m.reply_text(f"Total links found in given txt {len(links)}\n\nSend From range, you want to download,\n\nInitial is 1")
    input1: Message = await bot.listen(editable.chat.id)
    count = input1.text
    count = int(count)      	
    	            
    await m.reply_text("**Enter Batch Name**")
    inputy: Message = await bot.listen(editable.chat.id)
    raw_texty = inputy.text        
    try:
        for i in range(count -1, len(links)):
          name = links[i][0]
          url = links[i][1]
          cc = f'{str(count).zfill(3)}. {name}.pdf\n\n**Batch:-** {raw_texty}\n\n'
          os.system(f'yt-dlp  "{url}" -N 200 -o "{name}.pdf"')
          await m.reply_document(f'{name}.pdf', caption=cc)
          count += 1
          os.remove(f'{name}.pdf')
          time.sleep(2)
    except Exception as e:
        await m.reply_text(e)
    await m.reply_text("Completed ✅")

def meFormatter(milliseconds) -> str:
    milliseconds = int(milliseconds) * 1000
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
        (f"{str(days)}d, " if days else "")
        + (f"{str(hours)}h, " if hours else "")
        + (f"{str(minutes)}m, " if minutes else "")
        + (f"{str(seconds)}s, " if seconds else "")
        + (f"{str(milliseconds)}ms, " if milliseconds else "")
    )
    return tmp[:-2]    

def humanbytes(size):
    size = int(size)
    if not size:
        return ""
    power = 2**10
    n = 0
    Dic_powerN = {0: ' ', 1: 'Ki', 2: 'Mi', 3: 'Gi', 4: 'Ti'}
    while size > power:
        size /= power
        n += 1
    return f"{str(round(size, 2))} {Dic_powerN[n]}B"
@bot.on_message(filters.command(["speedtest"]) & filters.chat(sudo_groups))
async def speedtest_command(bot, message):
    running_message = await message.reply_text("🔄 Running speed test...")

    st = speedtest.Speedtest()
    st.get_best_server()
    download_speed = st.download() / 1024 / 1024  
    upload_speed = st.upload() / 1024 / 1024  
    result_text = (
        "🚀 **Speed Test Results** 🚀\n\n"
        "Download Speed: 📥\n"
    )
    download_bars = "▁▂▃▄▅▆▇█"[:int(download_speed / 10)]  
    result_text += f"{download_bars} {download_speed:.2f} Mbps\n\n"
    result_text += "Upload Speed: 📤\n"
    upload_bars = "▁▂▃▄▅▆▇█"[:int(upload_speed / 10)]  
    result_text += f"{upload_bars} {upload_speed:.2f} Mbps"

    await running_message.edit_text(result_text)
    await asyncio.sleep(60)
    await running_message.delete()

@bot.on_message(filters.command(["stats"]))
async def stats(_,event: Message):
    logging.info('31')
    currentTime = meFormatter((time.time() - botStartTime))
    osUptime = meFormatter((time.time() - boot_time()))
    total, used, free, disk= disk_usage('/')
    total = humanbytes(total)
    used = humanbytes(used)
    free = humanbytes(free)
    sent = humanbytes(net_io_counters().bytes_sent)
    recv = humanbytes(net_io_counters().bytes_recv)
    cpuUsage = cpu_percent(interval=0.5)
    p_core = cpu_count(logical=False)
    t_core = cpu_count(logical=True)
    swap = swap_memory()
    swap_p = swap.percent
    swap_t = humanbytes(swap.total)
    memory = virtual_memory()
    mem_p = memory.percent
    mem_t = humanbytes(memory.total)
    mem_a = humanbytes(memory.available)
    mem_u = humanbytes(memory.used)
    stats = f'Bot Uptime: {currentTime}\n'\
            f'OS Uptime: {osUptime}\n'\
            f'Total Disk Space: {total}\n'\
            f'Used: {used} | Free: {free}\n'\
            f'Upload: {sent}\n'\
            f'Download: {recv}\n'\
            f'CPU: {cpuUsage}%\n'\
            f'RAM: {mem_p}%\n'\
            f'DISK: {disk}%\n'\
            f'Physical Cores: {p_core}\n'\
            f'Total Cores: {t_core}\n'\
            f'SWAP: {swap_t} | Used: {swap_p}%\n'\
            f'Memory Total: {mem_t}\n'\
            f'Memory Free: {mem_a}\n'\
            f'Memory Used: {mem_u}\n'
    
    await event.reply_text(f"{stats}")    

@bot.on_message(filters.command(["tor"])&(filters.chat(sudo_groups)))
async def account_login(bot: Client, m: Message):
    editable = await m.reply_text("Send links listed in a txt file in format **Name:link**") 
    input: Message = await bot.listen(editable.chat.id)
    x = await input.download()
    
    await input.delete(True)

    path = f"./downloads/{m.chat.id}"
    file_name, ext = os.path.splitext(os.path.basename(x))
    credit = ""
    if m.from_user is not None:
        credit = "Downloaded by " + f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
    else:
        credit = "Downloaded anonymously"
    try:
       with open(x, "r") as f:
           content = f.read()
       content = content.split("\n")
       links = []
       for i in content:
           links.append(i.split("://", 1))
       os.remove(x)
            # print(len(links)
    except:
           await m.reply_text("Invalid file input.")
           os.remove(x)
           return
    
   
    await editable.edit(f"Total links found are **{len(links)}**\n\nSend From where you want to download initial is **1**")
    input0: Message = await bot.listen(editable.chat.id)
    raw_text = input0.text
    await input0.delete(True)

    await editable.edit("**Enter Batch Name or send `df` for grabbing it from txt.**")
    input1: Message = await bot.listen(editable.chat.id)
    raw_text0 = input1.text
    await input1.delete(True)
    if raw_text0 == 'df':
       b_name = file_name
       
    else:
       b_name = raw_text0
    await editable.edit("**Enter resolution**")
    input2: Message = await bot.listen(editable.chat.id)
    raw_text2 = input2.text
    await input2.delete(True)
    try:
        if raw_text2 == "144":
            res = "256x144"
        elif raw_text2 == "240":
            res = "426x240"
        elif raw_text2 == "360":
            res = "640x360"
        elif raw_text2 == "480":
            res = "854x480"
        elif raw_text2 == "720":
            res = "1280x720"
        elif raw_text2 == "1080":
            res = "1920x1080" 
        else: 
            res = "UN"
    except Exception:
            res = "UN"
    
    

    await editable.edit("**Enter Caption or send `df` for default or just /skip**")
    input3: Message = await bot.listen(editable.chat.id)
    raw_text3 = input3.text
    if raw_text3 == 'df':
        creditx = credit
    elif raw_text3 == '/skip':
        creditx = ''
    elif raw_text3 == '/skip':
    	creditx = ''
    elif raw_text3 == '/skip':
    	creditx = ''
    else:
        creditx = raw_text3    
    await input3.delete(True)
   
    await editable.edit("Now send the **Thumb url**\nEg » ```https://telegra.ph/file/0633f8b6a6f110d34f044.jpg```\n\nor Send `no`")
    input6 = message = await bot.listen(editable.chat.id)
    raw_text6 = input6.text
    await input6.delete(True)
    await editable.delete()

    thumb = input6.text
    if thumb.startswith("http://") or thumb.startswith("https://"):
        getstatusoutput(f"wget '{thumb}' -O 'thumb.jpg'")
        thumb = "thumb.jpg"
    else:
        thumb == "no"

    if len(links) == 1:
        count = 1
    else:
        count = int(raw_text)
    
    
    try:
        try:
            
            message = await bot.send_message(sudo_groups, f"❇️ {b_name}")
            await message.pin()
        except Exception as e:
               print(f"Error pinning message: {e}")
        for i in range(count - 1, len(links)):

            V = links[i][1].replace("file/d/","uc?export=download&id=").replace("www.youtube-nocookie.com/embed", "youtu.be").replace("?modestbranding=1", "").replace("/view?usp=sharing","") # .replace("mpd","m3u8")
            url = "https://" + V

            if "visionias" in url:
                async with ClientSession() as session:
                    async with session.get(url, headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Language': 'en-US,en;q=0.9', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'Pragma': 'no-cache', 'Referer': 'http://www.visionias.in/', 'Sec-Fetch-Dest': 'iframe', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'cross-site', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Linux; Android 12; RMX2121) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36', 'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"', 'sec-ch-ua-mobile': '?1', 'sec-ch-ua-platform': '"Android"',}) as resp:
                        text = await resp.text()
                        url = re.search(r"(https://.*?playlist.m3u8.*?)\"", text).group(1)

            elif 'videos.classplusapp' in url:
             url = requests.get(f'https://api.classplusapp.com/cams/uploader/video/jw-signed-url?url={url}', headers={'x-access-token': 'eyJhbGciOiJIUzM4NCIsInR5cCI6IkpXVCJ9.eyJpZCI6MzgzNjkyMTIsIm9yZ0lkIjoyNjA1LCJ0eXBlIjoxLCJtb2JpbGUiOiI5MTcwODI3NzQyODkiLCJuYW1lIjoiQWNlIiwiZW1haWwiOm51bGwsImlzRmlyc3RMb2dpbiI6dHJ1ZSwiZGVmYXVsdExhbmd1YWdlIjpudWxsLCJjb3VudHJ5Q29kZSI6IklOIiwiaXNJbnRlcm5hdGlvbmFsIjowLCJpYXQiOjE2NDMyODE4NzcsImV4cCI6MTY0Mzg4NjY3N30.hM33P2ai6ivdzxPPfm01LAd4JWv-vnrSxGXqvCirCSpUfhhofpeqyeHPxtstXwe0'}).json()['url']

            elif '/master.mpd' in url:
             id =  url.split("/")[-2]
             url =  "https://d26g5bnklkwsh4.cloudfront.net/" + id + "/master.m3u8"

            name1 = links[i][0].replace("\t", "").replace(":", "").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace("@", "").replace("*", "").replace(".", "").replace("https", "").replace("http", "").strip()
            name = f'{str(count).zfill(3)}) {name1[:60]}'

            if "youtu" in url:
                ytf = f"b[height<={raw_text2}][ext=mp4]/bv[height<={raw_text2}][ext=mp4]+ba[ext=m4a]/b[ext=mp4]"
            else:
                ytf = f"b[height<={raw_text2}]/bv[height<={raw_text2}]+ba/b/bv+ba"

            if "jw-prod" in url:
                cmd = f'yt-dlp -o "{name}.mp4" "{url}"'
            else:
                cmd = f'yt-dlp -f "{ytf}" "{url}" -o "{name}.mp4"'

            try:  
                
                cc = f'** {str(count).zfill(3)}.** {𝗻𝗮𝗺𝗲𝟭} {res}.mkv\n**Batch »** {b_name}\n\n{creditx}'
                cc1 = f'** {str(count).zfill(3)}.** {𝗻𝗮𝗺𝗲𝟭}.pdf \n**Batch »** {b_name}\n\n{creditx}'
                if "drive" in url:
                    try:
                        ka = await helper.download(url, name)
                        copy = await bot.send_document(chat_id=m.chat.id,document=ka, caption=cc1)
                        count+=1
                        os.remove(ka)
                        time.sleep(5)
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue
                
                elif ".pdf" in url:
                    try:
                        cmd = f'yt-dlp -o "{name}.pdf" "{url}"'
                        download_cmd = f"{cmd} -R 25 --fragment-retries 25"
                        os.system(download_cmd)
                        copy = await bot.send_document(chat_id=m.chat.id, document=f'{name}.pdf', caption=cc1)
                        count += 1
                        os.remove(f'{name}.pdf')
                        time.sleep(5)
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue
                else:
                    Show = f"**⥥ Downloading »**\n\n**Name »** `{name}\nQuality » {raw_text2}`\n\n**Url »** `{url}`"
                    prog = await m.reply_text(Show)
                    res_file = await helper.download_video(url, cmd, name)
                    filename = res_file
                    await prog.delete(True)
                    await helper.send_vid(bot, m, cc, filename, thumb, name, prog)
                    count += 1
                    time.sleep(20)

            except Exception as e:
                await m.reply_text(
                    f"**downloading Interupted **\n{str(e)}\n**Name** » {name}\n**Link** » `{url}`"
                )
                continue

    except Exception as e:
        await m.reply_text(e)
    await m.reply_text("Done ✅")

# Constants
defurl = "https://edge.api.brightcove.com/playback/v1/accounts/6206459123001/videos"
headers = {
    'authority': 'elearn.crwilladmin.com',
    'accept': 'application/json',
    'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
    'content-type': 'application/x-www-form-urlencoded',
    'origin': 'https://web.careerwill.com',
    'apptype': 'web',
    'expires': 'Mon, 26 Jul 1997 05',
    'referer': 'https://web.careerwill.com/',
    'user-agent': 'Gandi/5.0 (X11; Ubuntu; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0',
}

# Function to clean filename
def clean_filename(filename):
    invalid_chars = {':', '/', '“', '”'}
    for char in invalid_chars:
        filename = filename.replace(char, "_")
    return filename

# Function to get content
def get_content(batch_input, tid):
    fetched_contents = []
    try:
        topreq = f"https://elearn.crwilladmin.com/api/v5/batch-detail/{batch_input}?topicId={tid}"
        topres = requests.get(topreq, headers=headers).json()
        to_name = topres["data"]["class_list"]["batchName"]
        for lesson_data in reversed(topres["data"]["class_list"]["classes"]):
            lesson_name = lesson_data["lessonName"]
            lesson_id = lesson_data["id"]
            u6 = requests.get(f"https://elearn.crwilladmin.com/api/v5/class-detail/{lesson_id}", headers=headers)
            j6 = u6.json()
            lu = j6["data"]["class_detail"]["lessonUrl"]
            print(f"{lesson_name}{lesson_id}{lu}")
            if lu.startswith(("62", "63")):
                try:
                    surl = requests.get(f"https://elearn.crwilladmin.com/api/v5/livestreamToken?base=web&module=batch&type=brightcove&vid={lesson_id}", headers = headers)
                    livestream_url = f"{defurl}/{lu}/master.m3u8?bcov_auth={surl.json()['data']['token']}"
                    fetched_contents.append(f'{lesson_name}:{livestream_url}\n')
                except Exception as e:
                    print(f"Error obtaining livestream token: {str(e)}")
            else:
                youtube_url = f"https://www.youtube.com/embed/{lu}"
                fetched_contents.append(f'{lesson_name}:{youtube_url}\n')
    except KeyError:
        print("Can't get topics.")
    return fetched_contents

# Function to get batch topics
def get_batch_topics(batch_input, topic_type, headers):
    url = f"https://elearn.crwilladmin.com/api/v5/batch-topic/{batch_input}?type={topic_type}"
    return requests.get(url, headers=headers)

# Function to write content to file
def write_to_file(file, content):
    with open(file, 'a', encoding='utf-8') as f:
        f.write(content)

def count_video_urls(file):
    video_count = sum(1 for line in open(file) if "youtube.com" in line or "brightcove.com" in line)
    return video_count

# Command to trigger the login and batch fetching process
@bot.on_message(filters.command(["cw"]) & filters.chat(sudo_groups))
async def login_and_fetch_command_handler(client, message):
    try:
        credentials = await client.ask(message.chat.id, "Send your credentials in this format - email:password:")
        email, password = credentials.text.split(":")
        r = requests.post('https://elearn.crwilladmin.com/api/v5/login-other', headers=headers, data={'email': email, 'password': password}).json()
        token = r['data']['token']
        headers["token"] = f"{token}"
        batch_data = sorted(requests.get("https://elearn.crwilladmin.com/api/v5/my-batch", headers=headers).json()['data']['batchData'], key=lambda x: x['id'])
        batch_ids_list = [str(data['id']) for data in batch_data]
        batch_ids_str = ', '.join(batch_ids_list)
        batches_info = "\n".join(f"{data['id']} - {data['batchName']} By {data['instructorName']}" for data in batch_data)
        await message.reply(f'Token:\n{token}\n\nYou have these batches:\nBATCH-ID - BATCH NAME - INSTRUCTOR\n{batches_info}')

        batch_ids = await client.ask(message.chat.id, f"Now send the Batch IDs to Download\n\nSend like this 1,2,3,4 so on\nor copy paste or edit below IDs according to you:\n\n`\n{', '.join(str(data['id']) for data in batch_data)}\n`")

        batch_ids_list = [id.strip() for id in batch_ids.text.split(",")]
        if batch_ids_list:
            for batch_id in batch_ids_list:
                response = get_batch_topics(batch_id, "class", headers)
                bn = response.json()["data"]["batch_detail"]["name"]
                text_file = f'{clean_filename(bn)}.txt'
                with open(text_file, 'a', encoding='utf-8') as file:
                    for data in response.json()["data"]["batch_topic"]:
                        tid = data["id"]
                        if content := get_content(batch_id, tid):
                            file.writelines(content)

                response_notes = get_batch_topics(batch_id, "notes", headers)
                for data_notes in response_notes.json()["data"]["batch_topic"]:
                    tid_notes = data_notes["id"]
                    try:
                        notes_response = requests.get(f"https://elearn.crwilladmin.com/api/v5/batch-notes/{batch_id}?topicId={tid_notes}", headers=headers).json()
                        for doc_int in notes_response["data"]["notesDetails"]:
                            doc_title = doc_int["docTitle"]
                            doc_url = doc_int["docUrl"]
                            write_to_file(text_file, f"{doc_title}: {doc_url}\n")
                    except KeyError:
                        print("Can't get notes details.")

                video_count = count_video_urls(text_file)
                pdf_count = len([line for line in open(text_file) if line.endswith(".pdf\n")])

                caption = f"App Name: CareerWill\nBatch Name: `{bn}`\n\n🎬 Total Video: {video_count}\n📝 Total PDF: {pdf_count}"
                await client.send_document(message.chat.id, text_file, caption=caption)
                os.remove(text_file)
            await message.reply("✅ Done!")
        else:
            await message.reply("No batch IDs provided.")
    except Exception as e:
        await message.reply(f"Error: {str(e)}")


        
bot.run()
