# Windows 智慧批次列印（windows-smart-printer）

一個指令，把整個資料夾的 PDF 批次印出，支援「一式多份、逐套分裝、雙面、黑白／彩色」。
適合學校行政、辦公室常見的需求：成績報表、學生名冊、各類申請單要印好幾份、還要自己理紙。

同時是一個 **AI Skill**（`SKILL.md`）：放進 Claude Code／Antigravity 等 AI 助理的 skills 資料夾後，
對 AI 說「幫我把這個資料夾的 PDF 印三份、雙面」，它就會幫你執行。

## 特色
- **逐套分裝**：一式三份時依序印「第 1 套 → 第 2 套 → 第 3 套」，印出來就是成套的，免手動理紙。
- **智慧雙面**：2 頁以上的文件自動雙面省紙；1 頁的文件單面輸出，**不會把不同檔案混印在同一張紙的正反面**。
- **印表機關鍵字比對**：只要打印表機名稱的一部分（例如 `bizhub`、`Brother`）。
- **預設縮放符合紙張（fit）**：表格與核章欄位不會被邊界裁掉。
- 靜默列印：不開任何視窗，直接送進 Windows 印表機佇列。

## 需求
- Windows
- [SumatraPDF](https://www.sumatrapdfreader.org/)，預設路徑 `%LOCALAPPDATA%\SumatraPDF\SumatraPDF.exe`
- Python 3 與 `pip install -r requirements.txt`（pywin32）

## 用法
```bash
# 列出這台電腦可用的印表機
python scripts/smart_print.py --list-printers

# 整個資料夾的 PDF：一式三份、長邊雙面、黑白
python scripts/smart_print.py --dir "D:\公文\待印" --copies 3 --duplex long --color monochrome

# 指定印表機（關鍵字即可）與彩色
python scripts/smart_print.py --dir "D:\公文\待印" --printer bizhub --color color

# 只印指定檔案
python scripts/smart_print.py --files "a.pdf" "b.pdf" --copies 2
```

| 參數 | 說明 |
|---|---|
| `--dir` | 資料夾，自動抓取其中所有 `.pdf`（依檔名排序） |
| `--files` | 指定一個或多個檔案 |
| `--copies` | 份數（預設 1；大於 1 時逐套列印） |
| `--duplex` | `long` 長邊翻頁（直向，預設）／`short` 短邊翻頁（橫向）／`simplex` 單面 |
| `--color` | `monochrome` 黑白（預設）／`color` 彩色 |
| `--printer` | 印表機名稱或關鍵字，未指定用 Windows 預設印表機 |
| `--list-printers` | 列出所有印表機 |

## 當作 AI Skill 使用
把整個資料夾放進 AI 的 skills 目錄（例如 `~/.claude/skills/windows-smart-printer/`），
之後可以直接用中文說：「印出這幾份 PDF」「一式三份、雙面」「印到彩色影印機」。

## 注意
- 列印前請確認檔案內容與份數，送出後無法從這個工具取消，只能在 Windows 印表機佇列中刪除。
- 含個資的檔案請在列印完成後妥善收存，不要留在共用印表機。
