import os
import sys
import re
import tty
import termios


class FileManager:
    def __init__(self):
        self.setting = {}
        self.FileNumbers = {}

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

    # 打印路径下所有文件/文件夹<F8>
    def print_file(self, ChooseFile=1, path=os.getcwd()):
        # 获取路径所有文件/文件夹
        AllFile = os.listdir(path)
        # 所有文件
        files = []
        # 文件夹数量
        n = 1
        # 打印路径所有文件
        for i in AllFile:
            # 如果是文件夹则打印棕色字体，
            if os.path.isdir(i):
                print(f"\033[0;33;48m {n} {i}")
                # 对应编号添加在FileNumbers字典里
                self.FileNumbers[n] = i
                # 并且文件夹数量加1
                n += 1

            # 如果是文件则储存在列表里
            else:
                files.append(i)

        # 所有文件夹打印完后打印文件 白色字体
        for j in range(len(files)):
            print(f"\033[0;37;48m {j+n} {files[j]}")
            # 对应编号添加在FileNumbers字典里
            self.FileNumbers[j+n] = files[j]

    # 选择文件/文件夹
    def choose_file(self, ChooseFile=1):
        # print(self.FileNumbers)
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

        if ch == 'j':
            ChooseFile -= 1
        elif ch == 'k':
            ChooseFile += 1
        else:
            pass

        return ChooseFile


if __name__ == '__main__':
    fm = FileManager()
    fm.read_setting()
    fm.print_file()
    # os.system("clear")
    fm.print_file(ChooseFile=fm.choose_file())
