#!/usr/bin/env python3

import bear


def main():
    # results = bear.search_term('"## Backlinks"')
    # for stub in results:
    #     print(f'{stub.title} ({stub.id})')
    #
    # note = results[0].to_note()
    # print(f'{note.title} ({note.id})\n{note.content}')

    note = bear.get_note('5633AFE0-42CA-4A1A-A7FD-4DA2DCD98804-40661-000014305ECC282B')
    print(note.title_escaped_for_link)
    print(note.backlinks_search_terms)


if __name__ == "__main__":
    main()
