import os, sys, argparse, subprocess, time
import win32print

SUMATRA_EXE = os.path.expandvars(r"%LOCALAPPDATA%\SumatraPDF\SumatraPDF.exe")

def get_installed_printers():
    default_p = win32print.GetDefaultPrinter()
    printers = [p[2] for p in win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)]
    return default_p, printers

def smart_print(files, printer=None, copies=1, duplex="long", color="monochrome", fit=True, delay=1.2):
    if not os.path.exists(SUMATRA_EXE):
        raise FileNotFoundError(f"SumatraPDF not found at: {SUMATRA_EXE}")
    
    default_p, all_printers = get_installed_printers()
    target_printer = printer or default_p
    if target_printer not in all_printers:
        # fuzzy match
        matches = [p for p in all_printers if target_printer.lower() in p.lower()]
        if matches:
            target_printer = matches[0]
        else:
            raise ValueError(f"找不到印表機 '{target_printer}'。現有印表機: {all_printers}")
    
    # Build print settings
    settings = []
    if duplex == "long":
        settings.append("duplexlong")
    elif duplex == "short":
        settings.append("duplexshort")
    elif duplex == "simplex":
        settings.append("simplex")
    else:
        settings.append("duplexlong")
    
    if fit:
        settings.append("fit")
    
    if color == "monochrome":
        settings.append("monochrome")
    elif color == "color":
        settings.append("color")
    
    settings_str = ",".join(settings)
    
    print(f"=== 啟動智慧批次列印任務 ===")
    print(f"目標印表機 : {target_printer}")
    print(f"列印參數   : {settings_str}")
    print(f"列印份數   : 一式 {copies} 份 (自動按套分裝)")
    print(f"待印檔案數 : {len(files)} 個\n")
    
    # We loop copies so that sets are collated (Set 1 complete, then Set 2, then Set 3)
    for set_idx in range(1, copies + 1):
        print(f"--- 正在列印【第 {set_idx} 份】(共 {len(files)} 份檔案) ---")
        for f in files:
            if not os.path.exists(f):
                print(f"  [跳過] 檔案不存在: {f}")
                continue
            
            basename = os.path.basename(f)
            cmd = [
                SUMATRA_EXE,
                "-print-to", target_printer,
                "-print-settings", settings_str,
                "-silent",
                f
            ]
            res = subprocess.run(cmd)
            if res.returncode == 0:
                print(f"  已發送: {basename}")
            else:
                print(f"  [失敗] {basename} (錯誤碼: {res.returncode})")
            time.sleep(delay)
        
        print(f"=== 【第 {set_idx} 份】發送完畢 ===\n")
        if set_idx < copies:
            time.sleep(2)
            
    print(f"[完成] 全部 {copies} 份文件已全數發送至印表機列印完畢！")

def main():
    parser = argparse.ArgumentParser(description="Windows Smart Batch Printer")
    parser.add_argument("--files", nargs="*", help="List of PDF files to print")
    parser.add_argument("--dir", help="Directory containing PDF files to print")
    parser.add_argument("--printer", help="Target printer name or keyword (e.g. bizhub, Brother)")
    parser.add_argument("--copies", type=int, default=1, help="Number of collated copies (default: 1)")
    parser.add_argument("--duplex", choices=["long", "short", "simplex"], default="long", help="Duplex mode (default: long)")
    parser.add_argument("--color", choices=["monochrome", "color"], default="monochrome", help="Color mode (default: monochrome)")
    parser.add_argument("--list-printers", action="store_true", help="List all available printers")
    
    args = parser.parse_args()
    
    if args.list_printers:
        default_p, all_p = get_installed_printers()
        print("預設印表機:", default_p)
        print("所有可用印表機:")
        for p in all_p:
            print("  *", p)
        return
    
    target_files = []
    if args.files:
        target_files.extend(args.files)
    elif args.dir:
        if os.path.exists(args.dir):
            for f in sorted(os.listdir(args.dir)):
                if f.lower().endswith(".pdf"):
                    target_files.append(os.path.join(args.dir, f))
    
    if not target_files:
        print("請指定 --files 或 --dir")
        sys.exit(1)
        
    smart_print(
        files=target_files,
        printer=args.printer,
        copies=args.copies,
        duplex=args.duplex,
        color=args.color
    )

if __name__ == '__main__':
    main()
