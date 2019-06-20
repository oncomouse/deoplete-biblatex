#!/usr/bin/env
import re
import os
import subprocess
from shlex import quote

from .base import Base
from deoplete.util import load_external_module

load_external_module(__file__, 'sources/deoplete_biblatex')

class Source(Base):
    def __init__(self, vim):
        super().__init__(vim)

        self.filetypes = ['pandoc', 'markdown']
        self.mark = '[bib]'
        self.name = 'biblatex'
        self.vars = {
            'bibfile': '~/bibliography.bib',
            'delimiter': ',',
            'startpattern': r'\[(?:[\w,]+:)?',
            'keypattern': r'@?[\w-]+',
            'reloadbibfileonchange': 0,
            'addinfo': 0
        }

    def __make_dictionary(self, line):
        match = re.match(r'(^.*?)\s+\(([0-9]{0,4})\) (.*?)\[([^\]]+)\] \@(.*)$', line)
        if match:
            return {
                "author": match.group(1),
                "plain_date": match.group(2),
                "plain_title": match.group(3).split(",")[0],
                "ENTRYTYPE": match.group(4),
                "ID": match.group(5)
            }
        else:
            return None

    @property
    def __bibliography(self):
        # output = re.sub(r'\x1b\[.*?m','', subprocess.Popen("bibtex-ls {}".format(quote(self.__bib_file)), stdout=subprocess.PIPE, shell=True).communicate()[0].decode("utf-8")).split("\n")[0:-1]
        # return [i for i in list(map(self.__make_dictionary, output)) if i]
        if self.__reload_bibfile_on_change:
            mtime = os.stat(self.__bib_file).st_mtime
            if mtime != self.__bib_file_mtime:
                self.__bib_file_mtime = mtime
                self.__read_bib_file()

        return self.__bibliography_cached

    def __read_bib_file(self):
        output = re.sub(r'\x1b\[.*?m','', subprocess.Popen("bibtex-ls {}".format(quote(self.__bib_file)), stdout=subprocess.PIPE, shell=True).communicate()[0].decode("utf-8")).split("\n")[0:-1]
        self.__bibliography_cached = [i for i in list(map(self.__make_dictionary, output)) if i]

    def on_init(self, context):
        bib_file = self.get_var(
            'bibfile'
        )
        bib_file = os.path.abspath(os.path.expanduser(bib_file))

        self.__bib_file = bib_file
        self.__bib_file_mtime = os.stat(bib_file).st_mtime
        self.__read_bib_file()

        pattern_delimiter = self.get_var(
            'delimiter'
        )
        pattern_start = self.get_var(
            'startpattern'
        )
        pattern_key = self.get_var(
            'keypattern'
        )

        pattern_current = r'{}$'.format(pattern_key)
        pattern_completed = r'(?:{}{})*'.format(pattern_key, pattern_delimiter)

        self.__pattern = re.compile(
            pattern_start
            + pattern_completed
            + pattern_current
        )

        reload_bibfile_on_change = self.get_var(
            'reloadbibfileonchange'
        )
        reload_bibfile_on_change = bool(reload_bibfile_on_change)

        self.__reload_bibfile_on_change = reload_bibfile_on_change

        add_info = self.get_var(
            'addinfo'
        )
        add_info = bool(add_info)

        self.__add_info = add_info

    def __format_menu(self, entry):
        return '{title}'.format(
            title=('{}'.format(entry['plain_title'])
                   if 'plain_title' in entry else '')
        )
    def __format_info(self, entry):
        return '{title}{author}{date}'.format(
            title=('Title: {}\n'.format(entry['plain_title'])
                   if 'plain_title' in entry else ''),
            author=(
                'Author{plural}: {author}\n'.format(
                    plural='s' if len(entry['author']) > 1 else '',
                    author=entry['author'],
                )
                if 'author' in entry else ''
            ),
            date=('Year: {}\n'.format(entry['plain_date'])
                  if 'plain_date' in entry else ''),
        )

    def __entry_to_candidate(self, entry):
        candidate = {
            'abbr': entry['ID'],
            'word': entry['ID'],
            'kind': entry['ENTRYTYPE'],
        }
        candidate['menu'] = self.__format_menu(entry)

        if self.__add_info:
            candidate['info'] = self.__format_info(entry)

        return candidate

    def gather_candidates(self, context):
        if self.__pattern.search(context['input']):
            candidates = [
                self.__entry_to_candidate(entry)
                for entry in self.__bibliography
            ]
            return candidates
        else:
            return []
