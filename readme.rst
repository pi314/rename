======
Rename
======

Massive renaming tool.

There is no ``rename`` utility on FreeBSD and Mac OS X, so I decide to write one for practice.

Usage
-----

``rename [options] match-pattern replace-pattern files``

* Options

  - ``-t``

    + Transaction mode
    + Default: False
    + Everything will be done together, no partial renameing will be done

  - ``-i``

    + Interactive Mode
    + Default: False
    + Ask every renaming to user
    + Can be overrided by ``-t`` argument. (Ask only once)

* Patterns

  - Python ``re``

Example
-------

* ``$ rename '\.htm' .html *`` renames all ``.htm`` in file names with ``.html`` end.

