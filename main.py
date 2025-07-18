import tkinter as tk
import requests
from dotenv import load_dotenv
import os
import json
import threading

load_dotenv()

class Overlay:
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.geometry("+5+5")
        self.root.lift()
        self.root.wm_attributes("-topmost", True)
        self.root.attributes('-alpha', 0.85)

        self.windowFrame = tk.Frame(self.root)
        self.windowFrame.columnconfigure(0, weight = 1)
        self.windowFrame.columnconfigure(1, weight = 1)

        self.avp = tk.DoubleVar(value=1.0)

        self.frame = tk.Frame(self.windowFrame)
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)
        self.frame.rowconfigure(2, weight=1)
        self.frame.rowconfigure(3, weight=1)
        self.frame.rowconfigure(4, weight=1)

        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        self.frame.columnconfigure(2, weight=1)
        self.frame.columnconfigure(3, weight=1)
        self.frame.columnconfigure(4, weight=1)

        tk.Label(self.frame, height = 1, text= "TFT Stat Tracker", font = ('Comic Sans MS', 10), anchor='w').grid(row = 0, column = 0, columnspan=5, sticky=tk.NSEW)

        tk.Label(self.frame, height=1, width=6, text="Region", font=('Comic Sans MS', 10), anchor='w').grid(row=1, column=0, sticky=tk.NSEW)
        tk.Label(self.frame, height=1, width=20, text="Player Name", font=('Comic Sans MS', 10), anchor='w').grid(row=1, column=1, columnspan=2, sticky=tk.NSEW)
        tk.Label(self.frame, height=1, width=6, text="Tag", font=('Comic Sans MS', 10), anchor='w').grid(row=1, column=3, columnspan=2, sticky=tk.NSEW)

        self.regions = ("asia", "americas", "europe")
        self.options = tk.StringVar(value="americas")
        self.regionOptions = tk.OptionMenu(self.frame, self.options, *self.regions)
        self.regionOptions.config(height = 1, width = 6, font=('Comic Sans MS', 8), relief='flat')
        self.regionOptions.grid(row=2, column=0, sticky=tk.NSEW)

        self.playerName = tk.Text(self.frame, height=1, width = 20, font=('Comic Sans MS', 8))
        self.playerName.grid(row=2, column=1, sticky=tk.NSEW)

        self.hashTag = tk.Label(self.frame, height=1, width=1, text="#", font=('Comic Sans MS', 10))
        self.hashTag.grid(row=2, column=2, sticky=tk.NSEW)

        self.playerTag = tk.Text(self.frame, height=1, width = 6, font=('Comic Sans MS', 10))
        self.playerTag.grid(row=2, column=3, sticky=tk.NSEW)


        self.button = tk.Button(self.frame, text = "Stats", command=self.statsButton)
        self.button.grid(row=2, column=4)

        self.button = tk.Button(self.frame, text = "Quit", command=self.root.destroy)
        self.button.grid(row=0, column=4)


        tk.Label(self.frame, height = 1, text= "Last 20 Placements", font = ('Comic Sans MS', 10), anchor='w').grid(row = 3, column = 0, columnspan=4, sticky=tk.NSEW)

        tk.Label(self.frame, height = 1, text = "AVP", font = ('Comic Sans MS', 10), anchor='w').grid(row = 3, column = 4, sticky=tk.NSEW)

        self.placements = tk.StringVar(self.frame, ", ".join(["1" for i in range(20)]))


        tk.Label(self.frame, height = 1, textvariable = self.placements, font = ('Comic Sans MS', 10), anchor='w').grid(row = 4, column = 0, columnspan= 4, sticky=tk.NSEW)
        tk.Label(self.frame, height = 1, textvariable= self.avp, font = ('Comic Sans MS', 10), anchor='w').grid(row = 4, column = 4, sticky=tk.NSEW)

        self.unitFrame = tk.Frame(self.windowFrame)
        self.unitFrame.columnconfigure(0, weight=1)
        self.unitFrame.columnconfigure(1, weight=1)
        self.unitFrame.columnconfigure(2, weight=1)
        self.unitFrame.columnconfigure(3, weight=1)
        tk.Label(self.unitFrame, height = 1, text="Most Played", font = ('Comic Sans MS', 10), anchor='w').grid(row = 0, column = 0, columnspan= 2, sticky=tk.NSEW)
        tk.Label(self.unitFrame, height = 1, text="Best AVP", font = ('Comic Sans MS', 10), anchor='w').grid(row = 0, column = 2, columnspan= 2, sticky=tk.NSEW)
        self.mostPlayed = [tk.StringVar(self.unitFrame, "No Stats Yet") for i in range(3)]
        self.gamesPlayed = [tk.IntVar(self.unitFrame, 0) for i in range(3)]
        self.bestAvp = [tk.StringVar(self.unitFrame, "No Stats Yet") for i in range(3)]
        self.unitAvp = [tk.IntVar(self.unitFrame, 0) for i in range(3)]
        for i in range(3):
            tk.Label(self.unitFrame, textvariable=self.mostPlayed[i], font = ('Comic Sans MS', 8), anchor='w').grid(row = 1+i, column = 0, sticky=tk.NSEW)
            tk.Label(self.unitFrame, textvariable=self.gamesPlayed[i], font = ('Comic Sans MS', 8), anchor='w').grid(row = 1+i, column = 1, sticky=tk.NSEW)
            tk.Label(self.unitFrame, textvariable=self.bestAvp[i], font = ('Comic Sans MS', 8), anchor='w').grid(row = 1+i, column = 2, sticky=tk.NSEW)
            tk.Label(self.unitFrame, textvariable=self.unitAvp[i], font = ('Comic Sans MS', 8), anchor='w').grid(row = 1+i, column = 3, sticky=tk.NSEW)


        self.frame.grid(row = 0, column = 0)
        self.unitFrame.grid(row = 0, column = 1)
        self.windowFrame.pack(fill='both')
        self.root.mainloop()
    
    def statsButton(self):
        self.placements.set("updating")
        self.avp.set(0.0)
        for i in range(3):
            self.mostPlayed[i].set("No Stats Yet")
            self.gamesPlayed[i].set("0")
            self.bestAvp[i].set("No Stats Yet")
            self.unitAvp[i].set("0")
        threading.Thread(target=self.requestStats).start()


    def requestStats(self):
        requestString = f"http://{os.getenv('API_ADDRESS')}:{os.getenv('API_PORT')}/api/{self.options.get()}/{"%20".join(((self.playerName.get('1.0', tk.END)).strip()).split())}/{(self.playerTag.get('1.0', tk.END)).strip()}"
        res = requests.get(requestString)
        stats = json.loads(res.text)
        scores = stats['scores']
        units = stats['units']
        print(units)
        unitsSorted = sorted(units.items(), key=lambda x: -x[1]["games"])
        unitsAVP = sorted(units.items(), key=lambda x: x[1]["totalPlacement"]/x[1]["games"])

        self.root.after(0, self.updatePlayerStats, ", ".join([str(i) for i in scores]), sum(scores)/len(scores))
        self.root.after(0, self.updateMostPlayed, unitsSorted)
        self.root.after(0, self.updateUnitAvp, unitsAVP)

        return
    
    def updatePlayerStats(self, scores, avp):
        self.placements.set(scores)
        self.avp.set(avp)

    def updateMostPlayed(self, unitStats):
        for i in range(3):
            if i == len(unitStats):
                return
            self.mostPlayed[i].set(unitStats[i][0])
            self.gamesPlayed[i].set(unitStats[i][1]["games"])
    
    def updateUnitAvp(self, unitsAVP):
        for i in range(3):
            if i == len(unitsAVP):
                return
            self.bestAvp[i].set(unitsAVP[i][0])
            self.unitAvp[i].set(unitsAVP[i][1]["totalPlacement"]/unitsAVP[i][1]["games"])


    

Overlay()