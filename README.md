# aliddns
aliddns ipv6 by python

### 使用方式

首先打开脚本修改 `aliddnsipv6_ak ` 以及 `aliddnsipv6_sk` ，获取方式见阿里云文档 [https://help.aliyun.com/document_detail/34414.html](https://help.aliyun.com/document_detail/34414.html)

运行方式 `python3 ./aliddns.py RR DomainName Type`

#### 参数说明

- RR : 要设置的主机名，你要设置的域名前缀
- DomainName：域名 ，在阿里云购买的域名  例如 www.baidu.com ，www为RR，baidu.com 为DomainName
- Type：类型，IPv4 为 A，IPv6 为 AAAA

#### 运行示例

```
python3 ./aliddns.py www baidu.com A
```

