#!/bin/python 
import curses, curses.textpad

screen = curses.initscr()
curses.nonl()
curses.start_color()
def maketextbox(h,w,y,x,value="",deco=None,underlineChr=curses.ACS_HLINE,textColorpair=0,decoColorpair=0):
    nw = curses.newwin(h,w,y,x)
    txtbox = curses.textpad.Textbox(nw)
    if deco=="frame":
        screen.attron(decoColorpair)
        curses.textpad.rectangle(screen,y-1,x-1,y+h,x+w)
        screen.attroff(decoColorpair)
    elif deco=="underline":
        screen.hline(y+1,x,underlineChr,w,decoColorpair)

    nw.addstr(0,0,value,textColorpair)
    nw.attron(textColorpair)
    screen.refresh()
    return txtbox

foo = maketextbox(1,40, 10,20,"foo",deco="underline",textColorpair=curses.color_pair(0),decoColorpair=curses.color_pair(1))
text = foo.edit()
print(text)
