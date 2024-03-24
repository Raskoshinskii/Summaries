// Single Document Finding
db.papers.findOne({'keywords.0': 'fine arts'})

// Ordinary Query (Finds all documents)
db.papers.find({}) // {} can be ommited

// Projection (Defines what fields must be returned)
db.papers.find(
    {doc_type: 'Journal'}, // Condition
    {_id: false, title: 1, year: true} // Projection (either option: false or 1 can be used)
)

// Conditions for an array
db.papers.find({'keywords.0': 'fine arts'}) // All documents where the first array element is 'fine arts'

// Result Sorting
db.papers.find().sort({title: 1}) // 1: ASC, -1: DESC 

// $natural parameter (Returns documents in an order in which they were added in the collection)
db.papers.find().sort({$natural: 1})

// Result Skipping
db.papers.find().skip(3)

// Result Limiting
db.papers.find().limit(5)

// $exists finds documents where filed page_start exists
db.papers.find({
    page_start: {$exists: true}
})

// $type finds documents where certain fields have a certain type
db.users.find ({age: {$type:"string"}})

// regex is possible to apply
db.papers.find({
    title: {$regex: "Arm"}
})

// $inc (can be applied only to numeric values)
db.papers.update(
    {title: 'Arm attachment for mobile stackers'},
    {$inc: {year: 10}}
)