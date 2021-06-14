#!/usr/bin/python

from colorama import Fore, Back, Style
from os import system, name, environ, devnull
from time import sleep
import readline, sys, getopt, subprocess

version = f"0.4-{Fore.RED}beta{Style.RESET_ALL}"
dependencies = ['shodan', 'adb', 'scrcpy']
verbose = False
banner = rf'''{Fore.RED}
           _ _           _              _ _    _ _  
  __ _  __| | |__       | |_ ___   ___ | | | _(_) |_ 
 / _` |/ _` | '_ \ _____| __/ _ \ / _ \| | |/ / | __|
| (_| | (_| | |_) |_____| || (_) | (_) | |   <| | |_ 
 \__,_|\__,_|_.__/       \__\___/ \___/|_|_|\_\_|\__|

 adb-toolkit: {Style.RESET_ALL}{version}{Fore.RED}
 author: {Style.RESET_ALL}MasterAMV{Fore.RED} <AlphaProtonmail@protonmail.com>{Style.RESET_ALL}
'''

help = f'''
  Available commands:

    l: clear
    p: print (Prints the options)
    b: banner (Shows the banner and options)
    h: help
    r: return (Go back to the previous menu)
    e: exit
'''
opts, args = getopt.getopt(sys.argv[1:], 'v', ['verbose'])

for opt, args in opts:
  if opt in (['-v', '--verbose']):
    verbose = True

if name == 'nt':
  def clear():
    _ = system('cls')
  slash = '\\'
else:
  def clear():
    _ = system('clear')
  slash = '/'

def ask(q):
  return input(f'  {q}\n  {Fore.RED}>{Style.RESET_ALL} ')

def run(c):
  if verbose:
    print(f'{Fore.RED}[RUN]{Style.RESET_ALL} {c}\n')
  system(c)

def err(e, c):
  if verbose and c:
    print(f'\n  {Fore.RED}[V]{Style.RESET_ALL} {c}')
    print(f'  {Fore.RED}[ERR]{Style.RESET_ALL} {e}\n')
  else:
    print(f'\n  {Fore.RED}[ERR]{Style.RESET_ALL} {e}\n')

class Shell:
  def __init__(self, menu):

    self.menu = menu
    self.path = self.menu.name



    self.init()
  def query(self):
    RX = input(f'  {Fore.RED}({Style.RESET_ALL}{self.path}{Fore.RED}){Style.RESET_ALL}:{Fore.RED}\n  > {Style.RESET_ALL}')
 
    if RX in(['l', 'clear']):
      clear()
    elif RX in(['p', 'print']):
      clear()
      self.menu.render()
    elif RX in(['b', 'banner']):
      self.init()
    elif RX in(['h', 'help']):
      print(help)
    elif RX in(['r', 'return']):
      if not self.menu.prev == None:
        self.loadmenu(self.menu.prev)
    elif RX in(['e', 'exit']):
      sys.exit(f'  \n{Fore.RED}Goodbye!{Style.RESET_ALL}')
    else:
      if RX.isdigit() and int(RX) > 0 and int(RX) <= len(self.menu.opts):
        clear()
        self.menu.opts[int(RX) - 1].exec()
      elif not len(RX) == 0:
        print(f'  {Fore.RED}* Unkown command.{Style.RESET_ALL}\n')
  def init(self):
    clear()
    print(banner)
    self.menu.render()
  def genpath(self):
    def check(m, p):
      if not m.prev == None:
        p = f'{m.prev.name}/{p}'
        check(m.prev, p)
      else:
        self.path = p
        return
    check(self.menu, self.menu.name)
  def loadmenu(self, new):
    if not self.menu.prev == new:
      new.prev = self.menu
    self.menu = new
    self.genpath()
    self.init()

class Menu:

  prev = None

  def __init__(self, name, opts):
    self.name = name
    self.opts = opts
  
  def render(self):
    i = 1
    for opt in self.opts:
      print(f'  {Fore.RED}{i}){Style.RESET_ALL} {opt.name}')
      i += 1
    print(f'\n  {Fore.RED}Choose an option to continue.{Style.RESET_ALL}\n')

class Option:
  def __init__(self, name, exec):
    self.name = name
    self.exec = exec

def HandleTargets():

  def Find():
    print(f'  Credit: {Fore.RED}@gudishvibes:fairydust.space{Style.RESET_ALL}')
    path = ask(f'Path to save the file? {Fore.RED}(Default {environ["HOME"]}){Style.RESET_ALL}') or f'{environ["HOME"]}'
    limit = ask(f'Limit? {Fore.RED}(Default 5000){Style.RESET_ALL}') or '5000'
    name = ask(f'File name? {Fore.RED}(Default "android.json.gz"){Style.RESET_ALL}') or 'android.json.gz'
    filters = ask(f'Extra shodan options? {Fore.RED}(ADB is already included){Style.RESET_ALL}')

    if not path[-1] in('/', '\\'):
      path = path + slash

    run(f'shodan download --limit {limit} {path}{name} "Android Debug Bridge" {filters}')
  def Conn():
    print(f'  Credit: {Fore.RED}@gudishvibes:fairydust.space{Style.RESET_ALL}')
    ips = ask(f'Path to the saved file? {Fore.RED}(Leave empty to manually enter a target){Style.RESET_ALL}')

    if ips == '':
        ips = ask('IP Address?')
        if len(ips) > 0:
          run(f'adb connect {ips}')
    elif not ips[-1] == slash:
      run(f'for addr in $(shodan parse --fields ip_str,port --separator : {ips}); do adb connect $addr; done')
      dis = ask(f'Would you like to disconnect from all of those devices? {Fore.RED}(Y/n){Style.RESET_ALL}').lower()
      if dis == 'y':
        run('adb disconnect')
    else:
      err('Invalid Path.', f"'{slash} cannot be the last character of a valid file path.")
  def Disc():
    all = ask(f'Do you want to disconnect from all devices? {Fore.RED}(Y/n){Style.RESET_ALL}').lower()
    if all == 'y':
      run('adb disconnect')
    elif all == 'n':
      ip = ask('IP Address?')
      if not ip == '':
        run(f'adb disconnect {ip}')
  def View():
    run('adb devices')

  sh.loadmenu(Menu('targets', [Option('Find targets with shodan', Find), Option('Connect to a (list of) target(s) ', Conn), Option('Disconnect all/one device', Disc), Option('Show devices', View)]))

def Tools():

  def Control():
    ip = ask('IP Address?')
    if len(ip) > 0:
      run(f'env ANDROID_SERIAL={ip} scrcpy &')

  sh.loadmenu(Menu('tools', [Option('View & Control target', Control)]))

print(' {}* {}Dependency check.'.format(Fore.RED, Style.RESET_ALL))
print(' {}|'.format(Fore.RED))

fail = []

for dep in dependencies:
  try:
    subprocess.call(['{}'.format(dep)], stdout=open(devnull, 'w'), stderr=subprocess.STDOUT)
    sleep(0.1)
  except:
    print(' {}|{} {:<10s} {:>4s}'.format(Fore.RED, Style.RESET_ALL, dep, '{}[{}FAIL{}]'.format(Style.RESET_ALL, Fore.RED, Style.RESET_ALL)))
    fail.append(dep)
  else:
    print(' {}|{} {:<10s} {:>4s}'.format(Fore.RED, Style.RESET_ALL, dep, '{}[{} OK {}]'.format(Style.RESET_ALL, Fore.GREEN, Style.RESET_ALL)))
print(' {}|'.format(Fore.RED))

if len(fail) == 0:
  print(' {}* {}Done.'.format(Fore.RED, Style.RESET_ALL))
else:
  err('Dependencies not met.', 'Please install: {}'.format(str(fail)))
  q = ask(' {}* {}Do you still wanna continue? (Y/n)'.format(Fore.RED, Style.RESET_ALL)).lower()
  if not q == 'y':
    exit()

sleep(1)

sh = Shell(Menu('menu', [Option('Handle targets', HandleTargets), Option('Tools', Tools)]))

while True:
  sh.query()