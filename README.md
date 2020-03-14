# aliddns
aliddns by python

### 使用方式

首先打开脚本修改 `aliddnsipv6_ak ` 以及 `aliddnsipv6_sk` ，获取方式见阿里云文档 [https://help.aliyun.com/document_detail/34414.html](https://help.aliyun.com/document_detail/34414.html)

运行方式 `python3 ./aliddns.py RR DomainName Type`
### 使用方式(群晖DSM补充)
在`python3 ./aliddns.py RR DomainName Type` 前加上 'export PYTHONIOENCODING=UTF-8'
![设置截图](https://github.com/AkitoSilver/aliddns/blob/synology-fix/img/run.png)
#### 参数说明

1. RR : 要设置的主机名，你要设置的域名前缀
2. DomainName：域名 ，在阿里云购买的域名  例如 www.baidu.com ，www为RR，baidu.com 为DomainName
3. Type：类型，IPv4 为 A，IPv6 为 AAAA
4. value：值（可选），可以手动设置值，若不传改参数，则默认获取本机的地址

#### 运行示例


1. 设置本机外网ip     `python3 ./aliddns.py www baidu.com A`

2. 手动设置ip   `python3 ./aliddns.py www baidu.com A --value 1.1.1.1`

