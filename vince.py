def main():
    try:
        username = input("Enter Username: ")
        age_input = input("Enter Age: ")

        age = int(age_input)

        with open("users.txt", "a") as file:
            file.write(f"{username} - {age}\n")

        print("\nData saved successfully.")

        print("--- Saved Users ---")
        with open("users.txt", "r") as file:
            content = file.read()
            print(content)

    except ValueError:
        print("Error: Age must be a valid numerical integer.")
    except FileNotFoundError:
        print("Error: The file could not be found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        print("System complete.")

if __name__ == "__main__":
    main()