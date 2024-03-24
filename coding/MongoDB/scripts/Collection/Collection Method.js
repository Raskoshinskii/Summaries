// Collection Creation
db.createCollection('users')

// Collection Renaming
db.users.renameCollection('new_name')

// Capped Collections Creation (Limitted collections)
db.createCollection('users', {capped: true, size: 10000}) // capped collection Limitted by size

db.createCollection('users', {capped: true, size: 10000, max: 200}) // capped collection Limitted by size and by number of documents max 200

// Collection Dropping
db.collection.dcrop()