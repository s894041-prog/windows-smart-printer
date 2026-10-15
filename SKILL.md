---
name: windows-smart-printer
description: >
  Windows 本地智慧批次列印工具。支援一鍵批次將指定資料夾或檔案清單發送至本機/網路印表機列印。
  內建雙面列印（長邊/短邊翻頁）、自動按套分裝（逐套列印）、份數控制（如一式三份）、黑白/彩色切換與縮放符合紙張。
  當使用者提到「幫我列印」、「印出這幾份PDF」、「批次列印」、「一式三份」、「雙面列印」、
  「列印資料夾裡的檔案」、「印到影印機」時，立即使用此 Skill。
compatibility: Windows + SumatraPDF (位於 %LOCALAPPDATA%\SumatraPDF\SumatraPDF.exe) + win32print
---

# Windows 智慧批次列印工具 (windows-smart-printer)

在校園行政或辦公室日常中，常需要將多個 PDF 表單（如公務統計報表、學生名冊、各類申請單）批次印出，且有「一式多份」、「正反雙面省紙」、「逐套分裝（避免手動理紙）」之需求。
本 Skill 封裝本機 SumatraPDF 命令列靜默列印引擎，直接向 Windows 印表機佇列發送工作，完全無需人工開啟視窗逐張點擊。

## 核心特性

1. **逐套分裝（Collated Sets）**：列印多份時（例如一式三份），系統依序印出「第 1 套 ➔ 第 2 套 ➔ 第 3 套」，印出來直接成套，免手動理紙。
2. **智慧雙面防混印**：
   - 2 頁以上文件：自動正反雙面印在同一張紙上（省紙）。
   - 1 頁文件：印完正面直接出紙，絕不會將不同檔案混印在同一張紙的正反面。
3. **模糊匹配印表機**：支援關鍵字（例如輸入 `bizhub`，自動對應名稱含 bizhub 的印表機）。
4. **預設自動縮放（fit）**：確保表格與核章欄位不被邊界裁切。

---

## 常用指令範例

腳本路徑：
`scripts/smart_print.py`

### 1. 查詢目前電腦所有可用印表機
```bash
python scripts/smart_print.py --list-printers
```

### 2. 批次列印某資料夾下全部 PDF（一式三份、雙面、黑白）
```bash
python scripts/smart_print.py --dir "D:\路徑\資料夾" --copies 3 --duplex long --color monochrome
```

### 3. 指定特定印表機（以關鍵字指定）
```bash
# 印到黑白影印機（用印表機名稱的一部分當關鍵字）
python scripts/smart_print.py --dir "D:\路徑\資料夾" --printer bizhub --copies 1

# 印到彩色影印機
python scripts/smart_print.py --dir "D:\路徑\資料夾" --printer 彩色機關鍵字 --copies 1 --color color

# 印到桌上型印表機
python scripts/smart_print.py --dir "D:\路徑\資料夾" --printer Brother --copies 1
```

### 4. 參數說明
* `--dir` : 待列印資料夾路徑（自動抓取所有 .pdf 檔）。
* `--files` : 指定單一或多個檔案路徑清單。
* `--copies` : 列印份數（預設 1，若設為 3 則自動逐套列印 3 套）。
* `--duplex` : 雙面模式：
  * `long` : 長邊翻頁（直向文件標準，預設）。
  * `short` : 短邊翻頁（橫向文件標準）。
  * `simplex` : 單面列印。
* `--color` : 色彩模式：
  * `monochrome` : 黑白列印（預設）。
  * `color` : 彩色列表。
* `--printer` : 目標印表機名稱或關鍵字（未指定時自動使用 Windows 預設印表機）。
