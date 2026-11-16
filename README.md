# Claude Code setup

Skills, the two judge agents (`critic-engineering`, `critic-design`) and the global `CLAUDE.md` files.

```bash
git clone git@github.com:andrei102896/skills.git ~/.claude/skills
cp -R ~/.claude/skills/global/. ~/
```

The second line installs `~/CLAUDE.md`, `~/.claude/CLAUDE.md` and `~/.claude/agents/critic-*.md`.
`global/` mirrors the home directory; edit there and re-run the `cp`, so the repo stays the source.

Plugins (run inside Claude Code):

```
/plugin marketplace add addyosmani/agent-skills
/plugin marketplace add multica-ai/andrej-karpathy-skills
/plugin marketplace add DietrichGebert/ponytail
/plugin install agent-skills@addy-agent-skills
/plugin install andrej-karpathy-skills@karpathy-skills
/plugin install ponytail@ponytail
```

SEO skills: https://github.com/AgriciDaniel/claude-seo
