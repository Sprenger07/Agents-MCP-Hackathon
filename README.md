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

`<HTTP verb> <path>`

+ Description
+ Input
+ Output

## Database design + type interface

## UI by V0

## Other notes

+ Study how to do NL2SQL

## Execution Plan / Tasks

+ [ ] First tasks
