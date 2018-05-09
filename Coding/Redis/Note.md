* import redis

* redis.redis VS redis.StrictRedis [Here](https://stackoverflow.com/questions/19021765/redis-py-whats-the-difference-between-strictredis-and-redis)

为了和以前的版本兼容，保留了`redis.redis`，如果没有兼容的要求，则使用`redis.StrictRedis`。