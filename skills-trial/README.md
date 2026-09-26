# DSE skills trial / DSE 技能試用

這條分支只加試用技能與示範，不改網站根目錄的導數學習報告（`index.html`、`assets/`、`media/`）。

This branch adds a skills trial only. It does not change the derivatives learning report at the site root (`index.html`, `assets/`, `media/`).

## Upstream skills / 上游技能

Copied in full into `.cursor/skills/` on this branch.

| Skill | Upstream |
| --- | --- |
| `math-explainer` | [GordenSun/mathVideoMaker `skills/math-explainer`](https://github.com/GordenSun/mathVideoMaker/tree/main/skills/math-explainer) |
| `dependency-map` | [panpanc/math-skills `.claude/skills/dependency-map`](https://github.com/panpanc/math-skills/tree/main/.claude/skills/dependency-map) |
| `bottom-up` | [panpanc/math-skills `.claude/skills/bottom-up`](https://github.com/panpanc/math-skills/tree/main/.claude/skills/bottom-up) |

`dependency-map` 要求的審核步驟依上游 `dependency-map-audit` 的規格在本分支內聯完成，審核稿在驗證後刪除，沒有把第四個技能樹複製進來。

The dependency-map audit was done inline from the upstream `dependency-map-audit` instructions. The temporary audit file was deleted after verification. That fourth skill tree was not copied.

## Demo outputs / 示範產物

### 圓方程：由圓心半徑式到一般式

DSE 必修。`math-explainer`：分鏡、Manim 場景、互動網頁。

| File | Role |
| --- | --- |
| `demos/circle-equation/storyboard.md` | 分鏡與共享設計（繁中） |
| `demos/circle-equation/scene.py` | Manim 場景 `CircleEquation` |
| `demos/circle-equation/mathviz.py` | 模板副本；`ZH` 改為 `WenQuanYi Micro Hei` |
| `demos/circle-equation/index.html` | 互動網頁（滑塊 `h`、`k`、`r`、`theta`） |
| `demos/circle-equation/CircleEquation.mp4` | 720p 講解影片 |

先看影片，再打開 `index.html`。預設 `h=2`、`k=1`、`r=3`、`theta=50` 與影片主例相同。配色同為深藍底、藍 `#5b9cff`、青 `#2dd4bf`、金 `#ffd166`。

Watch the video first, then open `index.html`. The default sliders match the video example. Palette is shared.

### 數學歸納法入門

DSE M2。先 `dependency-map`，再 `bottom-up`。

| File | Role |
| --- | --- |
| `demos/mathematical-induction/mathematical_induction_dependency_map.md` | 14 個節點、22 條邊、`L0`–`L5` |
| `demos/mathematical-induction/mathematical_induction_dependency_map.html` | 互動圖（Prereqs / Unlocks / Bottleneck / Path） |
| `demos/mathematical-induction/mathematical_induction_bottom_up_v2.md` | 由數列與差分建到歸納法的修訂稿 |

英文小標題是檢查器要認的骨架，解釋用繁體中文。

English section headings are the checkers' skeleton. The explanation is in Traditional Chinese.

## Checks / 檢查

- `check_web.py`：`demos/circle-equation/index.html` 為 `[PASS]`。
- `check_text.py`：`scene.py` 為 `[PASS]`（63 條 `Text`，字體 WenQuanYi Micro Hei）。
- 靜幀與成片日誌：`[layout] DONE 共发现 0 处布局问题`。
- `verify_dependency_map.js` 與 `--strict-structure`：PASS（14 nodes, 22 edges）。
- `verify_bottom_up_depth.py`、`verify_markdown_math.py --strict-warnings`、`verify_mermaid_blocks.js --require-mermaid`：`mathematical_induction_bottom_up_v2.md` 均 PASS。Mermaid 只做了啟發式檢查，因為環境沒有 `mmdc`。

## Blockers and defaults / 阻礙與預設

- **MP4：有。** Manim Community 0.21.0 與系統 `ffmpeg` 可用，成片是 `CircleEquation.mp4`（720p）。`media/` 裡的中間檔不提交。
- **沒有 LaTeX。** 影片公式用 `Text` 與 `^2`，不用 `MathTex`。網頁公式用 KaTeX。
- **沒有 PingFang SC。** `fc-match` 會落到不含中日韓字形的 Noto Sans，所以示範目錄的 `mathviz.py` 改用文泉驛微米黑。上游技能檔本身沒改。
- `setup_manim.sh` 在這台機器上先因缺少 `python3-venv` 而建不起虛擬環境。補上 `python3.12-venv` 之後，Manim 裝在 `~/.cache/manim-explainer-venv`。`check_env.py` 用該環境的 Python 執行才會看到 Manim：venv 的 `python` 是指向系統解釋器的符號連結，腳本用 `realpath` 比較時不會自動切過去。
- 受眾預設為 DSE 高中，影片約一分鐘，深色高對比。沒有配音。

**MP4: yes.** Rendered with Manim Community 0.21.0 and system ffmpeg at 720p. Intermediate files under `media/` are not committed.

**No LaTeX.** The video uses `Text` and `^2` instead of `MathTex`. The page uses KaTeX.

**No PingFang SC.** The demo copy of `mathviz.py` uses WenQuanYi Micro Hei. The upstream skill file is unchanged.

`setup_manim.sh` needed `python3.12-venv` before the virtualenv could be created. `check_env.py` must be run with that venv's Python, because its symlink shares a realpath with system Python and the script then skips its own re-exec.
