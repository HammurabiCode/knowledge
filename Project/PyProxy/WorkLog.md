# 2017-06-15
 * 确定了基本的框架:
     - flask作为API的借口，为爬虫提供服务
     - redis作为存储可用代理的数据库
 * todo：
     - 获取新的代理地址，并加入到redis中去，refresh
     - 确定使用何种redis数据类型来存储代理
     - 删除代理地址
     - 获取代理地址

# 2017-06-16
 * 需要搜集书的哪些信息？
     - 豆瓣上的编号，在链接中
     - 书名
     - 副标题
     - 作者
     - 作者的国籍
     - 译者
     - 出版时间
     - 出版社
     - ISBN
     - 价格
     - 从书
     - 豆瓣标签
     - 内容简介
     - 评分
     - 参加评分的人数
     - 短评数量
     - 评论数量
     - 读过的数量
 * todo
      - 书的信息持久化，ORM？
      - 移动到linux上去？
      - 脚本来启动代理IP数据库（redis）和代理ip的服务（flask）

# 2017-06-20
 * 在linux上用popen来启动redis-server
 * 用在python脚本中获取sudo权限：
 ```python
 p = subprocess.Popen('echo %s | sudo -S netstat -naop | grep 6357' % 'helloworld',
 shell=True, close_fds=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
 ```

 * 使用python来查看端口的使用情况，从而判断redis-server是否启动，代理地址的api是否启动：
 * 在python中获得root权限
 ```python
 p = subprocess.Popen('sudo xxx',
 shell=True,
 close_fds=True,
 stdin=subprocess.PIPE,
 stdout=subprocess.PIPE)
 p.stdin.write('密码\n') 
 ```
 * while ... else ... 在while正常退出的时候执行else语句块，如果是break退出，就不执行else语句块。
 * 如何在requests.get中设置超时？requests.get(url, timeout=10)
 * requests中的异常基类：requests.exceptions.RequestException
 * 先将html页面保存到本地，然后再提取信息，便于调试
 * todo
      - 用进程池抓取到本地
      - 代理服务器对代理进行评分？
      - 解析书籍数据时的问题
           + 多名作者和译者，保存作者的主页链接

# 2017-06-20
 * 查看linux的CPU信息：核的个数
   ```shell
   cat /proc/cpuinfo
   ```
 * 使用进程池：http://www.cnblogs.com/kaituorensheng/p/4465768.html
   ```python
    pool = multiprocess.Pool(processes=4)
    result = [] # 收集进程运行的结果
    for x in range(n):
      result.append(pool.apply_async(fun, (arg,)))
    pool.close() # 不再接收新的任务
    pool.join() # 阻塞

    for r in result:
      print(r.get())
   ```

# 2017-06-27
 * linux 查看文件夹下的文件个数：ls | wc -l
 * linux 查看文件夹所占的磁盘空间大小：du -h dir_name

# 2017-06-28
 * 使用PyMySQL来连接MySQL
   - PEP: DB API，统一的数据库接口。
 * 使用sqlalchemy作为ORM框架
   - 创建引擎 create_engine()
   - ORM对象的基类，并创建子类，并处理子类的属性之间以及子类之间之间的关系:主键约束，一对多，多对多
   - 创建表格
   - 获取session
   - 对Session进行操作

