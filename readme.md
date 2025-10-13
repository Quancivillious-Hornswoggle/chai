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