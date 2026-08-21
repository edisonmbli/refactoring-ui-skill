Put one markdown report per case in a dated folder:

    eval/runs/2026-08-20-claude/
      01-settings.md
      02-login.md
      ...

Then:

    python3 eval/score.py --dir eval/runs/2026-08-20-claude
