# Recovery by actual failure

Preserve staged content, user files and the exact operation. Raw hook/tool output may contain secrets; report sanitized diagnostics and affected paths, not matching credential values.

| Result | Action |
| --- | --- |
| `user_confirmation_required` / exit 78 | Show the returned current plan and wait for the actual reply; only then supply its token. Saved `auto` does not generate this consent prompt within its scope |
| `local_disabled` / `remote_disabled` | Respect the saved choice; change it only when the user requests a preference change |
| Plan, branch, repository or destination mismatch | Stop; reconcile the actual changed scope, never silently enlarge a standing grant |
| `permission_boundary` / exit 77 | Follow [permissions.md](permissions.md); same bounded operation through an available allowed tool permission path, no persistent-denial retry loop |
| Tool approval timeout/disconnect | Determine whether execution started and its effect; an allowed transient request has at most three total attempts, a denial is not transient |
| Existing `index.lock` / exit 73 | Preserve it; inspect ownership/concurrent operation, never delete it |
| Private operation lock / exit 73 | Another closeout may be active; inspect the process and recover separately. Only the creator automatically removes its own lock |
| Credential filename/pattern / exit 3 | Inspect named paths only; do not print the value. A tracked/history secret needs its own authorized remedy; adding an ignore rule does not erase it |
| Large/history scan limit, submodule or publication symlink | Obtain a separate concrete review plan; do not skip scanning or make a false full-history claim |
| Partial staging, detached HEAD, merge/rebase or nested changes | Preserve state; resolve through a separately scoped task |
| Hook/identity failure | Keep hooks active and inspect the concrete cause. Commit failure may leave staged files; do not amend or manually stage around the gate |
| Concurrent changes / exit 75 | Report remaining paths and known producers. No automatic extra commits under an old single-use approval |
| Remote divergence / unknown history | Stop; fetch/pull/merge is a separate authorized workflow, not an automatic repair |
| Timeout / remote effect not verified | Inspect actual local HEAD or remote tip before retry. Never claim success from an old receipt or blindly repeat a potentially completed push |

The legacy retry entrypoint is retained for compatibility but forwards once. It cannot grant permissions or repair an approval service. A successful operation should be followed by a new independent audit/status, and remote target verification where requested.
