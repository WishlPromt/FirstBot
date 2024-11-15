import json

def load_base():
    with open('preposition.json', 'r', encoding='utf-8') as file:
        base = json.load(file)
        return base

def save_base(base):
    with open('preposition.json', 'w', encoding='utf-8') as file:
        json.dump(base, file, indent=4, ensure_ascii=False)
        file.close()


def add_card_to_prep(card, user, comment):
    base = load_base()

    base[user['id']] = {'card': card,
                        'username': user['username'],
                        'comment': comment}

    save_base(base)
