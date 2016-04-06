import trello
import re
import argparse
from config import KEY, TOKEN

REGEX_SCORE = r"^\(\d+\)"


def parse_args():
    parser = argparse.ArgumentParser(description='This will reset all points on your board with (0) on selected lists. Please be careful.')
    parser.add_argument('board_id', type=str, help='board id')
    parser.add_argument('-l', dest='list', nargs='+', help='Lists to use')
    parser.add_argument('--4-real', dest='dry_run', action='store_false', help='If this argument is set, then changes are permanent.')

    args = parser.parse_args()

    return args.board_id, args.dry_run, args.list


def main(board_id, dry_run, raw_lists):
    print "This will reset all points on your board with (0). Please be careful."
    if dry_run:
        print "NOTHING IS BEING CHANGED NOW. THIS IS DRY RUN. RUN WITH --4-real IF YOU WANT TO CHANGE ANYTHING."
    lists_to_use = map(lambda x: x.lower().strip(), raw_lists)
    trello_api = trello.TrelloApi(apikey=KEY, token=TOKEN)
    lists = trello_api.boards.get_list(board_id)
    list_ids_to_use = map(lambda x: x['id'], filter(lambda x: x['name'].lower() in lists_to_use, lists))
    cards_from_board = trello_api.boards.get_card(board_id)
    compiled = re.compile(REGEX_SCORE)
    for card in filter(lambda x: x['idList'] in list_ids_to_use, cards_from_board):
        matches = re.match(compiled, card['name'])
        if matches:
            print 'Reseting: {}'.format(card['name'])
            if dry_run is False:
                card_new_name = re.sub(compiled, '(0)', card['name'])
                trello_api.cards.update(card['id'], card_new_name)
        else:
            print 'Ignoring: {}'.format(card['name'])


if __name__ == '__main__':
    main(*parse_args())
