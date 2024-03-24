// Simple Documents Grouping 
db.papers.aggregate([
    {$group: {_id: 'year'}} // Groups documents by year
])

// Counts all document groups
db.papers.aggregate([
    {$group: {_id: 'year'}},
    {$count: 'total'},
])

// Counts number of papers in each year
db.papers.aggregate([
    {$group: {_id: '$year', total: {$sum: 1}}},
    {$sort: {_id: -1}}
])

// $sortByCount combines grouping, counting and sorting in DESC order
db.papers.aggregate([
    {$sortByCount: '$year'}
])

// $match and $projection (Filters out values that don't meet a condition)
db.papers.aggregate([
    {$match: {lang: 'en'}}, // finds only eng papers
    {$project: {_id: 0, title:1, lang: 1, year:1}}, // select only title, lang and a year
    {$limit: 10}, // limits by 10 documents
    {$sort: {year: -1}} // sorts by 
])

/* 
$unwind example ($unwind doesn't output a document if the field value is null, missing, or an empty array)

To include null/empty or missing values use preserveNullAndEmptyArrays: true

To unwind embedded arrays, apply unwind twice
*/

db.papers.aggregate(
    [
        {$unwind: '$authors'}, // unwinds the document by authors
        {$group: {_id: '$authors', total_papers: {$sum: 1}}}, // group by them
        {$sort: {total_papers: -1}}, //  find top 10 by number of papers
        {$limit: 10}
    ],
    {allowDiskUse: true} // use this to resolve a memory limitation (by default 100 Mb)
)