# aliddns
aliddns by python

### 使用方式

首先打开脚本修改 `aliddnsipv6_ak ` 以及 `aliddnsipv6_sk` ，获取方式见阿里云文档 [https://help.aliyun.com/document_detail/34414.html](https://help.aliyun.com/document_detail/34414.html)

运行方式 `python3 ./aliddns.py RR DomainName Type`

#### 参数说明

1. RR : 要设置的主机名，你要设置的域名前缀
2. DomainName：域名 ，在阿里云购买的域名  例如 www.baidu.com ，www为RR，baidu.com 为DomainName
3. Type：类型，IPv4 为 A，IPv6 为 AAAA
4. value：值（可选），可以手动设置值，若不传改参数，则默认获取本机的地址

#### 运行示例


1. 设置本机外网ip     `python3 ./aliddns.py www baidu.com A`

2. 手动设置ip   `python3 ./aliddns.py www baidu.com A --value 1.1.1.1`



#### 配合群晖使用

配合群晖计划任务使用时，由于编码问题，需要在计划任务执行的代码里填入如下代码

```

export PYTHONIOENCODING=utf8
export LANG=en_US.utf8
python3 /path/to/aliddns.py www baidu.com A

```

![UTOOLS1587388368832.png](http://yanxuan.nosdn.127.net/b7ccb012a5ef2380a9d2c321b375e604.png)