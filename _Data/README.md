## 一、目录结构

- **neo4j_csv**：知识图谱存储数据
- **os_query**：训练数据集

## 二、向Neo4j中导入CSV文件

### 1. 导入节点

#### 错误用法：

```CQL
USING PERIODIC COMMIT 10
LOAD CSV FROM "file:///subject.csv" AS line
create (a:subject{name:line[0],info:line[1],link:line[2]})
```

**ERROR: Please use CALL { ... } IN TRANSACTIONS instead**

```cql
CALL {
    LOAD CSV FROM "file:///subject.csv" AS line
    create (a:subject{name:line[0],info:line[1],link:line[2]})
} IN TRANSACTIONS
```

**ERROR: A query with 'CALL { ... } IN TRANSACTIONS' can only be executed in an implicit transaction, but tried to execute in an explicit transaction.**

#### 正确使用：

```cql
:auto CALL {
    LOAD CSV FROM "file:///subject.csv" AS line
    create (a:subject{name:line[0],info:line[1],link:line[2]})
} IN TRANSACTIONS
```

```cql
:auto CALL {
    LOAD CSV FROM "file:///module.csv" AS line
    create (a:module{name:line[0],info:line[1],page:line[2]})
} IN TRANSACTIONS
```

```cql
:auto CALL {
    LOAD CSV FROM "file:///content.csv" AS line
    create (a:content{name:line[0]})
} IN TRANSACTIONS
```

```cql
:auto CALL {
    LOAD CSV FROM "file:///detail.csv" AS line
    create (a:detail{name:line[0]})
} IN TRANSACTIONS
```

### 2. 导入关系

```cql
LOAD CSV FROM "file:///relation1.csv" AS line
MATCH (from:subject{name:line[0]}),(to:module{name:line[1]})
merge (from)-[r:CONTAIN]->(to)
return r
```

```cql
LOAD CSV FROM "file:///relation2.csv" AS line
MATCH (from:module{name:line[0]}),(to:content{name:line[1]})
merge (from)-[r:CONTAIN]->(to)
return r
```

```cql
LOAD CSV FROM "file:///relation3.csv" AS line
MATCH (from:content{name:line[0]}),(to:detail{name:line[1]})
merge (from)-[r:CONTAIN]->(to)
return r
```

### 3. 删除所有节点和关系

```cql
MATCH (r)
DETACH DELETE r
```

