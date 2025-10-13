import time
import os
from db_wrappers.flat_file_manager import FlatFileManager
import json

def main():
    """
    Main function to run the Chai AI chat application.
    Handles the REPL (Read-Eval-Print Loop) for user interaction.
    """
    print("Welcome to Chai!")
    user_id = input("Please enter your user ID to begin: ")


    # --- TODO 1: Instantiate the Database Wrapper ---
    # Create an instance of the FlatFileManager, passing the user_id to it.
    # This object will handle all our file reading and writing.
    # Specify the storage directory as "data"
    db_manager = FlatFileManager(storage_dir="data")

    # --- TODO 6 (do this last): Create a way for a user_id to have multiple conversation threads
    # Requirements:
    #   - If user already exists, then have the user select which thread (conversation_id) they want to use
    #       - Give the option to use a new thread
    #   - Proceed to run_chat() with the correct conversation_id
    #   Hint: This is not a "clean" addition, you may need to restructure how data is stored and indexed
    #         There are many ways to do this. Devise a plan and implement your own solution.

    # Get all conversation threads for this user
    user_threads = db_manager.get_user_threads(user_id)
    
    if len(user_threads) > 0:
        print("\nYour existing conversation threads:")
        for idx, thread_name in enumerate(user_threads, 1):
            print(f"{idx}. {thread_name}")
        print(f"{len(user_threads) + 1}. Create a new thread")

        while True:
            selection = input(f"\nSelect a thread (1-{len(user_threads) + 1}): ").strip()
            try:
                selection = int(selection)
                if 1 <= selection <= len(user_threads):
                    # User selected an existing thread
                    thread_name = user_threads[selection - 1]
                    print(f"\nOpening thread: '{thread_name}'")
                    break
                elif selection == len(user_threads) + 1:
                    # User wants to create a new thread
                    thread_name = input("Enter a name for the new thread: ").strip()
                    if not thread_name:
                        print("Thread name cannot be empty. Try again.")
                        continue
                    print(f"\nCreating new thread: '{thread_name}'")
                    break
                else:
                    print(f"Invalid selection. Please enter a number between 1 and {len(user_threads) + 1}.")
            except ValueError:
                print("Invalid input. Please enter a number.")
    else:
        # No existing threads, prompt for a new thread name
        print("\nWelcome! You don't have any conversation threads yet.")
        thread_name = input("Enter a name for your first thread: ").strip()
        if not thread_name:
            thread_name = "default"
            print(f"Using default thread name: '{thread_name}'")

    # Create the conversation_id from user_id and thread_name
    conversation_id = f"{user_id}_{thread_name}"
    run_chat(db_manager, conversation_id)

def run_chat(db_manager: FlatFileManager, conversation_id: str) -> None:
    # --- TODO 2: Check if conversation already exists, printout conversation if so ---
    #   - Add a timer that times how long it took to use get_conversation and print the results after
    start_time = time.perf_counter()
    messages = db_manager.get_conversation(conversation_id)
    end_time = time.perf_counter()
    duration = end_time - start_time

    if messages:
        print("\n--- Previous messages ---")
        for message in messages:
            role = message.get('role', 'unknown')
            content = message.get('content', '')
            if role == 'user':
                print(f"You: {content}")
            elif role == 'assistant':
                print(f"AI: {content}")
        print(f"--- End of history (Load time: {duration:.4f} seconds) ---\n")

    print(f"Conversation: '{conversation_id}'. Type 'exit' to quit.")

    while True:
        user_input = input("> ")
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break

        # --- TODO 3: Start the performance timer ---
        # Record the start time before performing the database operations.
        # Use time.perf_counter() for high precision.
        start_time = time.perf_counter()

        # --- TODO 4: Implement the Read-Append-Write Cycle ---
        # 1. Get the entire conversation history from the file (already loaded at start)
        # messages list is already in scope from above

        # 2. Append the new user message to the list of messages using messages.append()
        #    Each message should be a dictionary, e.g., {"role": "user", "content": user_input}
        messages.append({"role": "user", "content": user_input})

        # 3. Create a mock AI response and append it to the list.
        #    The AI response should also be a dictionary using format: {"role": "assistant", "content": ai_response}
        ai_response = "This is a mock response from the AI."
        messages.append({"role": "assistant", "content": ai_response})

        # 4. Save the *entire*, updated list of messages back to the file.
        #    Call your db_manager's save method.
        relative_filepath = f"{conversation_id}.json"
        db_manager.save_conversation(conversation_id, relative_filepath, messages)

        # ----------------------------------------------------

        # --- TODO 5: Stop the timer and calculate duration ---
        # Record the end time and calculate the difference to see how long the
        # entire read-append-write cycle took.
        end_time = time.perf_counter()
        duration = end_time - start_time
        # ---------------------------------------------------

        print(f"AI: {ai_response}")
        print(f"(Operation took {duration:.4f} seconds)")


if __name__ == "__main__":
    main()
