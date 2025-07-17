import tkinter as tk
import requests
from dotenv import load_dotenv
import os
import json
import asyncio

load_dotenv()

class Overlay:
    def __init__(self):
        self.root = tk.Tk()
        #self.root.overrideredirect(True)
        self.root.geometry("+5+5")
        self.root.lift()
        self.root.wm_attributes("-topmost", True)


        self.avp = tk.DoubleVar(value=1.0)

        self.frame = tk.Frame(self.root)
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)
        self.frame.rowconfigure(2, weight=1)
        self.frame.rowconfigure(3, weight=1)
        self.frame.rowconfigure(4, weight=1, uniform="yes")

        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        self.frame.columnconfigure(2, weight=1)
        self.frame.columnconfigure(3, weight=1)
        self.frame.columnconfigure(4, weight=1)

        tk.Label(self.frame, height = 1, text= "TFT Stat Tracker", font = ('Comic Sans MS', 10), anchor='w').grid(row = 0, column = 0, columnspan=5, sticky=tk.E+tk.W)

        tk.Label(self.frame, height=1, width=6, text="Region", font=('Comic Sans MS', 10), anchor='w').grid(row=1, column=0, sticky=tk.E+tk.W)
        tk.Label(self.frame, height=1, width=20, text="Player Name", font=('Comic Sans MS', 10), anchor='w').grid(row=1, column=1, columnspan=2, sticky=tk.E+tk.W)
        tk.Label(self.frame, height=1, width=6, text="Tag", font=('Comic Sans MS', 10), anchor='w').grid(row=1, column=3, columnspan=2, sticky=tk.E+tk.W)

        self.regions = ("asia", "americas", "europe")
        self.options = tk.StringVar(value="americas")
        self.regionOptions = tk.OptionMenu(self.frame, self.options, *self.regions)
        self.regionOptions.config(height = 1, width = 6, font=('Comic Sans MS', 10), relief='flat')
        self.regionOptions.grid(row=2, column=0, sticky=tk.E+tk.W)

        self.playerName = tk.Text(self.frame, height=1, width = 20, font=('Comic Sans MS', 10))
        self.playerName.grid(row=2, column=1, sticky=tk.E+tk.W)

        self.hashTag = tk.Label(self.frame, height=1, width=1, text="#", font=('Comic Sans MS', 10))
        self.hashTag.grid(row=2, column=2, sticky=tk.E+tk.W)

        self.playerTag = tk.Text(self.frame, height=1, width = 6, font=('Comic Sans MS', 10))
        self.playerTag.grid(row=2, column=3, sticky=tk.E+tk.W)


        self.button = tk.Button(self.frame, text = "Stats", command=lambda : asyncio.run(self.requestStats()))
        self.button.grid(row=2, column=4)



        tk.Label(self.frame, height = 1, text= "Last 20 Placements", font = ('Comic Sans MS', 10), anchor='w').grid(row = 3, column = 0, columnspan=4, sticky=tk.E+tk.W)

        tk.Label(self.frame, height = 1, text = "AVP", font = ('Comic Sans MS', 10), anchor='w').grid(row = 3, column = 4, sticky=tk.E+tk.W)

        self.placements = tk.StringVar(self.frame, ", ".join(["1" for i in range(20)]))


        tk.Label(self.frame, height = 1, textvariable = self.placements, font = ('Comic Sans MS', 10), anchor='w').grid(row = 4, column = 0, columnspan= 4, sticky=tk.E+tk.W)

        
        
        tk.Label(self.frame, height = 1, textvariable= self.avp, font = ('Comic Sans MS', 10), anchor='w').grid(row = 4, column = 4, sticky=tk.E+tk.W)

        self.frame.pack()
        self.root.mainloop()
    
    async def requestStats(self):
        requestString = f"http://{os.getenv('API_ADDRESS')}:{os.getenv('API_PORT')}/api/{self.options.get()}/{"%20".join(((self.playerName.get('1.0', tk.END)).strip()).split())}/{(self.playerTag.get('1.0', tk.END)).strip()}"
        res = await asyncio.to_thread(requests.get, requestString)
        stats = json.loads(res.text)
        scores = stats['scores']
        self.placements.set(", ".join([str(i) for i in scores]))
        self.avp.set(sum(scores)/len(scores))
        return
    

Overlay()