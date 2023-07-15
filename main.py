import utils as u
import re
from tools import *
import asyncio
# Push from terminal from a second user
# git config --local credential.helper ""


def main():
    asyncio.run(export_messages())
    

async def export_messages(export_file = "base.txt"):
    
        channel_dict = dict()  # {channel_id: channel_name}
        
        try:
            contenido = scraper()
            cleansed_content = cleanse_message(contenido)
            channel_dict = update_channel_dict(cleansed_content, channel_dict)
        except Exception as e:
            print("exportMessages : ERROR :", e)
            sys.exit(1)
            
        export_channels(channel_dict, export_file)
    
  
def cleanse_message(message_content):
    
    cleansed_content = ""
    rows = [row for row in message_content.split("\n") if len(row.strip()) > 0]
    channel_id_regex = r'[a-zA-Z0-9]{40}'
    
    if re.search(channel_id_regex, message_content):
        for i, row in enumerate(rows):
            if re.search(channel_id_regex, row):
                if i > 0:
                  cleansed_content += rows[i-1] + "\n" + row + "\n"
                else:
                  cleansed_content += "UNTITLED CHANNEL" + "\n" + row + "\n"
                
    return cleansed_content


def update_channel_dict(message_content, channel_dict):
    
    rows = message_content.split("\n")
    
    for i, row in enumerate(rows):
        if i % 2 == 1:
            channel_id = row
            channel_name = rows[i-1]
            if "DAZN F1 1080" in channel_name:
                channel_name = "DAZN F1 1080"
            elif "DAZN F1 720" in channel_name:
                channel_name = "DAZN F1 720"
            elif "SmartBanck" in channel_name:
                channel_name = channel_name.replace("SmartBanck", "Smartbank")
            elif "La1" in channel_name:
                channel_name = channel_name.replace("La1", "La 1")
            elif "LA 1" in channel_name:
                channel_name = channel_name.replace("LA 1", "La 1")
            elif "Tv" in channel_name:
                channel_name = channel_name.replace("Tv", "TV")
            elif "#0 de Movistar" in channel_name:
                channel_name = channel_name.replace("#0 de Movistar", "#0 M+ HD")
            elif "BarÃ§a" in channel_name:
                channel_name = channel_name.replace("BarÃ§a", "Barça")
            elif "beIN SPORTS Ã±" in channel_name:
                channel_name = channel_name.replace("beIN SPORTS Ã±", "beIN SPORTS ñ")
            elif "Golf" in channel_name:
                if "mex" in channel_name:
                    channel_name = channel_name.replace("mex", "Channel")
            #elif "M.L. Campeones" in channel_name:
                #channel_name = channel_name.replace("M.L. Campeones", "M+ Liga de Campeones")
            #elif "#Vamos" in channel_name:
                #channel_name = channel_name.replace("#Vamos", "M+ #Vamos")
                
            channel_dict[channel_id] = channel_name
            
    return channel_dict


def export_channels(channel_dict, export_file):
    
    channel_list = []
    
    for channel_id, channel_name in channel_dict.items():
        group_title = u.extract_group_title(channel_name)
        tvg_id = u.extract_tvg_id(channel_name)
        logo = u.get_logo(tvg_id)
        identif = (channel_id[0:4])
        channel_info = {"group_title": group_title,
                        "tvg_id": tvg_id,
                        "logo": logo,
                        "channel_id": channel_id,
                        "channel_name": channel_name + "  " + identif}
        channel_list.append(channel_info)

    # CANALES AÑADIDOS FUERA DE elcano
    channel_list.append({'group_title': 'DAZN F1', 'tvg_id': '','logo': 'https://d1yjjnpx0p53s8.cloudfront.net/styles/logo-thumbnail/s3/012018/untitled-1_20.png?An9Fa1zRO4z6Dj__EVR4da6YOWsvtEw2&itok=6PiLMTa5', 'channel_id': 'https://www.f1-tempo.com/', 'channel_name': 'F1 Tempo Telemetría'})
    #channel_list.append({'group_title': 'logo': 'https://i.imgur.com/U4w7Bgy.png', 'channel_id': '78aa81aedb1e2b6a9ba178398148940857155f6a', 'channel_name': 'Wimbledon UHD by Jonatan'})
    channel_list.append({'group_title': 'electroperra', 'tvg_id': 'HISTORIA', 'logo': 'https://www.movistarplus.es/recorte/m-NEO/canal/HIST.png', 'channel_id': 'http://mol-2.com:8080/play/live.php?mac=00:1A:79:C3:AF:36&stream=55609&extension=ts&play_token=ltn2GgE1z6', 'channel_name': 'Historia'})
    channel_list.append({'group_title': 'electroperra', 'tvg_id': 'NAT GEO WILD HD', 'logo': 'https://www.movistarplus.es/recorte/m-NEO/canal/NATGW.png', 'channel_id': 'http://mol-2.com:8080/play/live.php?mac=00:1A:79:C3:AF:36&stream=55611&extension=ts&play_token=ltn2GgE1z6', 'channel_name': 'Nat Geo Wild'})
    channel_list.append({'group_title': 'electroperra', 'tvg_id': 'NAT GEO HD', 'logo': 'https://www.movistarplus.es/recorte/m-NEO/canal/NATGEO.png', 'channel_id': 'http://mol-2.com:8080/play/live.php?mac=00:1A:79:C3:AF:36&stream=55613&extension=ts&play_token=ltn2GgE1z6', 'channel_name': 'National Geographic'})

    all_channels = ""
    all_channels += '#EXTM3U url-tvg="https://raw.githubusercontent.com/davidmuma/EPG_dobleM/master/guia.xml, https://raw.githubusercontent.com/acidjesuz/EPG/master/guide.xml"\n'
    #all_channels += '#EXTINF:-1 tvg-logo="https://logodownload.org/wp-content/uploads/2017/11/telegram-logo-0-2.png" ,HACKS LOVE + ROBOTS\nhttps://t.me/+__T5lqenMkcwMzdk\n'
    
    channel_pattern = '#EXTINF:-1 group-title="GROUPTITLE" tvg-id="TVGID" tvg-logo="LOGO" ,CHANNELTITLE\nacestream://CHANNELID\n'
    channel_pattern_http = '#EXTINF:-1 group-title="GROUPTITLE" tvg-id="TVGID" tvg-logo="LOGO" ,CHANNELTITLE\nCHANNELID\n'

    for group_title in u.group_title_order:
        for channel_info in channel_list:
            if channel_info["group_title"] == group_title:
                if "http" in channel_info["channel_id"]:
                    ch_pattern = channel_pattern_http
                else:
                    ch_pattern = channel_pattern
                channel = ch_pattern.replace("GROUPTITLE", channel_info["group_title"]) \
                                               .replace("TVGID", channel_info["tvg_id"]) \
                                               .replace("LOGO", channel_info["logo"]) \
                                               .replace("CHANNELID", channel_info["channel_id"]) \
                                               .replace("CHANNELTITLE", channel_info["channel_name"])
                all_channels += channel

    if all_channels != "":
        
        all_channels_kodi = all_channels.replace("acestream://", "plugin://script.module.horus?action=play&id=")
        all_channels_get = all_channels.replace("acestream://", "http://127.0.0.1:6878/ace/getstream?id=")
        all_channels_int = all_channels.replace("acestream://", "http://192.168.1.90:8008/ace/getstream?id=")



        with open(export_file, "w") as f:
            f.write(all_channels)
            print("exportChannels : OK : list exported to Github")
            f.close()

        with open("kodi.txt", "w") as k:
            k.write(all_channels_kodi)
            print("exportChannels : OK : kodi list exported to Github")
            k.close()

        with open("get.txt", "w") as g:
            g.write(all_channels_get)
            print("exportChannels : OK : get list exported to Github")
            g.close()
            
        with open("int.txt", "w") as int:
            int.write(all_channels_int)
            print("exportChannels : OK : int list exported to Github")
            int.close()
            
    else:
        print("exportChannels : ERROR : list is empty")
        

if __name__ == "__main__":
    main()
    #gitUpdate()
