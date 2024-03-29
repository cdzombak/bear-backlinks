#!/usr/bin/env python3

import bear
import datetime
import logging
import os
import time
import sys
import xcall

from config import be_verbose, get_backups_path


def main():
    logger = logging.getLogger('main')
    if be_verbose():
        logger.setLevel(logging.DEBUG)
        xcall.enable_verbose_logging()
    else:
        logger.setLevel(logging.INFO)

    # open the xcall app once to ensure callback url scheme is registered w/macOS:
    os.popen(f'open -a "{xcall.XCALL_PATH}"').read()
    time.sleep(1)  # allow xcall.app time to exit normally

    notes_needing_backlinks = {stub.to_note() for stub in bear.search_term('"## Backlinks"')}
    notes_needing_backlinks = {n for n in notes_needing_backlinks if ('---\n' in n.content and not n.trashed)}
    logger.info(f'{len(notes_needing_backlinks)} notes have Backlinks sections')

    # build a map of note -> stubs which link to this note
    backlinks = {}
    for note in notes_needing_backlinks:
        searches = note.backlink_search_terms
        stubs = set()
        for term in searches:
            stubs.update(bear.search_term(term))
        backlinks[note] = stubs
        logger.debug(f'Note {note.id} has {len(stubs)} backlinks')

    # build a map of note -> new content for that note, iff the content needs to change (ie. backlinks have changed)
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

    if len(new_note_content) == 0:
        logger.info("no notes need updating; all done!")
        sys.exit(0)

    # backup the notes we're about to update:
    backup_dir = os.path.join(get_backups_path(), datetime.datetime.now().strftime('%Y-%m-%dT%H-%M-%S%z'))
    os.mkdir(backup_dir)
    logger.info(f'backing up {len(new_note_content)} notes to {backup_dir}')
    for note in new_note_content.keys():
        fname = os.path.join(backup_dir, note.id+'.md')
        with open(fname, 'w') as f:
            f.write(note.content)

    # update each note that needs updating, in Bear:
    for note, new_content in new_note_content.items():
        logger.debug(f'updating content for note {note.id}')
        bear.replace_note_contents(note.id, new_content)

    logger.info(f'completed successfully; updated {len(new_note_content)} notes.')
    os.popen(f'terminal-notifier -message "✅ Updated Bear backlinks for {len(new_note_content)} notes." -title "Bear Backlinks" -sender net.shinyfrog.bear').read()


if __name__ == "__main__":
    main()
