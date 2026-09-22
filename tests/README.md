# Tests

Run `python -B -m unittest discover -s tests -v` from the repository root. Tests cover bilingual fixture retrieval, metadata, evaluation validation, external private outputs, repository integrity, sanitized errors, and Git path rejection. All private-mode test content is invented and uses temporary directories outside Git. Symlink tests report a skip if OS permissions prevent creating links; Windows junctions are tested separately. No real private material is loaded.
