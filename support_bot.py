import json
import os
import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TICKETS_FILE = os.path.join(BASE_DIR, "tickets.json")

if not os.path.exists(TICKETS_FILE):
    with open(TICKETS_FILE, "w") as f:
        json.dump([], f)


FAQ_LIST = {
    "password": "How do I reset my password?",
    "support hours": "What are your support hours?",
    "refund": "How can I request a refund?"
}


def load_tickets():
    with open(TICKETS_FILE, "r") as f:
        return json.load(f)


def save_tickets(tickets):
    with open(TICKETS_FILE, "w") as f:
        json.dump(tickets, f, indent=2)


def show_help():
    print("Commands:")
    print(" help       - show available commands")
    print(" faq        - show FAQ questions")
    print(" ticket     - create a support ticket (example: ticket my issue)")
    print(" tickets    - show all tickets")
    print(" exit/quit  - close the chatbot")
    print()


def show_faq():
    print("FAQ QUESTIONS:")
    for answer in FAQ_LIST.values():
        print(" -", answer)
    print()


def suggest_faq(description):
    description_lower = description.lower()
    for keyword, faq in FAQ_LIST.items():
        if keyword in description_lower:
            return faq
    return None


def create_ticket(user_input):
    parts = user_input.split(" ", 1)
    if len(parts) == 1:
        print("Please describe your issue. Example:")
        print("ticket my app crashes\n")
        return

    description = parts[1]

    # Check FAQ suggestions
    suggestion = suggest_faq(description)
    if suggestion:
        print(f"It looks like your issue might be related to: {suggestion}")
        answer = input("Do you still want to create a ticket? (yes/no): ").strip().lower()
        if answer != "yes":
            print("Ticket creation canceled.\n")
            return

    tickets = load_tickets()
    if tickets:
        last_id = tickets[-1]["id"]
        try:
            last_num = int(last_id.split("-")[1])
        except ValueError:
            last_num = 0
        next_num = last_num + 1
    else:
        next_num = 1

    ticket_id = f"TCK-{next_num:04d}"

    ticket = {
        "id": ticket_id,
        "description": description,
        "status": "open",
        "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    tickets.append(ticket)
    save_tickets(tickets)
    print(f"Ticket created! Your ticket ID is {ticket_id}\n")


def show_all_tickets():
    tickets = load_tickets()
    if not tickets:
        print("No tickets found.\n")
        return

    print("All Tickets:")
    for t in tickets:
        print(f"{t['id']} | {t['status']} | {t['description']} | {t['created_at']}")
    print()


def main():
    print("SupportBot is running. Type 'help' for commands.\n")

    while True:
        user_input = input("You: ").strip().lower()

        if user_input == "help":
            show_help()
        elif user_input == "faq":
            show_faq()
        elif user_input == "tickets":
            show_all_tickets()
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