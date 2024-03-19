// $eq 
db.papers.find({page_end: {$eq: '279'}})

// $ne 
db.papers.find({doc_type: {$ne: 'Journal'}})

// $gt and $gte
db.papers.find({year: {$gt: 2000}})
db.papers.find({year: {$gte: 2000}})

// $lt and $lte
db.papers.find({year: {$lt: 2000}})
db.papers.find({year: {$lte: 2000}})

// $in and $nin
db.papers.find({doc_type: {$in: ['Conference', 'Journal']}})
db.papers.find({doc_type: {$nin: ['Conference', 'Journal']}})

