# FileManager

## 说明:  
- 目前只适配于Linux系统
- ~~更不更新取决于作者懒不懒~~
- **禁止用于一切不当用途**
---
## 使用教程  
### 下载及运行
在终端输入：  
```
cd ~; git clone https://github.com/XXiaoA/FileManager ; echo 'python ~/FileManager/FileManager.py' >a.sh; chmod +x a.sh;mv a.sh filemanager;mv filemanager ~/../usr/bin  
```
等待程序下载完成，输入`filemanager`即可运行
---
### 设置  
1. 在~目录下创建FMSetting.py文件  
2. 配置  
- 添加打开文件命令，如py后缀和无后缀文件用vim打开，mp3后缀用mpv打开(% 表示文件)：  
```
open = {
    "vim %" : ["py", ""],
    "mpv %" : ['mp3']
}
```

### 操作  
- j/k，上下选择文件
- 空格进入文件夹/打开文件
- q/CTRL+c退出程序
---
## 更新日志  
### v0.02
- 配置打开方式更加人性化，允许用户自定义命令，不再是`命令 文件名`
