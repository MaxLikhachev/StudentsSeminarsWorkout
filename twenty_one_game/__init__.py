CARDS_DATA = {
    "categories": ("+", "*", "o", "#"),
    "values": (
        {"label": "A", "count": 11},
        {"label": "2", "count": 2},
        {"label": "3", "count": 3},
        {"label": "4", "count": 4},
        {"label": "5", "count": 5},
        {"label": "6", "count": 6},
        {"label": "7", "count": 7},
        {"label": "8", "count": 8},
        {"label": "9", "count": 9},
        {"label": "10", "count": 10}, 
        {"label": "J", "count": 4},
        {"label": "Q", "count": 4},
        {"label": "K", "count": 4}
    )
}

MESSAGES = {
    "uncorrect_value": 'ERROR!: Uncorrect value',
    "take_card": "New card",
    "exit": "Exit"
}


def take_card():
    print(MESSAGES["take_card"])


def exit():
    print(MESSAGES["exit"])


def card_view(card):
        print("{}{}: {}".format(card["label"], \
            card["category"], \
            card["count"]))


def cards_view(cards):
    for card in tuple(cards):
        card_view(card)


def generate_cards(cards_data=CARDS_DATA):
    cards = ({
                "category": category,
                "label": value["label"],
                "count": value["count"]
            } for value in CARDS_DATA["values"] \
                for category in CARDS_DATA["categories"])
    cards_view(cards)



MENU_ITEMS = [{
    "value": "1",
    "is_exit": False,
    "action": take_card,
    "messages": {
        "before": "1. Take a card",
        "after": "Taking a card..."
    },
},
{
    "value": "2",
    "is_exit": True,
    "action": exit,
    "messages": {
        "before": "2. Don't take a card and finish the game",
        "after": "Finishing the game..."
    },
},
{
    "value": "3",
    "is_exit": True,
    "action": generate_cards,
    "messages": {
        "before": "3. Generate card",
        "after": "Cards generating..."
    },
}]


def menu(items=MENU_ITEMS):
    def choose():
        for item in items:
            print(item["messages"]["before"])
        value = str(input("\nChoose a value: "))
        return value


    def analyse(value):
        def correct_action(items_values):
            def find_item_and_index(items_values):
                index = items_values.index(value)
                item = items[index]
                return item

            item = find_item_and_index(items_values)
            print(item["messages"]["after"])
            action = item["action"]
            action()
            is_exit = item["is_exit"]
            return is_exit
        
        def uncorrect_action():
            print(MESSAGES["uncorrect_value"])
            return False

        items_values = [item["value"] for item in items]
        
        return correct_action(items_values) \
        if value in items_values \
        else uncorrect_action()

    is_exit = False
    while not is_exit:
        value = choose()
        is_exit = analyse(value)


def main():
    menu()


if __name__ == "__main__":
    main()