import json
import os
import datetime
from PIL import Image,ImageDraw,ImageFont
from gi.repository import Gio

class tasks:
    tasks = []
    def add(self,message,date,urg_imp):
        task = {}
        task["message"] = message
        task["date"] = date
        task["urg/imp"] = urg_imp
        task["done"] = False
        self.tasks.append(task)

    def show(self,full_list=True,partial_list=None):
        if full_list:
            t = self.tasks
        else:
            t = partial_list
        for task in t:
            for key,value in task.items():
                print(f'{key}: {value}')
            print(' ')

    def empty(self):
        self.tasks = []

    def sort(self,key="urg/imp"):
        k = lambda x: x[key]
        self.tasks = sorted(self.tasks,key = k)

    def search(self,key,value):
        t = []
        for task in self.tasks:
            if task[key] == value:
                t.append(task)
        return t

    def keyword_search(self,keyword):
        t = []
        for task in self.tasks:
            if keyword in task["message"]:
                t.append(task)
        return t

    def save(self,out_file='to-do-list-data.json'):
        print(f'saving to {out_file}')
        data = {"to-do-list":self.tasks}
        with open(out_file,'w') as f:
            json.dump(data,f,indent = 4,default=str)

    def load(self,in_file ='to-do-list-data.json'):
        print(f'loading from {in_file}')
        with open(in_file) as f:
            self.tasks = json.load(f)["to-do-list"]
            for task in self.tasks:
                date = task["date"]
                year,month,day = date.split('-')
                task["date"] = datetime.date(int(year),int(month),int(day))

    #returns the path to the current wallpaper
    #utility for update_wallpaper
    def get_wallpaper(self):
        settings = Gio.Settings.new("org.gnome.desktop.background")
        uri = settings.get_string("picture-uri")

        if 'file' in uri:
            path =  uri.strip('file')[3:]
        else:
            with open('orig_wallpaper.txt') as f:
                path = f.read()

        with open('orig_wallpaper.txt','w') as f:
            f.write(str(path))

        return path

    #update wallpaper to given wallpaper
    def update_wallpaper(self):
        tasks = self.tasks
        final_img = self.make_img_from_list()
        final_img.save('final.png')
        path = os.getcwd() + '/final.png'
        os.system(f'/usr/bin/gsettings set org.gnome.desktop.background picture-uri {path}')
        #os.system('/usr/bin/gsettings set org.gnome.desktop.background picture-uri /home/manan/acm/summers-SIG-2018/Python-Scripts/To-do-list/final.png')

    #sets up the tasks on the current wallpaper
    #utility for update_wallpaper
    def set_up(self,wallpaper):
        tasks = self.tasks
        midx = int(round(wallpaper.size[0]/2,0))
        num = len(tasks)
        height = wallpaper.size[1]
        margin = 50
        txt_margin = 20

        #positions of all messages
        #leave one extra empty space (if last message is very long)
        pos = [i*height/num for i in range(num+2)]
        last = pos[-1]
        #del pos[-1]
        pos = [p + (height-last)/2 for p in pos]
        #print(pos1)

        # make a blank image for the text, initialized to transparent text color
        txt = Image.new('RGBA', wallpaper.size, (255,255,255,0))
        # get a font
        fnt = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 40)
        f1_size = 75
        fnt1 = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', f1_size)
        # get a drawing context
        draw = ImageDraw.Draw(txt)

        #draw rectangle to the right of the desktop
        draw.rectangle(((midx,margin), (wallpaper.size[0] - margin, wallpaper.size[1] - margin)), fill=(0,0,0,128))

        #write headers - urgent / important
        draw.text(( wallpaper.size[0] - 5*f1_size, margin), "Urgent", font=fnt1, fill=(255,0,0,255))
        draw.text(( wallpaper.size[0] - 6*f1_size, wallpaper.size[1] - margin - f1_size), "Important", font=fnt1, fill=(255,255,0,255))

        #write tasks
        for i in range(len(tasks)):
            #text goes beyond ending - wrap text
            if midx + txt_margin + fnt.getsize(tasks[i]["message"])[0] > wallpaper.size[0] - margin:
                l = len(tasks[i]["message"])
                c = fnt.getsize(tasks[i]["message"])[1]
                lst = tasks[i]["message"].split(' ')
                count = 0
                #break text into smaller pieces to fit in screen
                #until list with words is not empty
                while lst != []:
                    end = len(lst)
                    for l in lst:
                        if midx + txt_margin + fnt.getsize(' '.join(lst[:lst.index(l)]))[0] > wallpaper.size[0] - margin:
                            end = lst.index(l)-1
                            break
                    #write the chosen text
                    draw.text((midx+txt_margin,pos[i]+c*count), ' '.join(lst[:end]), font=fnt, fill=(255,255,255,255))
                    #delete text that has been written and continue
                    del lst[:end]
                    count+=1
            #only one line for this task
            else:
                draw.text((midx+txt_margin,pos[i]), tasks[i]["message"], font=fnt, fill=(255,255,255,255))

        out = Image.alpha_composite(wallpaper, txt)
        return out

    #utility for update_wallpaper
    def make_img_from_list(self):
        tasks = self.tasks
        #get the wallpaper image in RGBA format
        wallpaper = Image.open(self.get_wallpaper()).convert('RGBA')

        #add to-do list on top of the wallpaper
        new_wallpaper = self.set_up(wallpaper)

        return new_wallpaper