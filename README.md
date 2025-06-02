# Agents-MCP-Hackathon

## Description

Do data migration with NLP

## User stories / use cases

+ User want to migrate a subset of data from DB A to DB B (analytics DB)
  + Example : get all users of company X from DB A and add them to DB B

## Features

+ **LLM generate read-only SQL query** to preview the data
+ User data preview confirmation
+ LLM genernate Python for DB migration
+ Migration preview (something like terraform plan, LIMIT 10)
+ Migration execution directly on python server
+ (Optional Prio 1) Generate a migration report
+ (Optional Prio 1) LLM generate and deploy migration script to temporal
+ (Optional Prio 2) Data exploration

## Input constraint / assumptions

+ Start with 2 SQLite
+ Start with DB that supports SQL
+ The migration happen to data of small scale that can be done with 1 server
+ User know what data they want to migrate, no need for data exploration

## System design

![1st architecture](/documentation/architecture.png)

## API endpoints

### Preview
`/preview/{source DB}/{destination DB}`
####  Description
Check the preview of the query, what will be change in the database

### Input

```json
{
  "source" : "SELECT $column1, $column2 FROM $table",
  "destination" : "INSERT INTO $table ($column1, $column2) "
}
```
### Output
```json
{
  "expected" : {
    "source" : "
    --- |column1 | column2 | 
    --- |--------|---------|
    --- | value1 | value2  |
    --- | value3 | value4  |
    --- |  ***   |   ***   |
    --- | value3 | value4  |
    --- |--------|----------
    ",
    "destination" : "
    +++ |column1 | column2 | 
    +++ |--------|---------|
    +++ | value1 | value2  |
    +++ | value3 | value4  |
    +++ |  ***   |   ***   |
    +++ | value3 | value4  |
    +++ |--------|----------
    
    "
  }
}
```

### Apply
`/apply/{source DB}/{destination DB}`
+ Description

Apply the change in the database

#### Input
```json
{
  source : "SELECT $column1, $column2 FROM $table",
  destination : "INSERT INTO $table ($column1, $column2) "
}
```
#### Output
```json
{
  "info" : {
    "success" : true,
    "failed value" : []
  }
  "expected" : {
    "source" : "
    --- |column1 | column2 | 
    --- |--------|---------|
    --- | value1 | value2  |
    --- | value3 | value4  |
    --- |  ***   |   ***   |
    --- | value3 | value4  |
    --- |--------|----------
    ",
    "destination" : "
    +++ |column1 | column2 | 
    +++ |--------|---------|
    +++ | value1 | value2  |
    +++ | value3 | value4  |
    +++ |  ***   |   ***   |
    +++ | value3 | value4  |
    +++ |--------|----------
    
    "
  }
}
```

### Revert
`/revert`

#### Description

Revert the last state of the databases
#### Input
.stateDB folder from a S3 bucket

+ Output
```json
{
  "info" : "success"
}
```

`<HTTP verb> <path>`

+ Description
+ Input
+ Output

## Database design + type interface

## UI by V0

## Other notes

+ Study how to do NL2SQL

## Execution Plan / Tasks

+ [ ] Build API endpoint
+ [ ] Define BaseModel Class for connector
+ [ ] Add 2 sql connector
+ [ ] Add apply endpoint with the 2 connector 
+ [ ] Test the endpoint
+ [ ] Add a preview endpoint
+ [ ] Add a S3 bucket to dumps/load data
+ [ ] Add more connector
+ [ ] First tasks

