

import matplotlib.pyplot as plt
import numpy as np, math as Math
from math import pi as PI
from collections import namedtuple

class ease_funs():
    def __init__(self) -> None:
        self.clear =True
        self.xrange_start = 0
        self.xrange_end = 1
        self.yrange_start = 0
        self.yrange_end = 1
        self.cur_fun= None
        self.prev_fun = None
        self.proportion = True
        self.opposite = False

        #plt.style.use('dark_background')
        if __name__ == "__main__":
            self.ax = plt.subplot(111)
            self.box = self.ax.get_position()

        self.function_l = ["easeInSine",  "easeInCubic",  "easeInQuint",  "easeInCirc",  "easeInElastic",  "easeInQuad",  "easeInQuart",  "easeInExpo",  "easeInBack",  "easeInBounce",  
"easeOutSine",  "easeOutCubic",  "easeOutQuint",  "easeOutCirc",  "easeOutElastic",  "easeOutQuad",  "easeOutQuart",  "easeOutExpo",  "easeOutBack",  "easeOutBounce",  "easeInOutSine",  "easeInOutCubic",  "easeInOutQuint",  "easeInOutCirc",  "easeInOutElastic",  "easeInOutQuad",  "easeInOutQuart",  "easeInOutExpo",  "easeInOutBack",  "easeInOutBounce"]
        #self.pre_made_funs = {}
        line = namedtuple("line", "line opposite")
        for i, f in enumerate(self.function_l):
            ll_op =None
            ll = self.get_line(getattr(self, f))
            if i < 10: 
                ll_op =  self.get_line(getattr(self, self.function_l[i+10])) # self.get_mirror_fun(ll)
            elif i < 20: 
                ll_op =  self.get_line(getattr(self, self.function_l[i-10])) 
            else: 
                ll_op = ll
            #print(ll)
            #print(ll_op)
            setattr(self, f+"_yline", line(ll, ll_op))
                    
            #self.pre_made_funs[f] = self.get_line(getattr(self, f))
        #xx, yy = self.get_range_spline(self.easeOutBack_yline, 0.4, 1.7, 0.3, 1.3)
        # plt.plot(xx, yy, "r", label="test")
        
        # plt.title('Graph')
        # plt.xlabel('x', color='#1C2833')
        # plt.ylabel('y', color='#1C2833')
        # plt.legend(loc='upper center')
        
        # plt.grid()
        # plt.show()
        # for i, elem in enumerate(yy):
        #     print(xx[i], yy[i])

    def get_range_spline(self, fun_points, xrange_start, xrange_end, yrange_start, yrange_end):
        xx = np.linspace(xrange_start,xrange_end,100)
        yy = np.linspace(yrange_start,yrange_end,100)
        for i, elem in enumerate(yy):
            yy[i] = self.scale(fun_points[i] ,[0,1], [yrange_start, yrange_end])
        return xx, yy


    def get_line(self, fun):
        y = np.linspace(0,1,100) 
        for i, elem in enumerate(y):
            y[i] = fun(y[i])
        return y
    ##ease out
    def easeOutSine(self, x):
        return Math.sin((x * PI) / 2);
    def easeOutCubic(self, x):
        return 1 - Math.pow(1 - x, 3);  
    def easeOutQuint(self, x):
        return 1 - Math.pow(1 - x, 5);
    def easeOutCirc(self, x):
        return Math.sqrt(1 - Math.pow(x - 1, 2));
    def easeOutElastic(self, x):
        c4 = (2 * PI) / 3;
        if x == 0: return 0
        if x == 1: return 1
        else: return  Math.pow(2, -10 * x) * Math.sin((x * 10 - 0.75) * c4) + 1;
    def easeOutQuad(self, x):
        return 1 - (1 - x) * (1 - x);
    def easeOutQuart(self, x):
        return 1 - Math.pow(1 - x, 4);
    def easeOutExpo(self, x):
        if x == 1: return 1
        else: return 1 - Math.pow(2, -10 * x);
        #return x === 1 ? 1 : 1 - Math.pow(2, -10 * x);
    def easeOutBack(self, x):
        c1 = 1.70158;
        c3 = c1 + 1;
        return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2);
    def easeOutBounce(self, x):
        n1 = 7.5625
        d1 = 2.75
        if (x < 1 / d1):
            return n1 * x * x;
        elif (x < 2 / d1):
            xx = (x - 1.5 / d1)
            return n1 * xx *  xx + 0.75;
        elif (x < 2.5 / d1):
            xx =(x - 2.25 / d1)
            return n1 * xx * xx + 0.9375;
        else:
            xx =(x - 2.625 / d1)
            return n1 *xx *xx + 0.984375;
    
    #ease in
    def easeInSine(self, x):
        return 1 - Math.cos((x * PI) / 2);
    def easeInCubic(self, x):
        return x * x * x;
    def easeInQuint(self, x):
        return x * x * x * x * x;
    def easeInCirc(self, x):
        return 1 - Math.sqrt(1 - Math.pow(x, 2));
    def easeInElastic(self, x):
        c4 = (2 * PI) / 3;
        if x == 0:return 0
        elif x == 1: return 1
        else: return -Math.pow(2, 10 * x - 10) * Math.sin((x * 10 - 10.75) * c4)
    def easeInQuad(self, x):
        return x * x;
    def easeInQuart(self, x):
        return x * x * x * x;
    def easeInExpo(self, x):
        if x == 0: return 0
        else: return Math.pow(2, 10 * x - 10)
    def easeInBack(self, x):
        c1 = 1.70158;
        c3 = c1 + 1;
        return c3 * x * x * x - c1 * x * x;
    def easeInBounce(self, x):
        return 1 - self.easeOutBounce(1 - x);
    
    # #ease in out
    def easeInOutSine(self, x):
        return -(Math.cos(PI * x) - 1) / 2
    def easeInOutCubic(self, x):
        if x < 0.5: return 4 * x * x * x 
        else: return  1 - Math.pow(-2 * x + 2, 3) / 2
    def easeInOutQuint(self, x):
        if x < 0.5: return 16 * x * x * x * x * x 
        else: return 1 - Math.pow(-2 * x + 2, 5) / 2;
    def easeInOutCirc(self, x):
        if x < 0.5:  return (1 - Math.sqrt(1 - Math.pow(2 * x, 2))) / 2
        else: return(Math.sqrt(1 - Math.pow(-2 * x + 2, 2)) + 1) / 2;
    def easeInOutElastic(self, x):
        c5 = (2 * PI) / 4.5;
        if  x == 0: return 0
        elif x == 1: return 1
        elif x < 0.5: return -(Math.pow(2, 20 * x - 10) * Math.sin((20 * x - 11.125) * c5)) / 2
        else: return (Math.pow(2, -20 * x + 10) * Math.sin((20 * x - 11.125) * c5)) / 2 + 1;
    def easeInOutQuad(self, x):
        if x < 0.5: return 2 * x * x
        else: return 1 - Math.pow(-2 * x + 2, 2) / 2;
    def easeInOutQuart(self, x):
        if x < 0.5: return 8 * x * x * x * x 
        else: return 1 - Math.pow(-2 * x + 2, 4) / 2;
    def easeInOutExpo(self, x):
        if x == 0: return 0
        elif x == 1: return 1
        elif x < 0.5:return Math.pow(2, 20 * x - 10) / 2
        else:return (2 - Math.pow(2, -20 * x + 10)) / 2;
    def easeInOutBack(self, x):
        c1 = 1.70158;
        c2 = c1 * 1.525;
        if x < 0.5: return (Math.pow(2 * x, 2) * ((c2 + 1) * 2 * x - c2)) / 2
        else: return (Math.pow(2 * x - 2, 2) * ((c2 + 1) * (x * 2 - 2) + c2) + 2) / 2;
    def easeInOutBounce(self, x):
        if x < 0.5: return (1 - self.easeOutBounce(1 - 2 * x)) / 2
        else: return (1 + self.easeOutBounce(2 * x - 1)) / 2;
    @staticmethod
    def scale(val, src, dst):
        return ((val - src[0]) / (src[1]-src[0])) * (dst[1]-dst[0]) + dst[0]

    def get_mirror_fun(self, fun):
        x = np.linspace(0,1,100)
        for i, elem in enumerate(fun):
            x[99-i] = 1-elem
        return x

    def graph(self, text, w):
        self.prev_fun = self.cur_fun
        self.cur_fun = getattr(self ,text + "_yline")
        y = None
        if not self.opposite:
            y = self.cur_fun.line
        else:
            y = self.cur_fun.opposite
        # x = np.linspace(0,1,100)
        # y = np.linspace(0,1,100) 
        # for i, elem in enumerate(y):
        #     y[i] = self.cur_fun(x[i])
        
        xx = np.linspace(self.xrange_start,self.xrange_end,100)
        yy = np.linspace(self.yrange_start,self.yrange_end,100)
        for i, elem in enumerate(yy):
            yy[i] = self.scale(y[i] ,[0,1], [self.yrange_start, self.yrange_end])

        if self.clear:
            plt.cla()
        colors = ["#b41313", "#bbc439","#348912","#36a474", "#2890c7", "#0037ff", "#6423c6", "#9541b1", "#9e2c7f", "#000000"]

        
        plt.plot(xx, yy, random.choice(colors), label=f"{text.split('ease')[1]} x:[{self.xrange_start},{self.xrange_end}], y:[{self.yrange_start},{self.yrange_end}]")
        
        plt.title('Graph')
        plt.xlabel('x', color='#1C2833')
        plt.ylabel('y', color='#1C2833')
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
          fancybox=True, shadow=True, ncol=3)
        ax = plt.gca()
        box = ax.get_position()
        ax = self.ax; box = self.box
        ax.set_position([box.x0, box.y0 + box.height * 0.1,
                        box.width, box.height * 0.9])

        if self.proportion:    
            ax.set_aspect('equal', adjustable='box')
        else:
            ax.set_aspect('auto')#, adjustable='box')
        #if self.prev_fun and self.cur_fun.line != self.prev_fun.line:
        plt.grid()
        plt.show()
        # f, ax = plt.subplots()
        # backend = matplotlib.get_backend()
        # if backend == 'TkAgg':
        #     f.canvas.manager.window.wm_geometry("+%d+%d" % (1000, 100))
        # elif backend == 'WXAgg':
        #     f.canvas.manager.window.SetPosition((x, y))
        # else:
        #     f.canvas.manager.window.move(x, y)

if __name__ == "__main__":

    funs = ease_funs()
    v = dir(funs)


    import PySimpleGUI as sg
    import time, sys, random,matplotlib
    from scipy.interpolate import interp1d


    def new_layout(text):
        return [[sg.Button(enable_events=True, button_text=text, key=("-plus-", text))]]

    column_layout1 = [new_layout(elem)[0] for elem in funs.function_l[0:10]]
    column_layout2 = [new_layout(elem)[0] for elem in funs.function_l[10:20]]
    column_layout3 = [new_layout(elem)[0] for elem in funs.function_l[20:30]]

    layout = [
        [sg.T("X Range: "), 
        sg.InputText(size=(5,1), key="xrange_start", enable_events=True),
          sg.InputText(size=(5,1),  enable_events=True,key="xrange_end"),],[
        sg.T("Y Range: "), 
        sg.InputText(size=(5,1), key="yrange_start", enable_events=True),
          sg.InputText(size=(5,1),  enable_events=True,key="yrange_end"),],[  

          sg.Checkbox(text="clear",   enable_events=True, key="-cb-", default=True), 
          sg.Checkbox(text="1:1 proportion",   enable_events=True, key="-1:1 proportion-", default=True),
          sg.Checkbox(text="opposite",   enable_events=True, key="-opposite-", default=False)],
        [sg.Column(column_layout1, key='-Column-'),
        sg.Column(column_layout2, key='-Column-'),
        sg.Column(column_layout3, key='-Column-'),],
     #   [sg.Submit(button_text="Update/Insert"), sg.Cancel(button_text="Cancel")],
    ]


    window = sg.Window('Ease function visualizer', layout)
    import threading
   # t = threading.Thread(target=funs.graph_loop, args=(event[1], window))
  #  t.start()
    i = 1
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit', 'Cancel'):
            break
        elif event[0] == '-plus-':
            #time.sleep(1)
            #for elem in l:
            #    window.extend_layout(window['-Column-'], new_layout(elem))

            funs.graph(event[1], window)

        elif event == "-cb-":
            funs.clear = not funs.clear
        elif event == "-1:1 proportion-":
            funs.proportion = not funs.proportion
        elif event == "-opposite-":
            funs.opposite = not funs.opposite
        elif event == "xrange_start":
            try:
                funs.xrange_start = float(values[event])
            except Exception as e:
                print(e)
        elif event == "xrange_end":
            try:
                funs.xrange_end = float(values[event])
            except Exception as e:
                print(e)
        elif event == "yrange_start":
            try:
                funs.yrange_start = float(values[event])
            except Exception as e:
                print(e)
        elif event == "yrange_end":
            try:
                funs.yrange_end = float(values[event])
            except Exception as e:
                print(e)
        if "range" in event:
            print("val of ", event, " ", getattr(funs, event))
        print(event, values)

    #event, values = window.read()
    window.close()
    sys.exit()

