# TCP/IP
## TCP/IP协议栈模型
![TCP/IP参考模型](http://pic002.cnblogs.com/images/2012/314385/2012062314110518.jpg)


![](http://images.cnblogs.com/cnblogs_com/bluetzar/TCP4.jpg)

1. 应用层 HTTP, FTP, TELNET
2. 传输层 TCP/IP
3. 网络层 IP
4. 网络接口层

## IP报文格式
## TCP
### TCP：面向连接、字节流、可靠
### TCP报文格式
* 源端口号 16位
* 目标端口号 16位
* 顺序号 32位 表示报文中格点第一个字节
* 确认号 32位 ACK=1时，期望收到的下一个字节
* 头部长度 4位 值为[5，15]表示头部的长度为[20, 60]字节
* 保留 6位
* 标志位 6位
    - URG：紧急指针有效
    - ACK：确认号有效
    - PSH：尽快交付给应用层
    - RST：重新建立连接
    - SYN：建立连接
    - FIN：释放连接
* 窗口大小 16位
* 校验和 16位：头部和数据
* 紧急指针 16位：在URG=1时有效
* 

## TCP建立连接和断开连接
### 建立连接的3次握手
主机A发送给主机B：SYN=1，顺序号=ISN\_A，进入SYN-SEND

主机B发送给主机A：SYN=1，ACK=1，确认号=ISN\_A+1，顺序号=ISN\_B，进入SYN-RCVD

主机A发送给主机B：SYN=0，ACK=1，确认号=ISN\_B+1，顺序号=ISN\_A+1， 进入ESTABLISHED

![](http://hi.csdn.net/attachment/201108/7/0_131271823564Rx.gif)

### 断开连接

### 窗口滑动机制

## Socket网络编程
open -> read/write -> close
