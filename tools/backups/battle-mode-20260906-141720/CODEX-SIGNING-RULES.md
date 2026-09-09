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
11. Never call `ssh-add -D`.
12. Contributor selection may remove only known Nexa signing keys; unrelated SSH authentication identities remain loaded.
13. Allowed-signers membership is mandatory for `IDENTITY CONSISTENCY: PASS`.
14. After contributor session, run `nexa-signing-stop`; it removes Nexa signing identities only.
15. Local PASS does not prove GitHub enrollment. After first real push, visually or via API verify the GitHub `Verified` badge.
16. Healthy empty `ssh-agent` is reachable; do not confuse exit status 1 with unavailable agent.
17. Do not derive a private key immediately before `ssh-add`; contributor enters passphrase once.
18. `nexa-signing-status` must report `LOCAL IDENTITY CONSISTENCY: PASS` before commit.
19. Status PASS requires exact same-entry email principal, key type, and key blob in `nexa_allowed_signers`.
20. Status PASS also requires no other known Nexa signing key loaded; unrelated authentication keys are allowed.
