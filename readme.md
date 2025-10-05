# 安装模拟器和游戏

[下载 MUMU模拟器（安卓12或安卓6 64x）](https://mumu.163.com/index.html)

[下载 BCR](https://game.bilibili.com/pcr/#kv)

安装，登录，下载数据。

# 安装mitmproxy

[下载](https://www.mitmproxy.org/)，安装 

运行`mitmdump`，然后在 `%USERPROFILE%\.mitmproxy\` 找到`mitmproxy-ca.p12`，点击安装。

需要修改一个设置：`将所有证书都放入下列存储 → 受信任的根证书颁发机构`

# 配置python环境
（以Conda为例）
```
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pip -U
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
conda create -n pcr python=3.10
conda activate pcr
pip install mitmproxy
pip install crypto
pip install pycryptodome
```

打开crypto安装路径（例：`%USERPROFILE%\[anaconda3|miniconda3|.conda]\envs\pcr\Lib\site-packages`），将`crypto`改为`Crypto`（C大写）。实际路径可以通过vscode右下角选择解释器中找到。

# 使用
## 在本机中：

每次要抓包前：

1. 打开 console（`cmd`或`powershell`）（VSCode快捷键：`` ctrl+` ``） → 输入`ipconfig` → 找到当前正在使用的网络的IPv4地址并记下（例：192.168.0.108）
2. （本文件同目录下）打开 console（可能需要管理员），输入：

```
conda activate pcr
mitmdump -p 1825 -s run.py --quiet
```

（提示没有 conda 的话，就打开`Anaconda Powershell Prompt`，然后 cd 到本目录）

## 在模拟器中：

以下操作只需进行一次：

1. 打开代理界面
   - mumu6：打开设置 → WLAN → 长按已连接的这个wifi → 修改网络 → 高级选项（右侧的展开剪头）
   - mumu12：打开设置 → WLAN → 点击互联网 → 点击WiredSSID
   - mumu12新：打开设置 → 网络和互联网 → 点击互联网 → 点击wlan0 → 右上角笔图标 → 高级选项
2. 设置代理
   1. 代理 → 手动
   2. 输入代理服务器主机名（192.168.0.108）（或上述获取的地址）
   3. 输入代理服务器端口（1825）（或在启动mitmdump时自定义的其它端口）
3. 下载证书
   - 打开安卓的浏览器，输入`mitm.it`，下载android版的证书
4. 安装证书
   - mumu6 安装证书：直接点击下载好的文件（会要你设置pin）
   - mumu12 安装证书：见本说明最下方详。详细图文版见 [本 Repo 的 issue #1](https://github.com/watermellye/Capture-pcr-API/issues/1#issuecomment-2075260712)

至此万事大吉，可以启动 BCR 了。

注：
- 代理记录会保存，重启模拟器不需要重新设置代理。
- 不使用mitmdump时，模拟器中需要把代理改回“无”以正常联网。
- 下载游戏时不要开mitm，会很慢。

## 获取API数据

通过观察`last10`文件夹（中的`_.json`）和`./log.txt`（存储api调用历史记录的文件）以观察当前操作触发的api。

如需要，在`./debug/`中存储了每个api的最后一次调用结果。

如有异常错误，可以观察 console 获取信息。

## mumu12 安装证书文字版说明
1. 把模拟器的 Root 和系统盘可读写功能打开，重启模拟器。
2. 下载安装openssl。（Light 版即可。安装时一路默认。）https://slproweb.com/products/Win32OpenSSL.html
3. 获取证书的 subject_hash：`openssl x509 -subject_hash_old -in mitmproxy-ca-cert.crt`（证书在 download 文件夹下。download 文件夹就在 mumu 共享目录下。）
4. 重命名证书：把证书重命名为`<openssl console中（证书上方小写字母）显示的hash>.0`（例：`c8750f0d.0`）
5. 下载 Root Explorer。（mumu 桌面上的“小工具”文件夹中自带一个RE。点击即可安装。）（官方安装路径：https://rootexplorer.co/download/RootExplorer.apk）
6. 把根目录mount为读写 r/w
7. 把证书复制到 /etc/security/cacerts/
然后就可以启动mitmdump，然后启动BCR抓包了。