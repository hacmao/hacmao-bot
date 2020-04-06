from common import * 
import dateutil.parser 
import datetime 
from tabulate import tabulate 

URL = "https://ctftime.org/event/list/upcoming"
ROOT_URL = "https://ctftime.org"

async def upcomming_events():
    """Get names and URL of all the past events.

    :return: dictionary having name and URLs of CTFs
    """
    past = {}
    soup = await make_soup(URL)
    trs = soup.find_all("tr")
    trs.pop(0)
    next_ctf = [] 
    headers = ["Name", "Url", "Date", "Length", "Weight", "People"] 
    msg = [] 

    for ind, ctf in enumerate(trs):
        if ind >= 10 : 
            break 
        # get ctf offical link 
        ctfd_link = ROOT_URL + ctf.find("a").get("href") 
        # soup = await make_soup(ctfd_link)
        # ctf_url = soup.find('a', attrs={'rel' : 'nofollow'}).get("href")
        
        ctf_name = ctf.find("a").text 
        table = ctf.find_all("td")[1:] 

        # format date 
        start_date, end_date = list(map(dateutil.parser.parse, table[0].text.split(" — ")))
        start_day = start_date.day 
        start_hour = start_date.hour 
        type_time = table[0].text.split(" — ")[0].split(" ")[-1]
        length = str((end_date.day - start_date.day) * 24 + (end_date.hour - start_date.hour)) + "h"
        if "UTC" in type_time :  
            if start_hour + 7 >= 24 : 
                start_day += 1 
            start_hour = (start_hour + 7) % 24  
            type_time = "" 
        else : 
            type_time = "ERROR"
        if ind > 7 : 
            break 
        ctf_date = "{0:0>2d}:{1.minute:0>2d}-{2:0>2d}-{1.month:0>2d}-{1.year} {3}".format(start_hour, start_date, start_day , type_time)
        ctf_format = table[1].text 
        if "Jeopardy" not in ctf_format  : 
            ctf_name += "<att-def>"  
        if len(ctf_name) > 20 : 
            ctf_name = ctf_name[:20] + "..."
        ctf_location = table[2].text.strip()
        if "On-line" not in ctf_location : 
            continue  
        ctf_weight = table[3].text 
        ctf_participate = table[5].text.split(" ")[12]  
        next_ctf.append([ctf_name, ctfd_link.replace("https://", ""), ctf_date, length, ctf_weight, ctf_participate])
        tmp = tabulate(next_ctf, headers, tablefmt="fancy_grid") 
        if len(tmp) >= 1994 : 
            tmp = tabulate(next_ctf[:-1], headers, tablefmt="fancy_grid") 
            msg.append("```" + tmp + "```") 
            next_ctf = [next_ctf[-1]]
    table = tabulate(next_ctf, headers, tablefmt="fancy_grid") 
    msg.append("```" + table + "```" )
    return msg

async def getCtfInfo(ctfd_link) : 
    headers = ["Name", "Url", "Date", "Weight", "Participant"] 

    soup = await make_soup(ctfd_link)
    ctf_url = soup.find('a', attrs={'rel' : 'nofollow'}).get("href")
    
    ctf_name = soup.find("h2").text
    # table = ctf.find_all("td")[1:] 
    info = soup.find_all("p") 
    ctf_time =info[0].text.strip()
    ctf_location = info[1].text.strip()
    ctf_format = info[4].text.strip()
    ctf_url = info[5].text.strip()
    ctf_weight = info[7].text.strip() 
    msg = """```
        ⛳ Name : {0}  
        ⌚ Time : {1}  
        🌎 Location : {2}
        🚩 {3}  
        📎  {4}  
        🎁 {5}
    ```""".format(ctf_name, ctf_time, ctf_location, ctf_format, ctf_url, ctf_weight)
    return msg

if __name__ == "__main__":
    LOOP = asyncio.get_event_loop()
    LOOP.run_until_complete(upcomming_events())