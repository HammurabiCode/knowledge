# toc
 1. Spark安装部署：配置文件
 2. 过程监视：Web端口
 3. RDD操作：transformation, action, 创建RDD, 保存至文件
 4. 开发
	
	4.1. spark-shell

	4.2. Java: CUI & IDE

	4.3. Scala

	4.4. Python



3. Spark RDD操作

	3.1. 创建RDD 

	 - sc.parallelize

	 	> val intRDD = sc.parallelize(List(3, 2, 33, 12, 123, 213))


	3.2. transformation

	 3.2.1. 单个RDD的转换

	  - map()
	  - flatMap()：先map，然后在flatten，拍扁
	  - filter()
	  - distinct(): 除重
	  - randomSplit(): 随机方式，按照指定比例分成多个RDD
	  - groupBy(): 按照传入规则，将RDD分为多个Array

	 3.2.2. 多个RDD的转换

	  - union()
	  - intersection()
	  - subtract()
	  - cartesian()

	 3.2.3. 基于key-value的transformation

	  - keys
	  - values
	  - filter{case(key, value) => value < 5}
	  - mapValue()
	  - sortedByKey(true): 升序
	  - reduceByKey((x, y) => x+y)

	 3.2.4. 多个 key-value RDD的transformation

	  - join
	  - leftOuterJoin
	  - rightOuterJoin
	  - subtractByKey
	  - mapValue()
	  - sortedByKey(true): 升序
	  - reduceByKey((x, y) => x+y)

	3.3. Action

	 3.3.1. 普通RDD

	  - collect()
	  - first
	  - take(N)
	  - takeOrdered(N)
	  - stats: 统计
	  - min
	  - max
	  - stdev: 标准差
	  - sum
	  - count
	  - mean

	 3.3.2. key-value RDD

	  - first()
	  - take(N)
	  - countByKey(): 计算单个key值的条数
	  - collectAsMap(): 转换为map，对重复的key，部分记录会被覆盖
	  - (key): 获取value
	  - lookup(key): 获取key对应的value(s)

	3.3. 共享变量：广播变量、累加器

	 3.3.1 broadcast 

	  - 广播到每个WorkNode中去，节约访问时间 
	  - 创建：val bc = sc.broadcast(v) 
	  - 使用：bc.value

	3.3.2 accumulator

	  - 创建：sc.accumulator(init_val)
	  - 使用：在task中只能 +=，不能访问
	  - 只有在Driver中可以使用.value来取得值

	3.4. RDD Persistence

	 - 存储位置：仅内存、仅磁盘、内存+磁盘
	 - 是否序列化：_SER，序列化消耗CPU，节约存储
	 - 保存的副本数量
	 - MEMORY_ONLY, MEMORY_AND_DISK, MEMORY_ONLY_SER, MEMORY_AND_DISK_SER, DISK_ONLY

		 ```
		 	rdd.persistence(StorageLevel.MEMORY_AND_DISK)
			rdd.unpersistence()
		 ```

