// **Array Values Deletion**
// Values from an array can be deleted in several ways

// Set the whole array or embedded document to null
db.users.update(
    {name: 'John'},
    {$unset: {favFilms: 1}}
)

// Dropping an embedded field
db.users.update(
    {username: 'John123'},
    {$unset: {'school.name':1}}
) 

// Setting an array value to null (indexes start from 0)
db.users.update(
    {username: 'John123'},
    {$unset: {'school.websites.0': 1}} // the first element in websites array will be null
)

// Dropping a value from an embedded array
db.users.update(
    {username: 'John123'},
    {$pull: {'school.websites':'A'}}
)

// $unset turns a field or an array value into null
// $pull deletes a value in an array

// **Array Values Update**
db.users.update(
    {username: 'John123'},
    {$set: {'school.websites':'A'}} // substitutes the entire array into 'A'
)

db.users.update(
    {username: 'John123'},
    {$set: {'school.websites.0':'C'}} // sets an array element with an index 0 to 'C'
)

// Element addition into an array
db.users.update(
    {username: 'John123'},
    {$push: {'school.websites':'D'}} // 'D' will be added as the last element
)

// Array Element Inserting to a certain position
db.users.update(
    {username: 'bond123'},
    {$push: {favFilms: 
            {
                $each: ['New web'],
                $position: 0
            }
        }
    }
)
