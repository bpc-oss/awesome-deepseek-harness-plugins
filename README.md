# Awesome DeepSeek Harness Plugins

A curated list of plugins, tools, skins, bridges, and extensions for
[DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) (DSH) — the
open-source agent framework from DeepSeek, built on the motto
**"Everything is a Plugin."**

DSH launched its developer preview on **2026-08-13** (MIT license, Cordis-based).
Within a day the community shipped a wave of plugins; this list tracks the
notable ones and points to the rest.

> Star counts are a launch-day snapshot (2026-08-13) and drift fast. For the
> unmoderated, auto-refreshed index of every repo tagged `dsh-plugin`, see
> [PLUGINS.md](PLUGINS.md) (regenerated daily by
> [update.yml](.github/workflows/update.yml)).

## Contents

- [How to install a plugin](#how-to-install-a-plugin)
- [Official built-in plugins](#official-built-in-plugins)
- [Community plugins](#community-plugins)
  - [Web UI & Skins](#web-ui--skins)
  - [Terminal & Desktop](#terminal--desktop)
  - [Vision & Multimodal](#vision--multimodal)
  - [Tools & Editor UX](#tools--editor-ux)
  - [Agent orchestration & Workflow](#agent-orchestration--workflow)
  - [Integrations & Bridges](#integrations--bridges)
  - [Sidebar, Workspace & Ecosystem](#sidebar-workspace--ecosystem)
  - [Fun & Misc](#fun--misc)
- [Other awesome lists (meta)](#other-awesome-lists-meta)
- [Contributing](#contributing)

## How to install a plugin

DSH loads plugins as [Cordis](https://github.com/cordiverse/cordis) bundles.
Two common paths:

```sh
# npm-scoped plugin (recommended)
dsh plugin add <npm-package>

# repo-hosted plugin (the .dsh-plugin format)
# add to your profile's cordis.yml, or via the CLI patch layer:
# github:<owner>/<repo>#<ref>&path:/.dsh-plugin
```

Start the Web UI and manage models/workspaces there:

```sh
dsh web            # http://127.0.0.1:3080
```

## Official built-in plugins

The framework itself ships ~50 internal plugin packages under the
`@deepseek-ai/dsh-*` npm scope. They are the reference implementations and the
building blocks every community plugin extends. Highlights:

- **`deepseek-ai/deepseek-harness`** — the framework and all built-in packages.
  See [`packages/README`](https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/README.md)
  for the full map: `llm` (model adapters), `shell`/`terminal`/`code-runtime`
  (execution), `fs`/`lsp` (files & language servers), `web` (search/fetch),
  `subagent` (delegation), `plan`, `sandbox`, `hooks`, `skill`, `compaction`,
  `extensions` (runtime self-modifying plugins), and the `web`/`cli` apps.

Everything below is community-built and sits on top of these seams.

## Community plugins

### Web UI & Skins

- [zhu1090093659/dsh-web-ui](https://github.com/zhu1090093659/dsh-web-ui) (★300) — Plugin & skin collection for the DSH Web UI: task board, git graph, right-side panel, remote mobile UI, pet, live token stats, skin center.
- [Small-tailqwq/dsh-deep-whale](https://github.com/Small-tailqwq/dsh-deep-whale) (★56) — "Whale-girl" skin series (maid-atelier), CC BY-NC-SA 4.0.
- [Nagi-ovo/dsh-ads](https://github.com/Nagi-ovo/dsh-ads) (★61) — Tongue-in-cheek 2005-style Chinese-site ads in the sidebar / chat feed / popups.
- [alingalingling/ui-status-label](https://github.com/alingalingling/ui-status-label) (★18) — Customize the "deep diving" thinking-status label however you like.
- [omdsh-dev/dsh-genui](https://github.com/omdsh-dev/dsh-genui) (★9) — GenUI: interactive components (layout, charts, mermaid, 3D) rendered inline via the `dsh-ui` fence.
- [vlln/whale-girl](https://github.com/vlln/whale-girl) (★10) — Desktop-pet plugin (QQ-pet style): draggable, feedable, accumulative companion.
- [Nagi-ovo/dsh-visualize](https://github.com/Nagi-ovo/dsh-visualize) (★15) — Generative UI: the model draws interactive HTML cards straight into the chat stream.
- [ZSeven-W/dsh-openpencil](https://github.com/ZSeven-W/dsh-openpencil) (★19) — OpenPencil design preview & editing plugin.
- [omdsh-dev/dsh-annotation](https://github.com/omdsh-dev/dsh-annotation) (★9) — Select text → annotate → send as a message; bubble-hidden annotation blocks.
- [Anionex/dsh-computer-use](https://github.com/Anionex/dsh-computer-use) (★6) — Computer-use plugin for DSH.

### Terminal & Desktop

- [ccch1mneyyy/dsh-cc-tui](https://github.com/ccch1mneyyy/dsh-cc-tui) (★96) — Claude Code-style full-screen TUI: pixel-whale top bar, live status row, streaming thoughts, double-Esc rollback, context bar + TPS meter. One-line npm install.
- [huiliyi37/dsh-tianshu-tui](https://github.com/huiliyi37/dsh-tianshu-tui) (★53) — DSH terminal UI.
- [chen-001/dsh-grok-tui](https://github.com/chen-001/dsh-grok-tui) (★5) — Grok-style TUI.
- [hust-open-atom-club/oh-dsh-desktop](https://github.com/hust-open-atom-club/oh-dsh-desktop) (★46) — Extensible macOS workbench: native PTY, workspace tools, live bilingual plugins, isolated-preview plugin marketplace.
- [Ruler4396/dsh-launcher](https://github.com/Ruler4396/dsh-launcher) (★9) — Lightweight Windows launcher: silent logon autostart + a minimal WebView2 window instead of a full browser.
- [bitterSmilezzz/dsh-mac-desktop](https://github.com/bitterSmilezzz/dsh-mac-desktop) (★1) — macOS desktop wrapper.
- [hanelalo/browser-bridge](https://github.com/hanelalo/browser-bridge) (★17) — Let your agent drive your real browser window like you would.
- [Lum1104/dsh-browser](https://github.com/Lum1104/dsh-browser) (★16) — Chrome sidebar extension so DSH operates your browser directly, no vision needed.
- [whiteguo233/dsh-openbiliclaw](https://github.com/whiteguo233/dsh-openbiliclaw) (★4) — Bilibili integration for DSH.

### Vision & Multimodal

- [Anionex/dsh-vision-toolkit](https://github.com/Anionex/dsh-vision-toolkit) (★106) — Vision toolkit for text-only models: intent-aware image Q&A, long-screenshot OCR, UI restoration, grounding, pixel diff, Artifacts, Web UI.
- [zhouwumu2-lab/dsh-vision-fix](https://github.com/zhouwumu2-lab/dsh-vision-fix) (★10) — Vision fix / repair helper.
- [sjscy05/deepseek-harness-vision-plugin](https://github.com/sjscy05/deepseek-harness-vision-plugin) — Vision plugin for DSH.
- [good-boy4069/Deepseek-omnimodal](https://github.com/good-boy4069/Deepseek-omnimodal) (★2) — Omnimodal support.
- [YYTbit/dsh-plugin-vision-toolkit](https://github.com/YYTbit/dsh-plugin-vision-toolkit) — Vision-toolkit bridge.

### Tools & Editor UX

- [omdsh-dev/dsh-at-file](https://github.com/omdsh-dev/dsh-at-file) (★21) — Codex-style `@file` mentions: search workspace files in the composer and attach their contents to prompts.
- [omdsh-dev/dsh-custom-tool](https://github.com/omdsh-dev/dsh-custom-tool) (★17) — Create & manage sandboxed JavaScript tools with a Monaco editor and model-driven tool lifecycle.
- [Moeblack/dsh-message-edit](https://github.com/Moeblack/dsh-message-edit) (★9) — Branch-based message editing, reroll, retry, version timeline.
- [Anionex/dsh-turn-rewind](https://github.com/Anionex/dsh-turn-rewind) (★16) — Rewind conversation + workspace state via a persistent Change Ledger.
- [Electricitysheep/dsh-tool-turbo](https://github.com/Electricitysheep/dsh-tool-turbo) (★1) — Tool turbo.
- [LingLambda/dsh-undo](https://github.com/LingLambda/dsh-undo) (★1) — Undo support.
- [fakechris/dsh-track](https://github.com/fakechris/dsh-track) (★1) — Tracking helper.
- [omdsh-dev/dsh-plugin-skills](https://github.com/omdsh-dev/dsh-plugin-skills) (★1) — Skills plugin.
- [omdsh-dev/dsh-mnemon](https://github.com/omdsh-dev/dsh-mnemon) (★1) — Mnemonics plugin.
- [ArtificialNotImbecile/dsh-context-taxonomy](https://github.com/ArtificialNotImbecile/dsh-context-taxonomy) — Context taxonomy.

### Agent orchestration & Workflow

- [NanmiCoder/dsh-agent-teams](https://github.com/NanmiCoder/dsh-agent-teams) (★30) — AgentTeams plugin for DSH.
- [icetomoyo/dsh_workflow](https://github.com/icetomoyo/dsh_workflow) (★29) — Brings Claude Code's UltraCode to DSH; turns one-shot multi-agent dispatch into a generatable / savable / governable / observable / recoverable Workflow layer.
- [btspoony/mstar-harness](https://github.com/btspoony/mstar-harness) (★38) — Skill-driven Harness / Loop Engineering Workflow Agent Plugin.
- [LoserFox/distill](https://github.com/LoserFox/distill) (★11) — Automatic conversation distillation: background subagent reflection + skill create/update.
- [titanwings/dsh-plannotator](https://github.com/titanwings/dsh-plannotator) (★1) — Plan annotator.
- [yyh-001/dsh-companion](https://github.com/yyh-001/dsh-companion) (★2) — Companion plugin.
- [vibeinging/dsh-work](https://github.com/vibeinging/dsh-work) (★2) — Work plugin.
- [omdsh-dev/dsh-gomoku](https://github.com/omdsh-dev/dsh-gomoku) (★5) — Gomoku game plugin.

### Integrations & Bridges

- [omdsh-dev/dsh-open-in-vscode](https://github.com/omdsh-dev/dsh-open-in-vscode) (★28) — Open workspace directories in VS Code directly from the web GUI.
- [omdsh-dev/dsh-notification](https://github.com/omdsh-dev/dsh-notification) (★19) — Desktop notifications for turn completions, with per-outcome controls and include/exclude keyword rules.
- [Nagi-ovo/dsh-find-plugins](https://github.com/Nagi-ovo/dsh-find-plugins) (★12) — In-app plugin finder.
- [YYTbit/dsh-plugin-claude-bridge](https://github.com/YYTbit/dsh-plugin-claude-bridge) — Bridge to Claude.
- [YYTbit/dsh-plugin-codex-bridge](https://github.com/YYTbit/dsh-plugin-codex-bridge) — Bridge to Codex.
- [YYTbit/dsh-plugin-pi-bridge](https://github.com/YYTbit/dsh-plugin-pi-bridge) — Bridge to Pi.
- [YYTbit/dsh-plugin-opencode-bridge](https://github.com/YYTbit/dsh-plugin-opencode-bridge) — Bridge to OpenCode.
- [bobleer/deepseek-harness-plugin-mcp](https://github.com/bobleer/deepseek-harness-plugin-mcp) — MCP plugin.
- [yoke233/dsh-openai-codex-auth](https://github.com/yoke233/dsh-openai-codex-auth) (★1) — OpenAI Codex auth.

### Sidebar, Workspace & Ecosystem

- [omdsh-dev/DSH-better-sidebar](https://github.com/omdsh-dev/DSH-better-sidebar) (★66) — Full workbench sidebar with third-party tab registration: file render/edit, terminal, Git, subagent.
- [LaplaceYoung/oh-my-dsh](https://github.com/LaplaceYoung/oh-my-dsh) (★12) — Plugin ecosystem: 700+ plugins wired only through extension seams, no agent-loop changes.
- [kingjly/dsh-plugin-builder](https://github.com/kingjly/dsh-plugin-builder) (★1) — Plugin builder scaffolding.
- [vlln/plugin-registry](https://github.com/vlln/plugin-registry) (★6) — Plugin registry.
- [DeKrych/Dshell-plugins](https://github.com/DeKrych/Dshell-plugins) (★27) — Dshell plugin collection.
- [HackSing/dsh-plugins](https://github.com/HackSing/dsh-plugins) / [Yihong89/dsh-plugins](https://github.com/Yihong89/dsh-plugins) — Plugin collections.
- [coppynight/dsh-doctor](https://github.com/coppynight/dsh-doctor) (★2) — Diagnostics / doctor.
- [yyh-001/dsh-expression](https://github.com/yyh-001/dsh-expression) (★1) — Expression plugin.
- [Chinesezjc/dsh-interconnect](https://github.com/Chinesezjc/dsh-interconnect) (★8) — Cross-instance message/event handoff.

### Fun & Misc

- [SenmuuuuW/dsh-group-photo](https://github.com/SenmuuuuW/dsh-group-photo) (★11) — Internal-test group-photo wall (GitHub OAuth, frozen allowlist).
- [syy-shark/dsh-music-plugin](https://github.com/syy-shark/dsh-music-plugin) — Music plugin.
- [unknowbug/RE-Framework](https://github.com/unknowbug/RE-Framework) (★5) / [unknowbug/anchorlaw](https://github.com/unknowbug/anchorlaw) (★4) — Frameworks.
- [hxs996-beep/deepAct](https://github.com/hxs996-beep/deepAct) (★7) — deepAct.

## Other awesome lists (meta)

These are community "awesome" indexes for DSH — useful cross-references, some
with daily compatibility tracking:

- [AdamPlatin123/awesome-dsh-plugins](https://github.com/AdamPlatin123/awesome-dsh-plugins) (★187) — Directory with daily compatibility tracking.
- [0xsline/awesome-deepseek-harness](https://github.com/0xsline/awesome-deepseek-harness) (★84) — Curated plugins/tools/infra from `dsh-external/hub` and the `dsh-plugin` topic.
- [Alex-Yanggg/awesome-DSH-plugin](https://github.com/Alex-Yanggg/awesome-DSH-plugin) (★27)
- [awesome-dsh-plugin/awesome-dsh-plugin](https://github.com/awesome-dsh-plugin/awesome-dsh-plugin) (★19)
- [bruc3van/awesome-dsh-plugin](https://github.com/bruc3van/awesome-dsh-plugin) (★8)
- [walkinglabs/awesome-deepseek-harness-plugins](https://github.com/walkinglabs/awesome-deepseek-harness-plugins) (★1)

## Contributing

Found or built a plugin? Make it discoverable:

1. Add the **`dsh-plugin`** topic to your GitHub repository.
2. Open a pull request adding it to the right category above (include a one-line
   description and the star count snapshot).

The auto-generated [PLUGINS.md](PLUGINS.md) is refreshed daily from the
`dsh-plugin` topic by [update.yml](.github/workflows/update.yml) — no manual
entry needed there, but the curated list stays human-maintained.

## License

The list content is released under [CC0 1.0](LICENSE). Individual plugins keep
their own licenses (mostly MIT, some CC BY-NC-SA for skins).
