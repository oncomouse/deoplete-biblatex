# deoplete-biblatex

This is a port of [lionawurscht/deoplete-biblatex](https://github.com/lionawurscht/deoplete-biblatex) that uses [msprev/fzf-bibtex](https://github.com/msprev/fzf-bibtex) instead of [sciunto-org/python-bibtexparser](https://github.com/sciunto-org/python-bibtexparser). The Python bibtexparser library was throwing an error I couldn't figure out and is marked as no longer maintained. I'm already using `FZF-BibTeX`, so I figured why not reuse that project.

There are probably limitations to this implementation; I would strongly encourage you to use the original instead.

*Below is a modified version of the original README*

---

`Deoplete-biblatex` offers completion of biblatex ids. By default it looks for
citations of this pattern:

~~~markdown
   [AGreatCitation....

   [@AGreatCitation....

   [AGreatCitation,AnotherCitation....

   [@AGreatCitation,@AnotherCitation....

   [author:AGreatCitation...

   [author,authornumb:AnotherCitation...
~~~

## Required

- [`Neovim`](https://neovim.io)
- [`Deoplete`](https://github.com/Shougo/deoplete.nvim)
- [`FZF-BibTeX`](https://github.com/msprev/fzf-bibtex)
- [Go](https://golang.org/) (for `FZF-BibTeX`)

## Installation

To install `deoplete-biblatex`, use your favorite [`Neovim`](https://neovim.io)
plugin manager.


### [`vim-plug`](https://github.com/junegunn/vim-plug)

~~~

   Plug 'Shougo/deoplete.nvim', { 'do': ':UpdateRemotePlugins' }
   Plug 'oncomouse/deoplete-biblatex'
~~~

## Documentation

For information on the configuration see ``:help deoplete-biblatex``

