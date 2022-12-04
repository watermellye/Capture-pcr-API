# 安装模拟器和游戏
下载mumu（安卓6 64x） https://mumu.163.com/index.html
下载pcr https://game.bilibili.com/pcr/#kv
安装 登录 下载数据

# 安装mitmproxy
下载安装 https://www.mitmproxy.org/
运行mitmdump，然后在 C:\Users\didik\.mitmproxy\ 找到mitmproxy-ca.p12 点击安装。
需要修改一个设置：将所有证书都放入下列存储->受信任的根证书颁发机构

# 配置conda和python
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
conda create -n pcr python=3.8.3
conda activate pcr
pip install mitmproxy
pip install crypto
pip install pycryptodome
打开crypto安装路径（例：C:\Users\didik\anaconda3\envs\pcr\Lib\site-packages），将crypto改为Crypto（C大写）

# 使用
## pc（每次要抓包前）
打开cmd->ipconfig->找到当前正在使用的网络的IPv4地址（例：192.168.0.108）

## powshell（每次要抓包前）
（本文件同目录下）打开powershell（管理员）
conda activate pcr
mitmdump -p 1825 -s run.py

## mumu（只要设置一次）
打开设置->WLAN->长按已连接的这个wifi->修改网络->高级选项（右侧的展开剪头）->代理->手动->代理服务器主机名192.168.0.108->代理服务器端口1825
注：不使用mitmdump时，模拟器想正常联网，需要把代理改回“无”；下载游戏时不要开mitm，会很慢。
打开安卓的浏览器，输入mitm.it，安装android版的证书（会要你设置pin）

# 其它
通过powershell观察当前操作触发的api。如需要，在./debug/中找到对应文件，打开。
./log.txt中存储了api调用历史记录