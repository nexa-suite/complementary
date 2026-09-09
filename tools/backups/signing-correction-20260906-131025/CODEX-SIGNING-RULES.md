# Nexa SSH signing rules

Before Codex creates any commit attributed to a Nexa contributor:

1. Human contributor must be explicitly selected.
2. Run `nexa-signing-status`.
3. Require `IDENTITY CONSISTENCY: PASS`.
4. Do not alter `user.name`, `user.email`, `user.signingkey`, or `gpg.format`.
5. Create commit normally.
6. Immediately verify `git log -1 --show-signature`.
7. Inspect `git show --show-signature --format=fuller HEAD`.
8. If signature or identity is incorrect, stop before push.
9. Never use Diego's key for another contributor's commit.
10. Never infer contributor identity from work performed.
