// Filed Dropping 
db.users.update(
    {name: 'Alexa'}, 
    {$unset: {phones: 1}} // drops a nested document
) 

// Single Field Dropping ( several fields can be dropped)
db.users.update(
    {name: 'Jimmy'},
    {$unset: {loves_dogs: 1, surname: 1}} // drops a single filed 
) 

