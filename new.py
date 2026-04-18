try:
    
    message = input("Enter a short note: ")

    # 1b. Save to file (write mode)
    with open("notes.txt", "w") as file:
        file.write(message + "\n")

    print("\nSaved successfully!")

   
    with open("notes.txt", "r") as file:
        content = file.read()
        print("\nFile Content:")
        print(content)

   
    new_message = input("\nEnter another note: ")

    with open("notes.txt", "a") as file:
        file.write(new_message + "\n")

    
    with open("notes.txt", "r") as file:
        updated_content = file.read()
        print("\nUpdated File Content:")
        print(updated_content)


except FileNotFoundError:
    print("Error: File not found!")

except Exception as e:
    print("An error occurred:", e)