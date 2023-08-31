# -*- coding:gbk -*-
import win32gui,win32api,win32con,win32print,win32ui
import os,time,cv2,sys
from PIL import ImageGrab,Image
from ctypes import windll,cdll,c_uint64,string_at
# pip install -r venv/requirements.txt
# pyinstaller -D -w xxx.py
key_map = {
        "0": 48, "1": 49, "2": 50, "3": 51, "4": 52, "5": 53, "6": 54, "7": 55, "8": 56, "9": 57,
        'F1': 112, 'F2': 113, 'F3': 114, 'F4': 115, 'F5': 116, 'F6': 117, 'F7': 118, 'F8': 119,
        'F9': 120, 'F10': 121, 'F11': 122, 'F12': 123, 'F13': 124, 'F14': 125, 'F15': 126, 'F16': 127,
        "A": 65, "B": 66, "C": 67, "D": 68, "E": 69, "F": 70, "G": 71, "H": 72, "I": 73, "J": 74,
        "K": 75, "L": 76, "M": 77, "N": 78, "O": 79, "P": 80, "Q": 81, "R": 82, "S": 83, "T": 84,
        "U": 85, "V": 86, "W": 87, "X": 88, "Y": 89, "Z": 90,
        'BACKSPACE': 8, 'TAB': 9, 'TABLE': 9, 'CLEAR': 12,
        'ENTER': 13, 'SHIFT': 16, 'CTRL': 17,
        'CONTROL': 17, 'ALT': 18, 'ALTER': 18, 'PAUSE': 19, 'BREAK': 19, 'CAPSLK': 20, 'CAPSLOCK': 20, 'ESC': 27,
        'SPACE': 32, 'SPACEBAR': 32, 'PGUP': 33, 'PAGEUP': 33, 'PGDN': 34, 'PAGEDOWN': 34, 'END': 35, 'HOME': 36,
        'LEFT': 37, 'UP': 38, 'RIGHT': 39, 'DOWN': 40, 'SELECT': 41, 'PRTSC': 42, 'PRINTSCREEN': 42, 'SYSRQ': 42,
        'SYSTEMREQUEST': 42, 'EXECUTE': 43, 'SNAPSHOT': 44, 'INSERT': 45, 'DELETE': 46, 'HELP': 47, 'WIN': 91,
        'WINDOWS': 91, 'NMLK': 144,
        'NUMLK': 144, 'NUMLOCK': 144, 'SCRLK': 145,
        '[': 219, ']': 221, '+': 107, '-': 109, '~': 192, '`': 192,"/":111}
class imitate:
    def __init__(self,hclas=None,name=None,time=4000,path = ""):
        self.path = path
        self.hclas = hclas
        self.name = name
        self.wait_time = time
        res = imitate.resolution_ratio(self)
        self.location = res[0]
        self.zoom = res[1]
        filepath = "cache"
        if not os.path.isdir(filepath):os.mkdir(filepath)

    def resolution_ratio(self):
        if ((self.name==None)and(self.hclas==None)):self.hwnd=0
        else:
            self.hwnd = win32gui.FindWindow(self.hclas, self.name)
            if self.hwnd == 0:start(self.wait_time, path=self.path)
            for i in range(15):
                self.hwnd = win32gui.FindWindow(self.hclas, self.name)
                if self.hwnd != 0:break
                elif i == 14:
                    print("error:连接超时。(30s)")
                    self.hwnd = 0
                wait(2000)

        if self.hwnd != 0:
            imitate.foreground(self)
            left, top, right, bottom = win32gui.GetWindowRect(self.hwnd)
            self.frame=(left, top, right, bottom)
            print(self.hwnd, (left, top, right, bottom))
            wide = right - left
            high = bottom - top
        else:
            if self.name != None:print("未找到程序的窗口：" + self.name)
            print("应用全屏设置。")
            hDC = win32gui.GetDC(0)
            wide = win32print.GetDeviceCaps(hDC, win32con.DESKTOPHORZRES)
            high = win32print.GetDeviceCaps(hDC, win32con.DESKTOPVERTRES)
            (self.wide,self.high)=(wide,high)
            left, top = 0,0
            self.frame = (left, top, wide, high)
        # user32 = windll.user32
        # now_width = user32.GetSystemMetrics(0)
        # user32.SetProcessDPIAware()
        # origin_width = user32.GetSystemMetrics(0)
        # self.scal = round(origin_width / now_width, 2)
        # print(self.scal)
        if self.hwnd != 0:
            if (wide/high == 1920/1080) and (wide<=3840)and (wide>=1600):zoom=wide/1920
            else:
                print("不适配的分辨率" + str(wide) + "×" + str(high))
                sys.exit()
        else:zoom = 1.0
        print ((wide, high), zoom)
        return (left, top),zoom
    def zoom(self,list):
        if self.zoom !=1.0:
            nlist = []
            for i in list:nlist+=[(int(i[0]*self.zoom),int(i[1]*self.zoom))]
            list = nlist
        return list
    def trans(self,list):
        if self.location !=(0,0):
            nlist = []
            for i in list: nlist += [(i[0]+self.location[0],i[1]+self.location[1])]
            list = nlist
        return list
    def move(self,x, y):
        [(x,y)]=imitate.trans(self,imitate.zoom(self,[(x,y)]))
        win32api.SetCursorPos((x,y))

    def click(self,x=0, y=0):
        if (x!=0) or (y!=0):
            [(x,y)]=imitate.trans(self,imitate.zoom(self,[(x,y)]))
            win32api.SetCursorPos((x, y))
        win32api.mouse_event(2, x, y)
        win32api.mouse_event(4, x, y)

    def drag(self,pos,mov):
        x,y = pos
        [(xp,yp)]=imitate.trans(self,imitate.zoom(self,[pos]))
        [(xv, yv)] =imitate.zoom(self, [mov])
        win32api.SetCursorPos((xp,yp))
        from pyautogui import dragRel
        dragRel(xv, yv, duration=1, button='left')
        # pyautogui.zoomOut
    def clickup(self,x, y):
        [(x,y)]=imitate.trans(self,imitate.zoom(self,[(x,y)]))
        # win32api.SetCursorPos((x,y))
        win32api.mouse_event(4, x, y)
        # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

    def roll(self,x, y, num):
        [(x,y)]=imitate.trans(self,imitate.zoom(self,[(x,y)]))
        win32api.SetCursorPos((x,y))
        if num >0:u=1
        else:u=-1;num=-1*num
        for i in range(num):
            win32api.mouse_event(0x0800, 0, 0, 120*u, 0)
            wait(10)

    def rollh(self,x, y, num):
        [(x,y)]=imitate.trans(self,imitate.zoom(self,[(x,y)]))
        win32api.SetCursorPos((x,y))
        if num >0:u=1
        else:u=-1;num=-1*num
        for i in range(num):
            win32api.mouse_event(0x01000, 0, 0, -120*u, 0)
            wait(10)
    def rotate(self, rx, ry):#3600=360度
        #abs(int(rx/3600*3706* self.scal)), abs(int(ry/3600*3706 * self.scal))
        numx, numy = rx, ry
        if rx < 0:ix = -1
        elif rx >= 0:ix = 1
        if ry < 0:iy = -1
        elif ry >= 0:iy = 1
        rounding ,remainder= numx//10,numx%10
        for i in range(rounding):
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, ix*10, 0)
            wait(1)
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, ix * remainder, 0)
        wait(1)
    def screenshot(self):
        win32api.SetCursorPos((0,0))
        wait(10)
        sc = ImageGrab.grab(self.frame)  # 截取屏幕指定区域的图像
        scpic = "cache\\" + str(time.time())[-5:] + ".png"
        sc.save(scpic)
        return scpic
    # def screenshot2(self):
    #     win32api.SetCursorPos((0, 0))
    #     if self.hwnd !=0:
    #         left, top, right, bot = win32gui.GetWindowRect(self.hwnd)
    #         width,height = (right - left),(bot - top)
    #         hWndDC = win32gui.GetWindowDC(self.hwnd)
    #         mfcDC = win32ui.CreateDCFromHandle(hWndDC)
    #         saveDC = mfcDC.CreateCompatibleDC()
    #         saveBitMap = win32ui.CreateBitmap()
    #         saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
    #         saveDC.SelectObject(saveBitMap)
    #         saveDC.BitBlt((0, 0), (width, height), mfcDC, (0, 0), win32con.SRCCOPY)
    #         bmpinfo = saveBitMap.GetInfo()
    #         bmpstr = saveBitMap.GetBitmapBits(True)
    #         sc = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)
    #     else:
    #         sc = ImageGrab.grab((0,0,self.wide,self.high))
    #     scpic = "resource\\tem_pic\\" + str(time.time())[-5:] + ".png"
    #     sc.save(scpic)
    #     return scpic
    def findpic(self,bpic, picpath ,size_zoom=0,method =cv2.TM_CCOEFF_NORMED):
        if isinstance(bpic,str):
            bp = cv2.imread(bpic)
            (x1, y1, x2, y2) = (0,0,0,0)
        elif isinstance(bpic,tuple):
            (x1, y1,x2, y2)=bpic
            [(scx1, scy1),(scx2, scy2)] = imitate.zoom(self, [(x1, y1), (x2, y2)])
            scpath = imitate.screenshot(self)
            # print((scx1, scy1), (scx2, scy2))
            bp=cv2.imread(scpath)[scy1:scy2,scx1:scx2]
            # bp = cv2.resize(sc,)
        lp = cv2.imread(picpath)
        zoomlist = [1.0]
        if self.zoom<=1.0:
            for z in range(size_zoom): zoomlist += [(1 - (z + 1) * 0.1), (1 + (z + 1) * 0.1)]
        else:
            for z in range(size_zoom): zoomlist += [(1 - (z + 1) * 0.1), (1 + (z + 1) * 0.1)]
        # print(zoomlist)
        poslist,vallist=[],[]
        lpsy,lpsx,  num = lp.shape
        for zoom in zoomlist:
            if self.zoom<=1.0:lp = cv2.resize(lp, (int(lpsx * self.zoom * zoom),int(lpsy * self.zoom * zoom)))
            else:
                # lp = cv2.resize(lp, (int(x * self.zoom * zoom), int(y * self.zoom * zoom)))
                bpsx, bpsy, num = bp.shape
                bp = cv2.resize(bp, int((bpsy / self.zoom) * zoom),int((bpsx/ self.zoom) * zoom) )
            result = cv2.matchTemplate(bp,lp,method)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            # print(min_val, max_val, min_loc, max_loc)
            if (min_val>=-0.6) and (max_val<=0.6):pos,val=((0,0),0)
            else:
                min_val=min_val * -1
                if max_val>=min_val:(slx, sly), val = max_loc, max_val
                else:(slx,sly),val=min_loc,min_val
                if self.zoom<=1.0:(slx, sly) = (int(slx / self.zoom), int(sly / self.zoom))
                elif self.zoom > 1.0:(slx, sly) = (int((slx*self.zoom)/zoom),int((sly*self.zoom)/zoom))
                x = x1 + slx + int(lpsx / 2)
                y = y1 + sly + int(lpsy / 2)
                pos = (x, y)
            poslist += [pos]
            vallist += [val]
        val = max(vallist)
        pos = poslist[vallist.index(val)]
        if isinstance(bpic,tuple):os.remove(scpath)
        return (pos,val)

    def findcolor(self,bpic, hexlist,dif=0):
        if isinstance(bpic, str):
            scpath = bpic
            bp = Image.open(bpic)
            x1, y1, x2, y2 = 0,0,0,0
        elif isinstance(bpic, tuple):
            (x1, y1, x2, y2) = bpic
            [(x21, y21), (x22, y22)] = imitate.zoom(self,[(x1, y1),(x2, y2)])
            scpath = imitate.screenshot(self)
            sc = Image.open(scpath)
            bp = sc.crop((x21, y21,x22, y22))
        size = bp.size
        bp = bp.convert("RGBA")
        list = bp.load()
        if isinstance(bpic, tuple): os.remove(scpath)
        for hex in hexlist.split("+"):
            cb, cg, cr =  tuple(int(hex[i:i + 2], 16) for i in (0, 2, 4))
            cri,crx,cgi,cgx,cbi,cbx = cr-dif,cr+dif,cg-dif,cg+dif,cb-dif,cb+dif
            for x in range(size[0]):
                for y in range(size[1]):
                    r, g, b, a = list[x, y]
                    # hex = ('{:02X}' * 3).format(r, g, b)
                    if r<=crx:
                        if r>=cri:
                            if g<=cgx:
                                if g>=cgi:
                                    if b<=cbx:
                                        if b>=cbi:
                                            x = x1 + int(x / self.zoom)
                                            y = y1 + int(y / self.zoom)
                                            return (True,(x,y))
        return (False,(0,0))
    def ocr(self,sc,bstr=b'chi_sim+eng'):
        if isinstance(sc, str):scpath = sc
        elif isinstance(sc, tuple):
            (x1, y1, x2, y2) = sc
            [(x21, y21), (x22, y22)] = imitate.zoom(self,[(x1, y1),(x2, y2)])
            scpath = imitate.screenshot(self)
            sc = Image.open(scpath)
            sc = sc.crop((x21, y21, x22, y22))
            sc.save(scpath)
        ocr = OCR(lang = bstr)
        text = ocr.get_text(scpath.encode())
        if isinstance(sc,tuple):os.remove(scpath)
        return text


    def foreground(self):  # win32con.SW_SHOWNORMAL
        left, top, right, bottom = win32gui.GetWindowRect(self.hwnd)
        if left < 0:
            win32gui.ShowWindow(self.hwnd, win32con.SW_SHOWMAXIMIZED)
        else:win32gui.SetForegroundWindow(self.hwnd)

class OCR():
    def __init__(self, DLL_PATH='./libtesseract304.dll', TESSDATA_PREFIX = b'./tessdata', lang = b'chi_sim+eng',config='-psm 7'):
        self.DLL_PATH = DLL_PATH
        self.TESSDATA_PREFIX = TESSDATA_PREFIX
        self.lang = lang
        self.ready = False
        self.config = config
        if self.do_init():
            self.ready = True

    def do_init(self):
        self.tesseract = cdll.LoadLibrary(self.DLL_PATH)
        self.tesseract.TessBaseAPICreate.restype = c_uint64
        self.api = self.tesseract.TessBaseAPICreate()
        rc = self.tesseract.TessBaseAPIInit3(c_uint64(self.api), self.TESSDATA_PREFIX, self.lang)
        if rc:
            self.tesseract.TessBaseAPIDelete(c_uint64(self.api))
            print('Could not initialize tesseract.\n')
            return False
        return True

    def get_text(self, path):
        if not self.ready:
            return False
        self.tesseract.TessBaseAPIProcessPages(
            c_uint64(self.api), path, None, 0, None)
        self.tesseract.TessBaseAPIGetUTF8Text.restype = c_uint64
        text_out = self.tesseract.TessBaseAPIGetUTF8Text(c_uint64(self.api))
        return bytes.decode(string_at(text_out)).strip()


def press(key):
    try:key_num = key_map[key.upper ()]
    except:pass
    win32api.keybd_event(key_num, 0, 0, 0)
    win32api.keybd_event(key_num, 0, win32con.KEYEVENTF_KEYUP, 0)

def keydown(key):
    try:key_num = key_map[key.upper ()]
    except:pass
    win32api.keybd_event(key_num, 0, 0, 0)

def keyup(key):#
    try:key_num = key_map[key.upper()]
    except:pass
    win32api.keybd_event(key_num, 0, win32con.KEYEVENTF_KEYUP, 0)

def keyadd(key1,key2):
    key_num1 = key_map[key1.upper ()]
    key_num2 = key_map[key2.upper ()]
    win32api.keybd_event(key_num1, 0, 0, 0)  # ctrl按下
    win32api.keybd_event(key_num2, 0, 0, 0)  # a按下
    win32api.keybd_event(key_num2, 0, 0, 0)  # a抬起
    win32api.keybd_event(key_num1, 0, 0, 0)  # ctrl抬起
def wait(t):
    time.sleep(t/1000)
def start(time,path):
    if os.path.isfile(path):
        os.system("start \"\" \""+path+"\" -popupwindow")
        wait(time)
    else:
        print("设定的路径不正确："+path)
        sys.exit()

def killgame(path):
    os.system("taskkill /f /t /im "+os.path.split(path)[-1])
    print("已退出:"+path)
# imi=imitate()
# for fun in dir(imitate)[26:]:
#     globals()[fun] = eval("imi." + fun)
if __name__ == '__main__':
    pass