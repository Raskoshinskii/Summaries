// Single Document Deletion
db.users.deleteOne({username: 'jimmy631'})

// Multi Documents Deletion
db.users.deleteMany({age: 18})

// All Documents Deletion in a Collection
db.users.remove({}) // ! not efficient, better use drop() instead
db.users.remove({}, {justOne: true}) //deletes only one document

// The Entire Collection Dropping
db.users.drop()

// The Entire Database Dropping
db.dropDatabase()