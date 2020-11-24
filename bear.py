import json

from config import get_bear_api_token
from xcall import xcall


class Note(object):
    """
    Note is a complete note as returned by bear://x-callback-url/open-note
    """

    def __init__(self, xcall_dict):
        """
        Args:
            xcall_dict: note dict as returned from xcall, including handling any weird escaping
        """
        self.title = xcall_dict['title']
        self.id = xcall_dict['identifier']
        self.content = xcall_dict['note']
        if xcall_dict['is_trashed'] == 'yes':
            self.trashed = True
        else:
            self.trashed = False

    @property
    def title_escaped_for_link(self):
        """
        Returns: the title of this note, properly escaped to put inside [[...]]
                 for a link.

        Notes:
            - Bear does not escape backticks in these links (`), but links including
              are not actually clickable, probably because the editor doesn't generally
              handle nested Markdown.

        """
        return self.title.replace('/', '\\/')

    @property
    def backlinks_search_terms(self):
        search_title = self.title
        if '"' in search_title or '“' in search_title or '”' in search_title:
            search_title = search_title.replace('“', '"')
            search_title = search_title.replace('”', '"')
            parts = search_title.split('"')
            search_title = ""
            for p in parts:
                p = p.strip()
                if len(p) == 0:
                    continue
                search_title = search_title + '"' + p + '"' + ' '
            search_title = search_title.strip()
        else:
            search_title = '"' + search_title + '"'
        search_id = '"'+self.id+'"'
        return [search_title, search_id]


class NoteStub(object):
    """
    NoteStub is a "stub" note as returned by bear://x-callback-url/search
    """

    def __init__(self, xcall_dict):
        """
        Args:
            xcall_dict: note dict as returned from xcall, including handling any weird escaping
        """
        self.title = xcall_dict['title']
        self.id = xcall_dict['identifier']

    def to_note(self) -> Note:
        return get_note(self.id)


class SearchResults(object):
    """
    SearchResults is an iterable collection of note stubs returned from a Bear search.
    It handles the weird double-JSON-encoding we're getting back from xcall.
    """

    def __init__(self, xcall_dict):
        self.note_stubs = [NoteStub(s) for s in json.loads(xcall_dict['notes'])]

    def __iter__(self):
        return iter(self.note_stubs)

    def __len__(self):
        return len(self.note_stubs)

    def __getitem__(self, i):
        return self.note_stubs[i]


def search_term(term: str) -> SearchResults:
    """
    Search Bear for the given term.

    See Also:
        https://bear.app/faq/X-callback-url%20Scheme%20documentation/#search

    Args:
        term: Term to search for.

    Returns:
        SearchResults
    """
    return SearchResults(xcall_dict=xcall('bear', 'search', {
        'term': term,
        'token': get_bear_api_token(),
        'show_window': 'no',
    }))


def get_note(note_id: str) -> Note:
    return Note(xcall_dict=xcall('bear', 'open-note', {
        'id': note_id,
        'show_window': 'no',
        'open_note': 'no',
    }))
