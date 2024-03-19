// Index Creation (1: ASC order, 2: DESC order)
db.papers.createIndex({title: 1}) // Comarison: time execution: 00:00:01.238 (no index) and 00:00:00:002 (with index)

// Making Fields Values Unique
db.papers.createIndex({title: 1, url:1}, {unique: true}) // now it's impossible to insert papers with the same title and url

// All Indexes and Info
db.system.indexes.find()

// All Indexes For a Collection
db.papers.getIndexes()

// Index Dropping 
db.papers.dropIndex("title")