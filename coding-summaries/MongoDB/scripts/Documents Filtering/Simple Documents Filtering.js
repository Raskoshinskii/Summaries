// **Collection: papers**
// AND operator
db.papers.find({year: 2012, lang: 'en'})

// Array Conditions
db.papers.find({'keywords.0': 'fine arts'}) // all documents where the first array element is 'fine arts'

// Projection (defines what fields must be returned)
db.papers.find(
    {doc_type: 'Journal'}, // condition
    {_id: false, title: 1, year: true} // projection (either option: false or 1 can be used)
)
