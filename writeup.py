from common import * 
import dateutil.parser 
import datetime 
from tabulate import tabulate
import re 

URL = "https://ctftime.org/event/list/upcoming"
ROOT_URL = "https://ctftime.org" 

async def original_writeups(link):
    """Get all the information about events along with
       link to original writeups

    :link: A URL to the tasks of a CTF

    :return: Information about the all the task along with URL
             to original writeups in tabulated form
    """
    msg = []
    info = []
    headers = ["S.no", "Name", "Points", "tags", "URL"]
    soup = await make_soup(link)
    trs = soup.findAll("tr")

    # For getting tasks links
    for ind, tr in enumerate(trs[1:], start=1):
        rated = {}
        gen = tr.text.split("\n")

        # Check if writeup exists or not
        if gen[-1] == str(0):
            continue
        
        columns = tr.findAll("td") 
        url = "ctftime.org" + columns[0].find('a').get("href") 
        name = columns[0].text 
        if len(name) > 20 : 
            name = name[:18] + "..."
        point = columns[1].text 
        tags = ""
        for tag in columns[2].findAll("span") : 
            tags += tag.text + ","

        if len(tags) > 15 : 
            tags = tags[:15] + " ..." 
        info.append([ind, name, point, tags, url])
        tmp = tabulate(info, headers, tablefmt="fancy_grid") 
        if len(tmp) >= 1994 : 
            tmp = tabulate(info[:-1], headers, tablefmt="fancy_grid") 
            msg.append("```" + tmp + "```") 
            info = [info[-1]]
    
    table = tabulate(info, headers, tablefmt="fancy_grid") 
    msg.append("```" + table + "```" )
    return msg


async def original_writeups_tag(link, ortag):
    """Get all the information about events along with
       link to original writeups

    :link: A URL to the tasks of a CTF

    :return: Information about the all the task along with URL
             to original writeups in tabulated form
    """
    msg = []
    info = []
    headers = ["S.no", "Name", "Points", "tags", "URL"]
    soup = await make_soup(link)
    trs = soup.findAll("tr")

    # For getting tasks links
    for ind, tr in enumerate(trs[1:], start=1):
        rated = {}
        gen = tr.text.split("\n")

        # Check if writeup exists or not
        if gen[-1] == str(0):
            continue
        
        columns = tr.findAll("td") 
        url = "ctftime.org" + columns[0].find('a').get("href") 
        name = columns[0].text 
        if len(name) > 20 : 
            name = name[:18] + "..."
        point = columns[1].text 
        tags = ""
        for tag in columns[2].findAll("span") : 
            tags += tag.text + ","
        if ortag not in tags : 
            continue 
        if len(tags) > 15 : 
            tags = tags[:15] + " ..." 
        info.append([ind, name, point, tags, url])
        tmp = tabulate(info, headers, tablefmt="fancy_grid") 
        if len(tmp) >= 1994 : 
            tmp = tabulate(info[:-1], headers, tablefmt="fancy_grid") 
            msg.append("```" + tmp + "```") 
            info = [info[-1]]
    
    table = tabulate(info, headers, tablefmt="fancy_grid") 
    msg.append("```" + table + "```" )
    return msg


if __name__ == "__main__" : 
    link = "https://ctftime.org/event/1032/tasks/" 
    LOOP = asyncio.get_event_loop()
    LOOP.run_until_complete(original_writeups(link))
