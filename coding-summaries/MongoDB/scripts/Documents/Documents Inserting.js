// Single Document Inserting
db.users.insertOne({
    'username': 'John123',
    'name': 'John',
    'surname': 'Smith',
    'age': 20,
    'hasCar': true,
    'favFilms': ['Titanic', 'Iron Man'],
    'school': {
        'name': 'awesome school',
        'number': 3,
        'address': 'Awesome Street 7',
        'websites': ['A', 'B', 'C']
    }
})

// Multi Document Inserting
db.users.insertMany([
    {
        'username': 'alex444',
        'name': 'Alex',
        'age': 18,
        'hasCar': false,
    },
    {
        'username': 'alexa333',
        'name': 'Alexa',
        'phones':{
            'name': 'Iphone 10',
            'memoryGB': 64,
            'prodYear': 2020
        }
    }
])

// Any Type Inserting
db.users.insert(
    {
        'username': 'bond123',
        'name': 'Bond',
        'age': 18,
        'surname': 'James',
        'favFilms': ['James Bond Casino Royal']
    },
    {
        'username': 'jimmy631',
        'name': 'Jimmy',
        'loves_dogs': true,
        'age': 23,
        'surname': 'Kimmel'
    }
)

// Data Importing (Only using cmd line)
load('Path');