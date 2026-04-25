try:
    
    username = input("Enter Username: ").strip()
    age = int(input("Enter Age: "))

    if username == "" or age <= 0:
        print("Invalid input!")
    else:
        
        with open("users.txt", "a") as file:
            file.write(f"{username} - {age}\n")

        print("\nUser saved successfully!")

        print("\n=== Saved Users ===")
        with open("users.txt", "r") as file:
            print(file.read())

except ValueError:
    print("Error: Age must be a number!")

except Exception as e:
    print("An error occurred:", e)

finally:
    print("\nSystem complete.")