import os
import sys
import re
import tty
import termios


class FileManager:
    def __init__(self):
        # 设置
        self.setting = {
            'OpenCommand': {},
            'OtherOpenCommand': ''
        }
        # 文件编号
        self.FileNumbers = {}
        # 路径，默认当前工作目录
        self.path = os.getcwd()
        # 路径所有文件(包括..)
        self.AllFiles = os.listdir(self.path)
        self.AllFiles.insert(0, "..")
        # 各目录当前选择的文件
        self.SelectingFile = {self.path: 1}
        # 选中的文件/文件夹列表
        self.ChooseFileList = []
        # 提示
        self.prompt = []

    # 读取.FMSetting.py文件并把内容添加到setting字典
    def read_setting(self, SettingFile=os.path.expanduser('~')+"/FMSetting.py"):
        # 检测.FMSetting文件是否存在
        if os.path.exists(SettingFile):
            # 存在则打开文件并导入
            sys.path.append(os.path.expanduser('~'))
            import FMSetting as setting
            # 把打开命令添加到self.setting
            try:
                for Command in setting.OpenCommand:
                    self.setting['OpenCommand'][Command] = setting.OpenCommand.get(
                        Command)
            except AttributeError:
                pass

            try:
                self.setting['OtherOpenCommand'] = setting.OtherOpenCommand
            except AttributeError:
                pass

        # 文件不存在则提示
        else:
            self.prompt.append("⚠：没有找到FMSetting.py文件，一些功能将无法正常使用")
        # print(self.setting)

    # 设置当前所在路径及所有文件
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
    def print_file(self, SelectingFile=1):
        os.system("clear")
        # 所有文件
        files = []
        # 文件夹数量
        n = 0
        # 打印路径所有文件
        for i in self.AllFiles:
            # 如果是文件夹就打印
            if os.path.isdir(self.path+'/'+i):
                # 如果是选择状态则打印蓝色
                if self.FileNumbers.get(i) == SelectingFile:
                    print(f"\033[0;36;48m {n} {i}/")
                # 如果是..(返回上个目录)打印灰色
                elif i == '..':
                    print(f"\033[0;30;48m {n} {i}/")
                # 否则打印棕色
                else:
                    print(f"\033[0;33;48m {n} {i}/")
                # 对应编号添加在FileNumbers字典里
                self.FileNumbers[i] = n
                # 并且文件夹数量加1
                n += 1

            # 如果是文件则储存在列表里
            else:
                files.append(i)

        # 所有文件夹打印完后打印文件
        for j in range(len(files)):
            # 如果是选择状态则打印蓝色
            if self.FileNumbers.get(files[j]) == SelectingFile:
                print(f"\033[0;36;48m {j+n} {files[j]}")
            # 否则白色
            else:
                print(f"\033[0;37;48m {j+n} {files[j]}")
            # 对应编号添加在FileNumbers字典里
            self.FileNumbers[files[j]] = j+n
        # print(self.FileNumbers)
        # print(SelectingFile)
        # print(self.AllFiles)
        print(self.ChooseFileList)

    # 输出提示
    def print_prompt(self):
        if len(self.prompt) == 0:
            pass
        else:
            for i in self.prompt:
                print(i)

    # 选择文件/文件夹
    def selecting_file(self):
        # 获取用户输入
        self.prompt = []
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            # 1为允许输入字符的长度
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

        # 如果向下并选择且目前在最后一个则跳到第一个
        if ch == 'j' and self.SelectingFile[self.path] == len(self.AllFiles)-1:
            self.SelectingFile[self.path] = 1
        # 如果向上选择并且目前在第一个则跳到最后一个
        elif ch == "k" and self.SelectingFile[self.path] == 0:
            self.SelectingFile[self.path] = len(self.AllFiles)-1
        # j向下选择
        elif ch == 'j':
            self.SelectingFile[self.path] += 1
        # k向上选择
        elif ch == 'k':
            self.SelectingFile[self.path] -= 1
        # q或CTRL+c退出
        elif ch == 'q' or ord(ch) == 0x3:
            os.system("clear")
            sys.exit()
        # 空格进入文件夹/打开文件
        elif ch == ' ':
            # 文件(夹)名
            FileName = {self.FileNumbers.get(i): i for i in self.FileNumbers.keys()}.get(self.SelectingFile[self.path])
            # 文件(夹)绝对路径
            FilePath = self.path+"/"+FileName
            # print(FilePath)
            # 如果是文件夹
            if os.path.isdir(FilePath):
                # 如果文件夹名是 .. 表示返回上个路径
                if FileName == "..":
                    # 设置路径和所有文件为 当前路径去掉最后一个/后面的内容
                    self.set_allfiles("/".join(self.path.split("/")[:-1]))
                # 否则，果然是其他名字的文件夹
                else:
                    # 设置路径和所有文件为 选中文件夹的绝对路径
                    self.set_allfiles(FilePath)
                # 如果选选择路径文件不在字典里，选中文件重置为第一个
                if self.path not in self.SelectingFile.keys():
                    self.SelectingFile[self.path] = 1
                # raise AttributeError(self.SelectingFile)
                self.print_file(self.SelectingFile[self.path])
            # 否则如果是文件
            else:
                # 已打开为假
                IsOpen = False
                # 遍历设置里的打开命令
                for OpenCommand in self.setting['OpenCommand'].keys():
                    # 如果打开命令里包涵这个文件的后缀或这个命令打开其余后缀文件
                    if os.path.splitext(FileName)[1][1:] in self.setting['OpenCommand'].get(OpenCommand):
                        # 已打开设置为真
                        IsOpen = True
                        # 清屏并运行命令，%取代为文件绝对路径
                        os.system("clear")
                        os.system(OpenCommand.replace("%", FilePath))
                        # 停止遍历
                        break

                # 如果遍历结束已打开为假则运行其他后缀名命令
                if IsOpen is False:
                    # 清屏并运行命令，%取代为文件绝对路径
                    os.system("clear")
                    os.system(
                        self.setting['OtherOpenCommand'].replace("%", FilePath))
        # elif ch == 'c':
            # 文件(夹)名
            # FileName = {self.FileNumbers.get(i): i for i in self.FileNumbers.keys()}.get(self.SelectingFile[self.path])
            # 文件(夹)绝对路径
            # FilePath = self.path+"/"+FileName
            # if FileName == '..':
                # self.prompt.append('不允许选择..文件夹')
            # else:
                # self.ChooseFileList.append(FilePath)

        else:
            pass

        return self.SelectingFile[self.path]


if __name__ == '__main__':
    fm = FileManager()
    os.system("clear")
    fm.read_setting()
    fm.set_allfiles(os.getcwd())
    fm.set_file_number()
    fm.print_file()
    fm.print_prompt()
    while True:
        fm.set_file_number()
        fm.print_file(SelectingFile=fm.selecting_file())
        fm.print_prompt()
