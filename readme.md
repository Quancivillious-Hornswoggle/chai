# Project: Chai (Chat + AI)

This repository contains the source code for the "Chai" command-line AI chat application, developed as part of the DBT230 course.

## Author

**Name: Ian**

## Lab 1: Flat-File Persistence

This lab focuses on building the foundational persistence layer using a simple flat-file (JSON) system. The goal is to establish a performance baseline for file I/O operations, which will serve as a benchmark for subsequent labs involving more advanced database technologies.

## Questions

1. What are two different designs you contemplated for your multiple conversations implementation?
    - I mostly focused on one design: using a user ID along with the conversation name to organize and store each conversation.
2. A vibe coder wants to make a quick MVP (minimum viable product) over the weekend that handles chat threads with AI models. Do you recommend using JSON files for persistence? Why?
    - Yes, I’d recommend using JSON because it’s simple, flexible, and easy to modify. You can name files however you want and structure the data in any format that fits your needs.
3. You are interviewing at OpenAI. The interviewer asks if you would use raw JSON files to store user chats or if you would use a database or other form of persistence and to explain your choice. How would you reply?
    - I would use JSON files to store user chats, maybe with a JSON to hold all chats for the user.

4. What did you notice about performance using this file storage method?
    - The performance was fast for small-scale data and simple read/write operations, but it might slow down as the data size or number of concurrent users increases.

## Lab 2 Questions
1. Performance Analysis
    * The time for flat file barely went up; however, MongoDB did go up more in relation to the flat file.
    * The read times were about the same as the append time.

2. Atomic Operations
    * Atomic operations are important where multiple messages are added rapidly to make sure all of the messages are saved properly.

3. Scalability
    * Flat files get slower as the number of users and threads grows because it has to read more files.
    * MongoDB can handle lots of users and threads with indexes, so finding threads and loading conversations stays fast.
    * Flat files can hit file system limits, but MongoDB can store millions of documents and supports replication.

4. Data Modeling Design Challenge
    * Storing messages inside the conversation (embedded) is fast and simple for reading the whole conversation.
    * Storing each message separately is better for searching, filtering, or really long conversations.
    * You’d use separate messages if the chat is huge or you need to do analytics on individual messages.