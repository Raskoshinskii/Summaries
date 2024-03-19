// Slicing Array Elements ($slice: idx_start, amount)
db.papers.find({}, {url: {$slice:1}}) // Selects all documents with the first element of url array

// Selects all documents where array references has elements starting from -3d element till the last one
db.papers.find({}, {references: {$slice:[-3, 3]}}) 

// Searching methods ($all, $size, $elemMatch)
db.papers.find({
    keywords: {$all: ['learning', 'reading']} // Finds all documents where the array keywords has 'learning' and 'reading'
})

// Finds all documents with an array size 2 and a keyword 'degeneration'
db.papers.find({
    lang: 'en',
    $and: [ {keywords: {$size:2}}, {keywords: {$all: ['degeneration']}}]    
})

// $elemMatch is used to apply conditions on embedded docuemtns in an array
db.papers.find({
    authors: {$elemMatch: {name: 'Carles Padró'}}
})
