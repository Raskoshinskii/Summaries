/* 
All Logical operators has the following syntax (except for $not):
{ $log_operator: [ { <bool expression1> }...{ <bool expressionn> } 
*/

// AND
db.papers.find({year: 2012, lang: 'en'}) // the ordinary one 

// Uisng $and
db.papers.find({
    $and:
        [
            {year: 2012}, 
            {lang: 'en'}
        ]
})

// OR
db.papers.find({
    lang: 'en',   
    $or: 
        [
            {'authors.name': 'Mats Johansson'}, // Combination of AND and OR operators
            {'authors.name': 'Thomas Vamos'}
        ]
})

// NOT can be used only with operator expression (e.g. $eq, $ne and so forth)
db.papers.find({
    lang: {$not: {$eq:'en'}}
})

// NOR returns condittions to negative (i.e. year != 2013 and doc_type != 'Journal' )
db.papers.find({
    lang: 'en',
    $nor:
        [
            {doc_type: 'Journal'},
            {year: 2013}
        ]
    
})