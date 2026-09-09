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
21. Normal Mode requires interactive contributor unlock when selecting identity.
22. Battle Mode uses one persistent dedicated agent per contributor after that contributor arms it once.
23. Battle Mode does not store passphrases and does not prove physical contributor presence at every commit.
24. Use `nexa-arm-contributor <username>` for initial unlock, `nexa-use-contributor --battle <username>` for armed sessions, and `nexa-run-as <username> -- <command>` for argv-safe execution.
25. Use `nexa-battle-status` before autonomous work; stale agents are `NOT_ARMED`.
26. Use `nexa-disarm-contributor <username>` or `nexa-disarm-all` after work; unrelated SSH agents remain untouched.
27. Use `nexa-battle-start` for one sequential five-contributor unlock session; it stops on first failure.
28. After `NEXA BATTLE MODE: 5/5 READY`, Codex may run authorized Git operations without further contributor passphrase interaction while agents remain alive.
