# support_bot.py

def show_help():
    print("Commands:")
    print(" help       - show available commands")
    print(" faq        - show common FAQ questions")
    print(" ticket     - create a support ticket (example: ticket my issue here)")
    print(" exit/quit  - close the chatbot")
    print()


def show_faq():
    print("FAQ QUESTIONS:")
    print(" - How do I reset my password?")
    print(" - What are your support hours?")
    print(" - How can I request a refund?")
    print()


def create_ticket(user_input):
    parts = user_input.split(" ", 1)

    if len(parts) == 1:
        print("Please describe your issue.")
        print("Example: ticket my app is freezing\n")
    else:
        issue = parts[1]
        print(f"Ticket created: {issue}\n")


def main():
    print("SupportBot is running. Type 'help' for commands.\n")

    while True:
        user_input = input("You: ").strip().lower()

        if user_input == "help":
            show_help()

        elif user_input == "faq":
            show_faq()

        elif user_input.startswith("ticket"):
            create_ticket(user_input)

        elif user_input in ("exit", "quit"):
            print("Closing SupportBot. Goodbye!")
            break

        else:
            print("I'm not sure about that.")
            print("You can type 'help' or create a ticket using 'ticket'.\n")


if __name__ == "__main__":
    main()