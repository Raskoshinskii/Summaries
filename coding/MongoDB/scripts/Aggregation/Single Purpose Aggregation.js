// Count
db.papers.count() // Counts all documents in a collection
db.papers.find({doc_type: 'Journal'}).skip(10).count(true) // Counts documents where doc_type: 'Journal' (to use count with skip provide count(true))

// Distinct
db.papers.distinct('doc_type')

// estimatedDocumentCount
db.papers.estimatedDocumentCount()