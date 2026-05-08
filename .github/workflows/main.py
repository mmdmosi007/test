import requests
from bs4 import BeautifulSoup
import threading
import time
import re
import sys
from time import gmtime, strftime

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.core.window import Window

Window.size = (400, 700)
now = strftime("%a, %d %b %Y %H:%M:%S ", gmtime())
say = f"\n\n\t\t Starting collection at\n\t\t\t {now}"





tos = "\n Connetion Time Out... \n"

class V2rayFinderApp(App):
    
    def build(self):

        self.running = False
        self.thread = None

        layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        self.status_label = Label(
            text="Status: Ready",
            size_hint_y=None,
            height=40
        )
        layout.add_widget(self.status_label)

        self.log_box = TextInput(
            text="Logs will appear here...\n",

            readonly=True,
            multiline=True
        )
        layout.add_widget(self.log_box)
        self.add_log(say)
        button_layout = BoxLayout(size_hint_y=None, height=60, spacing=10)

        self.start_button = Button(text="START")
        self.start_button.bind(on_press=self.start_scraping)

        self.stop_button = Button(text="STOP")
        self.stop_button.bind(on_press=self.stop_scraping)

        button_layout.add_widget(self.start_button)
        button_layout.add_widget(self.stop_button)

        layout.add_widget(button_layout)

        return layout

    # ---------------- START ----------------

    def start_scraping(self, instance):

        if self.running:
            return

        self.running = True
        self.status_label.text = "Status: Running..."
        self.thread = threading.Thread(target=self.scrape_loop)
        self.thread.start()
        print(say,"\n")

    # ---------------- STOP ----------------

    def stop_scraping(self, instance):

        self.running = False
        self.status_label.text = "Status: Stopped"

    # ---------------- MAIN SCRAPER ----------------

    def scrape_loop(self):
        all_configs = []
        add_log = []
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        channels = [
     "AR14N24b", "Airdorap_Free", "Alpha_V2ray_Group", "Alpha_V2ray_Iran", "AmyraxVPN", "AmyraxVPNGap", "AzadNet", "BlueShekan", "ChinaPortGFW",
     "ConfigX2ray", "DrovOne", "Echo_Center", "Farah_VPN", "Filtereshekan", "Fr33C0nfig", "Ln2Ray", "MaKVaslim", "MdVpnSec", "NETMelliAnti", "Oghab_VPN",
     "ProxyDotNet", "ProxyTelCo", "SaghiVpnX", "TEHRANARGO", "TweetPublic", "V2RAY_SPATIAL", "V2rayEnglish", "V2ray_Alpha", "VPNSupportGroup", "Vaslchi_VPN",
     "VpnMaan", "XpnTeam", "YamYamProxy", "anty_filter", "beshcan", "bored_vpn", "chat_nakone", "configraygan", "confing_proxi1", "cpy_teeL", "duckvp_n",
     "hormozvpn", "iHomeii", "internetmelil", "mehrosaboran", "meliproxyy", "mitivpn", "nufilter", "numb_frozen", "shankamil", "sogoandfuckyourlove", "tabiatvpn1",
     "v2FreeHub", "v2raygencon", "v2rayngvpn", "v2wray", "wallpaper_4k3d", "xsfilternet","Idasaturnm","p1ctok","Do1rcci","Mrx_Vpn","oliver_soul","v2rayngte"
     ]
        

        
        
        pattern = r"(?:vmess|vless|trojan|ss|ssr|hy2|tuic)://[a-zA-Z0-9\-_@.:?=&%#\/]+"


        while self.running:

            for channel in channels:

                if not self.running:
                    break

                url = f"https://t.me/s/{channel}"

                try:
                    self.add_log(f"\n Checking:  {channel}")

                    response = requests.get(url, headers=headers, timeout=15)

                    soup = BeautifulSoup(response.text, "html.parser")

                    messages = soup.find_all("div", class_="tgme_widget_message_text")

                    for msg in messages:
                        msg_content = str(msg)
                        configs = re.findall(pattern, msg_content)
                        all_configs.extend(configs)

                        if not self.running:
                            break

                        text = msg.get_text()

                        if "v2ray" in text.lower() or "vmess" in text.lower():

                            self.add_log(f"FOUND in {channel}:\n{text}\n")
                

                # except Exception as e:
                    # self.add_log(f"Error in {channel}: {e}")


                except Exception as e:
                    self.add_log(f" Error in {channel}: {tos}")
                    print("\n Connetion Time Out... \n")
                    # with open("log.txt", "w", encoding="utf-8") as f:
                        # f.write('\n'+tos)
                    logggs = f"\n Error in {channel}:\n {e}\n"
                    # with open("log.txt", "w", encoding="utf-8") as f:
                    #     for line in logggs:
                    #         f.write(line + "\n")    
                    # with open("log.txt", "w", encoding="utf-8") as f:
                    #     f.write(str(logges))
                    # log_file = open("log.txt", "a", encoding="utf-8")
                    # sys.stdout = log_file
                    # sys.stderr = log_file


        unique_configs = list(set(all_configs))
        print(f"\n\nFound {len(unique_configs)} unique recent configs.\n\n")

            
        with open("configs_recent.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(unique_configs))
        # with open("log.txt", "w", encoding="utf-8") as f:
        #     f.write("\n".join(add_log))

        self.add_log("Scraping stopped.")
        self.add_log(f"\n\nFound {len(unique_configs)} unique recent configs.\n\n")
    # ---------------- UI SAFE LOG ----------------

    def add_log(self, message):

        Clock.schedule_once(lambda dt: self.update_log(message))


    def update_log(self, message):

        self.log_box.text += message + "\n"
        self.log_box.cursor = (0, len(self.log_box.text))




if __name__ == "__main__":
    V2rayFinderApp().run()
    def get_recent():
        import sys

        class Logger:
            def __init__(self, filename):
                self.terminal = sys.stdout
                self.log = open(filename, "a", encoding="utf-8")

            def write(self, message):
                self.terminal.write(message)
                self.log.write(message)

            def flush(self):
                self.terminal.flush()
                self.log.flush()

        sys.stdout = Logger("program_output.txt")
        sys.stderr = sys.stdout

    print("Starting recent collection...")
    # بقیه کد...
