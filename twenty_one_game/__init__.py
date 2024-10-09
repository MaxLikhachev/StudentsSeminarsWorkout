from random import randint


CARDS_DATA = {
    "categories": ("+", "*", "o", "#"),
    "values": (
        {"label": "A", "score": 1},
        {"label": "2", "score": 2},
        {"label": "3", "score": 3},
        {"label": "4", "score": 4},
        {"label": "5", "score": 5},
        {"label": "6", "score": 6},
        {"label": "7", "score": 7},
        {"label": "8", "score": 8},
        {"label": "9", "score": 9},
        {"label": "10", "score": 10}, 
        {"label": "J", "score": 4},
        {"label": "Q", "score": 4},
        {"label": "K", "score": 4}
    )
}

MESSAGES = {
    "uncorrect_value": 'ERROR!: Uncorrect value',
    "take_card": "New card",
    "exit": "Exit",
    "win": lambda name: "'{}' win!!!".format(name),
    "loose": lambda name: "'{}' loose...".format(name),
    "continue": "",
}

CARDS_SHUFFLE_COUNT = 1000


def take_card():
    print(MESSAGES["take_card"])

    for index in range(len(GAME_DATA["players"])):
        card = GAME_DATA["deck"].pop()
        
        # BOT logic
        if GAME_DATA["players"][index]["mode"] == "auto" and GAME_DATA["players"][index]["score"] > 18:
            return exit()
                
        GAME_DATA["players"][index]["deck"] += [card]
        GAME_DATA["players"][index]["score"] += card["score"]

        player_view(GAME_DATA["players"][index])

    return result(players=GAME_DATA["players"], win_score=GAME_DATA["win_score"])
    


def exit():
    print(MESSAGES["exit"])
    result(players=GAME_DATA["players"], win_score=GAME_DATA["win_score"])



def card_view(card, is_print=False):
    result = "{}{}: {}".format(card["label"], \
        card["category"], \
        card["score"])
    if is_print:
        print(result)
    return result


def cards_view(cards):
    return ", ".join([card_view(card) for card in tuple(cards)]) 


def generate_cards(cards_data=CARDS_DATA):
    cards = [{
                "category": category,
                "label": value["label"],
                "score": value["score"]
            } for value in cards_data["values"] \
                for category in cards_data["categories"]]
    return cards


def shuffle(cards, count=CARDS_SHUFFLE_COUNT):
    cards = generate_cards()
    index_last = len(cards) - 1

    for _ in range(count):
        index_from = randint(0, index_last - 1)
        index_to = randint(index_from + 1, index_last)
        cards[index_to], cards[index_from] = cards[index_from], cards[index_to]

    return cards


def result(players=[{"score": 0}], win_score=0): 
    for player in players:
        score = player["score"]
        name = player["label"]

        is_high_score = False not in [score < item["score"] for item in players]
        is_win_score = score == win_score

        is_loose = score > win_score
        is_win = is_high_score and is_win_score

        if is_loose:
            print(MESSAGES["loose"](name))
            return True
        elif is_win: 
            print(MESSAGES["win"](name))
            return True
    else:
        return False


GAME_DATA = {
    "deck": [],
    "players": [{
        "label": "bot",
        "mode": "auto",
    },{
        "label": "user",
        "mode": "hand"
    }],
    "win_score": 21,
    "initial_score": 0,
    "initial_cards_count": 2,
    "result": result
}


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
    }
}]

def player_view(player):
    print("Player '{}' have a deck: {} with total count {}".format(player["label"], cards_view(player["deck"]), player["score"]))

def start_game():
    cards = shuffle(generate_cards())
    GAME_DATA["deck"] = cards

    players = GAME_DATA["players"]

    for player in players:
        player["score"] = GAME_DATA["initial_score"]
        player["deck"] = [cards.pop() for _ in range(GAME_DATA["initial_cards_count"])]
        for item in player["deck"]:
            player["score"] += item["score"]
        player_view(player)
    
    menu()
        

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
            is_exit = action() or item["is_exit"]
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
    start_game()


if __name__ == "__main__":
    main()