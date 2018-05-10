# Key
## 需求
* 功能？优矿的策略系统+数字货币交易。一句话：用策略来交易数字货币！
* 优矿的策略怎么和数字货币的交易系统(OPU)通信？发布者/订阅者。通过`Redis`的`pubsub`来实现。
* 主要的通信内容有啥呢？数字货币交易的订单信息，以及与之关联的账户信息。
    + 策略发布订单，订阅订单情况的返回值。
    + 交易系统方订阅订单和账户消息（建立订单、撤销订单、查询订单、查询账户信息），发布订单成交情况。
* 我们提供的功能？user:平台账户，sub_account：user之下的虚拟账户，用来对应的策略。
## 实现
* sub/pub在哪儿？
```bash
redis-cli -h 128.1.135.86 -p 9418 -a hk_develop_1
```
* 策略向交易系统下达指令。Req。主要是下单，撤单。
    + 如何下单？
        - 频道：`ReqCreateOrder`
        - 参数：
    + 如何撤单？
        - 频道：`ReqCancelOrder`
        - 参数：
* 交易系统向我们返回的内容。Rtn.Rsp。
    + 内容：已经接受到指令；订单状态变化。
    + 已经收到指令Rsp
    + 订单状态
        + RtnOrder
        + RtnMatch
        + RtnPosition
    
     

## 开发
* 如何调试？
    + 先启动sub。在`bin/run.py`。才能接收到订单发送之后的返回值。
    + 然后pub订单：通过运行策略。
## 平台存储的内容
* 在哪儿？
    + mongodb: 10.22.132.30:27017
    + Database: digiccy
    + Account: app_digiccy_rw/h9sgk6RjALqKzJm1
* 数据库结构呢？
    + user
    + exchange_account:交易账号，在交易平台注册。
    + user_exchange_account_map:user和exchange_account的映射关系。多对多。
    + sub_account:子账号，用来运行策略的逻辑账号。
        - 与user的关系：从属，多个sub_account对应一个user。
        - 与交易账户的关系：一一对应，一个sub_account只有一个exchange_account。
        - 保存持仓信息。
    + strategy:user名下的策略。
    + live_strategy：user名下正在运行的策略。
        - 当前状态：运行/停止
    + order: 
        - UserDefineString:在通信的过程中，保证订单的唯一性。
        - 每次收到RtnOrder都会更新对应order的值。通过UserDefineString,找到对应的order，再更新。
    
## 疑问
* [x] OrderUID: 订单号。是由交易所产生的吗？何时产生的。**对，就是交易所产生的**
* TradeID: 是什么意思？
* 如果一个交易账号与多个子账号关联，那么子账号的持仓，如何更新？当前的数据库中，持仓信息保存在子账号中，而不是交易账号当中。
子账号只有一个交易账号，但是一个交易账号可以让多个子账号使用。所以交易账户持仓发生变化的时候，要更新所有的子账户的持仓信息？！

## subscriber
### RtnRspListener
#### 功能
* 连接OPU的redis，订阅特定的channel。
* 在构造函数中指明`channel`，可以用正则，列表。

### subscriber_loop.py
* 负责调用`RtnRspListenner`对`redis`进行监听，并更新数据库`digiccy`/mongo
* RtnPosition: 
    + 什么情况下收到？ 
    **只会在`完全成交`或者`订单部分成交后撤销`时会返回**。
    > 当订单完成 会使用这个方法返回Position结构, 提供成交回报（只会在"订单部份成交后撤销"以及"订单完全成交"发生)
    + 需要更新些什么内容？
        - 手续费
        - 当`订单部分成交后撤销`时，冻结的资金需要解冻。
    + TODO


## quartz
### account
#### digiccy_account
* order
* cancel_order
* get_positions
* 

# Database
## config
* mongo: 10.22.132.30:27017
* Database: digiccy
* Account: app_digiccy_rw/h9sgk6RjALqKzJm1

## Collections
### user
* 


### sub_account




