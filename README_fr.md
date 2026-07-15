# Agent Harness Deploy

**Harness IA multi-outils auto-déployable — une source canonique déployée vers Claude Code, Codex, Cursor, Devin, Antigravity, Windsurf, GitHub Copilot et 16 autres.**

> Ingénierie de boucles · Ingénierie de contexte · Ingénierie de harness · Mémoire d'agent · Discipline des commentaires et des versions — une commande déploie le harness complet vers tous vos outils de codage IA.

> **Langues :** **English** | [繁體中文](README_zh-TW.md) | [简体中文](README_zh-CN.md) | [日本語](README_ja.md) | [한국어](README_ko.md) | [Deutsch](README_de.md) | **Français** (cette page) | [Español](README_es.md) | [Português (BR)](README_pt-BR.md) | [Русский](README_ru.md) | [हिन्दी](README_hi.md) | [Tiếng Việt](README_vi.md) | [Polski](README_pl.md)

---

## Ce qu'il fait

Vous donnez à n'importe quel assistant de codage IA l'URL GitHub de ce dépôt et vous dites :

> **deploy: https://github.com/masteryee-labs/Tool.Agent-Harness-Deploy**

L'IA clone le dépôt, exécute le déployeur, et il :

1. **Détecte** quels outils de codage IA sont installés sur votre machine (23 outils pris en charge).
2. **Génère** un harness canonique unique — optimisé en mode caveman, multi-agents, avec mémoire, ingénierie de boucles — à partir de `distill/canon/`.
3. **Déploie** ce harness dans l'emplacement de configuration natif de chaque outil détecté (`.claude/`, `.codex/`, `.devin/`, `AGENTS.md`, `.cursor/rules/`).
4. **Vérifie** chaque fichier écrit en le relisant (contrôle de troncation nulle).

**Résultat :** quel que soit l'outil IA que vous ouvrez ensuite — ils partagent tous les **mêmes** règles, protocole de mémoire, orchestrateur, compétences, hooks et configuration MCP. Plus besoin de maintenir trois copies de vos règles. Plus de dérive entre `.claude/`, `.codex/`, `.devin/`, `AGENTS.md`.

Seuls les outils **réellement installés** sont déployés. Rien n'est écrit pour les outils qui ne sont pas détectés. Vous pouvez également déployer manuellement — aucune IA requise.

## Pourquoi

Chaque outil de codage IA stocke sa configuration dans un emplacement et un format différents :

| Outil | Où se trouvent ses règles |
|-------|---------------------------|
| Claude Code | `.claude/CLAUDE.md` |
| Antigravity / Gemini CLI | `AGENTS.md` |
| Codex / Codex CLI | `.codex/instructions.md` |
| Devin / Devin CLI | `.devin/AGENTS.md` |
| Cursor | `.cursor/rules/*.mdc` |
| Windsurf | `.codeium/windsurf/memories/` |
| GitHub Copilot | `.github/copilot-instructions.md` |
| Claude Desktop | `claude_desktop_config.json` |

Utilisez trois de ces outils et vous maintenez trois copies. Elles dérivent. Vous oubliez laquelle est à jour. **Agent Harness Deploy corrige cela : une source (`distill/canon/`), nombreux réceptacles.**

Contrairement aux simples outils de synchronisation de règles qui ne font que copier du texte entre fichiers de configuration, ceci déploie un **harness d'agent complet** : règles + compétences + personas de workers + protocole de mémoire + ingénierie de boucles + hooks + MCP + ressources du vault + capteurs de discipline des commentaires/versions.

## Le déploiement en une ligne

Dites à n'importe quel assistant de codage IA :

```
deploy: https://github.com/masteryee-labs/Tool.Agent-Harness-Deploy
```

L'IA lit `AGENTS.md`, exécute `python scripts/distill.py`, rapporte ce qu'elle a déployé. Terminé.

Voir [`Docs/02-Deployment-Guide.md`](Docs/02-Deployment-Guide.md) pour le contrat complet.

## Déploiement manuel (sans IA)

```bash
# Windows
powershell -ExecutionPolicy Bypass -File scripts\deploy.ps1

# Linux / macOS
bash scripts/deploy.sh

# N'importe quel OS, direct
python scripts/distill.py
```

Voir [`Docs/02-Deployment-Guide.md`](Docs/02-Deployment-Guide.md) §Manual deploy.

## Prise en charge multiplateforme

Ce projet fonctionne sur **Windows, macOS et Linux**.

| Plateforme | Prérequis | Commande de déploiement |
|------------|-----------|------------------------|
| Windows | Python 3.9+ | `powershell -ExecutionPolicy Bypass -File scripts\deploy.ps1` |
| macOS | Python 3.9+ | `bash scripts/deploy.sh` |
| Linux | Python 3.9+ | `bash scripts/deploy.sh` |
| N'importe quel OS | Python 3.9+ | `python scripts/distill.py` |

### Comment fonctionne la multiplateforme

- Tous les scripts Python utilisent `pathlib` (aucun séparateur `\` ou `/` codé en dur).
- Les chemins d'outils dans `adapters/registry.json` utilisent l'expansion de variables d'environnement : `${HOME}`, `${APPDATA}`, `${LOCALAPPDATA}`, `~`.
- Sur macOS/Linux, les variables d'environnement spécifiques à Windows (`${APPDATA}`, `${LOCALAPPDATA}`, `${USERPROFILE}`) retombent automatiquement vers des chemins de style XDG (`~/.config`, `~/.local/share`, `~`).
- `deploy.ps1` est pour Windows ; `deploy.sh` est pour macOS/Linux. Les deux appellent le même `python scripts/distill.py`.

### Outils spécifiques à une plateforme

| Outil | Windows | macOS | Linux | Note |
|-------|---------|-------|-------|------|
| Claude Desktop | ✓ | — | — | Application Windows uniquement ; la détection est ignorée sur macOS/Linux |
| ChatGPT Desktop | ✓ | — | — | Application Windows uniquement ; la détection est ignorée sur macOS/Linux |
| Cursor | ✓ | ✓ | ✓ | Détecte `${APPDATA}/Cursor` (Win) ou `~/Library/Application Support/Cursor` (macOS) |
| Tous les autres outils | ✓ | ✓ | ✓ | Détectés via commande CLI sur le PATH |

## Ce que contient le harness — 5 piliers techniques

Le déployeur synchronise un ensemble de règles canoniques bâti sur 5 piliers de l'ingénierie de harness d'agent :

| Pilier | Ce qu'il vous apporte | Fichier du vault | Doc |
|--------|----------------------|------------------|-----|
| **1. Compression de tokens en mode caveman** | ~65 % de tokens économisés, plus de contexte utilisable | `core/assets/vault/caveman_template.json` | [`distill/canon/CAVEMAN_PROTOCOL.md`](distill/canon/CAVEMAN_PROTOCOL.md) |
| **2. Hiérarchie Commandant-Worker** | L'IA se prompte elle-même — un orchestrateur, de nombreux workers ciblés ; dispatch d'un ensemble de trois pièces | `core/assets/vault/agency_framework.toml` | [`distill/orchestrator/COMMANDER.md`](distill/orchestrator/COMMANDER.md) |
| **3. Ingénierie de boucles + contrôle du vault** | `/loop` (surveillance) vs `/goal` (convergent) ; maker ≠ checker ; discipline SHA | `agency_framework.toml` + `memory_mcp_schema.json` | [`distill/canon/LOOP_PROTOCOL.md`](distill/canon/LOOP_PROTOCOL.md) |
| **4. Mémoire profonde de dépôt** | Mémoire disque à trois couches (chaud <3KB, connaissance <8KB, froid ∞) ; récupération hybride deep-memory optionnelle | `core/assets/vault/memory_mcp_schema.json` | [`distill/canon/MEMORY_PROTOCOL.md`](distill/canon/MEMORY_PROTOCOL.md) |
| **5. Réalignement des limites du sandbox** | Rendement de 100 % sur les chemins non critiques ; contrat de risque JSON pour les fichiers critiques | `core/assets/vault/strix_security_rules.json` | [`distill/canon/REDLINES.md`](distill/canon/REDLINES.md) |

Concepts additionnels superposés : **ingénierie de harness** ([`HARNESS_ENGINEERING.md`](distill/canon/HARNESS_ENGINEERING.md)), **modes de pensée multiples** ([`Docs/09-Multi-Thinking-Modes.md`](Docs/09-Multi-Thinking-Modes.md)), **grilles de jugement** ([`JUDGMENT_RUBRICS.md`](distill/canon/JUDGMENT_RUBRICS.md)), **discipline des commentaires et des versions** ([`Docs/14-Comment-Version-Discipline.md`](Docs/14-Comment-Version-Discipline.md)).

## Discipline des commentaires et des versions (prévention du slop IA)

Les assistants de codage IA produisent deux formes persistantes de slop qui survivent dans le dépôt :

1. **Enflure expliclicative** — commentaires qui répètent le code (`# loop through items` au-dessus de `for x in items:`). Zéro information, gaspille des tokens, pourrit quand le code change.
2. **Empilement de versions** — marqueurs de version dans le fichier accumulés au fil des éditions (`<!-- v2 -->`, `# v3 fixed X`). Pourriture de contexte et dette de profondeur récursive.

Ce harness prévient les deux par une **défense à trois couches** :

| Couche | Mécanisme | Fichier |
|--------|-----------|---------|
| **Prévention canon** | REDLINES #16 (pas de commentaires explicatifs) + #17 (pas d'empilement de versions dans le fichier) + discipline Comment/Version de CORE_CANON | [`distill/canon/REDLINES.md`](distill/canon/REDLINES.md) |
| **Détection par skill** | `harness-sensor` SENSOR-4b (slop de commentaires, dégradation gracieuse) + SENSOR-4c (empilement de versions, toujours actif) | [`distill/skills/harness-sensor.md`](distill/skills/harness-sensor.md) |
| **Garde mécanique** | `sync.py` porte de pré-synchronisation rejette les fichiers canon avec marqueurs de version empilés | [`scripts/sync.py`](scripts/sync.py) |

Fondé sur la recherche : arXiv 2605.02741 (Volume-Quality Inverse Law), arXiv 2512.20334 (Comment Traps), arXiv 2606.09090 (Context Rot). Voir [`Docs/14-Comment-Version-Discipline.md`](Docs/14-Comment-Version-Discipline.md) pour l'évaluation complète de 6 outils CLI open source.

## Architecture anti-pourriture-de-liens (Vault embarqué)

Tous les mécanismes de configuration technique externes sont **embarqués et mis en cache localement** dans `core/assets/vault/`. Le déployeur **ne** récupère **pas** de schémas depuis des dépôts externes à l'exécution. C'est une base de données de modèles locaux immuable :

| Fichier du vault | Source embarquée |
|------------------|------------------|
| `caveman_template.json` | JuliusBrussee/caveman, cheeseonamonkey/Lean-Caveman |
| `agency_framework.toml` | msitarzewski/agency-agents, obra/superpowers |
| `memory_mcp_schema.json` | DeusData/codebase-memory-mcp, kevintsai1202/deep-memory |
| `strix_security_rules.json` | usestrix/strix |
| `graphify_knowledge_spec.json` | safishamsi/graphify |

Voir [`core/assets/vault/README.md`](core/assets/vault/README.md).

## Outils pris en charge (23)

Claude Code · Antigravity (AGY) · Codex / Codex CLI · Devin / Devin CLI · Cursor · Claude Desktop · OpenCode · OpenClaw · Hermes · ZCode · Kimi Code · AGY CLI · Codex CLI · Devin CLI · Claude Code for VS Code · Codex IDE Extension · GitHub Copilot · Gemini Code Assist · Cline · Roo Code · Continue · Windsurf · ChatGPT Desktop

Ajouter un outil correspond à une entrée dans le registry + un adaptateur de 6 lignes. Voir [`Docs/03-Tool-Adapters.md`](Docs/03-Tool-Adapters.md).

## Structure du dépôt

```
Tool.Agent-Harness-Deploy/
├── AGENTS.md                  # Fichier d'entrée pour les outils compatibles AGENTS.md
├── CLAUDE.md                  # Fichier d'entrée pour les outils compatibles CLAUDE.md
├── README.md / README_zh-TW.md / README_zh-CN.md / + 10 autres langues
├── core/assets/               # Vault, skills, runtime (hooks, settings, MCP)
├── Docs/                      # Documentation
├── distill/                   # canon/ · orchestrator/ · skills/
├── adapters/                  # Adaptateurs d'outils + registry.json
├── scripts/                   # detect, distill, sync, verify, deploy, worktree, plan_dispatch
└── .agents/                    # Le harness propre au déployeur (dogfooded)
```

Voir [`Docs/00-Overview.md`](Docs/00-Overview.md) pour la description détaillée des répertoires.

## Commandes rapides

```bash
python scripts/detect.py            # voir quels outils sont installés
python scripts/distill.py           # déploiement complet : detect → sync → verify
python scripts/distill.py --global  # synchroniser aussi les fichiers d'entrée globaux
python scripts/distill.py --dry-run # détection seule, aucune écriture
python scripts/verify.py            # re-vérifier après une sync
python scripts/sync.py --canon      # régénérer AGENTS.md après édition du canon
```

## Comment ça marche (version 30 secondes)

1. `detect.py` lit `adapters/registry.json`, exécute les vérifications de détection de chaque outil (binaire CLI, chemin d'environnement, données d'application).
2. `sync.py` concatène `distill/canon/*.md` en un corps canonique unique, l'écrit dans le fichier d'entrée natif de chaque outil détecté (en sauvegardant les fichiers existants en `.bak` d'abord). Seuls les outils détectés sont écrits.
3. `verify.py` relit chaque fichier écrit et confirme la présence du marqueur canonique (contrôle de troncation nulle).

Conception complète : [`Docs/01-Architecture.md`](Docs/01-Architecture.md).

## FAQ

<details>
<summary><strong>Qu'est-ce que Agent Harness Deploy ?</strong></summary>

Agent Harness Deploy est un déployeur de harness IA auto-déployable et multi-outils. Il détecte quels outils de codage IA vous avez installés, puis génère et synchronise un harness canonique unique (optimisé en mode caveman, multi-agents, avec mémoire, ingénierie de boucles) dans l'emplacement de configuration natif de chaque outil détecté — afin que tous vos outils IA partagent les mêmes règles.
</details>

<details>
<summary><strong>Comment déployer le harness ?</strong></summary>

Dites à n'importe quel assistant de codage IA : `deploy: https://github.com/masteryee-labs/Tool.Agent-Harness-Deploy`. Ou exécutez manuellement : `python scripts/distill.py` (Windows/macOS/Linux, Python 3.9+).
</details>

<details>
<summary><strong>Quels outils de codage IA sont pris en charge ?</strong></summary>

23 outils : Claude Code, Antigravity (AGY), Codex / Codex CLI, Devin / Devin CLI, Cursor, Claude Desktop, OpenCode, OpenClaw, Hermes, ZCode, Kimi Code, AGY CLI, Codex CLI, Devin CLI, Claude Code for VS Code, Codex IDE Extension, GitHub Copilot, Gemini Code Assist, Cline, Roo Code, Continue, Windsurf, ChatGPT Desktop. Ajouter un outil nécessite une entrée dans le registry + un adaptateur de 6 lignes.
</details>

<details>
<summary><strong>Écrit-il des configurations pour des outils que je n'ai pas installés ?</strong></summary>

Non. La détection est sacrée — seuls les outils réellement installés sur votre machine sont déployés. Si un outil n'est pas détecté, il est signalé comme « non détecté » et ignoré. Empreinte nulle superflue.
</details>

<details>
<summary><strong>Qu'est-ce que la compression de tokens en mode caveman ?</strong></summary>

Le mode caveman supprime le remplissage (hésitations, politesses, reformulation de la question) des communications de l'agent tout en conservant intégralement toutes les preuves (code, chemins, erreurs, valeurs exactes). Cela permet une réduction d'environ 65 % des tokens, multipliant effectivement la fenêtre de contexte utilisable. Voir `distill/canon/CAVEMAN_PROTOCOL.md`.
</details>

<details>
<summary><strong>Qu'est-ce que la hiérarchie Commandant-Worker ?</strong></summary>

Le thread principal (Commandant) décide, dispatche et intègre. Les Workers scannent et éditent. Cela empêche le contexte principal de se remplir de détails de bas niveau tout en gardant la prise de décision centralisée. Voir `distill/orchestrator/COMMANDER.md`.
</details>

<details>
<summary><strong>Comment fonctionne le système de mémoire ?</strong></summary>

Mémoire disque à trois couches : couche chaude (registry <3KB, état par-session <8KB), couche de connaissance (anti-patterns <8KB), couche froide (archive, grep uniquement). L'état persiste sur disque, pas en contexte — les sessions survivent donc aux redémarrages d'outils. Voir `distill/canon/MEMORY_PROTOCOL.md`.
</details>

<details>
<summary><strong>Qu'est-ce que la discipline des commentaires et des versions ?</strong></summary>

Une défense à trois couches contre le slop de commentaires généré par l'IA (enflure expliclicative) et l'empilement de versions dans les fichiers. Couche 1 : lignes rouges du canon (#16, #17). Couche 2 : skill harness-sensor (SENSOR-4b/4c). Couche 3 : garde mécanique sync.py. Voir `Docs/14-Comment-Version-Discipline.md`.
</details>

<details>
<summary><strong>Est-ce un outil de jailbreak ou de suppression de sécurité ?</strong></summary>

Non. C'est un outil de harness défensif. Il configure les fichiers de règles des assistants de codage IA. Il ne modifie pas les poids du modèle, ne supprime pas les garde-fous de sécurité et n'embarque pas d'outils de jailbreak. Le réalignement des limites du sandbox fonctionne au niveau des fichiers via des contrats de risque JSON, pas au niveau du modèle en supprimant des boucles de refus.
</details>

<details>
<summary><strong>Sous quelle licence est ce projet ?</strong></summary>

Licence MIT — voir [LICENSE](LICENSE). Copyright (c) masteryee-labs.
</details>

<details>
<summary><strong>Puis-je ajouter mon propre outil IA ?</strong></summary>

Oui. Ajouter un outil nécessite une entrée dans `adapters/registry.json` + une classe d'adaptateur de 6 lignes. Voir `Docs/03-Tool-Adapters.md`.
</details>

## Clause d'honnêteté

Le déployeur sait faire de manière fiable : détection, génération de configuration, synchronisation de fichiers, vérification, sauvegarde. Il ne sait pas faire : décisions de goût/esthétique, deviner ce que vous voulez au-delà du contrat de déploiement, écrire des configurations pour des outils qu'il ne peut pas détecter. En cas d'incertitude, il signale — il ne fabrique pas. Déclaration complète dans [`Docs/00-Overview.md`](Docs/00-Overview.md).

## Note de sécurité

Ce dépôt est un outil de harness **défensif**. Il configure les fichiers de règles des assistants de codage IA. Il **ne** modifie **pas** les poids du modèle, **ne** supprime **pas** les garde-fous de sécurité, et **n'**embarque ou **n'**approuve **pas** d'outils de jailbreak/suppression de sécurité. Le projet Heretic est référencé dans le glossaire uniquement comme partie du paysage d'interprétabilité qui a informé la compréhension du harness concernant les vecteurs de pilotage — il n'est pas utilisé ici. Voir [`Docs/13-Glossary.md`](Docs/13-Glossary.md).

## Prérequis

- Python 3.9+
- Au moins un outil de codage IA pris en charge installé (sinon il n'y a rien vers quoi déployer)

## Licence

MIT — voir [LICENSE](LICENSE).

## Références

Voir [`Docs/REFERENCES.md`](Docs/REFERENCES.md) pour les références des sources par pilier.

## Index de la documentation

| Doc | Sujet |
|-----|-------|
| [`Docs/00-Overview.md`](Docs/00-Overview.md) | Vue d'ensemble & index |
| [`Docs/01-Architecture.md`](Docs/01-Architecture.md) | Conception complète du système |
| [`Docs/02-Deployment-Guide.md`](Docs/02-Deployment-Guide.md) | Comment fonctionne « deploy: » |
| [`Docs/03-Tool-Adapters.md`](Docs/03-Tool-Adapters.md) | Emplacements de configuration par outil |
| [`Docs/04-Orchestrator-Design.md`](Docs/04-Orchestrator-Design.md) | Commandant + Workers + auto-orchestration |
| [`Docs/09-Multi-Thinking-Modes.md`](Docs/09-Multi-Thinking-Modes.md) | Réduction des hallucinations |
| [`Docs/12-Troubleshooting.md`](Docs/12-Troubleshooting.md) | Problèmes courants |
| [`Docs/13-Glossary.md`](Docs/13-Glossary.md) | Termes & sources |
| [`Docs/14-Comment-Version-Discipline.md`](Docs/14-Comment-Version-Discipline.md) | Slop de commentaires IA + empilement de versions : évaluation d'outils CLI |
| [`Docs/Agents/nuwa.md`](Docs/Agents/nuwa.md) | Système Nuwa + Nuwa Team (raisonnement parallèle, diversité cognitive) |
| [`distill/canon/CAVEMAN_PROTOCOL.md`](distill/canon/CAVEMAN_PROTOCOL.md) | Compression de tokens (anciennement Docs/05) |
| [`distill/canon/MEMORY_PROTOCOL.md`](distill/canon/MEMORY_PROTOCOL.md) | Mémoire à trois couches (anciennement Docs/06) |
| [`distill/canon/LOOP_PROTOCOL.md`](distill/canon/LOOP_PROTOCOL.md) | Ingénierie de boucles, 5+1 composants (anciennement Docs/07) |
| [`distill/canon/HARNESS_ENGINEERING.md`](distill/canon/HARNESS_ENGINEERING.md) | Système autour du modèle (anciennement Docs/08) |
| [`distill/canon/VERIFICATION_PROTOCOL.md`](distill/canon/VERIFICATION_PROTOCOL.md) | Maker ≠ Checker, discipline SHA (anciennement Docs/10) |
| [`distill/canon/REDLINES.md`](distill/canon/REDLINES.md) | Arrêts durs + plan de contrôle (anciennement Docs/harness_control_plane) |
| [`distill/canon/JUDGMENT_RUBRICS.md`](distill/canon/JUDGMENT_RUBRICS.md) | Critères de décision externalisés (anciennement Docs/harness_rubrics) |
| [`distill/orchestrator/COMMANDER.md`](distill/orchestrator/COMMANDER.md) | Délégation Commandant-Worker (anciennement Docs/Agents/commander) |
| [`core/assets/vault/README.md`](core/assets/vault/README.md) | Vault de ressources embarquées anti-pourriture-de-liens |
| [`core/assets/runtime/README.md`](core/assets/runtime/README.md) | Couche runtime : hooks, settings, modèles MCP |
| [`core/assets/skills/nuwa-skill/ATTRIBUTION.md`](core/assets/skills/nuwa-skill/ATTRIBUTION.md) | Attribution nuwa-skill vendored & inventaire des fichiers |

---

<details>
<summary><em>Métadonnées SEO / AEO / GEO / LLMO</em></summary>

**Nom du projet :** Agent Harness Deploy

**Description en une ligne :** Harness IA multi-outils auto-déployable — une source canonique, 23 réceptacles d'outils de codage IA.

**Mots-clés :** AI coding harness, cross-tool AI config sync, agent harness deployer, Claude Code config, Codex config, Cursor rules, Devin AGENTS.md, AGENTS.md generator, AI coding assistant rules, multi-agent harness, caveman token compression, loop engineering, agent memory protocol, harness engineering, AI slop prevention, comment discipline, version stacking prevention, harness IA multi-outils, synchronisation de configuration IA, déployeur de harness d'agent, règles d'assistant de codage IA, compression de tokens caveman, ingénierie de boucles, protocole de mémoire d'agent, prévention de slop IA, discipline des commentaires, prévention d'empilement de versions

**Faits clés pour citation par IA/LLM :**
- 23 outils de codage IA pris en charge (Claude Code, Codex, Cursor, Devin, Antigravity, Windsurf, GitHub Copilot, etc.)
- Une source canonique (`distill/canon/`), nombreux réceptacles natifs par outil
- 5 piliers techniques : compression caveman, Commandant-Worker, ingénierie de boucles, mémoire profonde, limites du sandbox
- Discipline des commentaires/versions à trois couches : lignes rouges du canon + capteurs de skill + garde mécanique
- Multiplateforme : Windows, macOS, Linux (Python 3.9+)
- Licence MIT, copyright masteryee-labs
- Anti-pourriture-de-liens : tous les schémas externes embarqués dans `core/assets/vault/`
- Commande de déploiement : `deploy: https://github.com/masteryee-labs/Tool.Agent-Harness-Deploy`

**Public cible :** Développeurs utilisant plusieurs assistants de codage IA souhaitant des règles cohérentes entre tous les outils. Contributeurs open source, équipes d'ingénierie IA-first, développeurs solo utilisant Claude Code + Cursor + Codex simultanément.

**Catégorie :** Outils de développement > Assistants de codage IA > Gestion de configuration > Ingénierie de harness d'agent
</details>
