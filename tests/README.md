# Tests

Run `python -B -m unittest discover -s tests -v` from the repository root. Tests cover bilingual fixture retrieval, metadata, evaluation validation, external private outputs, repository integrity, sanitized errors, and Git path rejection. All private-mode test content is invented and uses temporary directories outside Git. Symlink tests report a skip if OS permissions prevent creating links; Windows junctions are tested separately. No real private material is loaded.

Compatibility tests compare both CLI entry points and verify generic-setting precedence, legacy fallback, and fail-closed invalid settings. Metadata tests check optional domains and extensible language-tag syntax; they do not measure retrieval quality in additional languages. The historical test filename remains for continuity.
