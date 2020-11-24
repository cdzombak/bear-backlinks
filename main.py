#!/usr/bin/env python3
import time

import bear
import datetime
import logging
import os

from config import get_backups_path
from mac import copy_to_clipboard


def main():
    logger = logging.getLogger('main')
    # logger.setLevel(logging.DEBUG)
    logger.setLevel(logging.INFO)

    notes_needing_backlinks = {stub.to_note() for stub in bear.search_term('"## Backlinks"')}
    notes_needing_backlinks = {n for n in notes_needing_backlinks if not n.trashed}
    logger.info(f'{len(notes_needing_backlinks)} notes need backlink updates')

    backlinks = {}
    for note in notes_needing_backlinks:
        searches = note.backlink_search_terms
        stubs = set()
        for term in searches:
            stubs.update(bear.search_term(term))
        backlinks[note] = stubs
        logger.debug(f'Note {note.id} has {len(stubs)} backlinks')

    new_note_content = {}
    for note, backlink_stubs in backlinks.items():
        if len(backlink_stubs) == 0:
            backlinks_md = '_No backlinks found._\n'
        else:
            backlinks_md = ''
            stubs_sorted = sorted(backlink_stubs, key=lambda stub: stub.title.lower())
            for stub in stubs_sorted:
                backlinks_md = f'{backlinks_md}- [[{stub.title_escaped_for_wiki_link}]]\n'
        backlinks_md = backlinks_md + '\n'
        note_parts = note.content.split('## Backlinks\n')
        if len(note_parts) < 2:
            logger.warning(f'{note} does not have a Backlinks header; skipping it to avoid unspecified behavior')
            continue
        if len(note_parts) > 2:
            logger.info(f'{note} has multiple backlink headers; we will populate the last one')
        pre_backlinks = '## Backlinks\n'.join(note_parts[:-1]) + '## Backlinks\n'
        footer_parts = note_parts[-1].split('---')
        if len(footer_parts) < 2:
            logger.warning(f'{note} does not have a horizontal rule (---) after its backlinks header; skipping it to avoid clobbering the rest of the note')
            continue
        old_backlinks = footer_parts[0]
        post_backlinks = '---' + '---'.join(footer_parts[1:])
        if old_backlinks == backlinks_md:
            logger.debug(f'note {note} does not have updated backlinks; skipping it')
            continue
        new_note_content[note] = pre_backlinks + backlinks_md + post_backlinks

    backup_dir = os.path.join(get_backups_path(), datetime.datetime.now().strftime('%Y-%m-%dT%H-%M-%S%z'))
    os.mkdir(backup_dir)
    logger.info(f'backing up {len(new_note_content)} notes to {backup_dir}')
    for note in new_note_content.keys():
        fname = os.path.join(backup_dir, note.id+'.md')
        with open(fname, 'w') as f:
            f.write(note.content)

    for note, new_content in new_note_content.items():
        bear.open_note_for_edit(note.id)
        logger.debug(f'updating content for note {note.id}')
        copy_to_clipboard(new_content)
        time.sleep(0.5)
        os.popen("""osascript -e 'tell application "Bear" to activate' -e 'delay 1' -e 'tell application "System Events" to keystroke "a" using command down' -e 'delay 0.5' -e 'tell application "System Events" to keystroke "v" using command down'""").read()
        time.sleep(0.5)

    logger.info(f'completed successfully; updated {len(new_note_content)} notes.')
    os.popen(f'terminal-notifier -message "✅ Updated Bear backlinks for {len(new_note_content)} notes." -title "Bear Backlinks" -sender net.shinyfrog.bear').read()


if __name__ == "__main__":
    main()
