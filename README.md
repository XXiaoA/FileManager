# FileManager

## 说明:  
- 目前只适配于Linux系统
- 更不更新取决于~~作者懒不懒~~
- **禁止用于一切不良用途**
---
## 使用教程  
### 设置  
1. 在~目录下创建FMSetting.py文件  
2. 配置  
- 添加打开文件方式，如py后缀和无后缀文件用vim打开，mp3后缀用mpv打开：   
```
open = {
    "vim" : ["py", ""],
    "mpv" : ['mp3']
}
```
**注：**打开文件的命令为：打开方式 文件名，如：vim xxx.py  
---
### 操作  
- j/k，上下选择文件
- 空格进入文件夹/打开文件
- q/CTRL+c退出程序
