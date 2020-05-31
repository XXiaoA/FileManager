import os
import sys
import re
import tty
import termios


class FileManager:
    def __init__(self):
        self.setting = {}
        self.FileNumbers = {}
        self.ChooseFile = 1

    # 读取.FMSetting文件并把内容转换成字典
    def read_setting(self, SettingFile="/home/.FMSetting"):
        # 检测.FMSetting文件是否存在
        if os.path.exists(SettingFile):
            # 存在则打开文件并读取内容
            with open(SettingFile) as f:
                text = f.readlines()
                f.close()
            # 去掉文件内容每行最后面的\n
            text = [t.replace("\n", "") for t in text]
            # 遍历文件内容
            # 如果是set开头则把=前后的内容变成键值对添加进setting字典
            for i in text:
                if i[:3] == "set":
                    i = re.split("[ =]", i)
                    self.setting[i[-2]] = i[-1]

        # 文件不存在则提示
        else:
            print("没有找到.FMSetting文件")

    # 设置文件数字编号
    def set_file_number(self, path=os.getcwd()):
        # 获取路径所有文件/文件夹
        AllFile = os.listdir(path)
        # 所有文件
        files = []
        # 文件夹数量
        n = 1
        # 打印路径所有文件
        for i in AllFile:
            # 如果是文件夹就打印
            if os.path.isdir(i):
                # 并且文件夹数量加1
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
    def print_file(self, ChooseFile=1, path=os.getcwd()):
        os.system("clear")
        # 获取路径所有文件/文件夹
        AllFile = os.listdir(path)
        # 所有文件
        files = []
        # 文件夹数量
        n = 1
        # 打印路径所有文件
        for i in AllFile:
            # 如果是文件夹就打印
            if os.path.isdir(i):
                # 如果是选中状态则打印蓝色
                if self.FileNumbers.get(i) == ChooseFile:
                    print(f"\033[0;36;48m {n} {i}")
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

    # 选择文件/文件夹
    def choose_file(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

        if ch == 'j':
            self.ChooseFile -= 1
        elif ch == 'k':
            self.ChooseFile += 1
        elif ch == 'q':
            sys.exit()
        else:
            pass

        return self.ChooseFile

if __name__ == '__main__':
    fm = FileManager()
    os.system("clear")
    fm.read_setting()
    fm.set_file_number()
    fm.print_file()
    while True:
        fm.print_file(ChooseFile=fm.choose_file())