# Seminar 4

Generally, this article is about a technique for data storage scaling. The requirements were that the system should be scalable, stable, without operating overhead, highly accessible, best effort update. Their solution, consdiering that basically MySQL instance is a single database and it was a scaling bottleneck - they started several db servers running one SQL instance each, which would have data distributed across with index ranging. They would split up tables in shards, which would be stored on different servers. They have a very neat implementation of UUID so that the id resembles the IP address - a combination of data type id, id in local table and shard ID. They use ZooKeeper for mapping shard ID to a database, where they can look up the table recorded in data type id and the row from local id.