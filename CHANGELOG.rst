Changelog
=========

Version 0.4.0
-------------

- Released at: 2012-04-24 15:07:58.
- `New feature <https://github.com/turicas/templater/issues/5>`_: named markers
  (new method ``add_headers``).
- `Bug fixed <https://github.com/turicas/templater/issues/7>`_: last blank
  wasn't being filled.
- `Bug fixed <https://github.com/turicas/templater/issues/6>`_: ignoring
  ``\r\n``/``\n`` in the end of files in ``save`` and ``open`` methods.
- `New Feature <https://github.com/turicas/templater/issues/6>`_: added method
  ``parse_file``.
- `Enhancement <https://github.com/turicas/templater/issues/2>`_: renamed
  ``tolerance`` to ``min_block_size``.
- Enhancement: refactored tests.
- Enhancement: refactored ``README.rst``.
- Enhancement: created ``CHANGELOG.rst``.


Version 0.3.0
-------------

- Released at: 2012-04-20 20:09:52.
- Enhancement: method ``save`` renamed to ``dump``.
- New feature: new methods ``save`` and ``open`` - saves and open the template
  to/from a document (file) - do not pickle the entire object as ``dump`` and
  ``load``.
- Enhancement: using nose coverage plugin.


Version 0.2.1
-------------

- Released at: 2012-04-30 18:34:35.
- Bug fixed: replaced ``README.markdown`` with ``README.rst`` in
  ``MANIFEST.in``.


Version 0.2.0
-------------

- Released at: 2012-04-20 18:30:23.
- `New feature <https://github.com/turicas/templater/issues/1>`_: ``tolerance``
  (min block size).
- Bug fixed: ``save`` and ``load`` now pickle the entire object (instead of
  only template definition).


Version 0.1.1
-------------

- Released at: 2012-04-20 15:08:05.
- Enhancement: ``README.markdown`` is now ``README.rst`` (reStructuredText).


Version 0.1.0
-------------

- Released at: 2012-04-20 14:57:44.
- First working version (``learn`` and ``parse`` methods created).
- New feature: ``save`` and ``load`` methods created.
- New feature: ``join`` method created.
