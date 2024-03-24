// Single Document Update
db.users.updateOne(
    {name: 'John'},
    {$set: {age: 40}}
) 

// Multiple Documents Update
db.users.updateMany(
    {age: 20},
    {$set: {username: 'test123', hasCar: false}} // all documents that meet the condition will be updated
) 

// Update has additional parameters (e.g. {mullti: true})
db.users.update(
    {age: 23},
    {$set: {name: 'noname'}},
    {multi: true} // all documents that meet the condition will be updated
)

// Adding an embedded field into a document
db.users.update(
    {age: 18},
    {$set: {phone:
            {
                phone_name: 'iPhone',
                type: ['A', 'B', 'C'],
                year: 2018
            }
        }
    }
)

// Increasing Numeric Values using $inc
db.users.update(
    {username: 'John123'},
    {$inc: {'school.number': 2}}
)

// Multiplying Numeric Values using $mul
db.users.update(
    {username: 'John123'},
    {$mul: {'school.number': 10}}
)

// $max (a field will be updated only if a new value is greater than the current one)
db.users.update(
    {username: 'John123'},
    {$max: {'age': 24}} // John's age is 20, thus the field will be updated to 24
)

// $min (a field will be updated only if a new value is lower than the current one)
db.users.update(
    {username: 'John123'},
    {$min: {'age': 18}} // John's age is 20, thus the field will be updated to 18
)

// Document Replacement ( If a document meets the condition, it will be replaced) 
db.users.replaceOne(
    {username: 'jinny007'},
    {username: 'jinny007', age: 30, favColor: 'Red'},
    {upsert: true}
)

// Field Renaming
db.users.update({}, 
    {$rename: {'name': 'first_name'}} // rename field name to first_name in all documents
)