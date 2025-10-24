#!/usr/bin/env python3
import sys
import code

# for code.InteractiveConsole to send stack traces to stdout
sys.excepthook = sys.__excepthook__

BANNER = r'''
                                                             ,----,            
,-.----.           ,--.                                    ,/   .`|            
\    /  \      ,--/  /|            .---.   ,----..       ,`   .'  :     ,---,. 
|   :    \  ,---,': / '           /. ./|  /   /   \    ;    ;     /   ,'  .' | 
|   |  .\ : :   : '/ /        .--'.  ' ; |   :     : .'___,/    ,'  ,---.'   | 
.   :  |: | |   '   ,        /__./ \ : | .   |  ;. / |    :     |   |   |   .' 
|   |   \ : '   |  /     .--'.  '   \' . .   ; /--`  ;    |.';  ;   :   :  :   
|   : .   / |   ;  ;    /___/ \ |    ' ' ;   | ;     `----'  |  |   :   |  |-, 
;   | |`-'  :   '   \   ;   \  \;      : |   : |         '   :  ;   |   :  ;/| 
|   | ;     |   |    '   \   ;  `      | .   | '___      |   |  '   |   |   .' 
:   ' |     '   : |.  \   .   \    .\  ; '   ; : .'|     '   :  |   '   :  '   
:   : :     |   | '_\.'    \   \   ' \ | '   | '/  :     ;   |.'    |   |  |   
|   | :     '   : |         :   '  |--"  |   :    /      '---'      |   :  \   
`---'.|     ;   |,'          \   \ ;      \   \ .'                  |   | ,'   
  `---`     '---'             '---"        `---`                    `----'     
                                                                               '''

class RestrictedConsole(code.InteractiveConsole):

    def __init__(self, locals, blacklist, *a, **kw):
        super().__init__(locals, *a, **kw)
        self.blacklist = blacklist.copy()
        
    def runsource(self, source, *a, **kw):
        if not source.isascii() or any(word in source for word in self.blacklist):
            print("Blacklisted word detected, exiting ...")
            sys.exit(1)
        return super().runsource(source, *a, **kw)
    
    def write(self, data):
        sys.stdout.write(data)
        
    def interact(self, banner=None):
        # 完全自定义交互式提示，不显示Python版本信息
        # 我们可以直接调用父类的interact方法，但传递一个空字符串作为banner
        super().interact(banner='')

def main():
    # 定义黑名单和安全环境
    blacklist = ['import', 'os', 'system', 'subprocess', 'sh', 'flag', 'open', 'eval', 'exec']
    
    # keep all the builtins except open
    safe_builtins = {
        k:v for k,v in __builtins__.__dict__.items() if k != "open" 
    }
    locals = {'__builtins__': safe_builtins}
    
    # 打印欢迎展板
    print(BANNER)
    print("\n" + "="*80)
    print("                    Welcome to the PyJail Challenge!")
    print("="*80)
    
    # 显示黑名单信息
    print("\n         ⚠️  BLACKLISTED WORDS:")
    print("             " + ", ".join(blacklist))
    print("\n          Chestnut: This time you are not allowed to execute the command.")
    print("-"*80 + "\n")
    
    # 启动交互式控制台，不显示Python版本信息
    RestrictedConsole(locals, blacklist).interact()

if __name__ == "__main__":
    main()