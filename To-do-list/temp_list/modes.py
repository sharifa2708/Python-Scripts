import random
import os
import pprint
from PIL import Image,ImageDraw,ImageFont
from gi.repository import Gio

#returns the path to the current wallpaper
#utility for update_wallpaper
def get_wallpaper():
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
def update_wallpaper(tasks):
    final_img = make_img_from_list(tasks)
    final_img.save('temp.png')
    path = os.getcwd() + '/temp.png'
    #os.system(f'/usr/bin/gsettings set org.gnome.desktop.background picture-uri {path}')

#sets up the tasks on the current wallpaper
#utility for update_wallpaper
def set_up_1(tasks,wallpaper):
    midx = int(round(wallpaper.size[0]/2,0))
    num = len(tasks)
    height = wallpaper.size[1]
    margin = 50
    txt_margin = 20

    #positions of all messages
    #leave one extra empty space (if last message is very long)
    pos = [i*height/(num+1) for i in range(num+1)]
    last = pos[-1]
    pos = [p + (height-last)/2 for p in pos]

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

#sets up the tasks on the current wallpaper
#utility for update_wallpaper
def set_up_2(tasks,wallpaper):
    midx = int(round(wallpaper.size[0]/2,0))
    num = len(tasks)
    height = wallpaper.size[1]
    margin = 50
    txt_margin = 20

    #positions of all messages
    #leave one extra empty space (if last message is very long)
    pos = [i*height/(num+1) for i in range(num+1)]
    last = pos[-1]
    pos = [p + (height-last)/2 for p in pos]

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
                #cut text if it is 'done'        
                if tasks[i]["done"] is True:
                    draw.line((midx+txt_margin,pos[i]+c*count+fnt.getsize(tasks[i]["message"])[1]/2,midx+txt_margin+fnt.getsize(' '.join(lst[:lst.index(l)-1]))[0],pos[i]+c*count+fnt.getsize(tasks[i]["message"])[1]/2),width=6,fill="white")
                #write the chosen text
                draw.text((midx+txt_margin,pos[i]+c*count), ' '.join(lst[:end]), font=fnt, fill=(255,255,255,255))
                #delete text that has been written and continue
                del lst[:end]
                count+=1
        #only one line for this task
        else:
            if tasks[i]["done"] is True:
                draw.line((midx+txt_margin,pos[i]+fnt.getsize(tasks[i]["message"])[1]/2,midx+txt_margin+fnt.getsize(tasks[i]["message"])[0],pos[i]+fnt.getsize(tasks[i]["message"])[1]/2),width=6,fill="white")
            draw.text((midx+txt_margin,pos[i]), tasks[i]["message"], font=fnt, fill=(255,255,255,255))

    out = Image.alpha_composite(wallpaper, txt)
    return out

#utility for update_wallpaper
def make_img_from_list(tasks):
    #get the wallpaper image in RGBA format
    wallpaper = Image.open(get_wallpaper()).convert('RGBA')

    #add to-do list on top of the wallpaper
    new_wallpaper = set_up_2(tasks,wallpaper)

    return new_wallpaper


if __name__ == '__main__':
    #sample tasks
    tasks = []
    for i in range(10):
        urg = random.randint(1,10)
        imp = random.randint(1,10)
        urg_imp = round(urg/imp,2)
        if i is 5:
            tasks.append({ 'message':f'sample {i+1} compulsory long message to check comaptibility with other piece of code', 'urg':urg, 'imp':imp, 'urg_imp':urg_imp, 'done':random.choice([True,False])  })
        else:
            tasks.append({ 'message':f'sample {i+1}', 'urg':urg, 'imp':imp, 'urg_imp':urg_imp, 'done':True  })
    pprint.pprint(tasks)

update_wallpaper(tasks)
