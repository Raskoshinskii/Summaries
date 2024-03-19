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
    {$unset: {'school.websites.0': 1}} // The first element in websites array will be null
)

// $pull (Dropping a value from an embedded array)
db.users.update(
    {username: 'John123'},
    {$pull: {'school.websites':'A'}} // or $pullAll can be used to drop duplicates as well
)

// $unset turns a field or an array value into null
// $pull deletes a value in an array (to delete duplicates use $pullAll)

// $pop (Deletes an array element using its index. )
db.papers.update(
    {title:'Foetal distress in labour.'},
    {$pop: {authors: 1}} // 1: From the end, -1: From the beginning
)

// **Array Values Update**
db.users.update(
    {username: 'John123'},
    {$set: {'school.websites':'A'}} // substitutes the entire array into 'A'
)

db.users.update(
    {username: 'John123'},
    {$set: {'school.websites.0':'C'}} // sets an array element with an index 0 to 'C'
)

// $push (Element addition into an array)
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
                $position: 0,
                $slice: 2 // leaves only two values in an array
            }
        }
    }
)

// $each (Several Values Inserting). Often used along with $push, $addToSet
// $sort orders array elements after inserting
db.papers.update(
    {title:'Foetal distress in labour.'},
    {$push: 
        {authors: 
            {$each: 
                [
                    {'name': 'New_Author_2'},
                    {'name': 'New_Author_1'}
                ],
            $sort: {name: 1}
            }
        }
    }
)

// $addToSet similar to $push operator. However, it inserts values only if they don't exist in an array 
db.papers.update(
    {title:'Foetal distress in labour.'},
    {$addToSet: {authors: {name: 'New_Author_2'}}} // the document won't be updated because an array already has 'New_Author_2'
)
