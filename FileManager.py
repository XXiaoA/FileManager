import os
import sys
import re
import tty
import termios


class FileManager:
    def __init__(self):
        self.setting = {'open':{}}
        self.FileNumbers = {}
        self.path = os.getcwd()
        self.AllFiles = os.listdir(self.path)
        self.AllFiles.insert(0, "..")
        self.ChooseFile = 1

    # 读取.FMSetting.py文件并把内容添加到setting字典
    def read_setting(self, SettingFile=os.path.expanduser('~')+"/FMSetting.py"):
        # 检测.FMSetting文件是否存在
        if os.path.exists(SettingFile):
            # 存在则打开文件并导入
            sys.path.append(os.path.expanduser('~'))
            import FMSetting as setting
            # 把打开方式添加到self.setting
            for open in setting.open:
                self.setting['open'][open] = setting.open.get(open)

        # 文件不存在则提示，并且退出程序
        else:
            print("⚠：没有找到FMSetting.py文件，一些功能将无法正常使用")
        # print(self.setting)

    # 设置当前所在路径
    def set_allfiles(self, path):
        self.path = path
        self.AllFiles = os.listdir(self.path)
        self.AllFiles.insert(0, "..")

    # 设置文件数字编号
    def set_file_number(self):
        self.FileNumbers = {}
        # 所有文件
        files = []
        # 文件夹数量
        n = 0
        # 遍历路径所有文件
        for i in self.AllFiles:
            # 如果是文件夹
            if os.path.isdir(self.path+'/'+i):
                # 编号添加进字典，文件夹数量加1
                self.FileNumbers[i] = n
                n += 1
            # 如果是文件则储存在列表里
            else:
                files.append(i)

        for j in range(len(files)):
            # 对应编号添加在FileNumbers字典里
            self.FileNumbers[files[j]] = j+n
        # print(self.FileNumbers)

    # 打印路径下所有文件/文件夹
    def print_file(self, ChooseFile=1):
        os.system("clear")
        # 所有文件
        files = []
        # 文件夹数量
        n = 0
        # 打印路径所有文件
        for i in self.AllFiles:
            # 如果是文件夹就打印
            if os.path.isdir(self.path+'/'+i):
                # 如果是选中状态则打印蓝色
                if self.FileNumbers.get(i) == ChooseFile:
                    print(f"\033[0;36;48m {n} {i}")
                # 如果是..(返回上个目录)打印灰色
                elif i == '..':
                    print(f"\033[0;30;48m {n} {i}")
                # 否则打印棕色
                else:
                    print(f"\033[0;33;48m {n} {i}")
                # 对应编号添加在FileNumbers字典里
                self.FileNumbers[i] = n
                # 并且文件夹数量加1
                n += 1

            # 如果是文件则储存在列表里
            else:
                files.append(i)

        # 所有文件夹打印完后打印文件
        for j in range(len(files)):
            # 如果是选中状态则打印蓝色
            if self.FileNumbers.get(files[j]) == ChooseFile:
                print(f"\033[0;36;48m {j+n} {files[j]}")
            # 否则白色
            else:
                print(f"\033[0;37;48m {j+n} {files[j]}")
            # 对应编号添加在FileNumbers字典里
            self.FileNumbers[files[j]] = j+n
        # print(self.FileNumbers)
        # print(ChooseFile)
        # print(self.AllFiles)

    # 选择文件/文件夹
    def choose_file(self):
        # 获取用户输入
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            # 1为允许输入字符的长度
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

        # 如果向下并选择且目前在最后一个则跳到第一个
        if ch == 'j' and self.ChooseFile == len(self.AllFiles)-1:
            self.ChooseFile = 1
        # 如果向上选择并且目前在第一个则跳到最后一个
        elif ch == "k" and self.ChooseFile == 0:
            self.ChooseFile = len(self.AllFiles)-1
        # j向下选择
        elif ch == 'j':
            self.ChooseFile += 1
        # k向上选择
        elif ch == 'k':
            self.ChooseFile -= 1
        # q或CTRL+c退出
        elif ch == 'q' or ord(ch) == 0x3:
            sys.exit()
        # 空格进入文件夹/打开文件
        elif ch == ' ':
            FileName = {self.FileNumbers.get(i): i for i in self.FileNumbers.keys()}.get(self.ChooseFile)
            FilePath = self.path+"/"+FileName
            # print(FilePath)
            if os.path.isdir(FilePath):
                if FileName == "..":
                    self.set_allfiles("/".join(self.path.split("/")[:-1]))
                else:
                    self.set_allfiles(FilePath)
                self.ChooseFile = 1
                self.print_file(self.ChooseFile)
            else:
                for open in self.setting['open'].keys():
                    if os.path.splitext(FileName)[1][1:] in self.setting['open'].get(open):
                        os.system("clear")
                        os.system(open.replace("%", FilePath))
                        # print(open.replace("%", FilePath))
                        # input()
        else:
            pass

        return self.ChooseFile


if __name__ == '__main__':
    fm = FileManager()
    os.system("clear")
    fm.read_setting()
    fm.set_allfiles(os.getcwd())
    fm.set_file_number()
    fm.print_file()
    fm.read_setting()
    while True:
        fm.set_file_number()
        fm.print_file(ChooseFile=fm.choose_file())
