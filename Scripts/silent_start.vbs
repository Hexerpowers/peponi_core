Set WshShell = WScript.CreateObject("WScript.Shell")
Return = WshShell.Run(WScript.Arguments.Item(0), 0, true)
