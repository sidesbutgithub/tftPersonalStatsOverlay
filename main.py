import tkinter as tk
import requests
from dotenv import load_dotenv
import os

load_dotenv()

class Overlay:
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.geometry("+5+5")
        self.root.lift()
        self.root.wm_attributes("-topmost", True)

        

        self.frame = tk.Frame(self.root)
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)
        self.frame.rowconfigure(2, weight=2)
        self.frame.rowconfigure(3, weight=2)
        for i in range(20):
            self.frame.columnconfigure(i, weight = 1)

        self.name = tk.Label(self.frame, text= "TFT Stat Tracker")
        self.name.grid(row = 0, column = 0)

        self.regions = ("asia", "americas", "europe")
        self.options = tk.StringVar(value="americas")
        self.regionOptions = tk.OptionMenu(self.frame, self.options, *self.regions)
        self.regionOptions.config(height = 1, width = 8, font=('Arial', 10), relief='flat')
        self.regionOptions.grid(row=1, column=0, columnspan=4)

        self.playerName = tk.Text(self.frame, height=1, width = 20, font=('Arial', 10))
        self.playerName.grid(row=1, column=4, columnspan=10)

        self.playerTag = tk.Text(self.frame, height=1, width= 5, font=('Arial', 10))
        self.playerTag.grid(row=1, column=14, columnspan=2)


        self.frame.pack(fill='both')

        self.button = tk.Button(self.frame, text = "Submit", command=self.message)
        self.button.grid(row=1, column=16, columnspan=4)


        self.root.mainloop()

    async def getStats(self, region, playerID, playerTag):
        stats = await requests(f"http://{os.getenv('API_ADDRESS')}:{os.getenv('API_PORT')}/api/{region}/{playerID}/{playerTag}")
        self.last20 = stats.scores
        self.unitStats = stats.unitStats
        return
    
    def message(self):
        print(f"http://{os.getenv('API_ADDRESS')}:{os.getenv('API_PORT')}/api/{self.options.get()}/{(self.playerName.get('1.0', tk.END)).strip()}/{(self.playerTag.get('1.0', tk.END)).strip()}")
        
        return

Overlay()