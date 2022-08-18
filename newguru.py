import feedparser
from tkinter import *
import pandas as pd
import webbrowser
import sv_ttk
from tkinter import ttk

# Use this to figure out how to not have the exe recognized as a false positive

def get_news():
    global news_df
    global dict
    dict = {'Game Informer': ['https://www.gameinformer.com/rss.xml'],
            'Polygon': ['https://www.polygon.com/rss/index.xml'],
            'IGN': ['http://feeds.feedburner.com/ign/all'],
            'PC Gamer': ['https://www.pcgamer.com/rss/']}

    feed = feedparser.parse(dict[var.get()][0])

    print(var.get())
    news_dict = {"Title":[],
                 "Summary":[],
                 "Link":[],
                 "Date":[]}

    for entry in feed.entries:
        news_dict['Title'] += [entry.title]
        news_dict['Summary'] += [entry.summary]
        news_dict['Link'] += [entry.link]
        # news_dict['Date'] += ["".join(entry.published.split(" ")[1:3])]
        news_dict['Date'] += [entry.published]

    news_df = pd.DataFrame(news_dict)
    news_df['Date'] = pd.to_datetime(news_df['Date'])
    news_df = news_df.sort_values(by='Date', ascending=False).reset_index()
    news_df['Date'] = news_df['Date'].dt.strftime('%d-%m-%y')

    list1.delete(0, END)
    for i in range(len(news_df)):
        list1.insert(END, f"{news_df['Date'][i]} {news_df['Title'][i]}")

def open_browser(event):
    i = list1.curselection()[0]
    webbrowser.open(news_df['Link'][i])

w = Tk()
w.title('News Guru')
w.geometry("925x540")
sv_ttk.use_dark_theme()
# https://stackoverflow.com/questions/45441885/how-can-i-create-a-dropdown-menu-from-a-list-in-tkinter
# Option Menu Guide
options = ['Game Informer', 'Polygon', 'IGN', 'PC Gamer']
var = StringVar(w)
var.set(options[0])
menu = OptionMenu(w, var, *options)
menu.grid(row=0, column=2)

list1 = Listbox(w, height=30, width=150)
list1.grid(row=1, column=0, columnspan=10)

sb1 = Scrollbar(w)
sb1.grid(row=1, column=11)
list1.configure(yscrollcommand=sb1.set)
sb1.configure(command=list1.yview)
list1.bind('<<ListboxSelect>>', open_browser)

b1 = Button(w, text="Get News", width=10, height=1, command=get_news)
b1.grid(row=0, column=8)

w.mainloop()
