# 安装模拟器和游戏

下载mumu（安卓12或安卓6 64x） https://mumu.163.com/index.html

下载pcr https://game.bilibili.com/pcr/#kv

安装 登录 下载数据

# 安装mitmproxy

下载安装 https://www.mitmproxy.org/

运行```mitmdump```，然后在 ```C:\Users\<your_username>\.mitmproxy\``` 找到```mitmproxy-ca.p12```，点击安装。

需要修改一个设置：```将所有证书都放入下列存储->受信任的根证书颁发机构```

# 配置conda和python
```
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
conda create -n pcr python=3.10
conda activate pcr
pip install mitmproxy
pip install crypto
pip install pycryptodome
```

打开crypto安装路径（例：```C:\Users\<your_username>\[anaconda3|miniconda3|.conda]\envs\pcr\Lib\site-packages```），将```crypto```改为```Crypto```（C大写）。实际路径可以通过vscode右下角选择解释器中找到。

# 使用
## pc（每次要抓包前）
打开cmd->```ipconfig```->找到当前正在使用的网络的IPv4地址（例：192.168.0.108）

## powshell（每次要抓包前）
（本文件同目录下）打开```powershell（管理员）```

```
conda activate pcr
mitmdump -p 1825 -s run.py --quiet
```

## mumu（只要设置一次）
mumu6：打开设置->WLAN->长按已连接的这个wifi->修改网络->高级选项（右侧的展开剪头）

mumu12：打开设置->WLAN->点击互联网->点击WiredSSID


代理->手动->代理服务器主机名192.168.0.108（上述获取的地址）->代理服务器端口1825（或在mitmdump中自定义的其它端口）

注：不使用mitmdump时，模拟器想正常联网，需要把代理改回“无”；下载游戏时不要开mitm，会很慢。

打开安卓的浏览器，输入```mitm.it```，下载android版的证书

mumu6安装证书：直接点击下载好的文件（会要你设置pin）

mumu12安装证书：打开设置->WLAN->互联网->网络偏好设置->安装证书

# 其它
通过观察```last10```文件夹和```./log.txt```（存储api调用历史记录的文件）以观察当前操作触发的api。

如需要，在```./debug/```中存储了每个api的最后一次调用结果。

如有异常错误，可以观察powershell窗口获取信息。