======
Rename
======

Massive renaming tool.

There is no ``rename`` utility on FreeBSD and Mac OS X, so I decide to write one for practice.

Usage
-----

``rename [options] match-pattern replace-pattern files``

* options

  - ``-v`` verbose mode, output every renaming. This is default.
  - ``-q`` quiet mode, just renaming without output.
  - ``-i`` interactive mode, ask every renaming to user. Override by ``-q`` argument.

* Patterns

  - Python ``re``.

* Files

  - ``files`` will be feed into ``ls -1``
