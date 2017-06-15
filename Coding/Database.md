# 数据库规范化

 - 范式:第一范式、第二范式、第三范式、BC范式、第四范式、第五范式。
    * 第一范式：所有列都是不可分割的原子数据项，而不是集合或数组。与具体需求有关（比如姓名，还是姓和名）
    * 第二范式：非key属性完全依赖于主键（不能存在只依赖于主键一部分的属性）。选取一个能区分每个实体的属性或属性组，作为主键。
    * 第三范式：非关键字段与关键字段是直接依赖关系，不存非关键字段对关键字段的传递函数依赖。比如员工的编号决定了职务，职务决定了薪资水平。所以薪资水平是直接依赖于职务，而间接依赖于员工的编号。

 - 数据库对象
     + 表格
     + 视图：虚拟的表，使用时动态检索生成。
         * 简化SQL操作，隐藏细节，保护数据。
         * 不能使用索引，不能关联触发器，不可更新。
     + 索引：是一种排序数据结构（B树或B+树），用于快速访问数据库表格或视图中的数据。会占用数据库存储空间，也会导致修改和插入数据时时间变长。
         * 优点：加速查找、表连接、分组（GROUP）、排序(ORDER BY)操作。
         * 缺点：维护索引消耗时间，需要空间存储。
         * 在什么字段上建立索引：经常搜索的字段，外键，范围搜索的字段，经常排序的字段，WHERE中的字段。
         * 在什么字段上不要建立索引：值域很少的字段（比如性别），text，image，bit类型的字段，对修改的性能要求高的字段
         * 聚集索引：行的物理顺序和索引中键值的逻辑顺序相同，一个表只能有一个聚集索引
         * 非聚集索引
     + 用户自定义函数
     + 存储过程：通过存储过程的名称来调用。
     + 触发器：强制是想不同表中的逻辑相关，来维护完整性和一致性。
     + 主键：是字段的集合，用以唯一标识一个记录。
     + 外键：用以建立两个表格的约束关系，表B中的字段K是表A的主键。

 - 数据库事务
     + 四个特征：ACID
         * 原子性Atomicity：要么全部完成，要么全部不完成
         * 一致性Correspondence：完整性约束没有被破坏
         * 隔离性Isolation：串行化，同一时间只执行一个事务
         * 持久性Durability：完成之后，持久保存，不会被回滚
         
 - SQL
     + drop, truncate, delete的区别
         * drop删除表；truncate删除所有记录；delete删除指定记录。

         | drop | truncate | delete |  
         | ---- | ----------------- | -------------------|  
         | 删除表 | 删除所有记录 | 删除指定记录 |  
         | | 不保存日志 | 保存日志 |  
         | 释放表的所有空间 | 恢复初始大小 | |  
         | 删除表的约束、触发器、索引 | | |  

     + 连接JOIN
         * 内连接 JOIN, INNER JOIN
         * 外连接 LEFT JOIN, RIGHT JOIN, FULL JOIN
         * 交叉连接 CROSS JOIN

 - 性能优化
     + SQL 语句优化
     + 索引优化
     + 数据库结构优化
     + 硬件







# SQL: 结构化查询语言
 * 声明式语言：说明想要的结果，而非获取结果的过程，与传统的编程语言不同。
 * 执行的顺序与语法顺序不同，一般的语法顺序 
    -  SELECT
    -  FROM
    - WHERE
    - GROUP BY
    - HAVING
    - UNION
    - ORDER BY

    而执行顺序通常是：

    - FROM
    - WHERE
    - GROUP BY
    - HAVING
    - SELECT
    - DISTINCT
    - UNION
    - ORDER BY

	注意：

	   - FROM 是执行的第一句，而非SELECT。
	   - SELECT 是在大部分语句执行之后再执行的。
	   - UNION 总是在 ORDER BY 之前。
 * SQL的核心是对表的引用，table reference

    ```
    <from clause> ::= FROM <table reference> [ { <comma> <table reference> }... ]
    ```

    ```
    FROM a, b
    ```

 * 灵活地使用表引用，从表引用的角度来思考
 * 推荐使用的表连接：JOIN 而不是 ，
 * SQL 中的5种连接操作
    - EQUI JOIN: INNER JOIN(JOIN), OUTER JOIN(LEFT/RIGHT/FUll OUTER JOIN)
    - SEMI JOIN
    - ANTI JOIN
    - CROSS JOIN
    - DIVISION 

```
        -- This table reference contains authors and their books.
        -- There is one record for each book and its author.
        -- authors without books are NOT included
        author JOIN book ON author.id = book.author_id
        
        -- This table reference contains authors and their books
        -- There is one record for each book and its author.
        -- ... OR there is an "empty" record for authors without books
        -- ("empty" meaning that all book columns are NULL)
        author LEFT OUTER JOIN book ON author.id = book.author_id
```


```
        -- Using IN
        FROM author
        WHERE author.id IN (SELECT book.author_id FROM book)
         
        -- Using EXISTS
        FROM author
        WHERE EXISTS (SELECT 1 FROM book WHERE book.author_id = author.id)
```


 * 像使用变量一样使用派生表: 为派生表取一个别名

```
		-- A derived table with an alias
		FROM (SELECT * FROM author) a

		WITH a AS (
		  SELECT first_name, last_name, current_date - date_of_birth age
		  FROM author
		)
		SELECT *
		FROM a
		WHERE age > 10000
```


    也可以为a创建一个视图。

 * GROUP BY 是对表的引用进行的操作
 * SELECT 语句事实上是对关系的映射: SELECT 将其他语句产生的表引用整合到一起
 * 集合运算和排序运算
	- 集合运算：
		* DISTINCT：去重
		* UNION：拼接并去重
		* UNION ALL：拼接但不去重
		* EXCEPT：差集
		* INTERSECT：交集
	- 排序
		* OFFSET...FETCH: 不同数据库有不同的方言. [参考](http://www.jooq.org/doc/3.1/manual/sql-building/sql-statements/select-statement/limit-clause/)
		* MySQL 和 PostgreSQL 的 LIMIT…OFFSET
		* Server 和 Sybase 的 TOP…START AT





