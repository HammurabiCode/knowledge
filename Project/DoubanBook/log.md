# 04
## 2017-05-09

完成：
- 获取IP代理
- 将IP代理保存到文件中
- 检测代理是否能使用
- 常用的代理网站：
    - http://www.kuaidaili.com/free/inha/1/
    - http://www.xicidaili.com/nn/1
    - http://www.proxy360.cn/Proxy

记住：
- 爬取页面：req = requests.get(url, headers, proxies)
    - url：页面地址
    - headers：请求的头，指明客户端的一些信息，比如User-Agent
    - proxies：使用代理，是字典键可以为'http', 'https'
- 从页面中读取信息：bs = BeautifulSoup(req.text, 'lxml')
    - 在页面中查找元素：bs.find_all(tag, attr)
- python中exel文件的读写
    - 写 
        ```
        import xlwt
        
        f = xlwt.Wookbook()
        sht = f.addSheet(sheet_name)
        sht.write(0, 0, cell_0_0)
        f.save(xl_file_name)
        ```
    - 读
        ```
        book = xlrd.open_Workbook(xl_file_name)
        sh = book.sheet_by_index(1)
        print(sh.cell(0, 0))
        print(sh.nrows)
        print(sh.ncols)
        ```
- 其他
    - 字符串，去除头尾的无意义的字符：s.strip(' \n\r')
    - 数组中删除某个元素：l.remove('hello')
    - while ... else 和 for ... else：else语句块中的语句，在循环没有break的时候执行
    - random.choice(list)：在list中随机选择一个元素
    - range 和 xrange的差别：后者得到的不是list，而是一个生成器。
    - 代理
        - 高匿：服务器不知道真实的客户端
        - 透明
        - 普通
- Python中的日期
    ```
    import datetime
    str_now = datetime.datetime.now().strftime('%Y-%b-%d')
    %a 	星期的英文单词的缩写：如星期一， 则返回 Mon
    %A 	星期的英文单词的全拼：如星期一，返回 Monday
    %b 	月份的英文单词的缩写：如一月， 则返回 Jan
    %B 	月份的引文单词的缩写：如一月， 则返回 January
    %c 	返回datetime的字符串表示，如03/08/15 23:01:26
    %d 	返回的是当前时间是当前月的第几天
    %f 	微秒的表示： 范围: [0,999999]
    %H 	以24小时制表示当前小时
    %I 	以12小时制表示当前小时
    %j 	返回 当天是当年的第几天 范围[001,366]
    %m 	返回月份 范围[0,12]
    %M 	返回分钟数 范围 [0,59]
    %P 	返回是上午还是下午–AM or PM
    %S 	返回秒数 范围 [0,61]。。。手册说明的
    %U 	返回当周是当年的第几周 以周日为第一天
    %W 	返回当周是当年的第几周 以周一为第一天
    %w 	当天在当周的天数，范围为[0, 6]，6表示星期天
    %x 	日期的字符串表示 ：03/08/15
    %X 	时间的字符串表示 ：23:22:08
    %y 	两个数字表示的年份 15
    %Y 	四个数字表示的年份 2015
    %z 	与utc时间的间隔 （如果是本地时间，返回空字符串）
    %Z 	时区名称（如果是本地时间，返回空字符串）
    ```
    
- TODO
    - 让代理服务化：http://kaito-kidd.com/2015/11/02/proxies-service/
    - https://www.zhihu.com/question/47464143?sort=created

- 为啥不是用多线程：python的多线程可能是假的，事实上是顺序执行
- 多进程：multiprocessing。Python 3自带的。
    - 进程池的使用：multiprocessing.Pool
        - apply
        - apply_async()：非阻塞
        - map
        - close():关闭进程池，使它不再接受新的任务
        - terminate():结束工作，尚未处理的任务也不处理
        - join()：等待阻塞的任务执行完毕，必须在close或terminate之后调用
        - 使用 res.append(pool.apply_async())可以得到进程的返回值
            ```
            if __name__ == "__main__":
            pool = multiprocessing.Pool(processes=4)
            result = []
            for i in xrange(3):
                msg = "hello %d" %(i)
                result.append(pool.apply_async(func, (msg, )))
            pool.close()
            pool.join()
            for res in result:
                print ":::", res.get()
            print "Sub-process(es) done."
    ```

    ```
    import multiprocess    
    ```

- logging 模块，
    - 解决什么问题：
        * 日志分级（debug, info, error, critical）
        * 日志的格式（formatter）
        * 日志存放在哪儿（handler）
    - 


- 爬虫中的代理
    - 用多进程的生产者和消费者模式来进行代理的获取和验证：获取是生产者，验证是消费者
    - 多进程验证结束之后，将代理保存到文件
    - 准备好代理之后，可以使用squid将代理服务化，也可以自己写一个策略来提供代理
    
