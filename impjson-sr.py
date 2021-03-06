#! /usr/bin/python3
import sys
import os
import json
import codecs
import math

### Get Character
print('\n\n\tWelcher Character soll geladen werden? (\033[94mX\033[39m.json)')
filename = input('\t >> ')
if filename == '':
    filename = 's'
print(filename + '.json wird geladen...')
filen = filename + '.json'

with codecs.open(filen,'r', 'utf-8-sig') as myfile:
    data = myfile.read()
d = json.loads(data)

character = d['characters']['character']

###### Colours
class bcolors:
    IND = ' ' 
    BGRh = '\033[101m'
    BGR = '\033[41m'
    BGB = '\033[44;30m'
    BGWh = '\033[103;30m'
    BGW = '\033[43;30m'
    BGAh = '\033[105m'
    BGA = '\033[45m'
    BLACKh = '\033[90m'
    BLACK = '\033[30m'
    WHITE = '\033[0;39m'
    PNZRGh = '\033[96m'
    ASTRALh = '\033[95m'
    BLUEh = '\033[94m'
    GREENh = '\033[92m'
    WARNINGh = '\033[93m'
    FAILh = '\033[91m'
    PNZRG = '\033[36m'
    ASTRAL = '\033[35m'
    BLUE = '\033[34m'
    GREEN = '\033[92m'
    WARNING = '\033[33m'
    FAIL = '\033[31m'
    BOLD = '\033[1m'
    KURSIV = '\033[3m'
    BLINK = '\033[5m'
    UNDERLINE = '\033[4m'
    ENDC = '\033[0m'

### INITIALISIEREN ###############
x = character['attributes'][1]['attribute']
for i,n in enumerate(x):
    if x[i]['name'] == 'EDG':
        edgeT = x[i]['total']
    elif x[i]['name'] == 'REA':
        reaktionT = x[i]['total']
    elif x[i]['name'] == 'KON':
        konstitutionT = x[i]['total']
    elif x[i]['name'] == 'GES':
        geschicklichkeitT = x[i]['total']
    elif x[i]['name'] == 'STR':
        staerkeT = x[i]['total']
    elif x[i]['name'] == 'CHA':
        charismaT = x[i]['total']
    elif x[i]['name'] == 'WIL':
        willenskraftT = x[i]['total']
    elif x[i]['name'] == 'INT':
        intuitionT = x[i]['total']
    elif x[i]['name'] == 'LOG':
        logicT = x[i]['total']
mali = {
        'koerperlich': 0,
        'geistig': 0,
        'zauber': 0
        }
paras = {
        'edge': edgeT,
        'maxedge': edgeT,
        'reaktion': reaktionT,
        'konstitution': konstitutionT,
        'geschicklichkeit': geschicklichkeitT,
        'staerke': staerkeT,
        'charisma': charismaT,
        'willenskraft': willenskraftT,
        'intuition': intuitionT,
        'logik': logicT,
        'panzerung': int(character['armor']),
        'maxkoerperlich': math.ceil(int(konstitutionT)/2) + 8, #int(character['physicalcm']),
        'koerperlich': int(character['physicalcm']) - int(character['physicalcmfilled']),
        'maxgeistig': math.ceil(int(willenskraftT)/2) + 8,
        'geistig': int(character['stuncm']) - int(character['stuncmfilled']),
        'mali': '',
        'limk': bcolors.GREENh + character['limitphysical'] + bcolors.ENDC,
        'limg': bcolors.GREENh + character['limitmental'] + bcolors.ENDC,
        'lims': bcolors.GREENh + character['limitsocial'] + bcolors.ENDC,
        'lima': bcolors.GREENh + character['limitastral'] + bcolors.ENDC
        }   

### VARIABLEN 
sf = {}
spacer = ' '*4
linewidth = 190
pan = ''
ppan = 0
ammocnt = 0
win = False
troden = False
contacts = False
glasses = False
imkampf = False
smrtlnk = False
smrtlnktype = ''
isastral = False
zauberaufrechthalten = False
waffeAusgewaehlt = [' ', '', '', '', '', '']
gearAusgewaehlt = ' '
### Check OS
def checkos():
    global win
    if sys.platform == 'win32':
        win = True
checkos()
### CLEARSCREEN
def clscrn():
    if win == True:
        os.system('cls')
    else:
        os.system('clear')
### Check Terminal size
def terminal_size():
    if win == True:
        tw = 200
    else:
        import fcntl, termios, struct
        th, tw, hp, wp = struct.unpack('HHHH',
                fcntl.ioctl(0, termios.TIOCGWINSZ,
                struct.pack('HHHH', 0, 0, 0, 0)))
        global linewidth
        linewidth = tw
### HEADER
def checkerf():
    cm = mali['koerperlich'] + mali['geistig'] + mali['zauber']
    if cm == 0:
        paras['mali'] = ''
    else:
        paras['mali'] = str(cm)
def liner(): 
    print('{:_<{liner}}'.format('_', liner=linewidth) + '\n')
def statusinfo():
    global pan
    zah = ia = sl = ko = dth = wa = ga = pa = ''
    if pan == '':
        n_pan = 0
        for i,n in enumerate(character['armors']['armor']):
            if character['armors']['armor'][i]['armor'].find('+') == -1 and n_pan < int(character['armors']['armor'][i]['armor']):
                n_pan = int(character['armors']['armor'][i]['armor'])
                pan = character['armors']['armor'][i]['name']
            paras['panzerung'] = n_pan
    if isastral == True:
        ia = str(' ' + bcolors.BGA + ' Charakter ist im Astralraum unterwegs! ' + bcolors.ENDC + ' ')
    if zauberaufrechthalten == True:
        zah = str(' ' + bcolors.BGA + ' Zauber aktiv! ' + bcolors.ENDC + ' ')
    if smrtlnk == True and isastral == False:
        sl = str(' ' + bcolors.BGW + bcolors.BOLD + ' SMARTLINK aktiv! ' + bcolors.ENDC + ' ')
    if (paras['koerperlich'] + int(paras['konstitution'])) <= 0:
        dth = str(' \033[40m' + bcolors.BOLD + bcolors.FAIL + 5*' ' +  'Charakter ist tot' + 5*' ' + bcolors.ENDC + ' ')
    elif paras['koerperlich'] < 0 and (paras['koerperlich'] + int(paras['konstitution'])) > 0:
        dth = str(' \033[5m' + bcolors.BGR + bcolors.BOLD + '     Charakter muss stabilisiert werden!    ' + bcolors.ENDC + ' ')
    if paras['geistig'] <= 0 or paras['koerperlich'] <= 0:
        ko = str(' ' + bcolors.BGR + '     Charakter ist ohnmächtig     ' + bcolors.ENDC + ' ')
    if waffeAusgewaehlt[0] != ' ': #(waffeAusgewaehlt[0] != ' ' and imkampf == True) or (waffeAusgewaehlt[0] != ' ' and isastral == True):
        if isastral == False:
            if smrtlnk == True:
                wa = waffeAusgewaehlt[0] + ' (' + bcolors.GREENh + waffeAusgewaehlt[1] + bcolors.ENDC + ') ' + waffeAusgewaehlt[3] + waffeAusgewaehlt[2] + waffeAusgewaehlt[4]
            else:
                wa = waffeAusgewaehlt[0] + ' (' + bcolors.GREENh + waffeAusgewaehlt[1] + bcolors.ENDC + ') ' + waffeAusgewaehlt[3] + waffeAusgewaehlt[4]
        elif isastral == True and waffeAusgewaehlt[5] == 'Foki':
            wa = waffeAusgewaehlt[0] + waffeAusgewaehlt[3]
        elif isastral == True and waffeAusgewaehlt[5] == 'Waffenlos':
            wa = waffeAusgewaehlt[0] + waffeAusgewaehlt[3]
        else:
            wa = ' - '
    if gearAusgewaehlt != ' ' and isastral == False:
        ga = ' [Gear: ' + gearAusgewaehlt + ']'
    if pan != '' and isastral == False:
        pa = '[' + bcolors.PNZRGh + pan + bcolors.ENDC + ']'
    print(bcolors.IND + wa.ljust(100) + (sl).center(60) + ga)
    print(bcolors.IND + pa.ljust(50) + (ia + ko + dth + zah).center(70))
def headerprnt():
    terminal_size()
    checkerf()
    if paras['mali'] == '':
        mali = '0'
    else:
        mali = paras['mali']
    def prntbar(x,y):
        if x == 'koerperlich':
            uebs = int(paras['konstitution']) + 1
        else:
            uebs = 0
        n_cnt = paras[x] + uebs
        n_mdl = (paras[y]+uebs) % 3
        n_b = 0
        for n in range(paras[y] + uebs):
            if uebs > 0 and n == 0 and n_cnt > 0:
                print(bcolors.FAIL + '\033[10m' + '☠' + bcolors.ENDC, end='')
            elif uebs > 0 and n < uebs and n_cnt > 0:
                print(bcolors.BLUE + '█' + bcolors.ENDC, end='')
            elif n_cnt > 0:
                if paras[x] <= 4:
                    print(bcolors.WARNINGh + '█' + bcolors.ENDC, end='')
                else:
                    print(bcolors.GREEN + '█' + bcolors.ENDC, end='')
            else:
                print(bcolors.BLACK + '█' + bcolors.ENDC, end='')
            if n_mdl > 0:
                n_mdl -= 1 
                n_b -= 1
            if (n_b+1)%3 == 0 and n < (paras[y] + uebs -1) and n_mdl == 0:
                print(bcolors.BLACKh + '▏' + bcolors.ENDC, end='')
            n_cnt -= 1
            n_b += 1
        print(']', end='')
    print(bcolors.IND + bcolors.WARNINGh + '{alias}'.format(**character) + bcolors.ENDC + ':', end='')
    print("{spacer}[KON:".format(**paras, spacer=spacer) + bcolors.GREENh + '{konstitution}'.format(**paras) + bcolors.ENDC + ' STR:' + bcolors.GREENh + '{staerke}'.format(**paras) + bcolors.ENDC + ' GES:' + bcolors.GREENh + '{geschicklichkeit}'.format(**paras) + bcolors.ENDC + ' REA:' + bcolors.GREENh + '{reaktion}'.format(**paras) + bcolors.ENDC + ' WIL:' + bcolors.GREENh + '{willenskraft}'.format(**paras) + bcolors.ENDC + ' CHA:' + bcolors.GREENh + '{charisma}'.format(**paras) + bcolors.ENDC + ' INT:' + bcolors.GREENh + '{intuition}'.format(**paras) + bcolors.ENDC + ' LOG:' + bcolors.GREENh + '{logik}'.format(**paras) + bcolors.ENDC + "]{spacer}".format(spacer=spacer), end='')
    print(bcolors.BLUEh + "EDG:{edge}/{maxedge}".format(**paras) + bcolors.ENDC, end='')
    print(bcolors.FAILh + bcolors.BOLD + '{spacer}Mali:{mali:>2}{spacer}'.format(mali=mali, spacer=spacer) + bcolors.ENDC, end='')
    print(' K[', end='')
    prntbar('koerperlich','maxkoerperlich')
    print(' G[', end='')
    prntbar('geistig','maxgeistig')
    print(bcolors.PNZRGh + '{spacer}Panzerung:{panzerung!s}'.format(**paras, spacer=spacer) + bcolors.ENDC, end='')
    print('{spacer}Lim:[K:{limk} G:{limg} S:{lims} A:{lima}]'.format(**paras, spacer=spacer), end='')
    print('{spacer}¥:{nuyen} K:{karma}'.format(**character, spacer=spacer), end='')
    print('\n')
    statusinfo() 
    if imkampf == True:
        print(bcolors.FAILh, end='')
        liner()
        print(bcolors.ENDC, end='')
    elif isastral == True:
        print(bcolors.ASTRALh, end='')
        liner()
        print(bcolors.ENDC, end='')
    else:
        liner()
def astralconv():
    print(bcolors.IND + bcolors.ASTRALh + 'Astral: [KON = WIL,{spacer}STR = CHA,{spacer}GES = LOG,{spacer}REA = INT]\t\tIni: 2x INT + 3W6\t\tKraftfoki: [WP + St.]'.format(spacer='  ').center(165) + bcolors.ENDC)
    liner()

### Exec_Menue
def exec_menu(choice):
    clscrn()
    ch = choice.lower()
    if ch == '':
        main_menu()
    else:
        try:
            menu_actions[ch]()
        except KeyError:
            print(bcolors.IND + 'Invalid selection, please try again.\n')
            menu_actions['main_menu']()
    return

### Check for save-file
def chckfsf():
    global sf
    if os.path.isfile('./sf-' + character['alias'] + '.json') == True:
        with codecs.open('sf-' + character['alias'] + '.json','r','utf-8-sig') as savefile:
            svfile = savefile.read()
        sf = json.loads(svfile)
        global pan, waffeAusgewaehlt, smrtlnk, ammocnt
        paras['koerperlich'] = sf['koerperlich']
        paras['geistig'] = sf['geistig']
        paras['edge'] = sf['edge']
        paras['panzerung'] = sf['panzerung']['num']
        pan = sf['panzerung']['name']
        ammocnt = sf['ammocnt']
        waffeAusgewaehlt[0] = sf['waffe']['0']
        waffeAusgewaehlt[1] = sf['waffe']['1']
        waffeAusgewaehlt[2] = sf['waffe']['2']
        waffeAusgewaehlt[3] = sf['waffe']['3']
        waffeAusgewaehlt[4] = sf['waffe']['4']
        waffeAusgewaehlt[5] = sf['waffe']['5']
        smrtlnk = sf['smartlink']

def svsfile():
    global pan, waffeAusgewaehlt, smrtlnk, sf, ammocnt
    sf['koerperlich'] = paras['koerperlich']
    sf['geistig'] = paras['geistig']
    sf['edge'] = paras['edge']
    sf['panzerung'] = {}
    sf['panzerung']['num'] = paras['panzerung']
    sf['panzerung']['name'] = pan
    sf['ammocnt'] = ammocnt
    sf['waffe'] = {}
    sf['waffe']['0'] = waffeAusgewaehlt[0]
    sf['waffe']['1'] = waffeAusgewaehlt[1]
    sf['waffe']['2'] = waffeAusgewaehlt[2]
    sf['waffe']['3'] = waffeAusgewaehlt[3]
    sf['waffe']['4'] = waffeAusgewaehlt[4]
    sf['waffe']['5'] = waffeAusgewaehlt[5]
    sf['smartlink'] = smrtlnk
    with codecs.open('sf-' + character['alias'] + '.json', 'w', 'utf-8-sig') as f:
        json.dump(sf, f, indent=4)

### SCH
def sch():
    print('')
    liner()
    print('', end='')
    choice = input(bcolors.GREENh + ' >> ' + bcolors.ENDC)
    exec_menu(choice)
    return

### SMARTLINK
def checksmrtlnk():
    global smrtlnktype, smrtlnk
    if character['cyberwares'] != None:
        x = character['cyberwares']['cyberware']
        if type(x) == dict:
            if x['category'] == 'Augen-Cyberware':
                if x['children'] != None:
                    if type(x['children']['cyberware']) == dict:
                        if x['children']['cyberware']['name'] == 'Smartlink':
                            smrtlnktype = 'cyberware'
                            smrtlnk = True
                    elif type(x['children']['cyberware']) == list:
                        for numma,namma in enumerate(x['children']['cyberware']):
                            if x['children']['cyberware'][numma]['name'] == 'Smartlink':
                                smrtlnktype = 'cyberware'
                                smrtlnk = True
        elif type(x) == list:
            for i,n in enumerate(x):
                y = x[i]
                if y['category'] == 'Augen-Cyberware':
                    if y['children'] != None:
                        if type(y['children']['cyberware']) == dict:
                            if y['children']['cyberware']['name'] == 'Smartlink':
                                smrtlnktype = 'cyberware'
                                smrtlnk = True
                        elif type(y['children']['cyberware']) == list:
                            for numma,namma in enumerate(y['children']['cyberware']):
                                if y['children']['cyberware'][numma]['name'] == 'Smartlink':
                                    smrtlnktype = 'cyberware'
                                    smrtlnk = True
    if smrtlnktype == '' and character['gears'] != None:
        x = character['gears']['gear'] 
        for i,n in enumerate(x):
            if x[i]['name'].find('Brille') != 1 or x[i]['name'].find('Kontaktlinsen') != 1:
                if x[i]['children'] != None:
                    if type(x[i]['children']['gear']) == dict:
                        if x[i]['children']['gear']['name'].find('Smartlink') != -1:
                            smrtlnktype = 'extern'
                    elif type(x[i]['children']['gear']) == list:
                        for num,nam in enumerate(x[i]['children']['gear']):
                            if x[i]['children']['gear'][num]['name'].find('Smartlink') != -1:
                                smrtlnktype = 'extern'
    return

### PROBEN
def probenarten():
    clscrn()
    headerprnt()
    print(bcolors.IND + bcolors.UNDERLINE + 'Arten von Proben:\n' + bcolors.ENDC)
    print(bcolors.IND + (bcolors.GREENh + 'Erfolgsproben' + bcolors.ENDC + ':').ljust(30) + 'Fertigkeit + Attribut  [Limit](Schwellenwert)')
    print(bcolors.IND + (bcolors.GREENh + 'Vergleichende Probe' + bcolors.ENDC + ':').ljust(30) + 'Fertigkeit + Attribut  [Limit]' + bcolors.FAILh + ' gegen ' + bcolors.ENDC + 'Fertigkeit + Attribut [Limit]')
    print(bcolors.IND + (bcolors.GREENh + 'Ausgedehnte Probe' + bcolors.ENDC + ':').ljust(30) + 'Fertigkeit + Attribut  [Limit](Schwellenwert, Intervall)')
    print('\t\t\t\t' + bcolors.IND + bcolors.BLUEh + 'Vorgang über längere Zeit')
    print('\t\t\t\t' + bcolors.IND + bcolors.BLUEh + 'Mehrere Würfelwürfe, Erfolge werden akkumuliert, bis Schwellenwert erreicht ist oder die Zeit ausgeht.')
    print('\t\t\t\t' + bcolors.IND + bcolors.BLUEh + 'Jeder folgende Würfelwurf um einen Würfel reduziert.\n')
    print(bcolors.IND + (bcolors.GREENh + 'Teamworkproben' + bcolors.ENDC + ':').ljust(30) + '1. Anführer und Helfer bestimmen')
    print(bcolors.IND + (bcolors.GREENh + ' ' + bcolors.ENDC + '').ljust(30) + '2. Helfer würfeln Fertigkeit + Attribut [Limit]')
    print(bcolors.IND + (bcolors.GREENh + ' ' + bcolors.ENDC + '').ljust(30) + '3. Jeder Erfolg wird zu dem Würfelpool des Anführers addiert')
    print(bcolors.IND + (bcolors.GREENh + ' ' + bcolors.ENDC + '').ljust(30) + '4. Jeder Helfer, der einen Erfolg hat wird zu den Limits des Anführers addiert')
    print(bcolors.IND + (bcolors.GREENh + ' ' + bcolors.ENDC + '').ljust(30) + bcolors.FAILh + 'Maximum an Zusatzwürfeln für WP ist die Fertigkeitsstufe des Anführers'+ bcolors.ENDC)
    print(bcolors.IND + (bcolors.GREENh + ' ' + bcolors.ENDC + '').ljust(30) + bcolors.FAILh +  'Falls Helfer Patzer würfelt, keine Erhöhung des Limits durch ihn!' + bcolors.ENDC)
    print(bcolors.IND + (bcolors.GREENh + ' ' + bcolors.ENDC + '').ljust(30) + bcolors.FAILh +  'Falls Helfer kritischen Patzer würfeln, garkeine Erhöhung des Limits für Anführer!' + bcolors.ENDC)
    sch()

### ATTRIBUTSPROBEN
def attributsproben():
    clscrn()
    headerprnt()
    #S.153
    sch()

### WIDERSTAND
def widerstand():
    clscrn()
    headerprnt()
    print(bcolors.IND + bcolors.UNDERLINE + 'Widerstände:\n' + bcolors.ENDC)
    print(bcolors.IND + bcolors.GREENh + 'Abhängigkeit:' + bcolors.ENDC + ' K: KON+WIL G: WIL+LOG')

    if imkampf == True:
        print('' + bcolors.FAILh)
        liner()
        print('', end='')
        s = input(' >_> ' + bcolors.ENDC)
        kampf()
    else:
        sch()

### ASTRAL
def getastral():
    if character['magician'] == 'True':
        global isastral
        global ppan
        funbreak = 0
        while funbreak <= 1:
            clscrn()
            headerprnt()
            print(bcolors.IND + bcolors.ASTRALh + bcolors.BOLD + 'Ist der Charakter im Astralraum unterwegs? (' + bcolors.ENDC + bcolors.WARNINGh + 'y' + bcolors.ASTRALh + bcolors.BOLD + '/' + bcolors.ENDC + bcolors.WARNINGh + 'n' + bcolors.ASTRALh + bcolors.BOLD + ')')
            print('')
            print(10*'______ ')
            s = input(' >>> ')
            if s == 'q':
                funbreak = 1
                break
            elif s == 'y':
                isastral = True
                ppan = paras['panzerung']
                paras['panzerung'] = 0
                funbreak = 1
                break
            elif s == 'n':
                isastral = False
                paras['panzerung'] = ppan 
                funbreak = 1
                break
            else:
                print(bcolors.IND + bcolors.WARNINGh + str(s) + ' ist keine gültige Angabe, nochmal!' + bcolors.ENDC)
    else:
        clscrn()
        headerprnt()
        print('\n\n\n\t' + bcolors.IND + 'Charakter ist nicht erwacht!\n\n\n')
        print('')
        liner()
        s = input(' >>> ')
    if imkampf == True:
        kampf()
    else:
        main_menu()

### ZAUBERAUFRECHT
def zauberaufrecht():
    funbreak = 0
    global zauberaufrechthalten
    clscrn()
    headerprnt()
    if character['magician'] == 'True':
        print(bcolors.IND + bcolors.ASTRALh + bcolors.UNDERLINE + 'Aufrechterhaltene Zauber:' + bcolors.ENDC)
        print('\n\t\t' + bcolors.IND + "'" + bcolors.BLUEh + '1' + bcolors.ENDC + "' Der Charakter hält einen Zauber " + bcolors.GREENh + 'aufrecht' + bcolors.ENDC + ".")
        print('\t\t' + bcolors.IND + "'" + bcolors.BLUEh + '2' + bcolors.ENDC + "' Der Charakter lässt " + bcolors.GREENh + 'einen' + bcolors.ENDC + " Zauber " + bcolors.GREENh + 'fallen' + bcolors.ENDC + ".")
        print('\t\t' + bcolors.IND + "'" + bcolors.BLUEh + '3' + bcolors.ENDC + "' Der Charakter lässt " + bcolors.GREENh + 'alle' + bcolors.ENDC + " Zauber " + bcolors.GREENh + 'fallen' + bcolors.ENDC + ".")
        print('\t\t' + bcolors.IND + "'" + bcolors.BLUEh + 'q' + bcolors.ENDC + "' Beenden.")
        print('')
        liner()
        while funbreak <= 1:
            s = input(bcolors.ASTRALh + ' >>> ' + bcolors.ENDC)
            if s == 'q':
                funbreak = 1
                break
            elif s == '1':
                mali['zauber'] -= 2
                zauberaufrechthalten = True
                funbreak = 1
                break
            elif s == '2':
                mali['zauber'] += 2
                if mali['zauber'] >= 0:
                    mali['zauber'] = 0
                    zauberaufrechthalten = False
                funbreak = 1    
                break
            elif s == '3':
                mali['zauber'] = 0
                zauberaufrechthalten = False
                funbreak = 1    
                break
            else:     
                print('\t' + bcolors.IND + bcolors.WARNINGh + str(s) + bcolors.FAILh + ' ist keine gültige Angabe, nochmal!' + bcolors.ENDC)
    else:
        print('\n\n\t' + bcolors.IND + 'Charakter ist nicht erwacht!\n\n\n')
        print('')
        liner()
        s = input(bcolors.ASTRALh + ' >>> ' + bcolors.ENDC)        
    if imkampf == True:
        kampf()
    else:
        main_menu()

def astral_menu():
    headerprnt()
    print(bcolors.IND,bcolors.UNDERLINE + 'Astral Projizieren:' + bcolors.ENDC)
    print('\t' + bcolors.IND + ('- Kann max [MAG x 2 Std] projizieren, bevor sich die Signatur auflöst. Pause muss gleich lang sein').ljust(140))
    print('\t' + bcolors.IND + ('- Signaturen erlischen erst nach [Anzahl Std gleich KS des magischen Effektes]').ljust(140))
    print('\t' + bcolors.IND + ('- Signaturen lesen:' + bcolors.GREENh + ' Askennen + INT [Astral](3)').ljust(140) + bcolors.ENDC + '\t SR5 312')
    print('\t' + bcolors.IND + ('- Signaturen verwischen:' + bcolors.GREENh + ' komplexe Handlung = um 1 Std beschleunigt').ljust(140) + bcolors.ENDC + '\t SR5 312')
    print('\n' + bcolors.IND,bcolors.UNDERLINE + 'Astral Wahrnehmen:' + bcolors.ENDC)
    print('\t' + bcolors.IND + ('- temporäres Dualwesen:' + bcolors.GREENh + ' WP-Malus von -2 auf alle physischen Handlungen').ljust(140) + bcolors.ENDC + '\t SR5 312')
    print('\t' + bcolors.IND + ('- Askennen:' + bcolors.GREENh + ' Askennen + INT [Astral]').ljust(140) + bcolors.ENDC + '\t SR5 312')
    print('\n' + bcolors.IND,bcolors.UNDERLINE + 'Astrale Entdeckung:' + bcolors.ENDC)
    print('\t' + bcolors.IND + ('- Falls durch eine physische Aura gleitet, hat Wesen die Chance zu entdecken:' + bcolors.GREENh + ' Wahrnehmung + INT [Geistig](4)').ljust(140) + bcolors.ENDC + '\t SR5 314')
    print('\t' + bcolors.IND + ('- Erwachte haben WP-Bonus von ' + bcolors.GREENh + '+2').ljust(140) + bcolors.ENDC + '\t SR5 314')
    print('\t' + bcolors.IND + ('- Wachpersonal ist geschult das Frösteln und Kitzeln als astralen Eindringling zu erkennen').ljust(140) + bcolors.ENDC + '\t SR5 278')
    print('\n' + bcolors.IND,bcolors.UNDERLINE + 'Astrales Spurenlesen:' + bcolors.ENDC)
    print('\t' + bcolors.IND + ('- fast alles hat eine astrale Verbindung zu dem, der es hervorgerufen hat' + bcolors.GREENh + '').ljust(140) + bcolors.ENDC + '\t SR5 314')
    print('\t' + bcolors.IND + ('- astrale Signatur lässt sich askennen und zurückverfolgen:' + bcolors.GREENh + ' Ausgedehnte Probe: [ Askennen + INT [Astral](5, 1 Std) ]').ljust(140) + bcolors.ENDC + '\t SR5 314')
    print('\t\t' + bcolors.IND + bcolors.BLUEh + ('Je verstrichene Std, seit die astrale Verbindung aktiv war:').ljust(90) + bcolors.GREENh + '+1 auf Schwellenwert')
    print('\t\t' + bcolors.IND + bcolors.BLUEh + ('Ziel befindet sich hinter einer Manabarriere').ljust(90) + bcolors.GREENh + '+KS der Barriere auf Schwellenwert')
    print('\t\t' + bcolors.IND + bcolors.BLUEh + ('Auffinden des Beschwörers durch gebundenen(' + bcolors.WARNINGh + '1' + bcolors.BLUEh + ') oder ungebundenen(' + bcolors.WARNINGh + '2' + bcolors.BLUEh + ') Geist').ljust(110) + bcolors.WARNINGh + '1' + bcolors.GREENh + ': +0, ' + bcolors.WARNINGh + '2' + bcolors.GREENh + ': +2 auf Schwellenwert' + bcolors.ENDC)
    sch()

def alchemy():
    clscrn()
    headerprnt()
    print(bcolors.IND + bcolors.UNDERLINE + 'Alchemie:' + bcolors.ENDC + '\tSR5 304\n')
    print(bcolors.IND + 'Gegenstände, die klein genug sind, um getragen und gehoben zu werden, können mithilfe von Alchemie zu alchemischen Erzeugnissen verzaubert werden.')
    print(bcolors.IND + 'Dabei wird ein Gegenstand der Tradition nach bearbeitet. (beritzt, verätzt, bemalt, ...)')
    print(bcolors.IND + '\tProbe zum Erkennen eines geeigneten Gegenstandes:' + bcolors.GREENh + ' Arkana + INT [geistig]\n' + bcolors.ENDC)
    print(bcolors.IND + bcolors.UNDERLINE + 'Wirken von Alchemie:' + bcolors.ENDC)
    print(bcolors.IND + 'Auswahl von Zauber und Kraftstufe.' + bcolors.FAILh + '\tKraftstufe nicht höher als MAGx2!' + bcolors.ENDC)
    print(bcolors.IND + 'Auswahl des Herzstücks.' + bcolors.FAILh + '\t\tHerzstück darf keine Aura besitzen!\n' + bcolors.ENDC)
    print(bcolors.IND + 'Auswahl des Auslösers:')
    print(bcolors.IND + ' Befehl:'.ljust(25) + bcolors.BLUEh + 'Verzauberer löst die Wirkung selbst aus (physische Ebene oder manifestiert).' + bcolors.ENDC)
    print(bcolors.IND + ' '.ljust(25) + bcolors.BLUEh + 'Erzeugnis muss sich in Blickfeld befinden.' + bcolors.ENDC)
    print(bcolors.IND + ' '.ljust(25) + bcolors.BLUEh + 'Auslösen ist eine einfache Handlung.' + bcolors.ENDC)
    print(bcolors.IND + ' '.ljust(25) + bcolors.GREENh + 'Entzug + 2' + bcolors.ENDC)
    print(bcolors.IND + ' Kontakt:'.ljust(25) + bcolors.BLUEh + 'Das nächste Lebewesen, das das Erzeugnis berührt, löst die Wirkung aus.' + bcolors.ENDC)
    print(bcolors.IND + ' '.ljust(25) + bcolors.GREENh + 'Entzug + 1' + bcolors.ENDC)
    print(bcolors.IND + ' Zeitzünder:'.ljust(25) + bcolors.BLUEh + 'Verzauberer wählt Zeitraum aus, bis Zauber zündet nach Fertigstellung des Erzeugnisses.' + bcolors.ENDC)
    print(bcolors.IND + ' '.ljust(25) + bcolors.BLUEh + 'Wenn Zeitspanne größer als die Wirksamkeit in Stunden, tritt die Wirkung verfrüht ein.' + bcolors.ENDC)
    print(bcolors.IND + ' '.ljust(25) + bcolors.GREENh + 'Entzug + 2\n' + bcolors.ENDC)
    print(bcolors.IND + 'Alchemische Aufbereitung:')
    print(bcolors.IND + ' Verzauberer muss für ' + bcolors.GREENh + 'Kraftstufe in Minuten' + bcolors.ENDC + ' ununterbrochen an Erzeugnis arbeiten, um es fertigzustellen.')
    print(bcolors.IND + ' Reagenzien sind als Limiterhöhung erlaubt.\n')
    print(bcolors.IND + ' Vergleichende Probe: ' + bcolors.GREENh + 'Alchemie + MAG [Kraftstufe]' + bcolors.FAILh + ' gegen ' + bcolors.GREENh + 'Kraftstufe des Erzeugnisses' + bcolors.ENDC)
    print(bcolors.IND + ' Wirksamkeit = ' + bcolors.GREENh + 'Nettoerfolge\n' + bcolors.ENDC)
    print(bcolors.IND + 'Entzugswiderstand:')
    print(bcolors.IND + ' Entzug wie bei Zauber + Erhöhung des Auslösers.')
    print(bcolors.IND + ' Wenn ' + bcolors.GREENh + 'Erfolge bei Alchemieprobe' + bcolors.ENDC + ' höher als Magieattribut, dann ist der Entzug körperlich, ansonsten geistig.\n')
    print(bcolors.IND + bcolors.FAILh + 'Patzer' + bcolors.ENDC + ': falscher Auslöser, Zeitspanne falsch, Entzug höher...')
    print(bcolors.IND + bcolors.FAILh + 'Kritischer Patzer' + bcolors.ENDC + ': lauf...\n')
    print(bcolors.IND + 'Erzeugnis:')
    print(bcolors.IND + ' Wirksamkeit legt fest wie lang und stark das Erzeugnis bei der Auslösung ist.')
    print(bcolors.IND + ' Das Erzeugnis hält die ' + bcolors.BLUEh + 'volle Wirksamkeit' + bcolors.ENDC + ' für ' + bcolors.GREENh + 'Wirksamkeit x2 Stunden' + bcolors.ENDC)
    print(bcolors.IND + ' Danach sinkt die Wirksamkeit um ' + bcolors.BLUEh + '1 pro Stunde' + bcolors.ENDC + '. Sie endet wenn sie auf 0 gesunken ist oder das Erzeugnis zerstört wird.')
    print('')
    liner()
    print(bcolors.IND + "'" + bcolors.BLUEh + 'm' + bcolors.ENDC + "' Einsatz von alchemischen Erzeugnissen")
    liner()
    print('', end='')
    choice = input(bcolors.GREENh + ' >> ' + bcolors.ENDC)
    if choice == 'm':
        alchemy_einsatz()
    else:
        exec_menu(choice)


def alchemy_einsatz():
    clscrn()
    headerprnt()
    print(bcolors.IND + bcolors.UNDERLINE + 'Einsatz von alchemischen Erzeugnissen:\n' + bcolors.ENDC)
    print(bcolors.IND + 'Die Wirkung des Zaubers ist wie bei der Spruchzauberei.')
    print(bcolors.IND + 'Dabei ist die Spruchzaubereiprobe: ' + bcolors.GREENh + 'Wirksamkeit + KS [KS]' + bcolors.ENDC + '  (anstatt Spruchzauberei + MAG [KS])')
    print(bcolors.IND + 'Wenn der Zauber aufrechterhalten werden muss, so hält er für ' + bcolors.GREENh + 'Wirksamkeit [Minuten]' + bcolors.ENDC)
    print(bcolors.IND + 'Permanente Zauber halten so lange, bis sie permanent geworden sind.')
    print(bcolors.IND + 'Ziele müssen sich auf der physischen Ebene befinden.\n')
    print(bcolors.IND + ' Berührung:'.ljust(40) + bcolors.BLUEh + 'Berührungszauber treffen das Lebewesen, das das Erzeugnis berührt.' + bcolors.ENDC)
    print(bcolors.IND + ' '.ljust(40) + bcolors.BLUEh + 'Wenn mehr als eins, dann wird Ziel von Hersteller gewählt (wenn ' + bcolors.GREENh + 'Befehls-Auslöser' + bcolors.BLUEh + ') sonst zufällig.\n' + bcolors.ENDC)
    print(bcolors.IND + ' Blickfeld:'.ljust(40) + bcolors.BLUEh + 'Ziel von Hersteller gewählt, wenn ' + bcolors.GREENh + 'Befehls-Auslöser' + bcolors.BLUEh + '.')
    print(bcolors.IND + ''.ljust(40) + bcolors.BLUEh + 'Ansonsten das nächste legale Ziel im Blickfeld.' + bcolors.ENDC)
    print(bcolors.IND + ' '.ljust(40) + bcolors.BLUEh + 'Max Entfernung: ' + bcolors.GREENh + 'Wirksamkeit x KS [Metern]\n' + bcolors.ENDC)
    print(bcolors.IND + ' Flächenzauber:'.ljust(40) + bcolors.BLUEh + 'Erzeugnis ist Zentrum mit Radius von ' + bcolors.GREENh + 'Wirksamkeit' + bcolors.BLUEh + ' in Metern.' + bcolors.ENDC)
    print('')
    liner()
    print('', end='')
    choice = input(bcolors.GREENh + ' >> ' + bcolors.ENDC)
    alchemy()

### EDGE
def looseedg():
    headerprnt()
    print(bcolors.IND + bcolors.UNDERLINE + 'Edge ausgeben:\n' + bcolors.ENDC)
    print('\t' + bcolors.IND + bcolors.GREENh + ('Die Grenzen sprengen' + bcolors.ENDC + ':').ljust(30) + " + Edge-Würfel zu WP (egal ob vor oder nach Würfeln). + " + bcolors.GREENh + 'Regel der Sechs' + bcolors.ENDC + '. Alle Limits werden ignoriert.')
    print('\t' + bcolors.IND + bcolors.GREENh + ('Zweite Chance' + bcolors.ENDC + ':').ljust(30) + ' Nochmal mit W ohne Erfolg. Patzer und Limits zählen trotzdem!')
    print('\t' + bcolors.IND + bcolors.GREENh + ('Die Initiative ergreifen' + bcolors.ENDC + ':').ljust(30) + ' Erster in seinen Initiativedurchgängen für eine Kampfrunde.')
    print('\t' + bcolors.IND + bcolors.GREENh + ('Blitzangriff' + bcolors.ENDC + ':').ljust(30) + ' Für Kampfrunde ' + bcolors.GREENh + '5W6' + bcolors.ENDC + ' Initiativewürfel.')
    print('\t' + bcolors.IND + bcolors.GREENh + ('Das war knapp' + bcolors.ENDC + ':').ljust(30) + ' Negieren der Auswirkungen eines Patzers, bzw. ein kritischer wird zum normalen Patzer.')
    print('\t' + bcolors.IND + bcolors.GREENh + ('Späte Rache' + bcolors.ENDC + ':').ljust(30) + ' Wenn Char kurz davor zu sterben oder bewusstlos zu werden, Probe auf: ' + bcolors.GREENh + 'KON + WIL (3)' + bcolors.ENDC + ' für eine letzte beliebige Handlung, außer Bewegung.')
    print('')
    print(bcolors.IND + bcolors.UNDERLINE + 'Edge verheizen:\n' + bcolors.ENDC)
    print('\t' + bcolors.IND + bcolors.WARNINGh + ('Durchbruch' + bcolors.ENDC + ':').ljust(30) + " Probe wir automatisch mit " + bcolors.GREENh + '4 Nettoerfolgen' + bcolors.ENDC + ' bestanden, solange Aktion und Fertigkeit zumindest improvisierbar.')
    print('\t' + bcolors.IND + bcolors.WARNINGh + ('Dem Tod von der Schippe' + bcolors.ENDC + ':').ljust(30) + " Charakter füllt wie durch ein Wunder nur den körperlichen Zustandsmonitor. Er muss " + bcolors.GREENh + 'stabilisiert' + bcolors.ENDC + ' werden. SL überlegt zusätzliche Auswirkungen.')
    print('')
    funbreak = 0
    while funbreak < 1:
        if int(paras['edge']) == 0:
            print('')
            liner()
            print('\n\n\n\n\n\t' + bcolors.IND + bcolors.BOLD + bcolors.FAILh + 'Kein Edge zum Ausgeben verfügbar!' + bcolors.ENDC + '\n\n\n\n')
            print('' + bcolors.WARNINGh)
            liner()
            print('', end='')
            edga = input(bcolors.WARNINGh + ' ##> ' + bcolors.ENDC)
            funbreak = 1
            break
        else:
            print('')
            liner()
            print(bcolors.IND + bcolors.GREENh + '1' + bcolors.ENDC + ' Edge ausgeben? (' + bcolors.BLUEh + 'y' + bcolors.ENDC + '/' + bcolors.BLUEh + 'n' + bcolors.ENDC + ')')
            print(''+ bcolors.WARNINGh)
            liner()
            print('', end='')
            edga = input(bcolors.WARNINGh + ' ##> ' + bcolors.ENDC)
            if edga == 'q':
                funbreak = 1
                break
            elif edga == 'n':
                funbreak = 1
                break
            elif edga == 'y':
                ge = int(paras['edge'])
                ge -= 1
                if ge < 0:
                    ge = 0
                paras['edge'] = str(ge)
                clscrn()
                headerprnt()
                print('\n\n\n\t\t' + bcolors.IND + bcolors.WARNINGh + bcolors.BOLD + '1 EDGE ausgegeben!' + bcolors.ENDC + '\n\n\n\n\n\n\n')
                print('' + bcolors.WARNINGh)
                liner()
                print('', end='')
                s = input(bcolors.WARNINGh + ' ##> ' + bcolors.ENDC)
                funbreak = 1
            else:
                print('\t\t' + bcolors.IND + bcolors.WARNINGh + edga + bcolors.FAILh + ' ist keine gültige Eingabe.' + bcolors.ENDC)
    if imkampf == True:
        kampf()
    else:
        main_menu()
    return

### NACHSCHLAGEN
def nachschlagen():
    headerprnt()
    widw = 100
    print(bcolors.IND + 'SR5 185: Waffenreichweiten')
    print('\n\n' + bcolors.IND + bcolors.UNDERLINE + 'Bücher [englisch - deutsch]'.ljust(widw) + 10*' ' + bcolors.ENDC)
    print(bcolors.IND + '[R5] Rigger 5 '.ljust(widw//4) + '- Asphaltkrieger'.ljust(widw//4) + 10*' ' + '[CF] Chrome Flesh '.ljust(widw//4) + '- Bodyshop'.ljust(widw//4))
    print(bcolors.IND + '[DT] Data Trails '.ljust(widw//4) + '- Datenpfade'.ljust(widw//4) + 10*' ' + '[KC] Kill Code '.ljust(widw//4) + '- Letaler Code'.ljust(widw//4))
    print(bcolors.IND + '[SS] Shadow Spells '.ljust(widw//4) + '- Schattenzauber'.ljust(widw//4) + 10*' ' + '[RF] Run Faster '.ljust(widw//4) + '- Schattenläufer'.ljust(widw//4))
    print(bcolors.IND + '[SG] Street Grimoire '.ljust(widw//4) + '- Straßengrimoire'.ljust(widw//4) + 10*' ' + '[SL] Street Lethal '.ljust(widw//4) + '- Tödliche Schatten'.ljust(widw//4))
    print(bcolors.IND + '[FA] Forbidden Arcana '.ljust(widw//4) + '- Verbotene Künste'.ljust(widw//4) + 10*' ' + '[RG] Run & Gun '.ljust(widw//4) + '- Kreuzfeuer'.ljust(widw//4))
    print(bcolors.IND + '[GH] Gun Heaven '.ljust(widw//4) + '- Feuer und Stahl'.ljust(widw//4) + 10*' ' + '[HT] Hard Targets '.ljust(widw//4) + '- Harte Ziele'.ljust(widw//4))
    sch()

### KAMPF
def kampf():
    global imkampf, fernk
    imkampf = True
    fernk = False
    def subexec_menu(choice):
        clscrn()
        ch = choice.lower()
        if ch == '':
            kampf_main()
        else:
            try:
                kampfmenu_actions[ch]()
            except KeyError:
                print(bcolors.IND + 'Invalid selection, please try again.\n')
                kampf_main()
        return
    def sub_ch():
        global fernk
        print('\n' + bcolors.FAILh + (linewidth//10)*'____ ____ ' + bcolors.ENDC + '\n')
        choice = input(bcolors.FAILh + ' *>> ' + bcolors.ENDC)
        if fernk == False:
            subexec_menu(choice)
        elif fernk == True:
            fernkampf()
        return

### K.ASTRAL
    def astralkampf():
        headerprnt()
        print(bcolors.IND + bcolors.UNDERLINE + 'Astralkampf:' + bcolors.ENDC) 
        print('\t' + bcolors.IND + ('- Wie Nahkampf auf physischer Ebene').ljust(40) + bcolors.GREENh + 'Astralkampf + WIL' + bcolors.ENDC)
        print('\t' + bcolors.IND + ('- Keine Fernkampfwaffen -> ' + bcolors.BLUEh + 'waffenlos' + bcolors.ENDC + ',' + bcolors.BLUEh + ' aktivierter Fokus' + bcolors.ENDC + ' oder' + bcolors.BLUEh + ' Manazauber').ljust(140) + bcolors.ENDC)
        print('\n\t' + bcolors.IND + ('Waffenlos:').ljust(40) + bcolors.GREENh + 'Astralkampf + WIL [Astral] '.ljust(30) + bcolors.FAILh + ' gegen INT + LOG' + bcolors.ENDC)
        print('\t' + bcolors.IND + ('Waffenfokus:').ljust(40) + bcolors.GREENh + 'Astralkampf + WIL [Präzision] '.ljust(30) + bcolors.FAILh + ' gegen INT + LOG' + bcolors.ENDC)
        print('\n\t' + bcolors.IND + bcolors.UNDERLINE+ 'Schaden' + bcolors.ENDC)
        print('\t\t' + bcolors.IND + ('Zauberer waffenlos').ljust(40) + bcolors.GREENh + 'CHA' + bcolors.ENDC)
        print('\t\t' + bcolors.IND + ('Waffenfokus').ljust(40) + bcolors.GREENh + 'CHA ersetzt STR in Waffe' + bcolors.ENDC)
        print('\t\t' + bcolors.IND + ('Geist').ljust(40) + bcolors.GREENh + 'KS' + bcolors.ENDC)
        print('\t\t' + bcolors.IND + ('Watcher').ljust(40) + bcolors.GREENh + '1' + bcolors.ENDC)
        print('\n\t' + bcolors.IND + bcolors.UNDERLINE+ 'Verteidigung' + bcolors.ENDC)        
        print('\t\t' + bcolors.IND + ('WIL + Astralpanzerung').ljust(40) + bcolors.GREENh + '{willenskraft}'.format(**paras) + bcolors.ENDC)


        sub_ch()
    
    def schaden():
        headerprnt()
        print(bcolors.IND + bcolors.UNDERLINE + 'Elektrizitätsschaden:' + bcolors.ENDC)
        print(bcolors.IND + ' Trifft bei Kontakt mit elektrischer Energie. Je nach Quelle körperlich oder geistig')
        print(bcolors.IND + ' Elektrische Isolierung addiert die Stufe auf Panzerung')
        print(bcolors.IND + ' Vielleicht erhöhte Leitfähigkeit durch Wasser')
        print(bcolors.IND + ' ' + bcolors.FAILh + 'Nebenwirkungen' + bcolors.ENDC + ': ' + bcolors.GREENh + '-1' + bcolors.ENDC + ' WP-Mod auf alle Proben (außer Schadenswiderstandsproben) für 1 Kampfrunde')
        print(bcolors.IND + ' \tsofortige Senkung der Initiative um ' + bcolors.GREENh + '5' + bcolors.ENDC + '. Wenn schon 0, dann Senkung in nächster Runde.')
        print(bcolors.IND + ' ' + bcolors.FAILh + 'Nebenwirkung bei elektrischen Geräten' + bcolors.ENDC + ': Kurzschlüsse und Überladungen. S.225')
        print(bcolors.IND + ' \t\tzusätzlicher Matrixschaden in Höhe abgerund. Hälfte des körp. Schadens.')
        sub_ch()

    def initiative():
        headerprnt()
        print(bcolors.IND + bcolors.UNDERLINE + 'Initiative:' + bcolors.ENDC)
        print('\n\t' + bcolors.IND + ('Normale Initiative:').ljust(40) + ('(' + bcolors.BLUEh + 'REA + INT' + bcolors.ENDC + ') + ' + bcolors.BLUEh + '1' + bcolors.ENDC + 'W6').ljust(40) + bcolors.GREENh + '\t\t\t{init!s:>8}'.format(**character) + bcolors.ENDC) 
        print('\n\t' + bcolors.IND + ('Astrale Initiative:').ljust(40) + ('(' + bcolors.BLUEh + 'INT x2' + bcolors.ENDC + ') + ' + bcolors.BLUEh + '2' + bcolors.ENDC + 'W6').ljust(40), end='') 
        if character['magician'] == True:
            print(bcolors.GREENh + '\t\t\t{astralinit!s:>8}'.format(**character) + bcolors.ENDC) 
        else:
            print(bcolors.GREENh + '\t\t\tnicht erwacht' + bcolors.ENDC)
        print('\n\t' + bcolors.IND + ('Matrix-Initiative (AR):').ljust(40) + ('(' + bcolors.BLUEh + 'REA + INT' + bcolors.ENDC + ') + ' + bcolors.BLUEh + '1' + bcolors.ENDC + 'W6').ljust(40) + bcolors.GREENh + '\t\t\t{matrixarinit!s:>8}'.format(**character) + bcolors.ENDC) 
        print('\n\t' + bcolors.IND + ('Matrix-Initiative (kaltes Sim):').ljust(40) + ('(' + bcolors.BLUEh + 'Datenverarbeitung + INT' + bcolors.ENDC + ') + ' + bcolors.BLUEh + '3' + bcolors.ENDC + 'W6').ljust(40) + bcolors.GREENh + '\t{matrixcoldinit!s:>8}'.format(**character) + bcolors.ENDC) 
        print('\n\t' + bcolors.IND + ('Matrix-Initiative (heißes Sim):').ljust(40) + ('(' + bcolors.BLUEh + 'Datenverarbeitung + INT' + bcolors.ENDC + ') + ' + bcolors.BLUEh + '4' + bcolors.ENDC + 'W6').ljust(40) + bcolors.GREENh + '\t{matrixhotinit!s:>8}'.format(**character) + bcolors.ENDC) 
        sub_ch()

    ### K.FERNK
    def fernkampf():
        global fernk
        fernk = True
        headerprnt()
        def subsubexec_menu(choice):
            clscrn()
            ch = choice.lower()
            if ch == '':
                fernkampf_main()
            else:
                try:
                    fernkampfmenu_actions[ch]()
                except KeyError:
                    print(bcolors.IND + 'Invalid selection, please try again.\n')
                    fernkampf_main()
            return
        def subsub_ch():
            print('\n' + bcolors.FAILh + (linewidth//10)*'____ ____ ' + bcolors.ENDC + '\n')
            choice = input(bcolors.FAILh + ' *>> ' + bcolors.ENDC)
            subsubexec_menu(choice)
            return
        
        def umweltmodi():
            clscrn()
            headerprnt()
            ueb = ['Sichtverhältnisse', 'Beleuchtung', 'Wind', 'Entfernung', 'Modifikator']
            print(bcolors.IND + bcolors.UNDERLINE + '{0:^35}{1:^40}{2:^35}{3:^30}{4:^20}'.format(*ueb) + bcolors.ENDC)
            print('\n' + bcolors.IND + 'Freie Sicht'.center(35) + 'Gute Beleuchtung/Keine Blendung'.center(40) + 'Windstille oder leichte Brise'.center(35) + 'Kurz'.center(30) + '-'.center(20))
            print('\n' + bcolors.IND + 'Leichter Regen/Nebel/Rauch'.center(35) + 'Teilbeleuchtung/Schwache Blendung'.center(40) + 'Leichter Wind'.center(35) + 'Mittel'.center(30) + '-1'.center(20))
            print('\n' + bcolors.IND + 'Mittlerer Regen/Nebel/Rauch'.center(35) + 'Schwache Beleuchtung/Mittlere Blendung'.center(40) + 'Steife Brise'.center(35) + 'Lang'.center(30) + '-3'.center(20))
            print('\n' + bcolors.IND + 'Starker Regen/Nebel/Rauch'.center(35) + 'Völlige Dunkelheit/Starke Blendung'.center(40) + 'Sturm'.center(35) + 'Maximal'.center(30) + '-6'.center(20))
            print('\n' + bcolors.IND + 'Zwei oder mehr Modifikatoren der Kategorie -6'.ljust(140) + '-10'.center(20))
            print('')
            print('\n' + bcolors.FAILh + (linewidth//10)*'____ ____ ' + bcolors.ENDC + '\n')
            choice = input(bcolors.FAILh + ' *>> ' + bcolors.ENDC)
            kampfregeln()


        def kampfregeln():
            clscrn()
            headerprnt()
            print(bcolors.IND + bcolors.UNDERLINE + 'Vergleichende Probe Angreifer vs Verteidiger' + bcolors.ENDC)
            print('\n' + bcolors.IND + 'Angriff:'.ljust(40) + 'Fertigkeitswert + Attribut + Mod [Limit/Präz]')
            print('\n' + bcolors.IND + 'Verteidigung:'.ljust(40) + 'REA + INT + Mod')
            print(bcolors.IND + ' '.ljust(40) + bcolors.GREENh + 'Volle Abwehr' + bcolors.ENDC + ': REA + INT + WIL + Mod')
            print('\n\n' + bcolors.IND + bcolors.UNDERLINE + 'Vergleich der Erfolge' + bcolors.ENDC)
            print('\n' + bcolors.IND + 'Verteidiger hat mehr Erfolge:'.ljust(50) + bcolors.BLUEh + 'erfolgreich ausgewichen' + bcolors.ENDC)
            print(bcolors.IND + 'Verteidiger hat gleich viele Erfolge:'.ljust(50) + 'Streifschuss (' + bcolors.BLUEh + 'Berührungsschaden' + bcolors.ENDC + ')')
            print(bcolors.IND + 'Verteidiger hat weniger Erfolge:'.ljust(50))
            print(bcolors.IND + '        Modifizierter Schadenscode:'.ljust(50) + bcolors.FAILh + 'Nettoerfolge + Schadenscode der Waffe' + bcolors.ENDC)
            print(bcolors.IND + '        Modifizierter Panzerungswert:'.ljust(50) + bcolors.FAILh + 'DK reduziert Panzerung des Verteidigers' + bcolors.ENDC)
            print('\n\n' + bcolors.IND + bcolors.UNDERLINE + 'Vergleich mod. Schaden und mod. Panzerung' + bcolors.ENDC)
            print('\n\t' + bcolors.IND + 'Mod. Schadenscode ist kleiner: ' + bcolors.BLUEh + 'geistiger Schaden' + bcolors.ENDC)
            print('\t' + bcolors.IND + 'Mod. Schadenscode ist größer: ' + bcolors.BLUEh + 'körperlicher Schaden' + bcolors.ENDC)
            print('\n\n' + bcolors.IND + bcolors.UNDERLINE + 'Schaden widerstehen' + bcolors.ENDC)
            print('\n' + bcolors.IND + 'Verteidiger würfelt: ' + bcolors.BLUEh + 'KON + mod. Panzerung' + bcolors.ENDC + ', um Schaden zu widerstehen.')
            print('\n\n')
            print(bcolors.FAILh + linewidth*'_' + bcolors.ENDC)
            print("\n'" + bcolors.BLUEh + 'm' + bcolors.ENDC + "' Umweltmodifikatoren")
            print(bcolors.FAILh + (linewidth//10)*'____ ____ ' + bcolors.ENDC + '\n')
            choice = input(bcolors.FAILh + ' *>> ' + bcolors.ENDC)
            if choice == 'm':
                umweltmodi()
            else:
                subsubexec_menu(choice)           

        def feuermodi():
            headerprnt()
            txtwdth = 65 
            txtwdthtwo = txtwdth-15
            txtwdththree = txtwdth-25
            txtwdthfour = txtwdth-30
            print(bcolors.IND + bcolors.UNDERLINE + 'Modus'.ljust(txtwdth-6) + ('Verteidigungsmodifikator' + bcolors.WARNINGh + '*' + bcolors.ENDC + bcolors.UNDERLINE).rjust(txtwdthtwo) + 'Munitionsverbrauch'.rjust(txtwdththree) + ('{:>40}'.format('Anmerkungen     ')).rjust(txtwdthfour) + bcolors.ENDC)
            print('\n' + bcolors.IND + (bcolors.GREENh + 'EM' + bcolors.ENDC + ' - Einzelschussmodus').ljust(txtwdth) +  ' 0'.center(txtwdthtwo) + ' 1'.center(txtwdththree) + 'Kein Rückstoß'.center(txtwdthfour))
            print(bcolors.IND + (bcolors.GREENh + 'HM' + bcolors.ENDC + ' - Halbautomatischer Modus').ljust(txtwdth) +  ' 0'.center(txtwdthtwo) + ' 1'.center(txtwdththree) + '-'.center(txtwdthfour))
            print(bcolors.IND + (bcolors.GREENh + 'HS' + bcolors.ENDC + ' - Halbautomatische Salve').ljust(txtwdth) +  '-2'.center(txtwdthtwo) + ' 3'.center(txtwdththree) + '-'.center(txtwdthfour))
            print(bcolors.IND + (bcolors.GREENh + 'SM' + bcolors.ENDC + ' - Salvenmodus').ljust(txtwdth) +  '-2'.center(txtwdthtwo) + ' 3'.center(txtwdththree) + '-'.center(txtwdthfour))
            print(bcolors.IND + (bcolors.GREENh + 'LS/AM' + bcolors.ENDC + '(e) - Lange Salve / Vollautomatischer Modus (einf. Handlung)').ljust(txtwdth) +  '-5'.center(txtwdthtwo-18) + ' 6'.center(txtwdththree+18) + '-'.center(txtwdthfour-18))
            print(bcolors.IND + (bcolors.GREENh + 'AM' + bcolors.ENDC + '(k) - Vollautomatischer Modus (kompl. Handlung)').ljust(txtwdth) +  '-9'.center(txtwdthtwo) + '10'.center(txtwdththree) + '-'.center(txtwdthfour))
            print(bcolors.IND + bcolors.GREENh + 'Sperrfeuer'.ljust(txtwdth-9) + bcolors.ENDC +  'Deckung oder Hinwerfen'.center(txtwdthtwo) + '20'.center(txtwdththree) + 'Kein Rückstoß'.center(txtwdthfour))
            liner()
            print(bcolors.IND + bcolors.WARNINGh + '*' + bcolors.ENDC + 'Sinkt der Verteidigungswürfelpool durch den Modifikator auf unter Null, werden die überzähligen Modifikatorpunkte zum Angriffwürfelpool addiert.')
            subsub_ch()
        
        ### SCHUSS
        def schuss():
            def getammo(strng):
                oi = ""
                for s in strng:
                    if s.isdigit() == True:
                        oi += s
                return int(oi)
            def chckammo(ammocnt,x):
                if (ammocnt - x) <= 0:
                    return ammocnt
                else:
                    return x
            headerprnt()
            y = character['gears']['gear']
            x = character['weapons']['weapon']
            global waffeAusgewaehlt, ammocnt
            modEM = modHM = modSM = modAM = False
            if waffeAusgewaehlt[0] == ' ' or waffeAusgewaehlt[5] == 'Waffenlos' or waffeAusgewaehlt[5] == 'Klingenwaffen' or waffeAusgewaehlt[5] == 'Knüppel':
                print('\n\n' + bcolors.IND + 'Charakter muss eine Fernkampfwaffe auswählen, um schießen zu können!\n')
            elif waffeAusgewaehlt[1] == ' ' or waffeAusgewaehlt[1] == '':
                print('\n\n' + bcolors.IND + 'Charakter muss einen Munitionstyp auswählen, um schießen zu können!\n')
            else:
                chlist = ['r']
                for i,namm in enumerate(x):
                    if x[i]['name'] == waffeAusgewaehlt[0] and waffeAusgewaehlt[5] != 'Unterlaufwaffen':
                        if x[i]['mode'].find('EM') != -1:
                            modEM = True
                            chlist.append('EM')
                        if x[i]['mode'].find('HM') != -1:
                            modHM = True
                            chlist.append('HM')
                        if x[i]['mode'].find('SM') != -1:
                            modSM = True
                            chlist.append('HS')
                            chlist.append('SM')
                        if x[i]['mode'].find('AM') != -1:
                            modAM = True
                            chlist.append('LS')
                            chlist.append('AM')
                            chlist.append('SF')
                        magtyp = x[i]['ammo']
                        magmax = getammo(x[i]['ammo'])
                        for num,nam in enumerate(y):
                            if y[num]['name'] == waffeAusgewaehlt[1] and x[i]['category'] == y[num]['extra']:
                                ammonum = int(y[num]['qty'])
                                ynum = num
                    elif waffeAusgewaehlt[5] == 'Unterlaufwaffen' and 'underbarrel' in x[i].keys() and x[i]['underbarrel']['weapon']['fullname'] == waffeAusgewaehlt[0]:
                        if x[i]['underbarrel']['weapon']['mode'].find('EM') != -1:
                            modEM = True
                            chlist.append('EM')
                        if x[i]['underbarrel']['weapon']['mode'].find('HM') != -1:
                            modHM = True
                            chlist.append('HM')
                        if x[i]['underbarrel']['weapon']['mode'].find('SM') != -1:
                            modSM = True
                            chlist.append('HS')
                            chlist.append('SM')
                        if x[i]['underbarrel']['weapon']['mode'].find('AM') != -1:
                            modAM = True
                            chlist.append('LS')
                            chlist.append('AM')
                            chlist.append('SF')
                        magtyp = x[i]['underbarrel']['weapon']['ammo']
                        magmax = getammo(x[i]['underbarrel']['weapon']['ammo'])
                        for num,nam in enumerate(y):
                            if y[num]['name'] == waffeAusgewaehlt[1]:
                                ammonum = int(y[num]['qty'])
                                ynum = num
                            elif y[num]['name'] == waffeAusgewaehlt[1] and y[num]['extra'] != None and x[i]['underbarrel']['weapon']['ranges']['name'] == y[num]['extra']:
                                ammonum = int(y[num]['qty'])
                                ynum = num
                if ammocnt > magmax:
                    ammocnt = magmax
                if ammocnt > ammonum:
                    ammocnt = ammonum
                funbreak = 0
                clscrn()
                headerprnt()
                print(bcolors.IND + 'Munition: [' + bcolors.GREENh + str(ammocnt) + bcolors.ENDC + '/' + magtyp + '] von insgesamt ' + bcolors.BLUEh + str(ammonum) + bcolors.ENDC + ' verfügbar.', end='')
                if ammocnt <= 1:
                    print(10*' ' + bcolors.BGRh + ' NACHLADEN ' + bcolors.ENDC + '\n')
                else:
                    print('\n')
                print(bcolors.IND + 'Mit ' + waffeAusgewaehlt[0] + ' (' + bcolors.GREENh + waffeAusgewaehlt[1] + bcolors.ENDC + ') schießen:\n')
                for n in chlist:
                    print(bcolors.IND + ' '*2 + bcolors.BLUEh + n.rjust(2) + bcolors.ENDC + ': ', end='')
                    if n == 'r':
                        print('Nachladen'.ljust(25) + 'komplexe Handlung [außer (s)] nach Tabelle [SR5 165]\n')
                    elif n == 'EM':
                        print('Einzelschussmodus'.ljust(25) + bcolors.GREENh + '1'.rjust(2) + bcolors.ENDC + ' Schuss' + 5*' ' + 'Verteidigermod: ' + bcolors.GREENh + '0'.rjust(2) + bcolors.ENDC + 5*' ' + '(kein Rückstoß)\n')
                    elif n == 'HM':
                        print('Halbautomatischermodus'.ljust(25) + bcolors.GREENh + '1'.rjust(2) + bcolors.ENDC + ' Schuss' + 5*' ' + 'Verteidigermod: ' + bcolors.GREENh + '0'.rjust(2) + bcolors.ENDC + 5*' ' + '\n')
                    elif n == 'HS':
                        print('Halbautomatische Salve'.ljust(25) + bcolors.GREENh + '3'.rjust(2) + bcolors.ENDC + ' Schuss' + 5*' ' + 'Verteidigermod: ' + bcolors.GREENh + '-2'.rjust(2) + bcolors.ENDC + 5*' ' + '\n')
                    elif n == 'SM':
                        print('Salvenmodus'.ljust(25) + bcolors.GREENh + '3'.rjust(2) + bcolors.ENDC + ' Schuss' + 5*' ' + 'Verteidigermod: ' + bcolors.GREENh + '-2'.rjust(2) + bcolors.ENDC + 5*' ' + '\n')
                    elif n == 'LS':
                        print('Lange Salve'.ljust(25) + bcolors.GREENh + '6'.rjust(2) + bcolors.ENDC + ' Schuss' + 5*' ' + 'Verteidigermod: ' + bcolors.GREENh + '-5'.rjust(2) + bcolors.ENDC + 5*' ' + '\t(einfache Handlung)\n')
                    elif n == 'AM':
                        print('Automatischer Modus'.ljust(25) + bcolors.GREENh + '10'.rjust(2) + bcolors.ENDC + ' Schuss' + 5*' ' + 'Verteidigermod: ' + bcolors.GREENh + '-9'.rjust(2) + bcolors.ENDC + 5*' ' + '\t(komplexe Handlung)\n')
                    elif n == 'SF':
                        print('Sperrfeuer'.ljust(25) + bcolors.GREENh + '20'.rjust(2) + bcolors.ENDC + ' Schuss' + 5*' ' + 'Verteidigermod: ' + bcolors.GREENh + 'Hinwerfen' + bcolors.ENDC + 5*' ' + '(kein Rückstoß)\n')
                print('\n  ' + bcolors.IND + bcolors.BLUEh + ' q' + bcolors.ENDC + ': Beenden\n')
                print('\n' + bcolors.FAILh + (linewidth//10)*'____ ____ ' + bcolors.ENDC + '\n')
                while funbreak <= 0:
                    ch = input(bcolors.FAILh + ' *>> ' + bcolors.ENDC)
                    if ch == 'q':
                        funbreak = 1
                    elif ch == 'r' or ch == 'R':
                        funbreak = 1
                        if magmax >= ammonum:
                            ammocnt = ammonum
                        else:
                            ammocnt = magmax
                    elif ch.upper() not in chlist:
                        print(bcolors.IND + bcolors.FAILh + '\tGewählter Schussmodus nicht verfügbar, erneut wählen!' + bcolors.ENDC)
                    elif ch == 'EM' or ch == 'em':
                        k = chckammo(ammocnt,1)
                        ammocnt -= k
                        ammonum -= k
                        y[ynum]['qty'] = str(ammonum)
                        funbreak = 1
                    elif ch == 'HM' or ch == 'hm':
                        k = chckammo(ammocnt,1)
                        ammocnt -= k
                        ammonum -= k
                        y[ynum]['qty'] = str(ammonum)
                        funbreak = 1
                    elif ch == 'HS' or ch == 'hs':
                        k = chckammo(ammocnt,3)
                        ammocnt -= k
                        ammonum -= k
                        y[ynum]['qty'] = str(ammonum)
                        funbreak = 1
                    elif ch == 'SM' or ch == 'sm':
                        k = chckammo(ammocnt,3)
                        ammocnt -= k
                        ammonum -= k
                        y[ynum]['qty'] = str(ammonum)
                        funbreak = 1
                    elif ch == 'LS' or ch == 'ls':
                        k = chckammo(ammocnt,6)
                        ammocnt -= k
                        ammonum -= k
                        y[ynum]['qty'] = str(ammonum)
                        funbreak = 1
                    elif ch == 'AM' or ch == 'am':
                        k = chckammo(ammocnt,10)
                        ammocnt -= k
                        ammonum -= k
                        y[ynum]['qty'] = str(ammonum)
                        funbreak = 1
                    elif ch == 'SF' or ch == 'sf':
                        k = chckammo(ammocnt,20)
                        ammocnt -= k
                        ammonum -= k
                        y[ynum]['qty'] = str(ammonum)
                        funbreak = 1
                clscrn()
                headerprnt()
                print('\n\n' + bcolors.IND + 'Munition: [' + bcolors.GREENh + str(ammocnt) + bcolors.ENDC + '/' + magtyp + '] von insgesamt ' + bcolors.BLUEh + str(ammonum) + bcolors.ENDC + ' verfügbar.')
            subsub_ch()

        def exit():
            global fernk
            fernk = False
            kampf()

        def fernkampf_main():
            clscrn() 
            headerprnt()
            print(bcolors.IND + bcolors.UNDERLINE + 'Fernkampf:'.ljust(15) + bcolors.ENDC + '\n')
            print(" '" + bcolors.FAILh + '1' + bcolors.ENDC + "': Kampfregeln")
            print(" '" + bcolors.FAILh + '2' + bcolors.ENDC + "': Feuermodi")
            print(" '" + bcolors.FAILh + '3' + bcolors.ENDC + "': Handlungsübersicht")
            print(" '" + bcolors.FAILh + '4' + bcolors.ENDC + "': Sonderschaden")
            print(" '" + bcolors.FAILh + '5' + bcolors.ENDC + "': Schießen")
            print(" '" + bcolors.FAILh + 'q' + bcolors.ENDC + "': Beenden")
            subsub_ch()
                        
        fernkampfmenu_actions = {
                'main_menu': fernkampf_main,
                '1': kampfregeln,
                '2': feuermodi,
                '3': handlungen,
                '4': schaden,
                '5': schuss,
                'q': exit
                }
        fernkampf_main()
        

    def nahkampf():
        clscrn()
        headerprnt()
        # 
        sub_ch()

    def wurf():
        headerprnt()
        print(bcolors.IND + 'Abweichungsdiagramm [2W6]'.center(49) + ' '*6 + 'Abweichung'.center(50))
        print(bcolors.IND + ' '*7 + '7'.center(35) + 13*' ' + bcolors.UNDERLINE + 'Art des Projektils'.ljust(25) + 'Abweichung'.center(25) + bcolors.ENDC)
        print(bcolors.IND + ' '.ljust(17) + bcolors.WARNINGh + '6 '.center(5) + 5*' ' + ' 8'.center(5) + bcolors.ENDC + ' '*23 + 'Standardgranate'.ljust(25) + '(1W6 - Erfolge) Meter'.center(25))
        print(bcolors.IND + ' '*12 + bcolors.WARNINGh + '  5'.center(5) + '.'.center(15) + '9 '.center(5) + bcolors.ENDC + ' '*18 + 'Aerodynamische Granate'.ljust(25) + '(2W6 - Erfolge) Meter'.center(25))
        print(bcolors.IND + ' '*7 + '4'.rjust(5) + bcolors.BOLD + bcolors.GREENh + 'X'.center(25) + bcolors.ENDC + '10'.ljust(5) + ' '*13 + 'Granatwerfer'.ljust(25) + '(3W6 - Erfolge) Meter'.center(25))
        print(bcolors.IND + ' '*12 + bcolors.WARNINGh + ' 3'.center(10) + ' '*5 + '11'.center(10) + bcolors.ENDC + ' '*18 + 'Lenkraketenwerfer'.ljust(25) + '  (4W6 - Erfolge - Sensorst. d. Rakete) Meter')
        print(bcolors.IND + ' '*22 + '2 12'.center(5) + ' '*28 + 'Raketenwerfer'.ljust(25) + '(5W6 - Erfolge) Meter'.center(25))

        #print(bcolors.IND + 'Abweichungsdiagramm'.center(49) + ' '*6 + 'Abweichung'.center(50))
        #print(bcolors.IND + '7'.center(49) + 6*' ' + bcolors.UNDERLINE + 'Art des Projektils'.ljust(25) + 'Abweichung'.center(25) + bcolors.ENDC)
        #print(bcolors.IND + ' '.ljust(14) + '6'.center(7) + 7*' ' + '8'.center(7) + ' '*20 + 'Standardgranate'.ljust(25) + '(1W6 - Erfolge) Meter'.center(25))
        #print(bcolors.IND + ' '*7 + '5'.center(7) + ' '*21 + '9'.center(7) + ' '*13 + 'Aerodynamische Granate'.ljust(25) + '(2W6 - Erfolge) Meter'.center(25))
        #print(bcolors.IND + '4'.center(7) + ' '*35 + '10'.center(7) + ' '*6 + 'Granatwerfer'.ljust(25) + '(3W6 - Erfolge) Meter'.center(25))
        #print(bcolors.IND + ' ' + '3'.center(20) + ' '*7 + '11'.center(20) + ' '*7 + 'Lenkraketenwerfer'.ljust(25) + '(4W6 - Erfolge - Sensorst. d. Rakete) Meter')
        #print(bcolors.IND + ' '*21 + '2 12'.center(7) + ' '*27 + 'Raketenwerfer'.ljust(25) + '(5W6 - Erfolge) Meter'.center(25))

        print('')
        print(bcolors.IND + 'Werfen von Granaten:')
        print(bcolors.IND + ' einfache Handlung mit Probe: ' + bcolors.GREENh + 'Wurfwaffen + GES' + bcolors.ENDC + ' [körperlich](3).\n')
        print(bcolors.IND + 'Granat- und Raketenwerfer:')
        print(bcolors.IND + ' einfache Handlung mit Probe: ' + bcolors.GREENh + 'Schwere Waffen + GES' + bcolors.ENDC + ' [Präzision](3).')
        print(bcolors.IND + ' Granaten und Raketen werden erst nach ' + bcolors.BLUEh + '5 m' + bcolors.ENDC + ' scharf.')
        print(bcolors.IND + ' Zum entfernen: Ausgedehnte Probe auf ' + bcolors.GREENh + 'Waffenbau + LOG' + bcolors.ENDC + ' [geistig](4, 10 Minuten)')
        sub_ch()

    def handlungen():
        clscrn()
        headerprnt()
        print(bcolors.IND + bcolors.UNDERLINE + 'Freie Handlungen' + bcolors.ENDC)
        print(bcolors.IND + ' Gegenstand fallen lassen'.ljust(50) + 'Satz sprechen/übermitteln'.ljust(50) + 'Gestikulieren')
        print(bcolors.IND + ' Sich hinwerfen'.ljust(50) + 'Laufen'.ljust(50) + 'Smartgunladestreifen auswerfen')
        print(bcolors.IND + ' Mehrfachangriffe'.ljust(50) + 'Ziel ansagen'.ljust(50) + 'Modus eines verlinkten Geräts ändern')
        print('')
        print(bcolors.IND + bcolors.UNDERLINE + 'Einfache Handlungen' + bcolors.ENDC)
        print(bcolors.IND + ' Aufstehen'.ljust(50) + 'Ladestreifen einschieben'.ljust(50) + 'Fokus aktivieren')
        print(bcolors.IND + ' Ladestreifen herausnehmen'.ljust(50) + 'Gegenstand aufheben/ablegen'.ljust(50) + 'Pfeil abschießen')
        print(bcolors.IND + ' Gegenstand benutzen'.ljust(50) + 'Schnellzaubern'.ljust(50) + 'Geist aktivieren')
        print(bcolors.IND + ' Schnellziehen'.ljust(50) + 'Geist befehligen'.ljust(50) + 'Waffe abfeuern (EM,HM,SM,AM)')
        print(bcolors.IND + ' Geist entlassen'.ljust(50) + 'Waffe bereitmachen'.ljust(50) + 'Genau beobachten')
        print(bcolors.IND + ' Wahrnehmung verlagern'.ljust(50) + 'Gerätemodus ändern'.ljust(50) + 'Werfen')
        print(bcolors.IND + ' In Deckung gehen'.ljust(50) + 'Zielen')
        print('')
        print(bcolors.IND + bcolors.UNDERLINE + 'Komplexe Handlungen' + bcolors.ENDC)
        print(bcolors.IND + ' Astrale Projektion'.ljust(50) + 'Montierte oder Fahrzeugwaffe abfeuern'.ljust(50) + 'Fertigkeit einsetzen')
        print(bcolors.IND + ' Nahkampfangriff'.ljust(50) + 'Geist herbeirufen'.ljust(50) + 'Sprinten')
        print(bcolors.IND + ' Geist verbannen'.ljust(50) + 'Waffe im Vollautomatischen Modus (AM) abfeuern'.ljust(50) + 'In ein geriggtes Fahrzeug springen')
        print(bcolors.IND + ' Waffe nachladen'.ljust(50) + 'Lange oder Halbautomatische Salve abfeuern'.ljust(50) + 'Zauber wirken')
        print('')
        print(bcolors.IND + bcolors.UNDERLINE + ('Unterbrechungshandlungen (-Initiative)' + bcolors.ENDC).ljust(42) + ' SR5 169')
        print(bcolors.IND + ' Abfangen (NK): +Nahkampfangriff in RW+1 (-5)'.ljust(50) + 'Parieren (NK): +Nahkampfwaffe [Präzision](-5)'.ljust(50) + 'Ausweichen (NK): +Akrobatik [körperlich](-5)')
        print(bcolors.IND + ' Volle Abwehr: +WIL (Kampfrunde) (-10)'.ljust(50) + 'Blocken (NK):  +Waffenloserkampf [körperlich](-5)'.ljust(50) + 'Volle Deckung: hinwerfen (-5)')
        print(bcolors.IND + ' Lauf um dein Leben/Auf Granate Werfen: fliehen mit restl. Bewegung / mit restl. Bew. auf Granate legen Schaden kompensieren (Gas halbierter Rad) (-5)')
        sub_ch()

    def exit():
        global imkampf
        imkampf = False
        main_menu()

    ### K.MENÜ
    def kampf_main():
        clscrn()
        headerprnt()
        print(bcolors.IND + bcolors.UNDERLINE + 'Kampfmenü:' + bcolors.ENDC + '\n')
        print(bcolors.IND + " '" + bcolors.FAILh + '1' + bcolors.ENDC + "': Initiative")
        print(bcolors.IND + " '" + bcolors.FAILh + '2' + bcolors.ENDC + "': Astralkampf")
        print(bcolors.IND + " '" + bcolors.FAILh + '3' + bcolors.ENDC + "': Fernkampf")
        print(bcolors.IND + " '" + bcolors.FAILh + '4' + bcolors.ENDC + "': Nahkampf")
        print(bcolors.IND + " '" + bcolors.FAILh + '5' + bcolors.ENDC + "': Wurfwaffen")
        print(bcolors.IND + " '" + bcolors.FAILh + '6' + bcolors.ENDC + "': Handlungsübersicht")
        print(bcolors.IND + " '" + bcolors.FAILh + '7' + bcolors.ENDC + "': Sonderschaden")
        print(bcolors.IND + " '" + bcolors.FAILh + 'q' + bcolors.ENDC + "': Beenden")
        sub_ch()
        
    kampfmenu_actions = {
        'main_menu': kampf_main,
        '1': initiative,
        '2': astralkampf,
        '3': fernkampf,
        '4': nahkampf,
        '5': wurf,
        '6': handlungen,
        '7': schaden,
        'q': exit,
        'dmg': dmg,
        'edg': looseedg,
        'eq': equip,
        'ga': getastral,
        'za': zauberaufrecht,
        'z': spells,
        'w': weapons,
        'geist': geist
        }

    kampf_main()
    return

### GEIST
def geist():
    headerprnt()
    with codecs.open('text-geister.json','r', 'utf-8-sig') as textgeist:
        txtgeist = textgeist.read()
    tg = json.loads(txtgeist)
    for i,n in enumerate(tg['texts']):
        print(bcolors.IND, end='')
        print((bcolors.UNDERLINE + '{name}'.format(**tg['texts'][i]) + bcolors.ENDC).ljust(25), end='')
        print('\t' + bcolors.IND + '[ KON:' + bcolors.GREENh + '{KON}'.format(**tg['texts'][i]) + bcolors.ENDC + '  GES:' + bcolors.GREENh + '{GES}'.format(**tg['texts'][i]) + bcolors.ENDC + '  REA:' + bcolors.GREENh + '{REA}'.format(**tg['texts'][i]) + bcolors.ENDC + '  STR:' + bcolors.GREENh + '{STR}'.format(**tg['texts'][i]) + bcolors.ENDC + '  WIL:' + bcolors.GREENh + '{WIL}'.format(**tg['texts'][i]) + bcolors.ENDC + '  LOG:' + bcolors.GREENh + '{LOG}'.format(**tg['texts'][i]) + bcolors.ENDC + '  INT:' + bcolors.GREENh + '{INT}'.format(**tg['texts'][i]) + bcolors.ENDC + '  CHA:' + bcolors.GREENh + '{CHA}'.format(**tg['texts'][i]) + bcolors.ENDC + '  EDG:' + bcolors.GREENh + '{EDG}'.format(**tg['texts'][i]) + bcolors.ENDC + '  ESS:' + bcolors.GREENh + '{ESS}'.format(**tg['texts'][i]) + bcolors.ENDC + '  MAG:' + bcolors.GREENh + '{MAG}'.format(**tg['texts'][i]) + bcolors.ENDC + ' ]') 
        print('\t\t' + bcolors.IND,bcolors.GREENh + 'Initiative:' + bcolors.ENDC + ' {INIT}\t\t'.format(**tg['texts'][i]) + bcolors.GREENh + 'Astrale Initiative:' + bcolors.ENDC + ' {ASTRALINIT}'.format(**tg['texts'][i]))
        print('\t\t' + bcolors.IND,bcolors.GREENh + 'Fertigkeiten:' + bcolors.ENDC + ' {skills}'.format(**tg['texts'][i]))
        print('\t\t' + bcolors.IND,bcolors.GREENh + 'Kräfte:' + bcolors.ENDC + ' {abilities}'.format(**tg['texts'][i]))
        print('\t\t' + bcolors.IND,bcolors.GREENh + 'Zusätzliche Kräfte:' + bcolors.ENDC + ' {addabilities}'.format(**tg['texts'][i]))
        print('\t\t' + bcolors.IND,bcolors.GREENh + 'Schwächen:' + bcolors.ENDC + ' {disabilities}'.format(**tg['texts'][i]))
        print('\t\t' + bcolors.IND,bcolors.GREENh + 'Besonderheit:' + bcolors.ENDC + ' {special}'.format(**tg['texts'][i]))
        print('')
    sch()    
    return

### BARRIEREN
def bar():
    def barrierest():
        clscrn()
        headerprnt()
        txtwdth = 70
        print(bcolors.IND + bcolors.UNDERLINE + 'Barriere'.ljust(txtwdth) + 'Struktur         Panzerung   ' + bcolors.ENDC)
        print('\n' + bcolors.IND + 'Zerbrechlich'.ljust(txtwdth) + ' 1 '.center(8) + ' \t' + ' 2 '.center(9))
        print(bcolors.IND + ' ' + bcolors.KURSIV + bcolors.BLUEh + 'gewöhnliches Glas' + bcolors.ENDC + '\n')
        print(bcolors.IND + 'Billiges Material'.ljust(txtwdth) + ' 2 '.center(8) + ' \t' + ' 4 '.center(9))
        print(bcolors.IND + ' ' + bcolors.KURSIV + bcolors.BLUEh + 'Gipswand, Gipskarton, Tür, normaler Reifen' + bcolors.ENDC + '\n')
        print(bcolors.IND + 'Durchschnittliches Material'.ljust(txtwdth) + ' 4 '.center(8) + ' \t' + ' 6 '.center(9))
        print(bcolors.IND + ' ' + bcolors.KURSIV + bcolors.BLUEh + 'Möbel, Sicherheitsglas, Plastik' + bcolors.ENDC + '\n')
        print(bcolors.IND + 'Schweres Material'.ljust(txtwdth) + ' 6 '.center(8) + ' \t' + ' 8 '.center(9))
        print(bcolors.IND + ' ' + bcolors.KURSIV + bcolors.BLUEh + 'Bäume, Hartholz, Datenterminal, Kettenglieder, Laternenpfahl' + bcolors.ENDC + '\n')
        print(bcolors.IND + 'Verstärktes Material'.ljust(txtwdth) + ' 8 '.center(8) + ' \t' + '12 '.center(9))
        print(bcolors.IND + ' ' + bcolors.KURSIV + bcolors.BLUEh + 'Densiplast, Sicherheitstür, Panzerglas, Kevlarplatten' + bcolors.ENDC + '\n')
        print(bcolors.IND + 'Tragendes Material'.ljust(txtwdth) + '10 '.center(8) + ' \t' + '16 '.center(9))
        print(bcolors.IND + ' ' + bcolors.KURSIV + bcolors.BLUEh + 'Ziegel, Plasbeton' + bcolors.ENDC + '\n')
        print(bcolors.IND + 'Schweres tragendes Material'.ljust(txtwdth) + '12 '.center(8) + ' \t' + '20 '.center(9))
        print(bcolors.IND + ' ' + bcolors.KURSIV + bcolors.BLUEh + 'Beton, Metallträger' + bcolors.ENDC + '\n')
        print(bcolors.IND + 'Gepanzertes schweres Material'.ljust(txtwdth) + '14 '.center(8) + ' \t' + '24 '.center(9))
        print(bcolors.IND + ' ' + bcolors.KURSIV + bcolors.BLUEh + 'Stahlbeton' + bcolors.ENDC + '\n')
        print(bcolors.IND + 'Gehärtetes Material'.ljust(txtwdth) + '16+'.center(8) + ' \t' + '32+'.center(9))
        print(bcolors.IND + ' ' + bcolors.KURSIV + bcolors.BLUEh + 'Bunker' + bcolors.ENDC + '\n')
        print('')
        liner()
        print('', end='')
        s = input(' >>> ')
        bar()
    clscrn()
    headerprnt()
    print(bcolors.IND + bcolors.UNDERLINE + 'Barrieren:' + bcolors.ENDC + '\n')
    print(bcolors.IND + 'Statt KON + Panzerung haben Barrieren: ' + bcolors.GREENh + 'Struktur + Panzerung' + bcolors.ENDC)
    print(bcolors.IND + 'Barrieren haben Schadensmonitor abh. Größe und Strukturstufe:' )
    print(bcolors.IND + bcolors.GREENh + '\tPro Quadratmeter' + bcolors.ENDC + ' (mit 10 cm Dicke) besitzen Barrieren ' + bcolors.GREENh + 'Kästchen gleich Strukturstufe' + bcolors.ENDC)
    print(bcolors.IND + 'Wenn Barriere sichtbehindernt, dann WP-Malus von ' + bcolors.GREENh + '-6' + bcolors.ENDC + ' für Angreifer, Verteidiger darf ' + bcolors.GREENh + 'nicht ausweichen' + bcolors.ENDC)
    print(bcolors.IND + 'Grundsätzlich muss jeder Angriff die Barriere durchschlagen.')
    print(bcolors.IND + 'SL würfelt ' + bcolors.GREENh + 'Struktur + Panzerung' + bcolors.ENDC + ' wenn Überschüssiger Schaden entsteht, dann wird dieser auf das Ziel dahinter weitergegeben.')
    print(bcolors.IND + ' Falls mod. Schadenscode geringer als durch DK mod. Panzerungswert der Barriere, ist der Angriff nicht stark genug.')
    print(bcolors.IND + 'Nicht widerstandene Schaden wird auf Zustandsmonitor der Barriere verzeichnet.')
    print(bcolors.IND + 'Wenn Barriere min so viel Schaden erleidet, wie ihre Strukturstufe, dann hat der Angriff ein Loch in sie geschlagen. ')
    print(bcolors.IND + bcolors.GREENh + '\tFläche des Loches in Quadratmeter ist gleich dem Faktor an Schaden in Höhe der Strukturstufe.' + bcolors.ENDC)
    print('\n' + bcolors.IND + bcolors.UNDERLINE + 'Penetrierende Waffen:' + bcolors.ENDC + '\n')
    print(bcolors.IND + 'Wenn penetrierende Waffe (Kugel, spitzes Schwert), dann 1 Schaden auf Barriere, Rest geht auf Ziel dahinter, wenn mod. Panzerung überschritten wird.')
    print(bcolors.IND + bcolors.GREENh + '2 Kästchen Schaden bei 3 Kugeln, 3 Kästchen bei 6 Kugeln, und 4 Kästchen bei 10 Kugeln.' + bcolors.ENDC)
    print(bcolors.IND + 'Erlittener Schaden minus erlittener Schaden der Barriere')
    print('\n' + bcolors.IND + bcolors.UNDERLINE + bcolors.BLUEh + 'Hausregeln:' + bcolors.ENDC + '\n')
    print(bcolors.IND + '  Struktur + Panzerung jeweils mit ' + bcolors.GREENh + 'Kraftstufe + (Erfolge [KS])' + bcolors.ENDC + '.')
    print(bcolors.IND + '  Wenn mod. Schaden nicht über mod. Panzerung der Barriere, dann wird Kugel gestoppt.')
    print(bcolors.IND + '  Wenn mod. Schaden höher als mod. Panzerung: Kompensieren der Barriere mit ' + bcolors.GREENh + 'Struktur + Panzerung' + bcolors.ENDC)
    print(bcolors.IND + '  Falls Schaden bleibt, dann ' + bcolors.GREENh + '1 Kästchen Schaden' + bcolors.ENDC + ' an Struktur der Barriere, der Rest geht an das Ziel dahinter.')
    print('')
    liner()
    print(bcolors.IND + "'" + bcolors.BLUEh + 's' + bcolors.ENDC + "' Barrierestufen")
    liner()
    print('', end='')
    choice = input(bcolors.GREENh + ' >> ' + bcolors.ENDC)
    if choice == 's':
        barrierest()
    else:
        exec_menu(choice)
    return

### BIO
def bio():
    headerprnt()
    print(bcolors.IND + bcolors.UNDERLINE + character['name'] + ' (\033[4;33m' + character['alias'] + '\033[4;39m)' + bcolors.ENDC)
    print(bcolors.IND + character['metatype'] + ', ' + character['sex'] + ', ' + character['age'])
    print(bcolors.IND + 'Hautfarbe: ' + character['skin'] + ', Haare: ' + character['hair'] + ', Augen: ' + character['eyes'])
    print(bcolors.IND + character['height'] + ' cm, ' + character['weight'] + ' kg')
    print(bcolors.IND + bcolors.GREENh + character['nuyen'] + bcolors.ENDC + ' Nuyen, ' + bcolors.GREENh + character['karma'] + bcolors.ENDC + ' Karma')
    print(bcolors.IND + 'Essenz: ' + character['totaless'])
    print('\n' + bcolors.IND + 'Bewegung: ' + character['movement']) 
    print('\n' + bcolors.IND + 'Heben: (15 kg x STR) ' + bcolors.GREENh + str(15*int(paras['staerke'])) + bcolors.ENDC + ' kg\tüber den Kopf heben: (5 kg x STR) ' + bcolors.GREENh + str(5*int(paras['staerke'])) + bcolors.ENDC + ' kg\tTragen: (10 kg x STR) ' + bcolors.GREENh + str(10*int(paras['staerke'])) + bcolors.ENDC + ' kg') 
    print(bcolors.IND + ' Für Weiteres Heben und Tragen: Probe auf ' + bcolors.GREENh + 'STR + KON' + bcolors.ENDC)
    print('\n' + bcolors.IND + 'Selbstbeherrschung: (' + bcolors.GREENh + 'WIL + CHA' + bcolors.ENDC + ') ' + bcolors.GREENh + '{composure}'.format(**character) + bcolors.ENDC + '\tErinnerung: (' + bcolors.GREENh + 'LOG + WIL' + bcolors.ENDC + ') ' + bcolors.GREENh + '{memory}'.format(**character) + bcolors.ENDC + '\tMenschenkenntnis: (' + bcolors.GREENh + 'INT + CHA' + bcolors.ENDC + ') ' + bcolors.GREENh + '{judgeintentions}'.format(**character) + bcolors.ENDC) 
    print('\n')
    if character['magician'] == 'True':
        print(bcolors.IND + 'Magie-Tradition:')
        print(bcolors.IND + '\t{fullname} [{drainattributes}]({drainvalue})\t\t{source} {page}'.format(**character['tradition']))
        print(bcolors.IND + '\tInitiantengrad: ' + bcolors.BOLD + '{initiategrade}'.format(**character) + bcolors.ENDC)
        print(bcolors.IND + '\tMetamagie: ', end='')
        print(bcolors.ASTRALh + '\t{fullname!s}\t{source} {page}'.format(**character['arts']['art']) + bcolors.ENDC)
        print(bcolors.IND + '\tGeister: [ {0:>12}:{spiritcombat:15}\t{1:>12}:{spiritdetection:15}\t{2:>12}:{spirithealth:15}\n\t\t   {3:>12}:{spiritillusion:15}\t{4:>12}:{spiritmanipulation:15}\t{5:>12}:{spiritform:15} ]'.format('Kampf', 'Sucher', 'Heilung', 'Illusion', 'Manipulation', 'Geisterform', **character['tradition']))
        print('\n')
    if paras['mali'] == '':
        mal = '0'
    else:
        mal = paras['mali']
    print(bcolors.IND, bcolors.FAILh + 'Mali:\t\tgesamt: {0}'.format(mal) + ', koerperlich: {koerperlich}, geistig: {geistig}, aufrechterhaltene Zauber: {zauber}'.format(**mali) + bcolors.ENDC)
    print('\n')
    print(bcolors.IND + 'Limitmodifikationen:')
    limmods = ['limitmodifiersphys', 'limitmodifiersment', 'limitmodifierssoc']
    for nam in limmods:
        if type(character[nam]) is not type(None):
            if nam == limmods[0]:
                print(bcolors.IND + bcolors.GREENh + 'K' + bcolors.ENDC + ':' + bcolors.IND*(-1), end='')            
            elif nam == limmods[1]:
                print(bcolors.IND + bcolors.GREENh + 'G' + bcolors.ENDC + ':' + bcolors.IND*(-1), end='')
            elif nam == limmods[2]:
                print(bcolors.IND + bcolors.GREENh + 'S' + bcolors.ENDC + ':' + bcolors.IND*(-1), end='')
            if type(character[nam]['limitmodifier']) is list: 
                for i,num in enumerate(character[nam]['limitmodifier']):
                    print(bcolors.IND + '\t{name!s}'.format(**character[nam]['limitmodifier'][i]))
            elif type(character[nam]['limitmodifier']) is dict:
                    print(bcolors.IND + '\t{name!s}'.format(**character[nam]['limitmodifier'])) 
   #### FARB 
    #clscrn() 
    #print('\n\n\n')
    #for n in range(130):
        #print(str(n) + ': \033[' + str(n) + 'm██abc ' + bcolors.ENDC, end='')
        #if n%10 == 0:
            #print('')
    sch()
    return

### ATTS
def atts():
    headerprnt()
    x = character['attributes'][1]['attribute']
    print(bcolors.IND, end='')
    for num,n in enumerate(x):
        if x[num]['name'] != 'RES' and x[num]['name'] != 'MCH':
            print('{name} {total} ({max})\t'.format(**x[num]), end='') 
    print('') 
    sch()
    return

### FAHRZEUGE
def fahrzeuge():
    clscrn()
    headerprnt()
    if character['vehicles'] != None:
        x = character['vehicles']['vehicle']
        for i,n in enumerate(x):
            print(bcolors.IND + ( bcolors.GREENh + '{fullname:30}'.format(**x[i]) + bcolors.ENDC + '\t({category})'.format(**x[i])).ljust(100) + ' '*17 +'{source:>3} {page:>3}'.format(**x[i]))
            print(bcolors.IND + '\tGeschwindigkeit: {speed}\tBeschleunigung: {accel}\tArmor: {armor}\tBody: {body}\tKosten: {cost} Nuyen'.format(**x[i]))
            print(bcolors.IND + '\tDataprocessing: {dataprocessing}\tFirewall: {firewall}\tRating: {devicerating}'.format(**x[i]))
            if x[i]['mods'] != None:
                if type(x[i]['mods']['mod']) == dict: 
                    print(bcolors.IND + bcolors.BLUEh + '\t+ {fullname:100}{source} {page}'.format(**x[i]['mods']['mod']) + bcolors.ENDC)
                elif type(x[i]['mods']['mod']) == list: 
                    for num,nam in enumerate(x[i]['mods']['mod']):
                        print(bcolors.IND + bcolors.BLUEh + '\t+ {fullname:100}{source} {page}'.format(**x[i]['mods']['mod'][num]) + bcolors.ENDC)
            print('')
    else:
        print('\n\n\t\t\tCharakter besitzt keine Fahzeuge.\n\n')
    sch()

### CYBERWARE
def cyberw():
    clscrn()
    headerprnt()
    if character['cyberwares'] != None:
        x = character['cyberwares']['cyberware']
        if type(x) == dict:
            if x['rating'] == '0':
                print(bcolors.IND + ( bcolors.GREENh + '{name:80}'.format(**x) + bcolors.ENDC + ' '*20 + 'Kosten: {cost} Nuyen'.format(**x)).ljust(140) + '{source:>3} {page:>3}'.format(**x))
            else:
                print(bcolors.IND + ( bcolors.GREENh + '{name:80}'.format(**x) + bcolors.ENDC + 'St. {rating}'.format(**x) + ' '*15 + 'Kosten: {cost} Nuyen'.format(**x)).ljust(140) + '{source:>3} {page:>3}'.format(**x))
            print(bcolors.IND + 'Qualität: {grade}\tBereich: {location}\tEssenzkosten: {ess}\t[f:{firewall} dp:{dataprocessing} dr:{devicerating}]'.format(**x))
            if x['children'] != None:
                if type(x['children']['cyberware']) == dict: 
                    print(bcolors.IND + bcolors.BLUEh + ( '\t+ {name:100} Rating: {rating}'.format(**x['children']['cyberware'])).ljust(140) + '{source:>3} {page:>3}'.format(**x['children']['cyberware']) + bcolors.ENDC)
                elif type(x['children']['cyberware']) == list: 
                    for num,nam in enumerate(x['children']['cyberware']):
                        print(bcolors.IND + bcolors.BLUEh + ( '\t+ {name:100} Rating: {rating}'.format(**x['children']['cyberware'][num])).ljust(140) + '{source:>3} {page:>3}'.format(**x['children']['cyberware'][num]) + bcolors.ENDC)
            print('')
        elif type(x) == list:
            for i,n in enumerate(x):
                if x[i]['rating'] == '0':
                    print(bcolors.IND + ( bcolors.GREENh + '{name:80}'.format(**x[i]) + bcolors.ENDC + ' '*20  + 'Kosten: {cost} Nuyen'.format(**x[i])).ljust(140) + '{source:>3} {page:>3}'.format(**x[i]))
                else:
                    print(bcolors.IND + ( bcolors.GREENh + '{name:80}'.format(**x[i]) + bcolors.ENDC + 'St. {rating}'.format(**x[i]) + ' '*15 + 'Kosten: {cost} Nuyen'.format(**x[i])).ljust(140) + '{source:>3} {page:>3}'.format(**x[i]))
                print(bcolors.IND + 'Qualität: {grade}\tBereich: {location}\tEssenz: {ess}\t[f:{firewall} dp:{dataprocessing} dr:{devicerating}]'.format(**x[i]))
                if x[i]['children'] != None:
                    if type(x[i]['children']['cyberware']) == dict: 
                        print(bcolors.IND + bcolors.BLUEh + ( '\t+ {name:100} Rating: {rating}'.format(**x[i]['children']['cyberware'])).ljust(140) + '{source:>3} {page:>3}'.format(**x[i]['children']['cyberware']) + bcolors.ENDC)
                    elif type(x[i]['children']['cyberware']) == list: 
                        for num,nam in enumerate(x[i]['children']['cyberware']):
                            print(bcolors.IND + bcolors.BLUEh + ( '\t+ {name:100} Rating: {rating}'.format(**x[i]['children']['cyberware'][num])).ljust(140) + '{source:>3} {page:>3}'.format(**x[i]['children']['cyberware'][num]) + bcolors.ENDC)
                print('')
    else:
        print('\n\n\t\t\tCharakter besitzt keine Cyberware.\n\n')
    sch()

### QUALITIES
def qualities():
    headerprnt()
    x = character['qualities']['quality']
    print(bcolors.IND + bcolors.UNDERLINE + 'Vorteile:' + bcolors.ENDC)
    for num,n in enumerate(x):
        if x[num]['qualitytype'] == 'Vorteile':
            if x[num]['extra'] != None:
                print(bcolors.IND + ' {name:40} ('.format(**x[num]) + '{extra})'.format(**x[num]).ljust(41) + ' Karmakosten: {bp:>3}'.format(**x[num]).ljust(20) + '\t{source:3} {page:>3}'.format(**x[num]))
            else:
                print(bcolors.IND + ' {name:83} Karmakosten: {bp:>3}'.format(**x[num]).ljust(20) + '\t\t{source:3} {page:>3}'.format(**x[num]))
    print('\n' + bcolors.IND + bcolors.UNDERLINE + 'Nachteile:' + bcolors.ENDC)
    for num,n in enumerate(x):
        if x[num]['qualitytype'] == 'Nachteile':
            if x[num]['extra'] != None:
                print(bcolors.IND + ' {name:40} ('.format(**x[num]) + '{extra})'.format(**x[num]).ljust(41) + ' Karma: {bp:>3}'.format(**x[num]).ljust(20) + '\t{source:3} {page:>3}'.format(**x[num]))
            else:
                print(bcolors.IND + ' {name:83} Karma: {bp:>3}'.format(**x[num]).ljust(20) + '\t\t{source:3} {page:>3}'.format(**x[num]))
    sch()

### SKILLS
def skills():
    headerprnt()
    x = character['skills']['skill']
    def prntsll(num, numstart, flg=0):
        bflg = 1
        if flg == 1:
            print(bcolors.BLUEh, end='')
            bflg = 1
        elif flg == 2:
            print(bcolors.ASTRALh, end='')
        elif flg == 3:
            bflg = 1
            print(bcolors.FAILh, end='')
        elif flg == 4:
            print(bcolors.WARNING, end='')
        elif flg == 5:
            print(bcolors.PNZRG, end='')
            bflg = 1
        if numstart == 0:
            if bflg == 0:
                print('{name:>34}'.format(**x[num]) + bcolors.ENDC + ' {rating:>2} ({displayattribute}): '.format(**x[num]) + bcolors.BOLD + '{total:>2}'.format(**x[num]) + bcolors.ENDC, end='')
            else:
                print('{name:>34} {rating:>2} ({displayattribute}): '.format(**x[num]) + bcolors.BOLD + '{total:>2}'.format(**x[num]) + bcolors.ENDC, end='')
        else:
            if type(x[num]['skillspecializations']['skillspecialization']) is dict:
                print(bcolors.GREENh + '  + {name}'.format(**x[num]['skillspecializations']['skillspecialization']).rjust(44) + bcolors.BOLD + ' {specializedrating:>2}'.format(**x[num]) + bcolors.ENDC, end='')
            else:
                print(bcolors.GREENh + '  ↳ {name}'.format(**x[num]['skillspecializations']['skillspecialization'][numstart-1]).rjust(44) + bcolors.BOLD + ' {specializedrating:>2}'.format(**x[num]) + bcolors.ENDC, end='')
    def prntsllchk(num, numstart):
        if x[num]['knowledge'] == 'True':
            prntsll(num, numstart,flg=1)
        elif x[num]['displayattribute'] == 'MAG':
            prntsll(num, numstart,flg=2)
        elif x[num]['skillcategory'] == 'Kampf-Aktionsfertigkeiten' or x[num]['name'] == 'Sprengstoffe':
            prntsll(num, numstart,flg=3)
        elif x[num]['skillcategory'] == 'Körperliche Aktionsfertigkeiten':
            prntsll(num, numstart,flg=4)
        elif x[num]['skillgroup'] == 'Biotech':
            prntsll(num, numstart,flg=5)
        else:
            prntsll(num, numstart)           
    n_lst = 0
    s_lst = []
    for i in range(len(x)):
        n_lst += 1
        if x[i]['skillspecializations'] == None:
            s_lst.append([i,0])
        elif x[i]['skillspecializations'] != None:
            s_lst.append([i,0])
            n_lst += len(x[i]['skillspecializations']['skillspecialization'])
            for k in range(len(x[i]['skillspecializations']['skillspecialization'])):
                s_lst.append([i, k+1])
    r_n_lst = n_lst%3
    for i in range(n_lst//3):
        if r_n_lst == 1:
            k = i+1+n_lst//3
            n = i+1+n_lst//3*2
        elif r_n_lst == 2:
            k = i+1+n_lst//3
            n = i+2+n_lst//3*2
        else:
            k = i+n_lst//3
            n = i+n_lst//3*2
        print(bcolors.IND, end='')
        prntsllchk(s_lst[i][0], s_lst[i][1])
        print('\t', end='')
        prntsllchk(s_lst[k][0], s_lst[k][1])
        print('\t', end='')
        prntsllchk(s_lst[n][0], s_lst[n][1])
        print('\n', end='')
    if r_n_lst == 1:
        i = n_lst//3 #+1
        print(bcolors.IND, end='')
        prntsllchk(s_lst[i][0], s_lst[i][1])
        print('\n', end='')
    elif r_n_lst == 2:
        i = n_lst//3
        k = n_lst//3*2+1 #+2
        print(bcolors.IND, end='')
        prntsllchk(s_lst[i][0], s_lst[i][1])
        print('\t', end='')
        prntsllchk(s_lst[k][0], s_lst[k][1])
        print('\n', end='')
    sch()
    return

### SPELLS:
def spells():
    if character['magician'] == 'True':
        headerprnt()
        astralconv()
        x = character['spells']['spell']
        n_kmpf = []
        n_mnpl = []
        n_illu = []
        n_heil = []
        for i,n in enumerate(x):
            if x[i]['category'] == 'Kampfzauber':
                n_kmpf.append(i)
            elif x[i]['category'] == 'Manipulationszauber':
                n_mnpl.append(i)
            elif x[i]['category'] == 'Illusionszauber':
                n_illu.append(i)
            elif x[i]['category'] == 'Heilzauber':
                n_heil.append(i)
        def prntspll(num):
            if x[num]['alchemy'] == 'True':
                print(bcolors.WARNINGh, end='')
                namez = x[num]['name']
                nameza = namez.replace(' (Alchemistisch)','')
                namezau = nameza.replace('Attribut',x[num]['extra'])
                print(bcolors.IND + "A {0:20}".format(namezau) + "  {type} ({duration})\t{range:5}\tSchaden: {damage}\tWürfel: {dicepool:2}\tEntzug: {dv:4}\t".format(**x[num]) + "({descriptors!s})".format(**x[num]).ljust(40) + "\t{source:3} {page}".format(**x[num]), end='')
                print(bcolors.ENDC)
            else:
                print(bcolors.IND + "  {name:20}  {type} ({duration})\t{range:5}\tSchaden: {damage}\tWürfel: {dicepool:2}\tEntzug: {dv:4}\t".format(**x[num]) + "({descriptors!s})".format(**x[num]).ljust(40) + "\t{source:3} {page}".format(**x[num]))
        print(bcolors.IND + bcolors.BOLD, bcolors.UNDERLINE + 'Kampfzauber:' + bcolors.ENDC, end='')
        print(bcolors.FAILh + '\t\t' + bcolors.IND + 'Direkt: vs. [KON(P)/WIL(M) + Antimagie]')
        print('\t\t\t' + bcolors.IND + 'Indirekt: vs. [REA+INT + Antimagie], Schaden: [Nettoerfolge + KS, DK:-KS], Widst: KON+mod.PNZRG' + bcolors.ENDC + '\n')
        for i,n in enumerate(n_kmpf):
            prntspll(int(n))
        print('\n' +bcolors.IND + bcolors.BOLD, bcolors.UNDERLINE + 'Manipulationszauber:' + bcolors.ENDC, end='')
        print(bcolors.FAILh + '\t' + bcolors.IND + 'Schaden: KS DK:0 WDST: KON+PNZRG,  Transformation: KON+STR / Objwdst' + bcolors.ENDC)
        print(bcolors.FAILh + '\t\t\t' + bcolors.IND + 'Beherrschung: WIL+LOG (kompl. HNDL pro HNDLPHSE, WP-M: Kraft des Zaubers, [Nettoerf(Zauber)-1 pro WDST-Erfolg])'.ljust(140) + bcolors.ENDC + '\n')
        for i,n in enumerate(n_mnpl):
            prntspll(int(n))
        print('\n' +bcolors.IND + bcolors.BOLD, bcolors.UNDERLINE + 'Illusionszauber:' + bcolors.ENDC, end='')
        print(bcolors.FAILh + '\t' + bcolors.IND + 'Widerstand:   M: WIL + LOG    P: LOG + INT   (unbel. Obj: Objwiderstand (SR5 290))' + bcolors.ENDC + '\n')
        for i,n in enumerate(n_illu):
            prntspll(int(n))
        print('\n' + bcolors.IND + bcolors.BOLD, bcolors.UNDERLINE + 'Heilzauber:' + bcolors.ENDC, end='')
        print(bcolors.FAILh + '\t\t' + bcolors.IND + 'Kein geistiger Schaden heilbar!\tBei Essenzverlust: WP-Malus: (ESS-6)' + bcolors.ENDC + '\n')
        for i,n in enumerate(n_heil):
            prntspll(int(n))
    else:
        headerprnt()
        print('\n\n\t' + bcolors.IND + 'Charakter ist nicht erwacht!\n\n\n\n')
    if imkampf == True:
        print('' + bcolors.FAILh)
        liner()
        print('', end='')
        choice = input(' *>> ' + bcolors.ENDC)
        kampf()
    else:
        sch()
    return

### DROGEN 
def drogen():
    def abhaengigkeitsprob():
        clscrn()
        headerprnt()
        print(bcolors.IND + bcolors.UNDERLINE + 'Abhängigkeitsproben:' + bcolors.ENDC)
        print(bcolors.IND + ' Jedes Mal, wenn ein Konsument eine suchterzeugende Substanz (' + bcolors.BLUEh + '11 - Abhängigkeitswert' + bcolors.ENDC + ') aufeinanderfolgende Wochen lang benutzt, muss er eine Probe ablegen.')
        print(bcolors.IND + ' Psychische Abhängigkeit:' + bcolors.GREENh + '\tWIL + LOG' + bcolors.ENDC)
        print(bcolors.IND + ' Physische Abhängigkeit:' + bcolors.GREENh + '\tKON + WIL' + bcolors.ENDC)
        print(bcolors.IND + ' Abhängigkeits-Schwellwert ist in der Tabelle angegeben.')
        print(bcolors.IND + ' Misslingt die Probe, bekommt er den Nachteil ' + bcolors.FAILh + 'Abhängigkeit' + bcolors.ENDC + ' SR5 S.88\t(Hat er bereits den Nachteil, so steigt die Schwere seiner Stufe.)\n')
        print(bcolors.IND + bcolors.FAILh + ' Ausgebrannte Charaktere' + bcolors.ENDC + ' die scheitern verlieren 1 Attributspunkt KON oder WIL (je nach dem was höher ist) und auch den Maximalwert für das Attribut.')
        print(bcolors.IND + ' Bei gleich hohen Werten sinkt KON bei physischen und WIL bei psychischen Abhängigkeiten. Ist Abh. beides, dann random.')
        print(bcolors.IND + ' Wenn ein Attribut auf 0, dann Koma + 1 überschüssiger Schaden.\n')
        
        print(bcolors.IND + bcolors.UNDERLINE + 'Im RPG:' + bcolors.ENDC)
        print(bcolors.IND + bcolors.BLUEh + ' leicht:' + bcolors.ENDC + '\t1 Dosis 1 x Monat\tGelegenheitskonsument, "hin und wieder" Bedürfnis. "Jederzeit damit aufhören"')
        print(bcolors.IND + bcolors.BLUEh + ' mittel:' + bcolors.ENDC + '\t1 Dosis 2 x Monat\tGewisse Toleranz: häufiger, erhöhte Dosis oder härteres. Andere sehen die Abhängigkeit. ')
        print(bcolors.IND + ' \t\t\t\t\tErste Konsequenzen der Sucht: Gefühlsschwankungen, unzuverlässig, erste finanzielle Probleme')       
        print(bcolors.IND + bcolors.BLUEh + ' schwer:' + bcolors.ENDC + '\t2 Dosen 1 x Woche\tStereotypischer Junkie, außer Kontrolle, hat nur den nächsten Schuss im Kopf, jeder Nuyen geht in die Sucht. ')
        print(bcolors.IND + ' \t\t\t\t\tStiehlt, leiht sich Geld oder geht auf den Strich, um an Geld zu kommen.')  
        print(bcolors.IND + bcolors.BLUEh + ' ausgebrannt:' + bcolors.ENDC + '\t3 Dosen 1 x Tag\t\tGanz unten angelangt. Geringe Lebenserwartung. Schwer artikulieren, Abszesse, Infektionen, ')
        print(bcolors.IND + ' \t\t\t\t\tInkontinenz, Gedächtnislücken, Flashbacks, drastische Stimmungsschwankungen, Schizophrenie, Paranoia...\n') 

        print(bcolors.IND + bcolors.UNDERLINE + 'Einen Schuss bekommen:' + bcolors.ENDC)
        print(bcolors.IND + ' Sobald abhängig, benötigt Charakter regelmäßig eine Dosis.')
        print(bcolors.IND + ' Will Char dem Suchtdruck widerstehen, kann er eine Entzugsprobe ablegen. (' + bcolors.BLUEh + 'Abhängigkeitsprobe' + bcolors.ENDC + ').')
        print(bcolors.IND + ' Je nach Schwere der Abhängigkeit, entschprechende Modifikatoren.')
        print(bcolors.IND + ' Legt er die Probe nicht ab oder scheitert, braucht er einen Schuss oder muss sich einem Entzug unterziehen.\n')

        print(bcolors.IND + bcolors.UNDERLINE + 'Entzugserscheinungen:' + bcolors.ENDC)
        print(bcolors.IND + ' psychisch: Paranoia, Angst, Schlaflosigkeit, Unruhe, Konzentrationsstörungen, Stimmungsschwankungen und Depressionen')       
        print(bcolors.IND + ' physisch:  Schmerz, Übelkeit, Zittern')
        print(bcolors.IND + bcolors.FAILh + ' Mali:' + bcolors.ENDC, end='')
        print(bcolors.IND + '\t' + bcolors.BLUEh + 'leicht' + bcolors.ENDC + ': -2\t' + bcolors.BLUEh + 'mittel' + bcolors.ENDC + ': -4\t' + bcolors.BLUEh + 'schwer' + bcolors.ENDC + ': -4 [permanent: soziale Proben:' + bcolors.FAILh + '-2' + bcolors.ENDC + ']\t' + bcolors.BLUEh + 'ausgebrannt' + bcolors.ENDC + ': -6 [permanent: soziale Proben:' + bcolors.FAILh + '-3' + bcolors.ENDC + ']\n')
        
        print(bcolors.IND + bcolors.UNDERLINE + 'Entzug:' + bcolors.ENDC)
        print(bcolors.IND + ' Entzug kann je nach Droge und Schwere eine Weile dauern.')
        print(bcolors.IND + ' Schafft es der Char eine Anzahl von Wochen, die dem Abhängigkeitswert der Droge entspricht, die Finger davon zu lassen, kann er eine Abhängigkeitsprobe für die Substanz ablegen.')
        print(bcolors.IND + ' \tWenn erfolgreich: kann er sich mit Karma von Nachteil freikaufen')
        print(bcolors.IND + ' \tWenn nicht oder zu wenig Karma: Prozess beginnt von vorne.\n')
        
        print(bcolors.IND + bcolors.UNDERLINE + 'Überdosis:' + bcolors.ENDC)
        print(bcolors.IND + ' Wenn Char Substanz zu sich nimmt, unter deren Einfluss er noch steht oder die eine vergleichbare Wirkung hat, erleidet er geistigen Schaden')
        print(bcolors.IND + ' mit der Summe der Abhängigkeitswerte, die der Drogendosen entspricht.')
        print(bcolors.IND + ' \tSchadenswiderstand mit: ' + bcolors.GREENh + 'KON + WIL' + bcolors.ENDC)

        print('')
        liner()    
        print("'" + bcolors.BLUEh + 't' + bcolors.ENDC + "' Abhängigkeitstabelle")
        liner()
        print('', end='')
        choice = input(bcolors.GREENh + ' >> ' + bcolors.ENDC)
        if choice == 't':
            abhaengingkeitstabelle()
        else:
            drogen()

    def abhaengingkeitstabelle():
        clscrn()
        headerprnt()
        print(bcolors.IND + 'Abhängigkeitstabelle:\n')
        print(bcolors.IND + bcolors.UNDERLINE + 'Substanz'.center(20) + 'Abhängigkeitswert'.ljust(18) + ' '*5 + 'Abhängigkeitsschwellwert'.ljust(24) + ' ' + bcolors.ENDC + '\n')
        print(bcolors.IND + 'Alkohol'.center(20) + '3'.center(18) + ' '*5 + '2'.center(24))
        print(bcolors.IND + 'Bliss'.center(20) + '5'.center(18) + ' '*5 + '3'.center(24))        
        print(bcolors.IND + 'Cram'.center(20) + '4'.center(18) + ' '*5 + '3'.center(24))        
        print(bcolors.IND + 'Deepweed'.center(20) + '5'.center(18) + ' '*5 + '2'.center(24))        
        print(bcolors.IND + 'Jazz'.center(20) + '8'.center(18) + ' '*5 + '3'.center(24))        
        print(bcolors.IND + 'Kamikaze'.center(20) + '9'.center(18) + ' '*5 + '3'.center(24))        
        print(bcolors.IND + 'Long Haul'.center(20) + '2'.center(18) + ' '*5 + '1'.center(24))        
        print(bcolors.IND + 'Nitro'.center(20) + '9'.center(18) + ' '*5 + '3'.center(24))        
        print(bcolors.IND + 'Novacoke'.center(20) + '7'.center(18) + ' '*5 + '2'.center(24))        
        print(bcolors.IND + 'Psyche'.center(20) + '6'.center(18) + ' '*5 + '2'.center(24))        
        print(bcolors.IND + 'Soykaf'.center(20) + '1'.center(18) + ' '*5 + '2'.center(24))        
        print(bcolors.IND + 'Stim-Patch'.center(20) + '2'.center(18) + ' '*5 + '1'.center(24))
        print(bcolors.IND + 'Zen'.center(20) + '3'.center(18) + ' '*5 + '1'.center(24))

        print('')
        print(bcolors.IND + bcolors.UNDERLINE + 'Desorientierung' + bcolors.ENDC + '\t\tGRW 410')
        print(bcolors.IND + ' 10 Minuten verwirrt und desorientiert.')
        print(bcolors.IND + ' -2 WP-Mod auf alle Handlungen.')

        print('')
        liner()
        print('', end='')
        choice = input(bcolors.GREENh + ' >> ' + bcolors.ENDC)
        abhaengigkeitsprob()

    def wechselwirkungen():
        clscrn()
        headerprnt()
        print(bcolors.IND + 'Wechselwirkungen von mehreren Drogen gleichzeitig:\t\t[Bodyshop S.192]\n')
        print(bcolors.IND + 'Wenn Char eine Droge nimmt, während eine andere noch wirkt oder sich von deren Nachwirkungen erholt, dann kann es zu einer Wechselwirkung kommen:\n')
        print(bcolors.IND + ' Für jede weitere Droge: ' + bcolors.GREENh + '1W6' + bcolors.ENDC + ' würfeln und die Wechselwirkung tritt ein.\n')
        print(bcolors.IND + 'Straßenware: \t\t' + bcolors.BLUEh + '+1' + bcolors.ENDC + ' für jede konsumierte Droge dieser Kategorie.')
        print(bcolors.IND + 'Personalisierte Droge: ' + bcolors.BLUEh + '-1' + bcolors.ENDC + ' auf das Gesamtergebnis, wenn alle personalisierte Drogen sind.\n\n')
        print(bcolors.IND + bcolors.UNDERLINE + ' Ergebnis' + 5*' ' + 'Wechselwirkung'.ljust(56) + bcolors.ENDC + '\n')
        print(bcolors.IND + '1'.center(9) + 5*' ' + 'Verdoppelung der Dauer aller Drogen')
        print(bcolors.IND + '2-4'.center(9) + 5*' ' + 'keine Nebenwirkung')
        print(bcolors.IND + '5-6'.center(9) + 5*' ' + 'Dauer der Nachwirkungen aller Drogen verdoppelt')
        print(bcolors.IND + '7-9'.center(9) + 5*' ' + 'Nachwirkungen treten sofort ein')
        print(bcolors.IND + '10 '.center(9) + 5*' ' + '3G Schaden (ohne Widerstandsprobe)')
        print(bcolors.IND + '11-13'.center(9) + 5*' ' + 'Schaden durch Nachwirkungen ist körperlich statt geistig')
        print(bcolors.IND + '14+'.center(9) + 5*' ' + '10K Schaden (Widerstand nur mit KON)')
        print(bcolors.IND + bcolors.UNDERLINE + ' '.ljust(71) + bcolors.ENDC + '\n')
        print('')
        liner()
        print('', end='')
        choice = input(bcolors.GREENh + ' >> ' + bcolors.ENDC)
        drogen()

    clscrn()
    headerprnt()
    with codecs.open('text-drogen.json','r', 'utf-8-sig') as textdrogen:
        txtdrogen = textdrogen.read()
    td = json.loads(txtdrogen)
    for i,n in enumerate(td['texts']):
        print(bcolors.IND, end='')
        print((bcolors.UNDERLINE + '{name}'.format(**td['texts'][i]) + bcolors.ENDC).ljust(24), end='')
        print('[Art:' + bcolors.GREENh + '{artabh}'.format(**td['texts'][i]) + bcolors.ENDC + ' Vector:' + bcolors.GREENh + '{vector}'.format(**td['texts'][i]) + bcolors.ENDC, end='')
        print(' Verf:' + bcolors.GREENh + '{verf}'.format(**td['texts'][i]) + bcolors.ENDC + ' Preis:' + bcolors.GREENh + '{preis}'.format(**td['texts'][i]) + bcolors.ENDC + ']', end='')
        print(bcolors.GREENh + ' Geschwindigkeit:' + bcolors.ENDC + '{geschw}'.format(**td['texts'][i]), end='')
        print(bcolors.GREENh + ' Dauer:' + bcolors.ENDC + '{dauer}'.format(**td['texts'][i]))
        print('\t\t' + bcolors.IND + bcolors.GREENh + 'Wirkung:' + bcolors.ENDC + ' {wrkg}'.format(**td['texts'][i]))
        print('\t\t' + bcolors.IND + bcolors.GREENh + 'Info:' + bcolors.ENDC + ' {info}'.format(**td['texts'][i]))
        print('')
   #sch()    
    print('')
    liner()
    print("'" + bcolors.BLUEh + 'a' + bcolors.ENDC + "' Abhängigkeitsproben")
    print("'" + bcolors.BLUEh + 't' + bcolors.ENDC + "' Abhängigkeitstabelle")
    print("'" + bcolors.BLUEh + 'w' + bcolors.ENDC + "' Wechselwirkungen")
    liner()
    print('', end='')
    choice = input(bcolors.GREENh + ' >> ' + bcolors.ENDC)
    if choice == 'a':
        abhaengigkeitsprob()
    elif choice == 't':
        abhaengingkeitstabelle()
    elif choice == 'w':
        wechselwirkungen()
    else:
        exec_menu(choice)
    return

### WEAPONS
def weapons():
    headerprnt()
    astralconv()
    rangedwps = ['Maschinenpistolen', 'Schwere Pistolen', 'Sturmgewehre', 'Leichte Pistolen', 'Schrotflinten']
    x = character['weapons']['weapon']
    y = character['gears']['gear']
    skll_astralkampf = character['skills']['skill'][5]['total']
    txtwdth = 160
    for i,n in enumerate(x):
        flg = -1 
        for k,nam in enumerate(y):
            if x[i]['fullname'] == str(y[k]['gearname']) and y[k]['category'] == 'Foki':
                flg = k
        if flg > -1:
            print(bcolors.WARNINGh, end='') 
            print(bcolors.IND + ('{fullname:40}'.format(**x[i]) + bcolors.ENDC + ' ({category})'.format(**y[flg])).ljust(75) + (' DMG: [{damage:^5}] {rawdamage:8}  DK: {ap:3} Präz: {accuracy:6}  Verstecken: {conceal}  Würfel: {dicepool:>2}'.format(**x[i]) + bcolors.WARNINGh +'+{rating}'.format(**y[flg]) + bcolors.ENDC + bcolors.ASTRALh + ' (' + str(skll_astralkampf) + bcolors.WARNINGh +'+{rating}'.format(**y[flg]) + bcolors.ASTRALh + ')' + bcolors.ENDC).ljust(txtwdth-74) + '\t{source:3} {page}'.format(**x[i]), end='')
            print(bcolors.ENDC)
        elif x[i]['type'] == 'Ranged' and x[i]['category'] == 'Ausrüstung':
            if x[i]['name'].find('Minigranate') == -1:
                print((bcolors.IND + bcolors.FAILh + '{fullname:40} DMG: [{damage:^21}] DK: {ap:3}  Verstecken: {conceal}  Würfel: {dicepool}'.format(**x[i])).ljust(txtwdth) + bcolors.ENDC + '\t{source:3} {page}'.format(**x[i]))
        else:
            if x[i]['name'].find('Cyber') != -1:
                print(bcolors.IND + bcolors.PNZRGh + ('{fullname!s:40}'.format(**x[i]) + bcolors.ENDC + ' ({category})'.format(**x[i])).ljust(71) + (' DMG: [{damage!s:^5}] {rawdamage!s:8}  DK: {ap!s:3} Präz: {accuracy!s:6}  Verstecken: {conceal!s}  Würfel: {dicepool!s:>2}'.format(**x[i])).ljust(txtwdth-74) + '\t{source:3} {page}'.format(**x[i]) + bcolors.ENDC)
            else:
                print(bcolors.IND + '{fullname!s:40} ({category})'.format(**x[i]).ljust(71) + (' DMG: [{damage!s:^5}] {rawdamage!s:8}  DK: {ap!s:3} Präz: {accuracy!s:6}  Verstecken: {conceal!s}  Würfel: {dicepool!s:>2}'.format(**x[i])).ljust(txtwdth-74) + '\t{source:3} {page}'.format(**x[i]))
        if x[i]['type'] == 'Ranged' and x[i]['category'] != 'Ausrüstung':
            print('\t\t\t\t\t' + bcolors.IND + ' Mun: {ammo!s:11}\tModi: {mode!s:10}\tRückstoß: {rc!s}'.format(**x[i]) + '\tReichweiten: k({short}) m({medium}) l({long}) e({extreme})'.format(**x[i]['ranges']))
            if 'accessories' in x[i] and x[i]['accessories'] != None:
                if type(x[i]['accessories']['accessory']) is dict:
                    print(bcolors.IND +  bcolors.BLUEh + '\t+ ' + x[i]['accessories']['accessory']["name"].ljust(40) + ' '.ljust(20) + '{source:>3} {page:>3}'.format(**x[i]['accessories']['accessory']) +  bcolors.ENDC)
                else:
                    for num in range(len(x[i]['accessories']['accessory'])): 
                        print(bcolors.IND +  bcolors.BLUEh + '\t+ ' + x[i]['accessories']['accessory'][num]["name"].ljust(40) + ' '.ljust(20) + '{source:>3} {page:>3}'.format(**x[i]['accessories']['accessory'][num]) + bcolors.ENDC + '\t') #, end='')
        if x[i]['type'] == 'Ranged' and isastral == False and 'underbarrel' in x[i] and x[i]['underbarrel'] != None:
            print(bcolors.IND + bcolors.PNZRG + ' U: ' + bcolors.ENDC + '{fullname!s:36} ({category})'.format(**x[i]['underbarrel']['weapon']).ljust(67) + bcolors.ENDC + (' DMG: [{damage!s:^5}] {rawdamage!s:8}  DK: {ap!s:3} Präz: {accuracy!s:6}  Verstecken: {conceal!s}  Würfel: {dicepool!s:>2}'.format(**x[i]['underbarrel']['weapon'])).ljust(txtwdth-74) + '\t{source:3} {page}'.format(**x[i]['underbarrel']['weapon']))
            print('\t\t\t\t\t' + bcolors.IND + ' Mun: {ammo!s:11}\tModi: {mode!s:10}\tRückstoß: {rc!s}'.format(**x[i]['underbarrel']['weapon']) + '\tReichweiten: k({short}) m({medium}) l({long}) e({extreme})'.format(**x[i]['underbarrel']['weapon']['ranges']))
        if x[i]['name'].find('Minigranate') == -1:
            print('')
    if imkampf == True:
        print('' + bcolors.FAILh)
        liner()
        print('', end='')
        choice = input(' *>> ' + bcolors.ENDC)
        kampf()
    else:
        sch()
    return

### ARMOR
def armor():
    headerprnt()
    x = character['armors']['armor']
    for i,n in enumerate(x):
        print(bcolors.IND + '{fullname:40} \tPanzerung: {armor:>2}\t\tKosten: {cost:>6}\t{source:3} {page:>3}'.format(**x[i]))
        if x[i]['armormods'] != None:
            z = x[i]['armormods']['armormod'] 
            for num in range(len(x[i]['armormods']['armormod'])):
                print('\t' + bcolors.IND, bcolors.BLUEh + '+ ' + z[num]['fullname'] + bcolors.ENDC)
            print('\n', end='')
    sch()
    return

### CONTACTS
def cont():
    headerprnt()
    x = character['contacts']['contact']
    for i,n in enumerate(x):
        print(bcolors.IND, bcolors.BLUEh + '{name:25}'.format(**x[i]) + bcolors.ENDC + '{metatype}, {age}, {sex}, Familie: {family}'.format(**x[i]))
        print(bcolors.IND + '[Kon: {connection}, Loyalität: {loyalty}]'.format(**x[i]) + bcolors.GREENh + '\t   {role:25}'.format(**x[i]) + bcolors.ENDC + '\tBezahlung: {preferredpayment}'.format(**x[i]))
        print(bcolors.IND + '{leer: <25} Hobbies: {hobbiesvice}'.format(**x[i], leer=' '))
        print(bcolors.IND + '{leer: <25} Kontaktart: {contacttype:25} Location: {location}'.format(**x[i], leer=' '))
        print('')
    sch()
    return

###GEAR
def gear(alles=1, komm=0):
    clscrn()
    headerprnt()
    n_fok = []
    n_ID = []
    n_ID_C = []
    n_MAG = []
    n_AMMO = []
    n_KOMM = []
    n_med = []
    n_rest = []
    n_rest_C = []
    l_gear = []
    n_items = 0
    x = character['gears']['gear']
    for i,n in enumerate(x):
        if x[i]['category'] == 'Foki':
            n_fok.append(i)
            n_items += 1
        elif x[i]['category'] == 'IDs/Credsticks':
            n_ID.append(i)            
            n_items += 1
            if x[i]['children'] != None:
                n_ID_C.append(len(x[i]['children']['gear']))
                n_items += len(x[i]['children']['gear'])
            else:
                n_ID_C.append(0)
                n_items += 1
        elif x[i]['category'] == 'Magische Güter':
            n_MAG.append(i)
            n_items += 1
        elif x[i]['isammo'] == 'True':
            n_AMMO.append(i)
            n_items += 1
        elif x[i]['iscommlink'] == 'True':
            n_KOMM.append(i)
            n_items += 1
        elif x[i]['category'] == 'Biotech':
            n_med.append(i)
            n_items += 1
        else:
            n_rest.append(i)
            n_items += 1
            if x[i]['children'] != None:
                n_rest_C.append(len(x[i]['children']['gear']))
                n_items += len(x[i]['children']['gear'])
            else:
                n_rest_C.append(0)
                n_items += 1
    txtwdth = 120 
    funbreak = 0
    nipp = 40
    cnt_nipp = 0
    lenx = len(x) - len(n_KOMM)
    n_pgs = n_items//nipp
    n_pgsl = n_items%nipp
    n_pg = 0
    l_gear.extend(n_fok)
    l_gear.extend(n_ID)
    l_gear.extend(n_MAG)
    l_gear.extend(n_AMMO)
    l_gear.extend(n_med)
    l_gear.extend(n_rest)
    if komm > 0:
        for num in range(len(n_KOMM)):
            y = n_KOMM[num]
            print(bcolors.IND + '{qty:>2} x {name:30}: St.{rating}\tAngriff: {attack} Schleicher: {sleaze} Datenverarbeitung: {dataprocessing} Firewall: {firewall}\t\tKosten: {cost:>7}\t\t{source:3} {page}'.format(**x[y]))
            for nnum in range(2):
                print('\t\t' + bcolors.IND, bcolors.BLUEh, end='') 
                for k in range(len(x[y]['children']['gear']['children']['gear'])//2):
                    print('{name}, '.format(**x[y]['children']['gear']['children']['gear'][k + nnum*(len(x[y]['children']['gear']['children']['gear'])//2)]), end='')
                print(bcolors.ENDC)
    elif komm == 0 and alles == 1:
        for num in range(len(n_fok)):
            y = n_fok[num]
            print((bcolors.IND + '{name:30}: '.format(**x[y]) + bcolors.WARNINGh + '{gearname:40} St.{rating}'.format(**x[y]) + bcolors.ENDC).ljust(txtwdth) + 'Kosten: {cost:>7}\t\t{source:3} {page}'.format(**x[y]))
            print('')
        for i in range(len(n_ID)):
            y = n_ID[i]
            print((bcolors.IND + '{name} St.{rating}: '.format(**x[y]) + bcolors.GREENh + '{extra:40}'.format(**x[y]) + bcolors.ENDC).ljust(txtwdth) + 'Kosten: {cost:>7}\t\t{source:3} {page}'.format(**x[y]))
            if x[y]['children'] != None:
                for k,nam in enumerate(x[y]['children']['gear']):
                    print('\t' + bcolors.IND, bcolors.BLUEh + '+ {name}: {extra!s:35} St.{rating}\t Kosten: {cost}'.format(**x[y]['children']['gear'][k]) + bcolors.ENDC)
            print('')
        for i in range(len(n_MAG)):
            y = n_MAG[i]
            print((bcolors.IND + bcolors.ASTRALh + '{qty:>5} x {name:30} [{extra}]'.format(**x[y]) + bcolors.ENDC).ljust(txtwdth) + 'Kosten: {cost:>7}\t\t{source:3} {page}'.format(**x[y]))
            print('')
        for i in range(len(n_AMMO)):
            y = n_AMMO[i]
            if 'weaponbonusdamage' in x[y].keys():
                print((bcolors.IND + bcolors.FAILh + '{qty:>5} x {name:40} [ DMG: {weaponbonusdamage} | DK: {weaponbonusap} ] für: {extra}'.format(**x[y]) + bcolors.ENDC).ljust(txtwdth) + 'Kosten: {cost:>7}\t\t{source:3} {page}'.format(**x[y]))
            else:
                print((bcolors.IND + bcolors.FAILh + '{qty:>5} x {name:40} {leer: <21} für: {extra}'.format(**x[y], leer=' ') + bcolors.ENDC).ljust(txtwdth) + 'Kosten: {cost:>7}\t\t{source:3} {page}'.format(**x[y]))
            print('')
        for i in range(len(n_med)):
            y = n_med[i]
            print((bcolors.IND + bcolors.GREENh + '{qty:>5}'.format(**x[y]) + bcolors.ENDC + ' x {name:30} St.{rating}'.format(**x[y]) + bcolors.ENDC).ljust(txtwdth) + 'Kosten: {cost:>7}\t\t{source:3} {page}'.format(**x[y]))
            print('')
        for i in range(len(n_rest)):            
            y = n_rest[i]
            print((bcolors.IND + '{qty!s:>5} {name!s:40} St.{rating!s}\tVerfügbarkeit: {avail!s}'.format(**x[y])).ljust(txtwdth-12) + 'Kosten: {cost!s:>7}\t\t{source:3} {page}'.format(**x[y]))
            if x[y]['children'] != None:
                if type(x[y]['children']['gear']) is dict:
                    print(bcolors.IND + bcolors.BLUEh + '\t+ {name:35} St.{rating}'.format(**x[y]['children']['gear']) + bcolors.ENDC)
                else:
                    for k,nam in enumerate(x[y]['children']['gear']):
                        if x[y]['iscommlink'] == 'False': 
                            print(bcolors.IND + bcolors.BLUEh + '\t+ {name:35} St.{rating}'.format(**x[y]['children']['gear'][k]) + bcolors.ENDC)
    elif komm == 0 and alles == 2:                        
        for num in range(len(n_fok)):
            y = n_fok[num]
            print((bcolors.IND + '{name:30}: '.format(**x[y]) + bcolors.WARNINGh + '{gearname:40} St.{rating}'.format(**x[y]) + bcolors.ENDC).ljust(txtwdth) + 'Kosten: {cost:>7}\t\t{source:3} {page}'.format(**x[y]))
            print('')
    elif komm == 0 and alles == 3:
        for i in range(len(n_ID)):
            y = n_ID[i]
            print((bcolors.IND + '{name} St.{rating}: '.format(**x[y]) + bcolors.GREENh + '{extra:40}'.format(**x[y]) + bcolors.ENDC).ljust(txtwdth) + 'Kosten: {cost:>7}\t\t{source:3} {page}'.format(**x[y]))
            if x[y]['children'] != None:
                for k,nam in enumerate(x[y]['children']['gear']):
                    print('\t' + bcolors.IND, bcolors.BLUEh + '+ {name}: {extra!s:35} St.{rating}\t Kosten: {cost}'.format(**x[y]['children']['gear'][k]) + bcolors.ENDC)
            print('')
    elif komm == 0 and alles == 4:
        for i in range(len(n_MAG)):
            y = n_MAG[i]
            print((bcolors.IND + bcolors.ASTRALh + '{qty:>5} x {name:30} [{extra}]'.format(**x[y]) + bcolors.ENDC).ljust(txtwdth) + 'Kosten: {cost:>7}\t\t{source:3} {page}'.format(**x[y]))
            print('')
    elif komm == 0 and alles == 5:
        for i in range(len(n_AMMO)):
            y = n_AMMO[i]
            if 'weaponbonusdamage' in x[y].keys():
                print((bcolors.IND + bcolors.FAILh + '{qty:>5} x {name:40} [ DMG: {weaponbonusdamage} | DK: {weaponbonusap} ] für: {extra}'.format(**x[y]) + bcolors.ENDC).ljust(txtwdth) + 'Kosten: {cost:>7}\t\t{source:3} {page}'.format(**x[y]))
            else:
                print((bcolors.IND + bcolors.FAILh + '{qty:>5} x {name:40} {leer: <21} für: {extra}'.format(**x[y], leer=' ') + bcolors.ENDC).ljust(txtwdth) + 'Kosten: {cost:>7}\t\t{source:3} {page}'.format(**x[y]))
            print('')
    elif komm == 0 and alles == 6:
        for i in range(len(n_med)):
            y = n_med[i]
            print((bcolors.IND + bcolors.GREENh + '{qty:>5}'.format(**x[y]) + bcolors.ENDC + ' x {name:30} St.{rating}'.format(**x[y]) + bcolors.ENDC).ljust(txtwdth) + 'Kosten: {cost:>7}\t\t{source:3} {page}'.format(**x[y]))
            print('')
    elif komm == 0 and alles == 7:
        for i in range(len(n_rest)):            
            y = n_rest[i]
            print((bcolors.IND + '{qty:>5} {name:40} St.{rating}\tVerfügbarkeit: {avail}'.format(**x[y])).ljust(txtwdth-12) + 'Kosten: {cost:>7}\t\t{source:3} {page}'.format(**x[y]))
            if x[y]['children'] != None:
                if type(x[y]['children']['gear']) is dict:
                    print(bcolors.IND + bcolors.BLUEh + '\t+ {name:35} St.{rating}'.format(**x[y]['children']['gear']) + bcolors.ENDC)
                else:
                    for k,nam in enumerate(x[y]['children']['gear']):
                        if x[y]['iscommlink'] == 'False': 
                            print(bcolors.IND + bcolors.BLUEh + '\t+ {name:35} St.{rating}'.format(**x[y]['children']['gear'][k]) + bcolors.ENDC)
    print('\n') 
    liner()
    print(bcolors.IND + "'" + bcolors.BLUEh + 'k' + bcolors.ENDC + "' Kommlinks, '" + bcolors.BLUEh + 'g' + bcolors.ENDC + "' Gesamtliste, '" + bcolors.BLUEh + 'f' + bcolors.ENDC + "' Foki, '" + bcolors.BLUEh + 'id' + bcolors.ENDC + "' IDs/Credsticks, '" + bcolors.BLUEh + 'm' + bcolors.ENDC + "' Magisches, '" + bcolors.BLUEh + 'a' + bcolors.ENDC + "' AMMO, '" + bcolors.BLUEh + 'med' + bcolors.ENDC + "' Medizinisches, '" + bcolors.BLUEh + 'r' + bcolors.ENDC + "' Sonstiges.")
    liner()
    choice = input(bcolors.GREENh + ' >> ' + bcolors.ENDC)
    if choice == 'k':
        gear(komm=1)
    elif choice == 'g':
        gear(alles=1)
    elif choice == 'f':
        gear(alles=2)
    elif choice == 'id':
        gear(alles=3)
    elif choice == 'm':
        gear(alles=4)
    elif choice == 'a':
        gear(alles=5)
    elif choice == 'med':
        gear(alles=6)
    elif choice == 'r':
        gear(alles=7)
    else:
        exec_menu(choice)
    return

### KAUFEN
def kaufen():
    funbreak = 0
    def mengek(name,preis):
        clscrn()
        headerprnt()
        print(bcolors.IND + 'Wie viel ' + bcolors.GREENh + name + bcolors.ENDC + ' soll gekauft werden?\n')
        funbreak = 0
        rtrn = ['','','']
        while funbreak < 1:
            print(25*'_')
            qt = input(bcolors.GREENh + ' >> ' + bcolors.ENDC)
            if qt.lower() == 'q':
                funbreak = 1
            elif qt.isdigit() == True and int(qt) > 0:
                clscrn()
                headerprnt()
                rtrn[0] = qt
                print('\n' + bcolors.IND + ' ' + bcolors.WARNINGh + qt + bcolors.ENDC + ' x ' + bcolors.GREENh + name + bcolors.ENDC + '.\n')
                if name.find('Taserpfeil') != -1:
                    rtrn[1] = 'Taser'
                elif name.find('Injektionspfeil') != -1:
                    rtrn[1] = 'Exotische Fernkampfwaffen'
                elif name.find('DMSO-Gelpacks') != -1:
                    rtrn[1] = 'Exotische Fernkampfwaffen'
                elif name.find('Sturmkanonenmunition') != -1:
                    rtrn[1] = 'Sturmkanonen'
                else:
                    print(bcolors.IND + 'Für welchen Waffentyp soll ' + name + ' gekauft werden?\n')
                    wafftyp = ['Holdout', 'Leichte Pistolen', 'Schwere Pistolen', 'Automatikpistolen', 'Maschinenpistolen', 'Sturmgewehre', 'Karabiner', 'Gewehre', 'Scharfschützengewehre', 'Schrotflinten', 'Leichte Maschinengewehre', 'Mittlere Maschinengewehre', 'Schwere Maschinengewehre', 'Unterlaufwaffen', 'Mikrodrohnenwaffen']
                    for i,nam in enumerate(wafftyp):
                        if i+1 < 10:
                            print(bcolors.IND + 2*' ' + bcolors.BLUEh, end='')
                        else:
                            print(bcolors.IND + ' ' + bcolors.BLUEh, end='')
                        print(str(i+1) + bcolors.ENDC + ') ' + nam)
                    print('')
                    print(25*'_')
                    funfunbreak = 0
                    while funfunbreak < 1:
                        wtn = input(bcolors.GREENh + ' >> ' + bcolors.ENDC)
                        if wtn.lower() == 'q':
                            rtrn = ['','','']
                            funfunbreak = 1
                        elif wtn.isdigit() == True and int(wtn) <= len(wafftyp):
                            rtrn[1] = wafftyp[int(wtn)-1]
                            funfunbreak = 1
                        else:
                            print(bcolors.IND + bcolors.WARNINGh + wtn + bcolors.FAILh + ' ist keine gültige Zahl. Nochmal!' + bcolors.ENDC)
                clscrn()
                headerprnt()
                print(bcolors.IND + 'Zu welchem Prozentsatz soll ' + name + ' gekauft werden?\n')
                prs = float(preis.replace('.', '').replace(',','.'))
                totalprs = int(prs*100)*int(qt)
                print(bcolors.IND + bcolors.GREENh + qt + bcolors.ENDC + ' x ' + preis + ' Nuyen x ' + bcolors.BLUEh + 'Prozentsatz' + bcolors.ENDC)
                print('')
                print(25*'_')
                funfunbreak = 0
                if rtrn != ['','','']:
                    while funfunbreak < 1:
                        prztn = input(bcolors.BLUEh + ' Prozentsatz' + bcolors.ENDC + '(0..100..)' + bcolors.BLUEh + ': ' + bcolors.ENDC)
                        if prztn.lower() == 'q':
                            rtrn = ['','','']
                            funfunbreak = 1
                        elif prztn.isdigit() == True and int(prztn) >= 0:
                            totalprs = float(totalprs*(int(prztn)/100)/100)
                            clscrn()
                            headerprnt()
                            print('\n' + bcolors.IND + bcolors.GREENh + qt + bcolors.ENDC + ' x ' + name + ' für ' + bcolors.WARNINGh + str(totalprs) + ' Nuyen ' + bcolors.ENDC + 'kaufen?')
                            print('')
                            print(25*'_')
                            abfr = input(' (' + bcolors.GREENh + 'j' + bcolors.ENDC + '/' + bcolors.GREENh + 'n' + bcolors.ENDC + '): ')
                            if abfr.lower() == 'j':
                                rtrn[2] = totalprs
                                funfunbreak = 1
                            else:
                                rtrn = ['','','']
                                funfunbreak = 1
                        else:
                            print(bcolors.IND + bcolors.WARNINGh + prztn + bcolors.FAILh + ' ist keine gültige Angabe. Nochmal!' + bcolors.ENDC)
                funbreak = 1
            else:    
                print(bcolors.IND + bcolors.WARNINGh + qt + bcolors.FAILh + ' ist keine gültige Zahl. Nochmal!' + bcolors.ENDC)
        return rtrn        

    def muntojson(nam,newcost,newqty,newwt):
        if nam == 'APDS':
            return {'active': 'False','armorcapacity': None,'attack': '0','avail': '12V', 'avail_english': '12F', 'bonded': 'False', 'capacity': None, 'category': 'Munition', 'category_english': 'Ammunition', 'children': None, 'conditionmonitor': '8', 'cost': newcost, 'dataprocessing': '0', 'devicerating': '0', 'equipped': 'True', 'extra': newwt, 'firewall': '0', 'gearname': None, 'homenode': 'False', 'isammo': 'True', 'iscommlink': 'False', 'isos': 'False', 'ispersona': 'False', 'isprogram': 'False', 'issin': 'False', 'location': None, 'matrixcmfilled': '0', 'maxrating': None, 'name': 'Munition: APDS', 'name_english': 'Ammo: APDS', 'owncost': '0,1', 'page': '436', 'programlimit': '0', 'qty': newqty, 'rating': '0', 'sleaze': '0', 'source': 'SR5', 'weaponbonusap': '-4', 'weaponbonusdamage': '+0', 'weaponbonusdamage_english': '+0', 'wirelesson': 'False'}
        elif nam == 'DMSO-Gelpacks':
            return {'active': 'False', 'armorcapacity': None, 'attack': '0', 'avail': '2E', 'avail_english': '2R', 'bonded': 'False', 'capacity': None, 'category': 'Munition', 'category_english': 'Ammunition', 'children': None, 'conditionmonitor': '8', 'cost': newcost, 'dataprocessing': '0', 'devicerating': '0', 'equipped': 'True', 'extra': 'Exotische Fernkampfwaffen', 'firewall': '0', 'gearname': None, 'homenode': 'False', 'isammo': 'True', 'iscommlink': 'False', 'isos': 'False', 'ispersona': 'False', 'isprogram': 'False', 'issin': 'False', 'location': None, 'matrixcmfilled': '0', 'maxrating': None, 'name': 'Munition: DMSO-Gelpacks', 'name_english': 'Ammo: DMSO Rounds', 'owncost': '0,1', 'page': '436', 'programlimit': '0', 'qty': newqty, 'rating': '0', 'sleaze': '0', 'source': 'SR5G', 'wirelesson': 'False'}
        elif nam == 'Explosivmunition':
            return {'active': 'False', 'armorcapacity': None, 'attack': '0', 'avail': '9V', 'avail_english': '9F', 'bonded': 'False', 'capacity': None, 'category': 'Munition', 'category_english': 'Ammunition', 'children': None, 'conditionmonitor': '8', 'cost': newcost, 'dataprocessing': '0', 'devicerating': '0', 'equipped': 'True', 'extra': newwt, 'firewall': '0', 'gearname': None, 'homenode': 'False', 'isammo': 'True', 'iscommlink': 'False', 'isos': 'False', 'ispersona': 'False', 'isprogram': 'False', 'issin': 'False', 'location': None, 'matrixcmfilled': '0', 'maxrating': None, 'name': 'Munition: Explosivgeschosse', 'name_english': 'Ammo: Explosive Rounds', 'owncost': '0,1', 'page': '436', 'programlimit': '0', 'qty': newqty, 'rating': '0', 'sleaze': '0', 'source': 'SR5', 'weaponbonusap': '-1', 'weaponbonusdamage': '+1', 'weaponbonusdamage_english': '+1', 'wirelesson': 'False'}
        elif nam == 'Flechettemunition':
            return {'active': 'False', 'armorcapacity': None, 'attack': '0', 'avail': '6E', 'avail_english': '6R', 'bonded': 'False', 'capacity': None, 'category': 'Munition', 'category_english': 'Ammunition', 'children': None, 'conditionmonitor': '8', 'cost': newcost, 'dataprocessing': '0', 'devicerating': '0', 'equipped': 'True', 'extra': newwt, 'firewall': '0', 'gearname': None, 'homenode': 'False', 'isammo': 'True', 'iscommlink': 'False', 'isos': 'False', 'ispersona': 'False', 'isprogram': 'False', 'issin': 'False', 'location': None, 'matrixcmfilled': '0', 'maxrating': None, 'name': 'Munition: Flechettegeschosse', 'name_english': 'Ammo: Flechette Rounds', 'owncost': '0,1', 'page': '436', 'programlimit': '0', 'qty': newqty, 'rating': '0', 'sleaze': '0', 'source': 'SR5', 'weaponbonusap': '+5', 'weaponbonusdamage': '+2K(f)', 'weaponbonusdamage_english': '+2P(f)', 'wirelesson': 'False'}
        elif nam == 'Gelmunition':
            return {'active': 'False', 'armorcapacity': None, 'attack': '0', 'avail': '2E', 'avail_english': '2R', 'bonded': 'False', 'capacity': None, 'category': 'Munition', 'category_english': 'Ammunition', 'children': None, 'conditionmonitor': '8', 'cost': newcost, 'dataprocessing': '0', 'devicerating': '0', 'equipped': 'True', 'extra': newwt, 'firewall': '0', 'gearname': None, 'homenode': 'False', 'isammo': 'True', 'iscommlink': 'False', 'isos': 'False', 'ispersona': 'False', 'isprogram': 'False', 'issin': 'False', 'location': None, 'matrixcmfilled': '0', 'maxrating': None, 'name': 'Munition: Gelgeschosse', 'name_english': 'Ammo: Gel Rounds', 'owncost': '0,1', 'page': '436', 'programlimit': '0', 'qty': newqty, 'rating': '0', 'sleaze': '0', 'source': 'SR5', 'weaponbonusap': '+1', 'weaponbonusdamage': '+0G', 'weaponbonusdamage_english': '+0S', 'wirelesson': 'False'}
        elif nam == 'Hohlspitzmunition':
            return {'active': 'False', 'armorcapacity': None, 'attack': '0', 'avail': '4V', 'avail_english': '4F', 'bonded': 'False', 'capacity': None, 'category': 'Munition', 'category_english': 'Ammunition', 'children': None, 'conditionmonitor': '8', 'cost': newcost, 'dataprocessing': '0', 'devicerating': '0', 'equipped': 'True', 'extra': newwt, 'firewall': '0', 'gearname': None, 'homenode': 'False', 'isammo': 'True', 'iscommlink': 'False', 'isos': 'False', 'ispersona': 'False', 'isprogram': 'False', 'issin': 'False', 'location': None, 'matrixcmfilled': '0', 'maxrating': None, 'name': 'Munition: Hohlspitzmunition', 'name_english': 'Ammo: Hollow Points', 'owncost': '0,1', 'page': '436', 'programlimit': '0', 'qty': newqty, 'rating': '0', 'sleaze': '0', 'source': 'SR5', 'weaponbonusap': '+2', 'weaponbonusdamage': '+1', 'weaponbonusdamage_english': '+1', 'wirelesson': 'False'}
        elif nam == 'Ijektionspfeile':
            return {'active': 'False', 'armorcapacity': None, 'attack': '0', 'avail': '4E', 'avail_english': '4R', 'bonded': 'False', 'capacity': None, 'category': 'Munition', 'category_english': 'Ammunition', 'children': None, 'conditionmonitor': '8', 'cost': newcost, 'dataprocessing': '0', 'devicerating': '0', 'equipped': 'True', 'extra': 'Exotische Fernkampfwaffen', 'firewall': '0', 'gearname': None, 'homenode': 'False', 'isammo': 'True', 'iscommlink': 'False', 'isos': 'False', 'ispersona': 'False', 'isprogram': 'False', 'issin': 'False', 'location': None, 'matrixcmfilled': '0', 'maxrating': None, 'name': 'Munition: Injektionspfeile', 'name_english': 'Ammo: Injection Darts', 'owncost': '0,1', 'page': '436', 'programlimit': '0', 'qty': newqty, 'rating': '0', 'sleaze': '0', 'source': 'SR5', 'wirelesson': 'False'}
        elif nam == 'Leuchtspurmunition':
            return {'active': 'False', 'armorcapacity': None, 'attack': '0', 'avail': '6E', 'avail_english': '6R', 'bonded': 'False', 'capacity': None, 'category': 'Munition', 'category_english': 'Ammunition', 'children': None, 'conditionmonitor': '8', 'cost': newcost, 'dataprocessing': '0', 'devicerating': '0', 'equipped': 'True', 'extra': newwt, 'firewall': '0', 'gearname': None, 'homenode': 'False', 'isammo': 'True', 'iscommlink': 'False', 'isos': 'False', 'ispersona': 'False', 'isprogram': 'False', 'issin': 'False', 'location': None, 'matrixcmfilled': '0', 'maxrating': None, 'name': 'Munition: Leuchtspur', 'name_english': 'Ammo: Tracer', 'owncost': '0,1', 'page': '436', 'programlimit': '0', 'qty': newqty, 'rating': '0', 'sleaze': '0', 'source': 'SR5', 'wirelesson': 'False'}
        elif nam == 'Schockermunition':
            return {'active': 'False', 'armorcapacity': None, 'attack': '0', 'avail': '6E', 'avail_english': '6R', 'bonded': 'False', 'capacity': None, 'category': 'Munition', 'category_english': 'Ammunition', 'children': None, 'conditionmonitor': '8', 'cost': newcost, 'dataprocessing': '0', 'devicerating': '0', 'equipped': 'True', 'extra': newwt, 'firewall': '0', 'gearname': None, 'homenode': 'False', 'isammo': 'True', 'iscommlink': 'False', 'isos': 'False', 'ispersona': 'False', 'isprogram': 'False', 'issin': 'False', 'location': None, 'matrixcmfilled': '0', 'maxrating': None, 'name': 'Munition: Schocker', 'name_english': 'Ammo: Stick-n-Shock', 'owncost': '0,1', 'page': '437', 'programlimit': '0', 'qty': newqty, 'rating': '0', 'sleaze': '0', 'source': 'SR5', 'weaponbonusap': '-5', 'weaponbonusdamage': '-2G(e)', 'weaponbonusdamage_english': '-2S(e)', 'wirelesson': 'False'}
        elif nam == 'Standardmunition':
            return {'active': 'False', 'armorcapacity': None, 'attack': '0', 'avail': '2E', 'avail_english': '2R', 'bonded': 'False', 'capacity': None, 'category': 'Munition', 'category_english': 'Ammunition', 'children': None, 'conditionmonitor': '8', 'cost': newcost, 'dataprocessing': '0', 'devicerating': '0', 'equipped': 'True', 'extra': newwt, 'firewall': '0', 'gearname': None, 'homenode': 'False', 'isammo': 'True', 'iscommlink': 'False', 'isos': 'False', 'ispersona': 'False', 'isprogram': 'False', 'issin': 'False', 'location': None, 'matrixcmfilled': '0', 'maxrating': None, 'name': 'Munition: Standardmunition', 'name_english': 'Ammo: Regular Ammo', 'owncost': '0,1', 'page': '436', 'programlimit': '0', 'qty': newqty, 'rating': '0', 'sleaze': '0', 'source': 'SR5', 'wirelesson': 'False'}
        elif nam == 'Sturmkanonenmunition':
            return {'active': 'False', 'armorcapacity': None, 'attack': '0', 'avail': '12V', 'avail_english': '12F', 'bonded': 'False', 'capacity': None, 'category': 'Munition', 'category_english': 'Ammunition', 'children': None, 'conditionmonitor': '8', 'cost': newcost, 'dataprocessing': '0', 'devicerating': '0', 'equipped': 'True', 'extra': 'Sturmkanonen', 'firewall': '0', 'gearname': None, 'homenode': 'False', 'isammo': 'True', 'iscommlink': 'False', 'isos': 'False', 'ispersona': 'False', 'isprogram': 'False', 'issin': 'False', 'location': None, 'matrixcmfilled': '0', 'maxrating': None, 'name': 'Munition: Sturmkanone', 'name_english': 'Ammo: Assault Cannon', 'owncost': '0,1', 'page': '437', 'programlimit': '0', 'qty': newqty, 'rating': '0', 'sleaze': '0', 'source': 'SR5', 'wirelesson': 'False'}
        elif nam == 'Taserpfeile':
            return {'active': 'False', 'armorcapacity': None, 'attack': '0', 'avail': '3', 'avail_english': '3', 'bonded': 'False', 'capacity': None, 'category': 'Munition', 'category_english': 'Ammunition', 'children': None, 'conditionmonitor': '8', 'cost': newcost, 'dataprocessing': '0', 'devicerating': '0', 'equipped': 'True', 'extra': 'Taser', 'firewall': '0', 'gearname': None, 'homenode': 'False', 'isammo': 'True', 'iscommlink': 'False', 'isos': 'False', 'ispersona': 'False', 'isprogram': 'False', 'issin': 'False', 'location': None, 'matrixcmfilled': '0', 'maxrating': None, 'name': 'Munition: Taserpfeil', 'name_english': 'Ammo: Taser Dart', 'owncost': '0,1', 'page': '437', 'programlimit': '0', 'qty': newqty, 'rating': '0', 'sleaze': '0', 'source': 'SR5', 'wirelesson': 'False'}
        elif nam == 'Ortungsmunition (Spionage)':
            return {'active': 'False', 'armorcapacity': None, 'attack': '0', 'avail': '8E', 'avail_english': '8R', 'bonded': 'False', 'capacity': None, 'category': 'Munition', 'category_english': 'Ammunition', 'children': None, 'conditionmonitor': '8', 'cost': newcost, 'dataprocessing': '0', 'devicerating': '0', 'equipped': 'True', 'extra': newwt, 'firewall': '0', 'gearname': None, 'homenode': 'False', 'isammo': 'True', 'iscommlink': 'False', 'isos': 'False', 'ispersona': 'False', 'isprogram': 'False', 'issin': 'False', 'location': None, 'matrixcmfilled': '0', 'maxrating': None, 'name': 'Munition: Ortergeschosse, Spionagemarker', 'name_english': 'Ammo: Tracker Rounds, Stealth Tag', 'owncost': '0,1', 'page': '55', 'programlimit': '0', 'qty': newqty, 'rating': '0', 'sleaze': '0', 'source': 'RG', 'wirelesson': 'False'}
        elif nam == 'Ortungsmunition (Sicherheit)':
            return {'active': 'False', 'armorcapacity': None, 'attack': '0', 'avail': '8E', 'avail_english': '8R', 'bonded': 'False', 'capacity': None, 'category': 'Munition', 'category_english': 'Ammunition', 'children': None, 'conditionmonitor': '8', 'cost': newcost, 'dataprocessing': '0', 'devicerating': '0', 'equipped': 'True', 'extra': newwt, 'firewall': '0', 'gearname': None, 'homenode': 'False', 'isammo': 'True', 'iscommlink': 'False', 'isos': 'False', 'ispersona': 'False', 'isprogram': 'False', 'issin': 'False', 'location': None, 'matrixcmfilled': '0', 'maxrating': None, 'name': 'Munition: Ortergeschosse, Sicherheitsmarker', 'name_english': 'Ammo: Tracker Rounds, Safety Tag', 'owncost': '0,1', 'page': '55', 'programlimit': '0', 'qty': newqty, 'rating': '0', 'sleaze': '0', 'source': 'RG', 'wirelesson': 'False'}
       ### Granaten 
        elif nam == 'Granate: Flash-Pack':
            return [{'active': 'False', 'armorcapacity': None, 'attack': '0', 'avail': '4', 'avail_english': '4', 'bonded': 'False', 'capacity': None, 'category': 'Munition', 'category_english': 'Ammunition', 'children': None, 'conditionmonitor': '8', 'cost': newcost, 'dataprocessing': '0', 'devicerating': '0', 'equipped': 'True', 'extra': None, 'firewall': '0', 'gearname': None, 'homenode': 'False', 'isammo': 'True', 'iscommlink': 'False', 'isos': 'False', 'ispersona': 'False', 'isprogram': 'False', 'issin': 'False', 'location': None, 'matrixcmfilled': '0', 'maxrating': None, 'name': 'Granate: Flash-Pack', 'name_english': 'Grenade: Flash-Pak', 'owncost': '1', 'page': '437', 'programlimit': '0', 'qty': newqty, 'rating': '0', 'sleaze': '0', 'source': 'SR5', 'wirelesson': 'False'}, {'accuracy': '5', 'alternateranges': {'extreme': None, 'long': None, 'medium': None, 'name': None, 'short': None}, 'ammo': '1', 'ammo_english': '1', 'ap': '-', 'avail': '4', 'availableammo': '2,0', 'category': 'Ausrüstung', 'category_english': 'Gear', 'clips': None, 'conceal': '+0', 'cost': newcost, 'currentammo': None, 'damage': 'Spezial', 'damage_english': 'Special', 'dicepool': '10', 'fullname': 'Granate: Flash-Pack', 'location': None, 'mode': None, 'name': 'Granate: Flash-Pack', 'name_english': 'Grenade: Flash-Pak', 'owncost': '1', 'page': '437', 'ranges': {'extreme': '19-30', 'long': '13-18', 'medium': '7-12', 'name': 'Standard Granaten', 'short': '0-6'}, 'rawdamage': 'Special', 'rc': '2', 'reach': '0', 'skill': 'Throwing Weapons', 'source': 'SR5', 'type': 'Ranged', 'weaponname': None, 'wirelesson': 'False'}]
        elif nam == 'Granate: Gas':
            return [{'active': 'False', 'armorcapacity': None, 'attack': '0', 'avail': '4E', 'avail_english': '4R', 'bonded': 'False', 'capacity': None, 'category': 'Munition', 'category_english': 'Ammunition', 'children': None, 'conditionmonitor': '8', 'cost': newcost, 'dataprocessing': '0', 'devicerating': '0', 'equipped': 'True', 'extra': None, 'firewall': '0', 'gearname': None, 'homenode': 'False', 'isammo': 'True', 'iscommlink': 'False', 'isos': 'False', 'ispersona': 'False', 'isprogram': 'False', 'issin': 'False', 'location': None, 'matrixcmfilled': '0', 'maxrating': None, 'name': 'Granate: Gas', 'name_english': 'Grenade: Gas', 'owncost': '1', 'page': '437', 'programlimit': '0', 'qty': newqty, 'rating': '0', 'sleaze': '0', 'source': 'SR5', 'wirelesson': 'False'}, {'accuracy': '0', 'alternateranges': {'extreme': None, 'long': None, 'medium': None, 'name': None, 'short': None}, 'ammo': '0', 'ammo_english': '0', 'ap': '-', 'avail': '4E', 'availableammo': '3', 'category': 'Ausrüstung', 'category_english': 'Gear', 'clips': None, 'conceal': '-2', 'cost': newcost, 'currentammo': None, 'damage': 'Chemisch (10m Radius)', 'damage_english': 'Chemical (10m Radius)', 'dicepool': '12', 'fullname': 'Granate: Gas', 'location': None, 'mode': None, 'name': 'Granate: Gas', 'name_english': 'Grenade: Gas', 'owncost': '1', 'page': '437', 'ranges': {'extreme': '19-30', 'long': '13-18', 'medium': '7-12', 'name': 'Standard Granaten', 'short': '0-6'}, 'rawdamage': 'Chemical (10m Radius)', 'rc': '2', 'reach': '0', 'skill': 'throwing Weapons', 'source': 'SR5', 'type': 'Ranged', 'weaponname': None, 'wirelesson': 'False'}]
        elif nam == 'Granate: IR-Rauch':
            return [{'active': 'False', 'armorcapacity': None, 'attack': '0', 'avail': '6E', 'avail_english': '6R', 'bonded': 'False', 'capacity': None, 'category': 'Munition', 'category_english': 'Ammunition', 'children': None, 'conditionmonitor': '8', 'cost': newcost, 'dataprocessing': '0', 'devicerating': '0', 'equipped': 'True', 'extra': None, 'firewall': '0', 'gearname': None, 'homenode': 'False', 'isammo': 'True', 'iscommlink': 'False', 'isos': 'False', 'ispersona': 'False', 'isprogram': 'False', 'issin': 'False', 'location': None, 'matrixcmfilled': '0', 'maxrating': None, 'name': 'Granate: IR-Rauch', 'name_english': 'Grenade: Thermal Smoke', 'owncost': '1', 'page': '437', 'programlimit': '0', 'qty': newqty, 'rating': '0', 'sleaze': '0', 'source': 'SR5', 'wirelesson': 'False'}, {'accuracy': '5', 'alternateranges': {'extreme': None, 'long': None, 'medium': None, 'name': None, 'short': None}, 'ammo': '1', 'ammo_english': '1', 'ap': '-', 'avail': '6E', 'availableammo': '5', 'category': 'Ausrüstung', 'category_english': 'Gear', 'clips': None, 'conceal': '+0', 'cost': newcost, 'currentammo': None, 'damage': ' (10m Radius)', 'damage_english': ' (10m Radius)', 'dicepool': '10', 'fullname': 'Granate: IR-Rauch', 'location': None, 'mode': None, 'name': 'Granate: IR-Rauch', 'name_english': 'Grenade: Thermal Smoke', 'owncost': '1', 'page': '437', 'ranges': {'extreme': '19-30', 'long': '13-18', 'medium': '7-12', 'name': 'Standard Granaten', 'short': '0-6'}, 'rawdamage': '(10m Radius)', 'rc': '2', 'reach': '0', 'skill': 'Throwing Weapons', 'source': 'SR5', 'type': 'Ranged', 'weaponname': None, 'wirelesson': 'False'}]
        elif nam == 'Granate: Rauch':
            return [{'active': 'False', 'armorcapacity': None, 'attack': '0', 'avail': '4E', 'avail_english': '4R', 'bonded': 'False', 'capacity': None, 'category': 'Munition', 'category_english': 'Ammunition', 'children': None, 'conditionmonitor': '8', 'cost': newcost, 'dataprocessing': '0', 'devicerating': '0', 'equipped': 'True', 'extra': None, 'firewall': '0', 'gearname': None, 'homenode': 'False', 'isammo': 'True', 'iscommlink': 'False', 'isos': 'False', 'ispersona': 'False', 'isprogram': 'False', 'issin': 'False', 'location': None, 'matrixcmfilled': '0', 'maxrating': None, 'name': 'Granate: Rauch', 'name_english': 'Grenade: Smoke', 'owncost': '1', 'page': '438', 'programlimit': '0', 'qty': newqty, 'rating': '0', 'sleaze': '0', 'source': 'SR5', 'wirelesson': 'False'}, {'accuracy': '5', 'alternateranges': {'extreme': None, 'long': None, 'medium': None, 'name': None, 'short': None}, 'ammo': '1', 'ammo_english': '1', 'ap': '-', 'avail': '4E', 'availableammo': '5', 'category': 'Ausrüstung', 'category_english': 'Gear', 'clips': None, 'conceal': '+0', 'cost': newcost, 'currentammo': None, 'damage': ' (10m Radius)', 'damage_english': ' (10m Radius)', 'dicepool': '10', 'fullname': 'Granate: Rauch', 'location': None, 'mode': None, 'name': 'Granate: Rauch', 'name_english': 'Grenade: Smoke', 'owncost': '1', 'page': '438', 'ranges': {'extreme': '19-30', 'long': '13-18', 'medium': '7-12', 'name': 'Standard Granaten', 'short': '0-6'}, 'rawdamage': '(10m Radius)', 'rc': '2', 'reach': '0', 'skill': 'Throwing Weapons', 'source': 'SR5', 'type': 'Ranged', 'weaponname': None, 'wirelesson': 'False'}]
        elif nam == 'Granate: Schock':
            return [{'active': 'False', 'armorcapacity': None, 'attack': '0', 'avail': '6E', 'avail_english': '6R', 'bonded': 'False', 'capacity': None, 'category': 'Munition', 'category_english': 'Ammunition', 'children': None, 'conditionmonitor': '8', 'cost': newcost, 'dataprocessing': '0', 'devicerating': '0', 'equipped': 'True', 'extra': None, 'firewall': '0', 'gearname': None, 'homenode': 'False', 'isammo': 'True', 'iscommlink': 'False', 'isos': 'False', 'ispersona': 'False', 'isprogram': 'False', 'issin': 'False', 'location': None, 'matrixcmfilled': '0', 'maxrating': None, 'name': 'Granate: Schock', 'name_english': 'Grenade: Flash-Bang', 'owncost': '1', 'page': '438', 'programlimit': '0', 'qty': newqty, 'rating': '0', 'sleaze': '0', 'source': 'SR5', 'wirelesson': 'False'}, {'accuracy': '5', 'alternateranges': {'extreme': None, 'long': None, 'medium': None, 'name': None, 'short': None}, 'ammo': '1', 'ammo_english': '1', 'ap': '-4', 'avail': '6E', 'availableammo': '5', 'category': 'Ausrüstung', 'category_english': 'Gear', 'clips': None, 'conceal': '+0', 'cost': newcost, 'currentammo': None, 'damage': '10G (10m Radius)', 'damage_english': '10S (10m Radius)', 'dicepool': '10', 'fullname': 'Granate: Schock', 'location': None, 'mode': None, 'name': 'Granate: Schock', 'name_english': 'Grenade: Flash-Bang', 'owncost': '1', 'page': '438', 'ranges': {'extreme': '19-30', 'long': '13-18', 'medium': '7-12', 'name': 'Standard Granaten', 'short': '0-6'}, 'rawdamage': '10S (10m Radius)', 'rc': '2', 'reach': '0', 'skill': 'Throwing Weapons', 'source': 'SR5', 'type': 'Ranged', 'weaponname': None, 'wirelesson': 'False'}]
        elif nam == 'Granate: Splitter':
            return [{'active': 'False', 'armorcapacity': None, 'attack': '0', 'avail': '11V', 'avail_english': '11F', 'bonded': 'False', 'capacity': None, 'category': 'Munition', 'category_english': 'Ammunition', 'children': None, 'conditionmonitor': '8', 'cost': newcost, 'dataprocessing': '0', 'devicerating': '0', 'equipped': 'True', 'extra': None, 'firewall': '0', 'gearname': None, 'homenode': 'False', 'isammo': 'True', 'iscommlink': 'False', 'isos': 'False', 'ispersona': 'False', 'isprogram': 'False', 'issin': 'False', 'location': None, 'matrixcmfilled': '0', 'maxrating': None, 'name': 'Granate: Splitter', 'name_english': 'Grenade: Fragmentation', 'owncost': '1', 'page': '438', 'programlimit': '0', 'qty': newqty, 'rating': '0', 'sleaze': '0', 'source': 'SR5', 'wirelesson': 'False'}, {'accuracy': '5', 'alternateranges': {'extreme': None, 'long': None, 'medium': None, 'name': None, 'short': None}, 'ammo': '1', 'ammo_english': '1', 'ap': '+5', 'avail': '11V', 'availableammo': '5', 'category': 'Ausrüstung', 'category_english': 'Gear', 'clips': None, 'conceal': '+0', 'cost': newcost, 'currentammo': None, 'damage': '18K(f) (-1/M)', 'damage_english': '18P(f) (-1/m)', 'dicepool': '10', 'fullname': 'Granate: Splitter', 'location': None, 'mode': None, 'name': 'Granate: Splitter', 'name_english': 'Grenade: Fragmentation', 'owncost': '1', 'page': '438', 'ranges': {'extreme': '19-30', 'long': '13-18', 'medium': '7-12', 'name': 'Standard Granaten', 'short': '0-6'}, 'rawdamage': '18P(f) (-1/m)', 'rc': '2', 'reach': '0', 'skill': 'Throwing Weapons', 'source': 'SR5', 'type': 'Ranged', 'weaponname': None, 'wirelesson': 'False'}]
        elif nam == 'Granate: Spreng':
            return [{'active': 'False', 'armorcapacity': None, 'attack': '0', 'avail': '11V', 'avail_english': '11F', 'bonded': 'False', 'capacity': None, 'category': 'Munition', 'category_english': 'Ammunition', 'children': None, 'conditionmonitor': '8', 'cost': newcost, 'dataprocessing': '0', 'devicerating': '0', 'equipped': 'True', 'extra': None, 'firewall': '0', 'gearname': None, 'homenode': 'False', 'isammo': 'True', 'iscommlink': 'False', 'isos': 'False', 'ispersona': 'False', 'isprogram': 'False', 'issin': 'False', 'location': None, 'matrixcmfilled': '0', 'maxrating': None, 'name': 'Granate: Spreng', 'name_english': 'Grenade: High Explosive', 'owncost': '1', 'page': '438', 'programlimit': '0', 'qty': newqty, 'rating': '0', 'sleaze': '0', 'source': 'SR5', 'wirelesson': 'False'}, {'accuracy': '5', 'alternateranges': {'extreme': None, 'long': None, 'medium': None, 'name': None, 'short': None}, 'ammo': '1', 'ammo_english': '1', 'ap': '-2', 'avail': '11V', 'availableammo': '5', 'category': 'Ausrüstung', 'category_english': 'Gear', 'clips': None, 'conceal': '+0', 'cost': newcost, 'currentammo': None, 'damage': '16K (-2/M)', 'damage_english': '16P (-2/m)', 'dicepool': '10', 'fullname': 'Granate: Spreng', 'location': None, 'mode': None, 'name': 'Granate: Spreng', 'name_english': 'Grenade: High Explosive', 'owncost': '1', 'page': '438', 'ranges': {'extreme': '19-30', 'long': '13-18', 'medium': '7-12', 'name': 'Standard Granaten', 'short': '0-6'}, 'rawdamage': '16P (-2/m)', 'rc': '2', 'reach': '0', 'skill': 'Throwing Weapons', 'source': 'SR5', 'type': 'Ranged', 'weaponname': None, 'wirelesson': 'False'}]
        ### Minigranaten 
        elif nam == 'Minigranate: Flash-Pack':
            return [{'active': 'False', 'armorcapacity': None, 'attack': '0', 'avail': '4', 'avail_english': '4', 'bonded': 'False', 'capacity': None, 'category': 'Munition', 'category_english': 'Ammunition', 'children': None, 'conditionmonitor': '8', 'cost': newcost, 'dataprocessing': '0', 'devicerating': '0', 'equipped': 'True', 'extra': None, 'firewall': '0', 'gearname': None, 'homenode': 'False', 'isammo': 'True', 'iscommlink': 'False', 'isos': 'False', 'ispersona': 'False', 'isprogram': 'False', 'issin': 'False', 'location': None, 'matrixcmfilled': '0', 'maxrating': None, 'name': 'Minigranate: Flash-Pack', 'name_english': 'Minigrenade: Flash-Pak', 'owncost': '1', 'page': '437', 'programlimit': '0', 'qty': newqty, 'rating': '0', 'sleaze': '0', 'source': 'SR5', 'wirelesson': 'False'}, {'accuracy': '5', 'alternateranges': {'extreme': None, 'long': None, 'medium': None, 'name': None, 'short': None}, 'ammo': '1', 'ammo_english': '1', 'ap': '-', 'avail': '4', 'availableammo': '2,0', 'category': 'Ausrüstung', 'category_english': 'Gear', 'clips': None, 'conceal': '+0', 'cost': newcost, 'currentammo': None, 'damage': 'Spezial', 'damage_english': 'Special', 'dicepool': '10', 'fullname': 'Minigranate: Flash-Pack', 'location': None, 'mode': None, 'name': 'Minigranate: Flash-Pack', 'name_english': 'Minigrenade: Flash-Pak', 'owncost': '1', 'page': '437', 'ranges': {'extreme': '19-30', 'long': '13-18', 'medium': '7-12', 'name': 'Standard Granaten', 'short': '0-6'}, 'rawdamage': 'Special', 'rc': '2', 'reach': '0', 'skill': 'Throwing Weapons', 'source': 'SR5', 'type': 'Ranged', 'weaponname': None, 'wirelesson': 'False'}]
        elif nam == 'Minigranate: Gas':
            return [{'active': 'False', 'armorcapacity': None, 'attack': '0', 'avail': '4E', 'avail_english': '4R', 'bonded': 'False', 'capacity': None, 'category': 'Munition', 'category_english': 'Ammunition', 'children': None, 'conditionmonitor': '8', 'cost': newcost, 'dataprocessing': '0', 'devicerating': '0', 'equipped': 'True', 'extra': None, 'firewall': '0', 'gearname': None, 'homenode': 'False', 'isammo': 'True', 'iscommlink': 'False', 'isos': 'False', 'ispersona': 'False', 'isprogram': 'False', 'issin': 'False', 'location': None, 'matrixcmfilled': '0', 'maxrating': None, 'name': 'Minigranate: Gas', 'name_english': 'Minigrenade: Gas', 'owncost': '1', 'page': '437', 'programlimit': '0', 'qty': newqty, 'rating': '0', 'sleaze': '0', 'source': 'SR5', 'wirelesson': 'False'}, {'accuracy': '0', 'alternateranges': {'extreme': None, 'long': None, 'medium': None, 'name': None, 'short': None}, 'ammo': '0', 'ammo_english': '0', 'ap': '-', 'avail': '4E', 'availableammo': '3', 'category': 'Ausrüstung', 'category_english': 'Gear', 'clips': None, 'conceal': '-2', 'cost': newcost, 'currentammo': None, 'damage': 'Chemisch (10m Radius)', 'damage_english': 'Chemical (10m Radius)', 'dicepool': '12', 'fullname': 'Minigranate: Gas', 'location': None, 'mode': None, 'name': 'Minigranate: Gas', 'name_english': 'Minigrenade: Gas', 'owncost': '1', 'page': '437', 'ranges': {'extreme': '19-30', 'long': '13-18', 'medium': '7-12', 'name': 'Standard Granaten', 'short': '0-6'}, 'rawdamage': 'Chemical (10m Radius)', 'rc': '2', 'reach': '0', 'skill': 'throwing Weapons', 'source': 'SR5', 'type': 'Ranged', 'weaponname': None, 'wirelesson': 'False'}]
        elif nam == 'Minigranate: IR-Rauch':
            return [{'active': 'False', 'armorcapacity': None, 'attack': '0', 'avail': '6E', 'avail_english': '6R', 'bonded': 'False', 'capacity': None, 'category': 'Munition', 'category_english': 'Ammunition', 'children': None, 'conditionmonitor': '8', 'cost': newcost, 'dataprocessing': '0', 'devicerating': '0', 'equipped': 'True', 'extra': None, 'firewall': '0', 'gearname': None, 'homenode': 'False', 'isammo': 'True', 'iscommlink': 'False', 'isos': 'False', 'ispersona': 'False', 'isprogram': 'False', 'issin': 'False', 'location': None, 'matrixcmfilled': '0', 'maxrating': None, 'name': 'Minigranate: IR-Rauch', 'name_english': 'Minigrenade: Thermal Smoke', 'owncost': '1', 'page': '437', 'programlimit': '0', 'qty': newqty, 'rating': '0', 'sleaze': '0', 'source': 'SR5', 'wirelesson': 'False'}, {'accuracy': '5', 'alternateranges': {'extreme': None, 'long': None, 'medium': None, 'name': None, 'short': None}, 'ammo': '1', 'ammo_english': '1', 'ap': '-', 'avail': '6E', 'availableammo': '5', 'category': 'Ausrüstung', 'category_english': 'Gear', 'clips': None, 'conceal': '+0', 'cost': newcost, 'currentammo': None, 'damage': ' (10m Radius)', 'damage_english': ' (10m Radius)', 'dicepool': '10', 'fullname': 'Minigranate: IR-Rauch', 'location': None, 'mode': None, 'name': 'Minigranate: IR-Rauch', 'name_english': 'Minigrenade: Thermal Smoke', 'owncost': '1', 'page': '437', 'ranges': {'extreme': '19-30', 'long': '13-18', 'medium': '7-12', 'name': 'Standard Granaten', 'short': '0-6'}, 'rawdamage': '(10m Radius)', 'rc': '2', 'reach': '0', 'skill': 'Throwing Weapons', 'source': 'SR5', 'type': 'Ranged', 'weaponname': None, 'wirelesson': 'False'}]
        elif nam == 'Minigranate: Rauch':
            return [{'active': 'False', 'armorcapacity': None, 'attack': '0', 'avail': '4E', 'avail_english': '4R', 'bonded': 'False', 'capacity': None, 'category': 'Munition', 'category_english': 'Ammunition', 'children': None, 'conditionmonitor': '8', 'cost': newcost, 'dataprocessing': '0', 'devicerating': '0', 'equipped': 'True', 'extra': None, 'firewall': '0', 'gearname': None, 'homenode': 'False', 'isammo': 'True', 'iscommlink': 'False', 'isos': 'False', 'ispersona': 'False', 'isprogram': 'False', 'issin': 'False', 'location': None, 'matrixcmfilled': '0', 'maxrating': None, 'name': 'Minigranate: Rauch', 'name_english': 'Minigrenade: Smoke', 'owncost': '1', 'page': '438', 'programlimit': '0', 'qty': newqty, 'rating': '0', 'sleaze': '0', 'source': 'SR5', 'wirelesson': 'False'}, {'accuracy': '5', 'alternateranges': {'extreme': None, 'long': None, 'medium': None, 'name': None, 'short': None}, 'ammo': '1', 'ammo_english': '1', 'ap': '-', 'avail': '4E', 'availableammo': '5', 'category': 'Ausrüstung', 'category_english': 'Gear', 'clips': None, 'conceal': '+0', 'cost': newcost, 'currentammo': None, 'damage': ' (10m Radius)', 'damage_english': ' (10m Radius)', 'dicepool': '10', 'fullname': 'Minigranate: Rauch', 'location': None, 'mode': None, 'name': 'Minigranate: Rauch', 'name_english': 'Minigrenade: Smoke', 'owncost': '1', 'page': '438', 'ranges': {'extreme': '19-30', 'long': '13-18', 'medium': '7-12', 'name': 'Standard Granaten', 'short': '0-6'}, 'rawdamage': '(10m Radius)', 'rc': '2', 'reach': '0', 'skill': 'Throwing Weapons', 'source': 'SR5', 'type': 'Ranged', 'weaponname': None, 'wirelesson': 'False'}]
        elif nam == 'Minigranate: Schock':
            return [{'active': 'False', 'armorcapacity': None, 'attack': '0', 'avail': '6E', 'avail_english': '6R', 'bonded': 'False', 'capacity': None, 'category': 'Munition', 'category_english': 'Ammunition', 'children': None, 'conditionmonitor': '8', 'cost': newcost, 'dataprocessing': '0', 'devicerating': '0', 'equipped': 'True', 'extra': None, 'firewall': '0', 'gearname': None, 'homenode': 'False', 'isammo': 'True', 'iscommlink': 'False', 'isos': 'False', 'ispersona': 'False', 'isprogram': 'False', 'issin': 'False', 'location': None, 'matrixcmfilled': '0', 'maxrating': None, 'name': 'Minigranate: Schock', 'name_english': 'Minigrenade: Flash-Bang', 'owncost': '1', 'page': '438', 'programlimit': '0', 'qty': newqty, 'rating': '0', 'sleaze': '0', 'source': 'SR5', 'wirelesson': 'False'}, {'accuracy': '5', 'alternateranges': {'extreme': None, 'long': None, 'medium': None, 'name': None, 'short': None}, 'ammo': '1', 'ammo_english': '1', 'ap': '-4', 'avail': '6E', 'availableammo': '5', 'category': 'Ausrüstung', 'category_english': 'Gear', 'clips': None, 'conceal': '+0', 'cost': newcost, 'currentammo': None, 'damage': '10G (10m Radius)', 'damage_english': '10S (10m Radius)', 'dicepool': '10', 'fullname': 'Minigranate: Schock', 'location': None, 'mode': None, 'name': 'Minigranate: Schock', 'name_english': 'Minigrenade: Flash-Bang', 'owncost': '1', 'page': '438', 'ranges': {'extreme': '19-30', 'long': '13-18', 'medium': '7-12', 'name': 'Standard Granaten', 'short': '0-6'}, 'rawdamage': '10S (10m Radius)', 'rc': '2', 'reach': '0', 'skill': 'Throwing Weapons', 'source': 'SR5', 'type': 'Ranged', 'weaponname': None, 'wirelesson': 'False'}]
        elif nam == 'Minigranate: Splitter':
            return [{'active': 'False', 'armorcapacity': None, 'attack': '0', 'avail': '11V', 'avail_english': '11F', 'bonded': 'False', 'capacity': None, 'category': 'Munition', 'category_english': 'Ammunition', 'children': None, 'conditionmonitor': '8', 'cost': newcost, 'dataprocessing': '0', 'devicerating': '0', 'equipped': 'True', 'extra': None, 'firewall': '0', 'gearname': None, 'homenode': 'False', 'isammo': 'True', 'iscommlink': 'False', 'isos': 'False', 'ispersona': 'False', 'isprogram': 'False', 'issin': 'False', 'location': None, 'matrixcmfilled': '0', 'maxrating': None, 'name': 'Minigranate: Splitter', 'name_english': 'Minigrenade: Fragmentation', 'owncost': '1', 'page': '438', 'programlimit': '0', 'qty': newqty, 'rating': '0', 'sleaze': '0', 'source': 'SR5', 'wirelesson': 'False'}, {'accuracy': '5', 'alternateranges': {'extreme': None, 'long': None, 'medium': None, 'name': None, 'short': None}, 'ammo': '1', 'ammo_english': '1', 'ap': '+5', 'avail': '11V', 'availableammo': '5', 'category': 'Ausrüstung', 'category_english': 'Gear', 'clips': None, 'conceal': '+0', 'cost': newcost, 'currentammo': None, 'damage': '18K(f) (-1/M)', 'damage_english': '18P(f) (-1/m)', 'dicepool': '10', 'fullname': 'Minigranate: Splitter', 'location': None, 'mode': None, 'name': 'Minigranate: Splitter', 'name_english': 'Minigrenade: Fragmentation', 'owncost': '1', 'page': '438', 'ranges': {'extreme': '19-30', 'long': '13-18', 'medium': '7-12', 'name': 'Standard Granaten', 'short': '0-6'}, 'rawdamage': '18P(f) (-1/m)', 'rc': '2', 'reach': '0', 'skill': 'Throwing Weapons', 'source': 'SR5', 'type': 'Ranged', 'weaponname': None, 'wirelesson': 'False'}]
        elif nam == 'Minigranate: Spreng':
            return [{'active': 'False', 'armorcapacity': None, 'attack': '0', 'avail': '11V', 'avail_english': '11F', 'bonded': 'False', 'capacity': None, 'category': 'Munition', 'category_english': 'Ammunition', 'children': None, 'conditionmonitor': '8', 'cost': newcost, 'dataprocessing': '0', 'devicerating': '0', 'equipped': 'True', 'extra': None, 'firewall': '0', 'gearname': None, 'homenode': 'False', 'isammo': 'True', 'iscommlink': 'False', 'isos': 'False', 'ispersona': 'False', 'isprogram': 'False', 'issin': 'False', 'location': None, 'matrixcmfilled': '0', 'maxrating': None, 'name': 'Minigranate: Spreng', 'name_english': 'Minigrenade: High Explosive', 'owncost': '1', 'page': '438', 'programlimit': '0', 'qty': newqty, 'rating': '0', 'sleaze': '0', 'source': 'SR5', 'wirelesson': 'False'}, {'accuracy': '5', 'alternateranges': {'extreme': None, 'long': None, 'medium': None, 'name': None, 'short': None}, 'ammo': '1', 'ammo_english': '1', 'ap': '-2', 'avail': '11V', 'availableammo': '5', 'category': 'Ausrüstung', 'category_english': 'Gear', 'clips': None, 'conceal': '+0', 'cost': newcost, 'currentammo': None, 'damage': '16K (-2/M)', 'damage_english': '16P (-2/m)', 'dicepool': '10', 'fullname': 'Minigranate: Spreng', 'location': None, 'mode': None, 'name': 'Minigranate: Spreng', 'name_english': 'Minigrenade: High Explosive', 'owncost': '1', 'page': '438', 'ranges': {'extreme': '19-30', 'long': '13-18', 'medium': '7-12', 'name': 'Standard Granaten', 'short': '0-6'}, 'rawdamage': '16P (-2/m)', 'rc': '2', 'reach': '0', 'skill': 'Throwing Weapons', 'source': 'SR5', 'type': 'Ranged', 'weaponname': None, 'wirelesson': 'False'}]
         

    def kaufaction(nam,neuemun):
        x = character['gears']['gear']
        for i,n in enumerate(x):
            if x[i]['name'].find(nam) != -1 and x[i]['extra'] == neuemun[1]:
                xnum = i
        if 'xnum' in locals():
            cost = x[xnum]['cost']
            qty = x[xnum]['qty']
            newcost = str(neuemun[2] + float(cost.replace('.','').replace(',','.')))
            newqty = str(int(neuemun[0]) + int(qty))
            newwt = neuemun[1]
            x[xnum] = muntojson(nam,newcost,newqty,newwt)
        else:
            newcost = str(neuemun[2])
            newqty = neuemun[0]
            newwt = neuemun[1]
            x.append(muntojson(nam,newcost,newqty,newwt))

    def kaufregeln():
        clscrn()
        headerprnt()
        print(bcolors.IND + bcolors.UNDERLINE + 'Kaufregeln:' + bcolors.ENDC + 'SR5 418\n'.rjust(50))
        print(bcolors.IND + 'Standardwaren: \tohne Verfügbarkeitswert, überall zu bekommen, gebunden an SIN beim Kaufen.')
        print(bcolors.IND + 'Schwarzmarktwaren: \t(e) Eingeschränkt oder (v) Verbotene Ware\n')
        print(bcolors.IND + ' \tVerfügbarkeitsprobe: ' + bcolors.GREENh + 'Verhandlung + CHA' + bcolors.ENDC + ' [sozial] gegen ' + bcolors.FAILh + 'Verfügbarkeitswert des Gegenstandes' + bcolors.ENDC + '\n')
        print(bcolors.IND + ' \tWenn die Probe erfolgreich, dann Gegenstand zu angegebener Lieferzeit.')
        print(bcolors.IND + ' \tBei Patt: Doppelte Lieferzeit.')
        print(bcolors.IND + ' \tBei Misslingen: Neuer Versuch nach Wartezeit von doppelter Lieferzeit.')
        print(bcolors.IND + ' \tGeld löst alle Probleme: ' + bcolors.GREENh + '1 Extrawürfel für 25% Mehrkosten' + bcolors.ENDC + '. (max. 12 Würfel)')
        print(bcolors.IND + ' \t' + bcolors.FAILh + 'Patzer' + bcolors.ENDC + ': \t   Unerwünschte Aufmerksamkeit (Undercover-Star, rivalisierende Gang)')
        print(bcolors.IND + ' \t' + bcolors.FAILh + 'Kritischer Patzer' + bcolors.ENDC + ': Extremste Situation, Gegenstand nicht verfügbar.\n')
        print(bcolors.IND + bcolors.UNDERLINE + 'Connections' + bcolors.ENDC)
        print(bcolors.IND + ' Schieber, Taliskrämer, Deckmeister .. können Gegenstand finden')
        print(bcolors.IND + ' Ihr Verhandeln + CHA und Extrawürfel in Höhe von Einflussstufe.\n')
        print(bcolors.IND + bcolors.UNDERLINE + 'Ausrüstungspreis'.ljust(20) + 5*' ' + 'Lieferzeit'.center(15) + bcolors.ENDC)
        print(bcolors.IND + ' bis 100'.ljust(20) + 5*' ' + '6 Stunden'.center(15))
        print(bcolors.IND + ' 101 bis 1.000'.ljust(20) + 5*' ' + '1 Tag'.center(15))
        print(bcolors.IND + ' 1.001 bis 10.000'.ljust(20) + 5*' ' + '2 Tage'.center(15))
        print(bcolors.IND + ' 10.001 bis 100.000'.ljust(20) + 5*' ' + '1 Woche'.center(15))
        print(bcolors.IND + ' Mehr als 100.000'.ljust(20) + 5*' ' + '1 Monat'.center(15))
        print('')
        print(bcolors.IND + bcolors.UNDERLINE + 'Ausrüstung verkaufen'+ bcolors.ENDC)
        print(bcolors.IND + ' Je höher die Verfügbarkeit desto höher die Chance des Verkaufs.')
        print(bcolors.IND + bcolors.BLUEh + ' Zuerst' + bcolors.ENDC + ': Käufer finden: Ausgedehnte Probe auf ' + bcolors.GREENh + 'Gebräuche + CHA' + bcolors.ENDC + ' [sozial] (10, Lieferzeit)')
        print(bcolors.IND + bcolors.BLUEh + ' Dann' + bcolors.ENDC + ': vergleichende Probe auf ' + bcolors.GREENh + 'Verhandeln + CHA' + bcolors.ENDC + ' [sozial]')
        print(bcolors.IND + ' Käufer bietet 25% des Listenpreises. Jeder Nettoerfolg: ' + bcolors.GREENh + '+5%' + bcolors.ENDC)
        print(bcolors.IND + ' \t\t\t   Jeder Nettoerfolg des Käufers: ' + bcolors.FAILh + '-5%' + bcolors.ENDC)
        print(bcolors.IND + ' ' + bcolors.UNDERLINE + 'Connections:' + bcolors.ENDC)
        print(bcolors.IND + '  Nehmen die Ware sofort. Zahlen ' + bcolors.GREENh + '5% x Loyalitätsstufe' + bcolors.ENDC)
        print('')
        liner()
        ch = input(' >> ')

    while funbreak < 1:
        clscrn()
        headerprnt()
        print(bcolors.IND + 'Was soll gekauft werden?\n')
        print(bcolors.IND + bcolors.BLUEh + ' r' + bcolors.ENDC + ') Kaufregeln \t[SR5 418]\n')
        print(bcolors.IND + bcolors.BLUEh + ' 1' + bcolors.ENDC + ') Munition\n')
        print(bcolors.IND + bcolors.BLUEh + ' 2' + bcolors.ENDC + ') Medizin\n')
        print(bcolors.IND + bcolors.BLUEh + ' 3' + bcolors.ENDC + ') Drogen\n')
        print(bcolors.IND + bcolors.BLUEh + ' q' + bcolors.ENDC + ') Beenden\n')
        print('')
        liner()
        choice = input(bcolors.GREENh + ' >> ' + bcolors.ENDC)
        if choice.lower() == 'q':
            funbreak = 1
        if choice.lower() == 'r':
            kaufregeln()
        if choice == '1':
            funfunbreak = 0
            while funfunbreak < 1:
                clscrn()
                headerprnt()
                print(bcolors.IND + 'Welche Munition soll gekauft werden?\t[SR5 436]\n')
                print(bcolors.IND + bcolors.UNDERLINE + 4*' ' + ('Munition (' + bcolors.GREENh + '10 Schuss' + bcolors.ENDC + bcolors.UNDERLINE + ')').ljust(25) + 10*' ' + 'Schaden' + 5*' ' + 'DK' + 5*' ' + 'Verfügbarkeit' + 5*' ' + 'Preis  ' + bcolors.ENDC + '\n')
                print(bcolors.IND + bcolors.BLUEh + ' 1' + bcolors.ENDC + ') ' + 'APDS'.ljust(25) + 5*' ' + '-'.center(7) + 5*' ' + '-4' + 5*' ' + '12V'.center(13) + 5*' ' + '120'.center(5) + bcolors.ENDC)
                print(bcolors.IND + bcolors.BLUEh + ' 2' + bcolors.ENDC + ') ' + 'DMSO-Gelpacks'.ljust(25) + 5*' ' + '-'.center(7) + 5*' ' + ' -' + 5*' ' + '2E'.center(13) + 5*' ' + '20'.center(5) + bcolors.ENDC)
                print(bcolors.IND + bcolors.BLUEh + ' 3' + bcolors.ENDC + ') ' + 'Explosivmunition'.ljust(25) + 5*' ' + '+1'.center(7) + 5*' ' + '-1' + 5*' ' + '9V'.center(13) + 5*' ' + '80'.center(5) + bcolors.ENDC)
                print(bcolors.IND + bcolors.BLUEh + ' 4' + bcolors.ENDC + ') ' + 'Flechettemunition'.ljust(25) + 5*' ' + '+2'.center(7) + 5*' ' + '+5' + 5*' ' + '6E'.center(13) + 5*' ' + '65'.center(5) + bcolors.ENDC)
                print(bcolors.IND + bcolors.BLUEh + ' 5' + bcolors.ENDC + ') ' + 'Gelmunition'.ljust(25) + 5*' ' + '+0G'.center(7) + 5*' ' + '+1' + 5*' ' + '2E'.center(13) + 5*' ' + '25'.center(5) + bcolors.ENDC)
                print(bcolors.IND + bcolors.BLUEh + ' 6' + bcolors.ENDC + ') ' + 'Hohlspitzmunition'.ljust(25) + 5*' ' + '+1'.center(7) + 5*' ' + '+2' + 5*' ' + '4V'.center(13) + 5*' ' + '70'.center(5) + bcolors.ENDC)
                print(bcolors.IND + bcolors.BLUEh + ' 7' + bcolors.ENDC + ') ' + 'Injektionspfeile'.ljust(25) + 5*' ' + '-'.center(7) + 5*' ' + ' -' + 5*' ' + '4E'.center(13) + 5*' ' + '75'.center(5) + bcolors.ENDC)
                print(bcolors.IND + bcolors.BLUEh + ' 8' + bcolors.ENDC + ') ' + 'Leuchtspurmunition'.ljust(25) + 5*' ' + '-'.center(7) + 5*' ' + ' -' + 5*' ' + '6E'.center(13) + 5*' ' + '60'.center(5) + bcolors.ENDC)
                print(bcolors.IND + bcolors.BLUEh + ' 9' + bcolors.ENDC + ') ' + 'Schockermunition'.ljust(25) + 5*' ' + '-2G(e)'.center(7) + 4*' ' + '[-5]' + 4*' ' + '6E'.center(13) + 5*' ' + '80'.center(5) + bcolors.ENDC)
                print(bcolors.IND + bcolors.BLUEh + '10' + bcolors.ENDC + ') ' + 'Standardmunition'.ljust(25) + 5*' ' + '-'.center(7) + 5*' ' + ' -' + 5*' ' + '2E'.center(13) + 5*' ' + '20'.center(5) + bcolors.ENDC)
                print(bcolors.IND + bcolors.BLUEh + '11' + bcolors.ENDC + ') ' + 'Sturmkanonenmunition'.ljust(25) + 5*' ' + '-'.center(7) + 5*' ' + ' -' + 5*' ' + '12V'.center(13) + 5*' ' + '400'.center(5) + bcolors.ENDC)
                print(bcolors.IND + bcolors.BLUEh + '12' + bcolors.ENDC + ') ' + 'Taserpfeile'.ljust(25) + 5*' ' + '-'.center(7) + 5*' ' + ' -' + 5*' ' + '3'.center(13) + 5*' ' + ' 50\n'.center(5) + bcolors.ENDC)
                print(bcolors.IND + bcolors.BLUEh + ' g' + bcolors.ENDC + ') ' + 'Granaten und Raketen\n'.ljust(25))
                print(bcolors.IND + bcolors.BLUEh + ' q' + bcolors.ENDC + ') ' + 'Beenden\n'.ljust(25))
                liner()
                ch = input(bcolors.GREENh + ' >> ' + bcolors.ENDC)
                ### KAUFEN.MUNITION
                if ch.lower() == 'q':
                    funfunbreak = 1
                elif ch.lower() == 'g':
                    clscrn()
                    headerprnt()
                    print(bcolors.IND + 'Granaten')
                    chh = input(bcolors.GREENh + ' >> ' + bcolors.ENDC)
                    funfunbreak = 1
                elif ch == '1':
                    nam = 'APDS'
                    neuemun = mengek(nam,'12')
                    clscrn()
                    headerprnt()
                    if neuemun == ['','','']:
                        print('\n' + bcolors.IND + ' Es wurde ' + bcolors.FAILh + 'keine' + bcolors.ENDC + ' Munition gekauft.')
                    else:
                        print('\n' + bcolors.IND + bcolors.GREENh + neuemun[0] + bcolors.ENDC + ' x ' + bcolors.GREENh + nam + bcolors.ENDC + ' für ' + neuemun[1] + ' wurde für ' + bcolors.WARNINGh + str(neuemun[2]) + bcolors.ENDC + ' Nuyen gekauft.')
                        kaufaction('APDS',neuemun)
                    print('')
                    liner()
                    bla = input(bcolors.GREENh + ' >> ' + bcolors.ENDC)
                    funfunbreak = 1

    main_menu()


### EQUIP
def equip():
    headerprnt()
    def sub_line():
        print('\n' + 60*'_' + '\n')
    def getammo(strng):
        oi = ""
        for s in strng:
            if s.isdigit() == True:
                oi += s
        return int(oi)
    funbreak = 0
    n_lst = 0
    global smrtlnk, smrtlnktype, isastral, waffeAusgewaehlt, gearAusgewaehlt, troden, contacts, glasses, ammocnt
    while funbreak < 1:
        clscrn()
        headerprnt()
        print(bcolors.IND + 'Was soll ausgerüstet werden?')
        print('\n\t\t' + bcolors.IND + "'" + bcolors.BLUE + 'w' + bcolors.ENDC + "' Waffe")
        print('\t\t' + bcolors.IND + "'" + bcolors.BLUE + 'p' + bcolors.ENDC + "' Panzerung")
        print('\t\t' + bcolors.IND + "'" + bcolors.BLUE + 's' + bcolors.ENDC + "' Smartlink")
        print('\t\t' + bcolors.IND + "'" + bcolors.BLUE + 'a' + bcolors.ENDC + "' Ausrüstung")
        print('\t\t' + bcolors.IND + "'" + bcolors.BLUE + 'q' + bcolors.ENDC + "' Beenden")
        sub_line()
        ch = input(' >>> ')
        if ch.lower() == 'w':
            clscrn()
            headerprnt()
            print(bcolors.IND + bcolors.BOLD + 'Welche Waffe soll ausgerüstet werden?\n' + bcolors.ENDC)
            x = character['weapons']['weapon']
            y = character['gears']['gear']
            skll_astralkampf = character['skills']['skill'][5]['total']
            txtwdth = 160
            for i,n in enumerate(x):
                flg = -1 
                n_lst = i
                for k,nam in enumerate(y):
                    if x[i]['fullname'] == str(y[k]['gearname']) and y[k]['category'] == 'Foki':
                        flg = k
                if flg > -1:
                    print(bcolors.IND + bcolors.GREEN + bcolors.BOLD + str(i+1) + bcolors.ENDC + ')  ' + bcolors.WARNINGh + ('{fullname:40}'.format(**x[i]) + bcolors.ENDC + ' ({category})'.format(**y[flg])).ljust(80) + (' DMG: [{damage:^5}] {rawdamage:8}  DK: {ap:3} Präz: {accuracy:6}  Verstecken: {conceal}  Würfel: {dicepool:>2}'.format(**x[i]) + bcolors.WARNINGh +'+{rating}'.format(**y[flg]) + bcolors.ENDC + bcolors.ASTRALh + ' (' + str(skll_astralkampf) + bcolors.WARNINGh +'+{rating}'.format(**y[flg]) + bcolors.ASTRALh + ')' + bcolors.ENDC).ljust(txtwdth-74) + '\t{source:3} {page}'.format(**x[i]), end='')
                    print(bcolors.ENDC)
                elif x[i]['type'] == 'Ranged' and x[i]['category'] == 'Ausrüstung' and x[i]['name'].find('Minigranate') == -1 and isastral == False:
                    print((bcolors.IND + bcolors.GREEN + bcolors.BOLD + str(i+1) + bcolors.ENDC + ')  ' + bcolors.FAILh + '{fullname:40} DMG: [{damage:^21}] DK: {ap:3}  Verstecken: {conceal}  Würfel: {dicepool}'.format(**x[i])).ljust(txtwdth) + bcolors.ENDC + '\t{source:3} {page}'.format(**x[i]))
                else:
                    if isastral == False or x[i]['fullname'] == 'Waffenlos':
                        if x[i]['name'].find('Cyber') != -1:
                            print(bcolors.IND + bcolors.GREEN + bcolors.BOLD + str(i+1) + bcolors.ENDC + ')  ' + bcolors.PNZRGh + ('{fullname!s:40}'.format(**x[i]) + bcolors.ENDC + ' ({category})'.format(**x[i])).ljust(76) + (' DMG: [{damage!s:^5}] {rawdamage!s:8}  DK: {ap!s:3} Präz: {accuracy!s:6}  Verstecken: {conceal!s}  Würfel: {dicepool!s:>2}'.format(**x[i])).ljust(txtwdth-74) + '\t{source:3} {page}'.format(**x[i]))
                        else:
                            if x[i]['category'] != 'Ausrüstung':
                                print(bcolors.IND + bcolors.GREEN + bcolors.BOLD + str(i+1) + bcolors.ENDC + ')  ' + '{fullname!s:40} ({category})'.format(**x[i]).ljust(76) + (' DMG: [{damage!s:^5}] {rawdamage!s:8}  DK: {ap!s:3} Präz: {accuracy!s:6}  Verstecken: {conceal!s}  Würfel: {dicepool!s:>2}'.format(**x[i])).ljust(txtwdth-74) + '\t{source:3} {page}'.format(**x[i]))
                if x[i]['type'] == 'Ranged' and x[i]['category'] != 'Ausrüstung' and isastral == False:
                    print('\t\t\t\t\t' + bcolors.IND + ' Mun: {ammo!s:11}\tModi: {mode!s:10}\tRückstoß: {rc!s}'.format(**x[i]) + '\tReichweiten: k({short}) m({medium}) l({long}) e({extreme})'.format(**x[i]['ranges']))
                    if 'accessories' in x[i] and x[i]['accessories'] != None:
                        if type(x[i]['accessories']['accessory']) is dict:
                            if x[i]['accessories']['accessory']["name"].find('Smartgunsystem') != -1:
                                print(bcolors.IND +  bcolors.BLUEh + '\t+ ' + bcolors.WARNING + x[i]['accessories']['accessory']["name"], bcolors.ENDC)
                            else:
                                print(bcolors.IND +  bcolors.BLUEh + '\t+ ' + x[i]['accessories']['accessory']["name"], bcolors.ENDC)
                        else:
                            for num in range(len(x[i]['accessories']['accessory'])): 
                                if x[i]['accessories']['accessory'][num]["name"].find('Smartgunsystem') != -1:
                                    print(bcolors.IND +  bcolors.BLUEh + '\t+ ' + bcolors.WARNING + x[i]['accessories']['accessory'][num]["name"], bcolors.ENDC, end='')
                                else:
                                    print(bcolors.IND +  bcolors.BLUEh + '\t+ ' + x[i]['accessories']['accessory'][num]["name"] + bcolors.ENDC + '\t', end='')
                                if (num+1)%4 == 0 and (num+1) < len(x[i]['accessories']['accessory']):
                                    print('')
                            print('')
                if x[i]['type'] == 'Ranged' and isastral == False and 'underbarrel' in x[i] and x[i]['underbarrel'] != None:
                    print('')
                    print(bcolors.IND + bcolors.GREEN + bcolors.BOLD + 'u' + str(i+1) + bcolors.ENDC + ')  ' + bcolors.PNZRG + ' U:  ' + bcolors.ENDC + '{fullname!s:40} ({category})'.format(**x[i]['underbarrel']['weapon']).ljust(60) + bcolors.ENDC + (' DMG: [{damage!s:^5}] {rawdamage!s:8}  DK: {ap!s:3} Präz: {accuracy!s:6}  Verstecken: {conceal!s}  Würfel: {dicepool!s:>2}'.format(**x[i]['underbarrel']['weapon'])).ljust(txtwdth-74) + '\t{source:3} {page}'.format(**x[i]['underbarrel']['weapon']))
                if x[i]['name'].find('Minigranate') == -1: 
                    print('')
            sub_line()
            s = input(' >>> ')
            if s == 'q':
                break
            elif len(s) > 0 and s[0] == 'u' and s[1:].isdigit() and int(s[1:]) > 0 and int(s[1:]) <= n_lst+1:
                sin = int(s[1:]) - 1
                if x[sin]['type'] == 'Ranged' and x[sin]['category'] != 'Ausrüstung':
                    clscrn()
                    headerprnt()
                    chlist = []
                    n_ch = 0
                    print(bcolors.IND + bcolors.BOLD + 'Welche Munition soll ausgerüstet werden?\n' + bcolors.ENDC)
                    if x[sin]['underbarrel']['weapon']['damage'] == 'Granate':
                        for i,n in enumerate(x):
                            for k,m in enumerate(y):
                                if x[i]['name'].find('Minigranate') != -1 and x[i]['name'] == y[k]['name']: ###HIERMARKER
                                    chlist.append(i)
                                    n_ch += 1 
                                    print((bcolors.IND + bcolors.GREEN + bcolors.BOLD + str(n_ch) + bcolors.ENDC + ')  ' + '{qty:>5} x {name:40}'.format(**y[k]) + ' [ DMG: {damage} | DK: {ap} ]'.format(**x[i])).ljust(txtwdth) + 'Kosten: {cost:>7}\t\t{source:3} {page}'.format(**y[k]))
                                    print('')
                    elif y[i]['extra'] == 'Schrotflinten' and x[sin]['underbarrel']['weapon']['range']['name'] == 'Schrotflinten': ###HIERMARKER
                        for i,n in enumerate(y):
                            chlist.append(i)
                            n_ch += 1 
                            if 'weaponbonusdamage' in y[i].keys():
                                print((bcolors.IND + bcolors.GREEN + bcolors.BOLD + str(n_ch) + bcolors.ENDC + ')  ' + '{qty:>5} x {name:40} [ DMG: {weaponbonusdamage} | DK: {weaponbonusap} ] für: {extra}'.format(**y[i])).ljust(txtwdth) + 'Kosten: {cost:>7}\t\t{source:3} {page}'.format(**y[i]))
                            else:
                                print((bcolors.IND + bcolors.GREEN + bcolors.BOLD + str(n_ch) + bcolors.ENDC + ')  ' + '{qty:>5} x {name:40} {leer: <21} für: {extra}'.format(**y[i], leer=' ')).ljust(txtwdth) + 'Kosten: {cost:>7}\t\t{source:3} {page}'.format(**y[i]))
                            print('')
                    sub_line()
                    b = input(' >>> ')
                    if b == 'q':
                        break
                    elif b.isdigit() and int(b) > 0 and int(b) <= n_ch:
                        bint = chlist[int(b)-1]
                        if 'weaponbonusdamage' in y[bint].keys():
                            wbd = y[bint]['weaponbonusdamage']
                            wba = y[bint]['weaponbonusap']
                        else:
                            wbd = ''
                            wba = ''
                            smtl = ''
                        if 'accessories' in x[sin] and x[sin]['accessories']['accessory'] is dict:
                            if x[sin]['accessories']['accessory']['name'].find('Smartgunsystem') != -1:
                                if smrtlnktype == 'cyberware':
                                    smtl = '+2'
                                elif smrtlnktype == 'extern':
                                    smtl = '+1'
                        elif 'accessories' in x[sin]:
                            for num in range(len(x[sin]['accessories']['accessory'])):
                                if x[sin]['accessories']['accessory'][num]['name'].find('Smartgunsystem') != -1:
                                    if smrtlnktype == 'cyberware':
                                        smtl = '+2' 
                                    elif smrtlnktype == 'extern':
                                        smtl = '+1'
               ####2MARK
                        if int(y[bint]['qty']) >= getammo(x[sin]['underbarrel']['weapon']['ammo']):
                            ammocnt = getammo(x[sin]['underbarrel']['weapon']['ammo'])
                        else:
                            ammocnt = int(y[bint]['qty'])
                        if x[sin]['underbarrel']['weapon']['damage'] == 'Granate':
                            del waffeAusgewaehlt
                            waffeAusgewaehlt = [' ']
                            #waffeAusgewaehlt[0] = str(x[sin]['underbarrel']['weapon']['fullname'] + ' (' + bcolors.GREENh + x[bint]['name'] + bcolors.ENDC + ') DMG:' + x[bint]['damage'] +' DK:' + x[bint]['ap'] + ' ' + x[sin]['underbarrel']['weapon']['ammo'] + ' ' + x[sin]['underbarrel']['weapon']['mode'] + ' RS:' + x[sin]['underbarrel']['weapon']['rc'] + ' Würfel:' + x[sin]['underbarrel']['weapon']['dicepool'])
                            waffeAusgewaehlt[0] = x[sin]['underbarrel']['weapon']['fullname']
                            waffeAusgewaehlt.append(x[bint]['name'])
                            waffeAusgewaehlt.append(str(bcolors.BLACK + bcolors.BGW + smtl + bcolors.ENDC))
                            waffeAusgewaehlt.append(str('DMG:' + x[bint]['damage'] +' DK:' + x[bint]['ap'] + ' ' + x[sin]['underbarrel']['weapon']['ammo'] + ' ' + x[sin]['underbarrel']['weapon']['mode'] + ' RS:' + x[sin]['underbarrel']['weapon']['rc'] + ' Würfel:' + x[sin]['underbarrel']['weapon']['dicepool']))
                            waffeAusgewaehlt.append(str(' [' + x[sin]['underbarrel']['weapon']['accuracy'] + ']'))
                            waffeAusgewaehlt.append(x[sin]['underbarrel']['weapon']['category'])
                        else:
                            del waffeAusgewaehlt
                            waffeAusgewaehlt = [' ']
                            #waffeAusgewaehlt[0] = str(x[sin]['underbarrel']['weapon']['fullname'] + ' (' + bcolors.GREENh + y[bint]['name'] + bcolors.ENDC + ') DMG:' + x[sin]['underbarrel']['weapon']['damage'] + bcolors.WARNINGh + wbd + bcolors.ENDC +' DK:' + x[sin]['underbarrel']['weapon']['ap'] + bcolors.WARNINGh + wba + bcolors.ENDC + ' ' + x[sin]['underbarrel']['weapon']['ammo'] + ' ' + x[sin]['underbarrel']['weapon']['mode'] + ' RS:' + x[sin]['underbarrel']['weapon']['rc'] + ' Würfel:' + x[sin]['underbarrel']['weapon']['dicepool'])
                            waffeAusgewaehlt[0] = x[sin]['underbarrel']['weapon']['fullname']
                            waffeAusgewaehlt.append(y[bint]['name'])
                            waffeAusgewaehlt.append(str(bcolors.BLACK + bcolors.BGW + smtl + bcolors.ENDC))
                            waffeAusgewaehlt.append(str('DMG:' + x[sin]['underbarrel']['weapon']['damage'] + bcolors.WARNINGh + wbd + bcolors.ENDC +' DK:' + x[sin]['underbarrel']['weapon']['ap'] + bcolors.WARNINGh + wba + bcolors.ENDC + ' ' + x[sin]['underbarrel']['weapon']['ammo'] + ' ' + x[sin]['underbarrel']['weapon']['mode'] + ' RS:' + x[sin]['underbarrel']['weapon']['rc'] + ' Würfel:' + x[sin]['underbarrel']['weapon']['dicepool']))
                            waffeAusgewaehlt.append(str(' [' + x[sin]['underbarrel']['weapon']['accuracy'] + ']'))
                            waffeAusgewaehlt.append(x[sin]['underbarrel']['weapon']['category'])
                    else:
                        print(bcolors.IND + bcolors.BOLD + bcolors.WARNINGh + '\t' + str(s) + bcolors.FAILh + ' liegt nicht im Auswahlbereich, bitte erneut auswählen.')
                else:
                    del waffeAusgewaehlt
                    waffeAusgewaehlt = [' ',' ',' ',' ',' ',' ']
                    flg = -1
                    for k,nam in enumerate(y):
                        if x[sin]['fullname'] == y[k]['gearname'] and y[k]['category'] == 'Foki':
                            flg = k
                    if flg > -1:
                        dcbonus = str(bcolors.WARNINGh + '+' + y[flg]['rating'] + bcolors.ASTRALh + ' (' + str(skll_astralkampf) + bcolors.WARNINGh + '+' + y[flg]['rating'] + bcolors.ASTRALh + ')' + bcolors.ENDC)
                        dmgbnus = str(bcolors.ASTRALh + ' (' + x[sin]['rc'] + bcolors.WARNINGh + '+' + bcolors.ASTRALh + 'CHA)' + bcolors.ENDC)
                        waffenname = str(bcolors.WARNINGh + x[sin]['fullname'] +  bcolors.ENDC)
                        waffeAusgewaehlt[5] = y[flg]['category']
                    else:
                        waffenname = x[sin]['fullname']
                        dmgbnus = ''
                        dcbonus = ''
                        waffeAusgewaehlt[5] = x[sin]['category']
                    waffeAusgewaehlt[0] = waffenname
                    waffeAusgewaehlt[3] = str(' DMG:' + x[sin]['damage'] + dmgbnus + ' DK:' + x[sin]['ap'] + ' Würfel: ' + x[sin]['dicepool'] + dcbonus + ' [' + x[sin]['accuracy'] + ']')
            elif (s.isdigit()) and int(s) > 0 and int(s) <= n_lst+1:
                sin = int(s) - 1
                if x[sin]['type'] == 'Ranged' and x[sin]['category'] != 'Ausrüstung':
                    clscrn()
                    headerprnt()
                    chlist = []
                    n_ch = 0
                    print(bcolors.IND + bcolors.BOLD + 'Welche Munition soll ausgerüstet werden?\n' + bcolors.ENDC)
                    for i,n in enumerate(y):
                        if str(y[i]['isammo']) == 'True' and y[i]['extra'] == x[sin]['category']: ###HIERMARKER
                            chlist.append(i)
                            n_ch += 1 
                            if 'weaponbonusdamage' in y[i].keys():
                                print((bcolors.IND + bcolors.GREEN + bcolors.BOLD + str(n_ch) + bcolors.ENDC + ')  ' + '{qty:>5} x {name:40} [ DMG: {weaponbonusdamage} | DK: {weaponbonusap} ] für: {extra}'.format(**y[i])).ljust(txtwdth) + 'Kosten: {cost:>7}\t\t{source:3} {page}'.format(**y[i]))
                                print('')
                            else:
                                print((bcolors.IND + bcolors.GREEN + bcolors.BOLD + str(n_ch) + bcolors.ENDC + ')  ' + '{qty:>5} x {name:40} {leer: <21} für: {extra}'.format(**y[i], leer=' ')).ljust(txtwdth) + 'Kosten: {cost:>7}\t\t{source:3} {page}'.format(**y[i]))
                                print('')
                    sub_line()
                    b = input(' >>> ')
                    if b == 'q':
                        break
                    elif b.isdigit() and int(b) > 0 and int(b) <= n_ch:
                        bint = chlist[int(b)-1]
                        if 'weaponbonusdamage' in y[bint].keys():
                            wbd = y[bint]['weaponbonusdamage']
                            wba = y[bint]['weaponbonusap']
                        else:
                            wbd = ''
                            wba = ''
                            smtl = ''
                        if 'accessories' in x[sin] and type(x[sin]['accessories']['accessory']) is dict:
                            if x[sin]['accessories']['accessory']['name'].find('Smartgunsystem') != -1:
                                if smrtlnktype == 'cyberware':
                                    smtl = '+2'
                                elif smrtlnktype == 'extern':
                                    smtl = '+1'
                        elif 'accessories' in x[sin]:
                            for num in range(len(x[sin]['accessories']['accessory'])):
                                if x[sin]['accessories']['accessory'][num]['name'].find('Smartgunsystem') != -1:
                                    if smrtlnktype == 'cyberware':
                                        smtl = '+2' 
                                    elif smrtlnktype == 'extern':
                                        smtl = '+1'
               ####2MARK
                        if int(y[bint]['qty']) >= getammo(x[sin]['ammo']):
                            ammocnt = getammo(x[sin]['ammo'])
                        else:
                            ammocnt = int(y[bint]['qty'])
                        del waffeAusgewaehlt
                        waffeAusgewaehlt = [' ']
                        #waffeAusgewaehlt[0] = str(x[sin]['fullname'] + ' (' + bcolors.GREENh + y[bint]['name'] + bcolors.ENDC + ') DMG:' + x[sin]['damage'] + bcolors.WARNINGh + wbd + bcolors.ENDC +' DK:' + x[sin]['ap'] + bcolors.WARNINGh + wba + bcolors.ENDC + ' ' + x[sin]['ammo'] + ' ' + x[sin]['mode'] + ' RS:' + x[sin]['rc'] + ' Würfel:' + x[sin]['dicepool'])
                        waffeAusgewaehlt[0] = x[sin]['fullname']
                        waffeAusgewaehlt.append(y[bint]['name'])
                        waffeAusgewaehlt.append(str(bcolors.BLACK + bcolors.BGW + smtl + bcolors.ENDC))
                        waffeAusgewaehlt.append(str('DMG:' + x[sin]['damage'] + bcolors.WARNINGh + wbd + bcolors.ENDC +' DK:' + x[sin]['ap'] + bcolors.WARNINGh + wba + bcolors.ENDC + ' ' + x[sin]['ammo'] + ' ' + x[sin]['mode'] + ' RS:' + x[sin]['rc'] + ' Würfel:' + x[sin]['dicepool']))
                        waffeAusgewaehlt.append(str(' [' + x[sin]['accuracy'] + ']'))
                        waffeAusgewaehlt.append(x[sin]['category'])
                    else:
                        print(bcolors.IND + bcolors.BOLD + bcolors.WARNINGh + '\t' + str(s) + bcolors.FAILh + ' liegt nicht im Auswahlbereich, bitte erneut auswählen.')
                else:
                    del waffeAusgewaehlt
                    waffeAusgewaehlt = [' ',' ',' ',' ',' ',' ']
                    flg = -1
                    for k,nam in enumerate(y):
                        if x[sin]['fullname'] == y[k]['gearname'] and y[k]['category'] == 'Foki':
                            flg = k
                    if flg > -1:
                        dcbonus = str(bcolors.WARNINGh + '+' + y[flg]['rating'] + bcolors.ASTRALh + ' (' + str(skll_astralkampf) + bcolors.WARNINGh + '+' + y[flg]['rating'] + bcolors.ASTRALh + ')' + bcolors.ENDC)
                        dmgbnus = str(bcolors.ASTRALh + ' (' + x[sin]['rc'] + bcolors.WARNINGh + '+' + bcolors.ASTRALh + 'CHA)' + bcolors.ENDC)
                        waffenname = str(bcolors.WARNINGh + x[sin]['fullname'] +  bcolors.ENDC)
                        waffeAusgewaehlt[5] = y[flg]['category']
                    else:
                        waffenname = x[sin]['fullname']
                        dcbonus = ''
                        dmgbnus = ''
                        waffeAusgewaehlt[5] = x[sin]['category']
                    waffeAusgewaehlt[0] = waffenname
                    waffeAusgewaehlt[3] = str(' DMG:' + x[sin]['damage'] + dmgbnus + ' DK:' + x[sin]['ap'] + ' Würfel: ' + x[sin]['dicepool'] + dcbonus + ' [' + x[sin]['accuracy'] + ']')
            else:
                print(bcolors.IND + bcolors.BOLD + bcolors.WARNINGh + '\t' + str(s) + bcolors.FAILh + ' liegt nicht im Auswahlbereich, bitte erneut auswählen.' + bcolors.ENDC)
            funbreak = 1
        elif ch == 'q':
            funbreak = 1
            break
        elif ch == 'p':  #### EQUIP.PANZERUNG
            clscrn()
            headerprnt()
            y = character['armors']['armor']
            print(bcolors.IND + bcolors.BOLD + '\n\tWelche Panzerung soll angelegt werden?\n\n' + bcolors.ENDC)
            chlist = []
            chalist = []
            for i,n in enumerate(y):
                if y[i]['armor'].find('+') == -1:
                    chlist.append(i)
                else:
                    chalist.append(i)
            for i in range(len(chlist)):
                print((bcolors.IND + bcolors.GREEN + bcolors.BOLD + str(i+1) + bcolors.ENDC + ') ' + '{name:40} Panzerung: {armor:>2}'.format(**y[chlist[i]])).ljust(120) + '{source:3} {page:>3}'.format(**y[chlist[i]]))
                if y[chlist[i]]['armormods'] != None:
                    for k,nam in enumerate(y[chlist[i]]['armormods']['armormod']): 
                        print('\t\t' + bcolors.BLUEh + '{fullname:35}'.format(**y[chlist[i]]['armormods']['armormod'][k]) + bcolors.ENDC)
                print('')
            sub_line()
            s = input(' >>> ')
            if s == 'q':
                break
            elif s.isdigit() and int(s) > 0 and int(s) <= len(chlist):
                sin = chlist[int(s)-1]
                gpa = y[sin]['fullname']
                gpaw = int(y[sin]['armor'])
                global pan
                pan = gpa
                paras['panzerung'] = gpaw
                ### Helme
                clscrn()
                headerprnt()
                print(bcolors.IND + bcolors.BOLD + '\n\tSoll ein Helm angelegt werden?\n\n' + bcolors.ENDC)
                print(bcolors.IND + bcolors.GREEN + bcolors.BOLD + str(1) + bcolors.ENDC + ') ' + 'Kein Helm.\n')
                for i in range(len(chalist)):
                    print((bcolors.IND + bcolors.GREEN + bcolors.BOLD + str(i+2) + bcolors.ENDC + ') ' + '{name:40} Panzerung: {armor:>2}'.format(**y[chalist[i]])).ljust(120) + '{source:3} {page:>3}'.format(**y[chalist[i]]))
                    if y[chlist[i]]['armormods'] != None:
                        for k,nam in enumerate(y[chalist[i]]['armormods']['armormod']): 
                            print('\t\t' + bcolors.BLUEh + '{fullname:35}'.format(**y[chalist[i]]['armormods']['armormod'][k]) + bcolors.ENDC)
                    print('')
                sub_line()
                b = input(' >>> ')
                if b == 'q':
                    break
                elif b.isdigit() and int(b) > 0 and int(b) <= len(chalist)+1:
                    if len(chalist) > 0:
                        bin = chalist[int(b)-2]
                    if b == '1':
                        apa = ''
                        apaw = 0
                    else:
                        apa = ' + ' + y[bin]['fullname']
                        apaw = int(y[bin]['armor'][1:])
                    pan = gpa + apa
                    paras['panzerung'] = gpaw + apaw
                else:
                    print(bcolors.IND + bcolors.BOLD + bcolors.WARNINGh + '\t' + str(b) + bcolors.FAILh + ' ist nicht in der Auswahlliste, bitte erneut auswählen.' + bcolors.ENDC)
            else:
                print(bcolors.IND + bcolors.BOLD + bcolors.WARNINGh + '\t' + str(s) + bcolors.FAILh + ' ist nicht in der Auswahlliste, bitte erneut auswählen.' + bcolors.ENDC)
        elif ch == 'a':  #### EQUIP.AUSRÜSTUNG
            clscrn()
            headerprnt()
            y = character['gears']['gear']
            print(bcolors.IND + bcolors.BOLD + '\n\tWelche Ausrüstung soll angelegt werden?' + bcolors.ENDC)
            chlist = []
            for k,nam in enumerate(y):
                if y[k]['name'] == 'Troden':
                    chlist.append(k)
                if y[k]['name'] == 'Kontaktlinsen':
                    chlist.append(k)
                if y[k]['name'] == 'Brille':
                    chlist.append(k)
            for i in range(len(chlist)):
                print((bcolors.IND + bcolors.GREEN + bcolors.BOLD + str(i+1) + bcolors.ENDC + ') ' + '{name:40} Firewall: {firewall} Datenverarbeitung: {dataprocessing} Konditionsmonitor: {conditionmonitor}'.format(**y[chlist[i]])).ljust(120) + 'Kosten: {cost:>7}\t\t{source:3} {page}'.format(**y[chlist[i]]))
                if y[chlist[i]]['children'] != None:
                    for k,nam in enumerate(y[chlist[i]]['children']['gear']): 
                        print('\t\t' + bcolors.BLUEh + '{name:35} {rating}'.format(**y[chlist[i]]['children']['gear'][k]) + bcolors.ENDC)
                print('')
            sub_line()
            s = input(' >>> ')
            if s == 'q':
                break
            elif s.isdigit() and int(s) > 0 and int(s) <= len(chlist):
                sin = chlist[int(s)-1]
                print(y[sin]['name'])
                if y[sin]['name'] == 'Troden':
                    if troden == True:
                        troden = False
                        smrtlnk = False
                    else:
                        troden = True
                        if contacts == True:
                            smrtlnk = True
                        elif glasses == True:
                            smrtlnk = True
                if y[sin]['name'] == 'Kontaktlinsen':
                    if contacts == True:
                        contacts = False
                        smrtlnk = False
                    else:
                        contacts = True
                        if troden == True:
                            smrtlnk = True
                if y[sin]['name'] == 'Brille':
                    if glasses == True:
                        glasses = False
                        smrtlnk = False
                    else:
                        glasses = True
                        if troden == True:
                            smrtlnk = True
                if troden == True and contacts == True:
                    trodens = '& Troden'
                elif troden == True and glasses == True:
                    trodens = '& Troden'
                elif troden == True:
                    trodens = 'Troden'
                else:
                    trodens = ''
                if contacts == True:
                    contactss = 'Kontaktlinsen'
                elif glasses == True:
                    contactss = 'Brille'
                else:
                    contactss = ''
                gearAusgewaehlt = str(contactss + ' ' + trodens)
            else:
                print(bcolors.IND + bcolors.BOLD + bcolors.WARNINGh + '\t' + str(s) + bcolors.FAILh + ' ist nicht in der Auswahlliste, bitte erneut auswählen.' + bcolors.ENDC)
        elif ch == 's':  #### EQUIP.SMARTLINK
            clscrn()
            headerprnt()
            y = character['gears']['gear']
            if smrtlnktype == '':
                print(bcolors.IND + bcolors.BOLD + '\n\tSmartlink nicht verfügbar!\n' + bcolors.ENDC)
                print('')
                sub_line()
                s = input(' >>> ')
            else:
                if smrtlnk == False:
                    print(bcolors.IND + bcolors.BOLD + '\n\tSmartlink aktivieren?\n' + bcolors.ENDC)
                else:
                    print(bcolors.IND + bcolors.BOLD + '\n\tSmartlink deaktivieren?\n' + bcolors.ENDC)
                print(bcolors.IND + bcolors.GREEN + bcolors.BOLD + '1' + bcolors.ENDC + ') ' + 'Ja.')
                print(bcolors.IND + bcolors.GREEN + bcolors.BOLD + '2' + bcolors.ENDC + ') ' + 'Nein.')
                print('')
                sub_line()
                s = input(' >>> ')
                if s == 'q':
                    break
                elif s.isdigit() and int(s) > 0 and int(s) <= 2:
                    if s == '1' and smrtlnk == False:
                        smrtlnk = True
                    elif s == '1' and smrtlnk == True:
                        smrtlnk = False
                else:
                    print(bcolors.IND + bcolors.BOLD + bcolors.WARNINGh + '\t' + str(s) + bcolors.FAILh + ' ist nicht in der Auswahlliste, bitte erneut auswählen.' + bcolors.ENDC)
        else:
            print(bcolors.IND + bcolors.BOLD + bcolors.WARNINGh + '\t' + str(ch) + bcolors.FAILh + ' ist nicht in der Auswahlliste, bitte erneut auswählen.' + bcolors.ENDC)
    if imkampf == True:
        kampf()
    else:
        main_menu() 
    return
 
## DMG
def dmg():
    headerprnt()
    funbreak = 0
    while funbreak < 1:
        print(bcolors.IND + bcolors.WARNINGh + '\tWelche Art von Schaden hat der Charakter erhalten? (' + bcolors.ENDC + bcolors.BLUEh + 'g' + bcolors.ENDC + bcolors.WARNINGh + ' / ' + bcolors.ENDC + bcolors.BLUEh + 'k' + bcolors.ENDC + bcolors.WARNINGh + ')' + bcolors.ENDC)
        s = input(' >>> ')
        if s.lower() == 'g':
            print(bcolors.IND + bcolors.WARNINGh + '\tWie hoch ist der geistig erlittene Schaden?' + bcolors.ENDC)
            h = input(' >>> ')
            if( h.isdigit()):
                paras['geistig'] -= int(h)
                dmgx = (paras['maxgeistig'] - paras['geistig'])//3
                if dmgx > 0:
                    mali['geistig'] = (-1)*dmgx
                funbrk = 1
                break 
            elif h == 'q':
                break 
            else:
                print(bcolors.IND + bcolors.WARNING + str(h) + bcolors.FAILh + ' ist keine Zahl, bitte nochmal eingeben.' + bcolors.ENDC)
        elif s.lower() == 'k':
            print(bcolors.IND + bcolors.WARNINGh + '\tWie hoch ist der körperlich erlittene Schaden?' + bcolors.ENDC)
            h = input(' >>> ')
            if( h.isdigit()):
                paras['koerperlich'] -= int(h)
                dmgx = ((paras['maxkoerperlich'] + int(paras['konstitution'])) - paras['koerperlich'] - int(paras['konstitution']))//3
                if dmgx > 0:
                    mali['koerperlich'] = (-1)*dmgx
                funbrk = 1 
                break
            elif h == 'q':
                break
            else:
                print(bcolors.IND + bcolors.WARNING + str(h) + bcolors.FAILh + ' ist keine Zahl, bitte nochmal eingeben.' + bcolors.ENDC)
        elif s.lower() == 'q':
            funbrk = 1
            break
        else:
            print(bcolors.IND + bcolors.WARNING + str(s) + bcolors.FAILh + ' ist kein Schadensoperator, bitte nochmal eingeben' + bcolors.ENDC)
    if imkampf == True:
        kampf()
    else:
        main_menu() 
    return

### HEIL
def heil():
    funbreak = 0
    x = character['qualities']['quality']
    flg = 0
    for i in range(len(x)):
        if 'Schnellheilung' == x[i]['name']:
            flg = 1
    if flg == 1:
        shl = ' +2'
        shlng = bcolors.WARNINGh + '\t\tVorteil: Schnellheilung' + bcolors.ENDC
    else:
        shl = ''
        shlng = ''
    def heilmod():
        clscrn()
        headerprnt()
        print(bcolors.IND + bcolors.UNDERLINE + 'Heilungsmodifikatoren:\n' + bcolors.ENDC)
        print(bcolors.IND + bcolors.UNDERLINE + 'Situation'.ljust(70) + '{:^35}'.format('WP-Mods') + '\n' + bcolors.ENDC)
        print(bcolors.IND + 'Gute Bedingungen (sterile, klinische Umgebung)'.ljust(70, '.') + '{:.>16}'.format(' ') + bcolors.GREENh + '+0' + bcolors.ENDC)
        print(bcolors.IND + 'Durchschnittliche Bedingungen (drinnen)'.ljust(70, '.') + '{:.>16}'.format(' ') + bcolors.GREENh + '-1' + bcolors.ENDC)
        print(bcolors.IND + 'Mäßige Bedingungen (Straße oder Wildnis)'.ljust(70, '.') + '{:.>16}'.format(' ') + bcolors.GREENh + '-2' + bcolors.ENDC)
        print(bcolors.IND + 'Schlechte Bedingungen (Kampf, schlechtes Wetter, Sumpf)'.ljust(70, '.') + '{:.>16}'.format(' ') + bcolors.GREENh + '-3' + bcolors.ENDC)
        print(bcolors.IND + 'Katastrophale Bedingungen (Feuer, starker Sturm)'.ljust(70, '.') + '{:.>16}'.format(' ') + bcolors.GREENh + '-4' + bcolors.ENDC + '\n')
        print(bcolors.IND + 'Keine medizinischen Vorräte'.ljust(70, '.') + '{:.>16}'.format(' ') + bcolors.GREENh + '-3' + bcolors.ENDC)
        print(bcolors.IND + 'Improvisierte medizinische Vorräte'.ljust(70, '.') + '{:.>16}'.format(' ') + bcolors.GREENh + '-1' + bcolors.ENDC)
        print(bcolors.IND + 'Kabelloses Medkit/Autodoc'.ljust(70, '.') + '{:.>14}'.format(' ') + bcolors.GREENh + '+Stufe' + bcolors.ENDC)
        print(bcolors.IND + 'Ferngelenkte Versorgung durch Medkit/Autodoc'.ljust(70, '.') + '{:.>16}'.format(' ') + bcolors.GREENh + '-2' + bcolors.ENDC)
        print(bcolors.IND + 'Assistenz'.ljust(70, '.') + '{:.>9}'.format(' ') + bcolors.GREENh + 'Teamworkprobe S.51' + bcolors.ENDC + '\n')
        print(bcolors.IND + 'Unkooperativer Patient'.ljust(70, '.') + "{:.>16}".format(' ') + bcolors.GREENh + '-2' + bcolors.ENDC)
        print(bcolors.IND + 'Patient ist Erwacht oder Technomancer'.ljust(70, '.') + '{:.>16}'.format(' ') + bcolors.GREENh + '-2' + bcolors.ENDC)
        print(bcolors.IND + 'Patient hat Implantate'.ljust(70, '.') + '{:.>1}'.format(' ') + bcolors.GREENh + '-1 pro volle 2 Punkte Essensverlust' + bcolors.ENDC)
        print('')
        liner()
        kaesheil = input(' < ' + bcolors.FAIL + '+' + bcolors.ENDC + ' > ')
    while funbreak < 1:
        mali['geistig'] = 0 - ((paras['maxgeistig'] - paras['geistig'])//3)
        mali['koerperlich'] = 0 - ((paras['maxkoerperlich'] - paras['koerperlich'])//3)
        clscrn()
        headerprnt()
        print(bcolors.IND + 'Wie soll der Charakter geheilt werden?\n')
        print(bcolors.IND + bcolors.BLUEh + '1' + bcolors.ENDC + ') Schaden heilen')
        print(bcolors.IND + bcolors.BLUEh + '2' + bcolors.ENDC + ') Natürliche Genesung [' + bcolors.PNZRG + '+Medizin' + bcolors.ENDC + ']')
        print(bcolors.IND + bcolors.BLUEh + '3' + bcolors.ENDC + ') Erste Hilfe')
        print(bcolors.IND + bcolors.BLUEh + '4' + bcolors.ENDC + ') Zauber Heilung')
        print(bcolors.IND + bcolors.BLUEh + '5' + bcolors.ENDC + ') Medizin')
        print(bcolors.IND + bcolors.BLUEh + '6' + bcolors.ENDC + ') Stabilisieren')
        print(bcolors.IND + bcolors.BLUEh + '7' + bcolors.ENDC + ') Edge')
        print(bcolors.IND + bcolors.BLUEh + '8' + bcolors.ENDC + ') Ausrüstung')
        print(bcolors.IND + bcolors.BLUEh + 'q' + bcolors.ENDC + ') Beenden')
        print('\n')
        liner()
        print('', end='')
        choice = input(' < ' + bcolors.FAIL + '+' + bcolors.ENDC + ' > ')
        if choice == 'q':
            funbreak = 1
            break
        elif choice == '1': ### HEIL.SCHADEN HEILEN
            funfunbreak = 0
            clscrn()
            headerprnt()
            print(bcolors.IND + 'Welcher Schaden soll geheilt werden (' + bcolors.BLUEh + 'k' + bcolors.ENDC + ' oder ' + bcolors.BLUEh + 'g' + bcolors.ENDC + ')?')
            print('')
            liner()
            while funfunbreak < 1:
                s = input(' < ' + bcolors.FAIL + '+' + bcolors.ENDC + ' > ')
                if s == 'q':
                    funfunbreak = 1
                    break
                elif s == 'g':
                    clscrn()
                    headerprnt()
                    if paras['geistig'] == paras['maxgeistig']:
                        print('\n\t' + bcolors.IND + bcolors.WARNINGh + bcolors.BOLD + 'Der Charakter ist ' + bcolors.BLUEh + 'geistig' + bcolors.WARNINGh + ' vollständig gesund!' + bcolors.ENDC)
                        print('')
                        liner()
                        print('')
                        kaesheil = input(' < ' + bcolors.FAIL + '+' + bcolors.ENDC + ' > ')
                        funfunbreak = 1
                        break
                    else:
                        print('\n\t' + bcolors.IND + 'Wie viel ' + bcolors.BLUEh + 'geistiger Schaden' + bcolors.ENDC + ' soll geheilt werden?')
                        print('')
                        liner()
                        print('')
                        kaesheil = input(' < ' + bcolors.FAIL + '+' + bcolors.ENDC + ' > ')
                        if kaesheil == 'q':
                            funfunbreak = 1
                            break
                        elif kaesheil.isdigit():
                            paras['geistig'] += int(kaesheil)
                            if paras['geistig'] > paras['maxgeistig']:
                                paras['geistig'] = paras['maxgeistig']
                            funfunbreak = 1
                elif s == 'k':
                    clscrn()
                    headerprnt()
                    if paras['koerperlich'] == paras['maxkoerperlich']:
                        print('\n\t' + bcolors.IND + bcolors.WARNINGh + bcolors.BOLD + 'Der Charakter ist ' + bcolors.BLUEh + 'koerperlich' + bcolors.WARNINGh + ' vollständig gesund!' + bcolors.ENDC)
                        print('')
                        liner()
                        print('')
                        kaesheil = input(' < ' + bcolors.FAIL + '+' + bcolors.ENDC + ' > ')
                        funfunbreak = 1
                        break
                    else:
                        print('\n\t' + bcolors.IND + 'Wie viel ' + bcolors.BLUEh + 'körperlicher Schaden' + bcolors.ENDC + ' soll geheilt werden?')
                        print('')
                        liner()
                        print('')
                        kaesheil = input(' < ' + bcolors.FAIL + '+' + bcolors.ENDC + ' > ')
                        if kaesheil == 'q':
                            funfunbreak = 1
                            break
                        elif kaesheil.isdigit():
                            paras['koerperlich'] += int(kaesheil)
                            if paras['koerperlich'] > paras['maxkoerperlich']:
                                paras['koerperlich'] = paras['maxkoerperlich']
                            funfunbreak = 1
        elif choice == '2':  ### HEIL.GENESUNG
            funfunbreak = 0
            clscrn()
            headerprnt()
            print(bcolors.IND + bcolors.UNDERLINE + 'Natürliche Genesung von Schaden' + bcolors.ENDC + '\n')
            print(bcolors.IND + 'Körperlicher Schaden heilt erst, wenn etwaiger geistiger Schaden vollständig geheilt ist!')
            print(bcolors.IND + 'Ausgedehnte Proben können mit ' + bcolors.PNZRGh + 'Medizin' + bcolors.ENDC + ',' + bcolors.PNZRGh + ' Medkit' + bcolors.ENDC + ' oder ' + bcolors.PNZRGh + 'Autodoc-Drohne' + bcolors.ENDC + ' unterstützt, bzw. beschleunigt werden.')
            print(bcolors.IND + 'Geistig:\n\t' + bcolors.IND + 'Ausgedehnte Probe: ' + bcolors.GREENh + 'KON + WIL ' + bcolors.PNZRGh + '+ Mod ' + bcolors.GREENh + '(1 Std)\n\t' + bcolors.ENDC + bcolors.IND + 'Charakter muss ruhen (Bewusstlosigkeit oder erzwungener Schlaf zählen.)') 
            print(bcolors.IND + 'Körperlich:\n\t' + bcolors.IND + 'Ausgedehnte Probe: ' + bcolors.GREENh + 'KON x 2 ' + bcolors.PNZRGh + '+ Mod ' + bcolors.GREENh + '(1 Tag)\n\t' + bcolors.ENDC + bcolors.IND + 'Charakter muss ruhen (Bewusstlosigkeit oder erzwungener Schlaf zählen.)') 
            print('\n' + bcolors.IND + bcolors.FAILh + 'Patzer'.rjust(17) + bcolors.ENDC + ': Die Ruhezeit verdoppelt sich.')
            print(bcolors.IND + bcolors.FAILh + 'Kritischer Patzer' + bcolors.ENDC + ': Der Schaden erhöht sich zusätzlich um ' + bcolors.GREENh + '1W6 / 2 (' + bcolors.ENDC + 'aufgerundet' + bcolors.GREENh + ')' + bcolors.ENDC + '.')
            print('')
            liner()
            print('')
            while funfunbreak < 1:
                if paras['geistig'] < paras['maxgeistig']:
                    print(bcolors.IND + 'Heilung des geistigen Schadens:\n')
                    print(bcolors.IND + 'Würfel: ' + str(int(paras['konstitution']) + int(paras['willenskraft'])) + bcolors.WARNINGh + shl + ' ' + bcolors.PNZRGh + '+ Mod ' + bcolors.FAILh + paras['mali'] + bcolors.ENDC + '  (1 Std)', end='')  
                    print(shlng.rjust(20))
                    print('')
                    print(bcolors.IND + 'Wie viele Kästchen werden geheilt?')
                    liner()
                    kaesheil = input(' < ' + bcolors.FAIL + '+' + bcolors.ENDC + ' > ')
                    if kaesheil.isdigit():
                        paras['geistig'] += int(kaesheil)
                        if paras['geistig'] > paras['maxgeistig']:
                            paras['geistig'] = paras['maxgeistig']
                        funfunbreak = 1
                    elif kaesheil == 'q':
                        funfunbreak = 1                  
                    else:
                        print(bcolors.IND + bcolors.FAILh + 'Bitte eine Zahl eingeben!' + bcolors.ENDC)
                elif paras['koerperlich'] < paras['maxkoerperlich']:
                    print(bcolors.IND + 'Heilung des körperlichen Schadens:\n')
                    print(bcolors.IND + 'Würfel: ' + str(2*int(paras['konstitution'])) + bcolors.WARNINGh + shl + ' ' +bcolors.PNZRGh + '+ Mod ' + bcolors.FAILh + paras['mali'] + bcolors.ENDC + '  (1 Tag)', end='')
                    print(shlng.rjust(20))
                    print('')
                    print(bcolors.IND + 'Wie viele Kästchen werden geheilt?')
                    liner()
                    kaesheil = input(' < ' + bcolors.FAIL + '+' + bcolors.ENDC + ' > ')
                    if kaesheil.isdigit():
                        paras['koerperlich'] += int(kaesheil)
                        if paras['koerperlich'] > paras['maxkoerperlich']:
                            paras['koerperlich'] = paras['maxkoerperlich']
                        funfunbreak = 1
                    elif kaesheil == 'q':
                        funfunbreak = 1
                    else:
                        print(bcolors.IND + bcolors.FAILh + 'Bitte eine Zahl eingeben!' + bcolors.ENDC)
                else:
                    print(bcolors.IND + bcolors.WARNINGh + bcolors.BOLD + 'Der Charakter ist vollständig gesund.' + bcolors.ENDC)
                    print('')
                    liner()
                    kaesheil = input(' < ' + bcolors.FAIL + '+' + bcolors.ENDC + ' > ')
                    funfunbreak = 1
        elif choice == '3': ### HEIL.ERSTEHILFE
            funfunbreak = 0
            while funfunbreak < 1:
                clscrn()
                headerprnt()
                print(bcolors.IND + bcolors.UNDERLINE + 'Erste Hilfe\n' + bcolors.ENDC)
                print(bcolors.IND + 'Erforderlich: Fertigkeit ' + bcolors.GREENh + 'Erste Hilfe' + bcolors.ENDC + ' und ' + bcolors.GREENh + 'Medkit' + bcolors.ENDC)
                print(bcolors.IND + ' '.ljust(14) + 'Erste Hilfe muss innerhalb ' + bcolors.GREENh + '1 Stunde' + bcolors.ENDC + ' geleistet werden.\n')
                print(bcolors.IND + ('Probe: ' + bcolors.GREENh + 'Erste Hilfe + LOG' + bcolors.PNZRG + ' + Mod' + bcolors.GREENh + ' [geistig ' + bcolors.PNZRGh + '+ Medkit' + bcolors.GREENh + '](2)').ljust(90) + bcolors.ENDC + 'es gelten Heilungsmodifikatoren\tSR5 206')
                print(bcolors.IND + ('').ljust(65) + 'bei eigenem Wirken gelten Verletzungsmodifikatoren!\n')
                print(bcolors.IND + 'Jeder ' + bcolors.GREENh + 'Nettoerfolg überhalb des Schwellenwerts ' + bcolors.ENDC + 'senkt den Schaden um ' + bcolors.GREENh + '1 Kästchen' + bcolors.ENDC)
                print(bcolors.IND + 'Falls der zu heilende Charakter eine ' + bcolors.WARNINGh + 'Ganzkörperpanzerung' + bcolors.ENDC + ' trägt: ' + bcolors.BLUEh + 'Heilung / 2\n' + bcolors.ENDC)
                print(bcolors.IND + bcolors.FAILh + 'Kritischer Patzer' + bcolors.ENDC + ': Schaden erhöht sich um: ' + bcolors.GREENh + '1W6 / 2 (' + bcolors.ENDC + 'aufgerundet' + bcolors.GREENh + ')\n' + bcolors.ENDC)
                print(bcolors.IND + bcolors.FAILh + 'Entzug kann nicht geheilt werden!' + bcolors.ENDC) 
                print(bcolors.IND + 'Maximale Heilung entspricht der Fertigkeitsstufe!')
                print(bcolors.IND + 'Erste Hilfe kann nur einmal pro Verletzungssatz eingesetzt werden.')
                print(bcolors.IND + 'Erste Hilfe erfordert eine ' + bcolors.GREENh + 'komplexe Handlung pro Kampfrunde' + bcolors.ENDC + ' und dauert ' + bcolors.GREENh + 'Anzahl an Kampfrunden gleich der Heilpunkte' + bcolors.ENDC)
                print(bcolors.IND + 'Erste Hilfe kann zur Diagnose eingesetzt werden.')
                print('')
                liner()
                x = character['gears']['gear']
                flg = -1 
                for i,n in enumerate(x):
                    if x[i]['name'] == 'Medkit':
                        flg = i 
                if flg > -1: 
                    hatmedkit = True
                else:
                    hatmedkit = False
                y = character['skills']['skill']
                for num,nam in enumerate(y):
                    if y[num]['name'] == 'Erste Hilfe':
                        erstehilfe = y[num]['rating']
                        eht = y[num]['total']
                if int(erstehilfe) != 0 and hatmedkit == True:
                    print(bcolors.IND + 'Würfel: ' + eht + bcolors.WARNINGh + shl + bcolors.PNZRGh + ' +' + x[flg]['rating'] + '(Medkit)' + bcolors.FAILh + ' ' +  paras['mali'] + bcolors.ENDC + '  [' + paras['limg'] + bcolors.PNZRGh + ' + ' + x[flg]['rating'] + bcolors.ENDC + '](2)', end='') 
                    print(shlng.rjust(20))
                    print(bcolors.IND + 'Maximale Heilung: ' + bcolors.GREENh + str(int(erstehilfe)) + bcolors.ENDC + ' Kästchen')
                elif int(erstehilfe) == 0 and hatmedkit == True:
                    print(bcolors.IND + bcolors.BOLD + bcolors.WARNINGh + 'Erste Hilfe nicht gelernt! Medkit selbst Erste Hilfe leisten lassen (' + bcolors.GREENh + 'Gerätestufe x2' + bcolors.WARNINGh +')' + bcolors.ENDC)
                else:
                    print(bcolors.IND + bcolors.BOLD + bcolors.WARNINGh + 'Medkit erforderlich!' + bcolors.ENDC)
                print('\n')
                liner()
                print(bcolors.IND + "'" + bcolors.BLUEh + 'h' + bcolors.ENDC + "' Heilungsmodifikatoren (" + bcolors.PNZRG + 'Mods' + bcolors.ENDC + ')')
                liner()
                kaesheil = input(' < ' + bcolors.FAIL + '+' + bcolors.ENDC + ' > ')
                if kaesheil == 'h':
                    heilmod()
                else:
                    funfunbreak = 1
        elif choice == '4':  ### HEIL.ZAUBERHEILEN
            clscrn()
            headerprnt()
            print(bcolors.IND + bcolors.UNDERLINE + 'Zauber: Heilung' + bcolors.ENDC + '\n')
            print(bcolors.IND + 'Zur Heilung von ' + bcolors.GREENh + 'körperlichem Schaden' + bcolors.ENDC)
            print(bcolors.IND + 'Schaden durch Entzug kann ' + bcolors.FAILh + 'nicht' + bcolors.ENDC + ' magisch geheilt werden!')
            print(bcolors.IND + 'Der Zauber Heilung sollte erst eingesetzt werden, ' + bcolors.GREENh + 'nachdem' + bcolors.ENDC + ' Erste Hilfe angewandt worden ist!\n')
            print(bcolors.IND + 'Probe: ' + bcolors.GREENh + 'Spruchzauberei + MAG' + bcolors.WARNINGh + shl + bcolors.GREENh + ' [KS]' + bcolors.ENDC + ': Erfolge heilen Kästchen' + shlng)
            print('')
            liner()
            kaesheil = input(' < ' + bcolors.FAIL + '+' + bcolors.ENDC + ' > ')
        elif choice == '5':  ### HEIL.MEDIZIN
            clscrn()
            headerprnt()
            print(bcolors.IND + bcolors.UNDERLINE + 'Medizin' + bcolors.ENDC + '\n')
            print(bcolors.IND + 'Zur ' + bcolors.GREENh + 'Beschleunigung' + bcolors.ENDC + ' der ' + bcolors.GREENh + 'Genesung' + bcolors.ENDC)
            print(bcolors.IND + 'Medizin ist ' + bcolors.FAILh + 'nicht' + bcolors.ENDC + ' im Kampf einsetzbar!')
            print(bcolors.IND + 'Medizin kann benutzt werden, um eine Diagnose zu erstellen.')
            print(bcolors.IND + 'Charakter muss sich um Patienten kümmern: ' + bcolors.GREENh + '30 Minuten / Tag' + bcolors.ENDC + ' bei körperlichem Schaden und ' + bcolors.GREENh + '10 Minuten / Std' + bcolors.ENDC + ' bei geistigem Schaden.\n')
            print(bcolors.IND + 'Probe: ' + bcolors.GREENh + 'Medizin + LOG' + bcolors.PNZRGh + ' + Mods' + bcolors.GREENh + ' [geistig]' + bcolors.ENDC + ': Erfolge geben dem Patienten einen WP-Bonus von ' + bcolors.GREENh + '+1\n' + bcolors.ENDC)
            y = character['skills']['skill']
            for num,nam in enumerate(y):
                if y[num]['name'] == 'Medizin':
                    medizin = y[num]['total']
            print(bcolors.IND + 'Würfel: ' + medizin + bcolors.WARNINGh + shl + bcolors.FAILh + paras['mali'] + bcolors.PNZRGh + ' + Mods' + bcolors.GREENh + ' [geistig]' + bcolors.ENDC + shlng)
            print('')
            liner()
            kaesheil = input(' < ' + bcolors.FAIL + '+' + bcolors.ENDC + ' > ')
        elif choice == '6': ### HEIL.STABILISIEREN
            funfunbreak = 0
            while funfunbreak < 1:
                clscrn()
                headerprnt()
                print(bcolors.IND + bcolors.UNDERLINE + 'Überschüssiger körperlicher Schaden:' + bcolors.ENDC + '\n')
                print(bcolors.IND + 'Wenn der Zustandsmonitor überschritten wird, befindet sich der Charakter in Todesgefahr.'.ljust(130) + 'SR5 172')
                print(bcolors.IND + 'Wenn ein Charakter mehr überschüssigen Schaden erleidet als seine ' + bcolors.GREENh + 'Konstitution' + bcolors.ENDC + ', dann stirbt er.')
                print(bcolors.IND + 'Wenn ein Charakter überschüssigen Schaden erlitten hat, erleidet er pro (' + bcolors.GREENh + 'KON' + bcolors.ENDC + ') ' + bcolors.GREENh + 'Minuten ' + bcolors.FAILh + '1' + bcolors.GREENh + ' zusätzlichen Schaden' + bcolors.ENDC + ' durch Blutverlust, Schock etc.')
                print('\n' + bcolors.IND + bcolors.UNDERLINE + 'Stabilisieren:\n' + bcolors.ENDC)
                print(bcolors.IND + 'Probe: ' + bcolors.GREENh + 'Erste Hilfe + Logik ' + bcolors.PNZRG + '+ Mods' + bcolors.GREENh + ' [Geistig](3)' + bcolors.ENDC + ' oder ' + bcolors.GREENh + 'Medizin + Logik ' + bcolors.PNZRG + '+ Mods' + bcolors.GREENh + ' [Geistig](3)' + bcolors.ENDC)
                print(bcolors.IND + 'Situationsmodi gelten!')
                print(bcolors.IND + bcolors.GREENh + 'Medkits' + bcolors.ENDC + ' und ' + bcolors.GREENh + 'Autodocs' + bcolors.ENDC + ' können zum Stabilisieren eingesetzt werden.')
                print('\n' + bcolors.IND + 'Wenn Probe geligt, erleidet der Charakter keinen zusätzlichen Schaden mehr.\n\tAndernfalls kann die Probe ohne Begrenzung wiederholt werden, jedoch steigt kummulativ ein Malus von ' + bcolors.GREENh + '-2' + bcolors.ENDC + ' pro neuem Versuch.')
                print('\n' + bcolors.IND + 'Der ' + bcolors.GREENh + 'Zauber Stabilisieren' + bcolors.ENDC + ' kann ebenfalls eingesetzt werden.')
                print('')
                liner()
                print(bcolors.IND + "'" + bcolors.BLUEh + 'h' + bcolors.ENDC + "' Heilungsmodifikatoren (" + bcolors.PNZRG + 'Mods' + bcolors.ENDC + ')')
                liner()
                kaesheil = input(' < ' + bcolors.FAIL + '+' + bcolors.ENDC + ' > ')
                if kaesheil == 'h':
                    heilmod()
                else:
                    funfunbreak = 1
        elif choice == '7': ### HEIL.EDGE
            clscrn()
            headerprnt()
            funfunbreak = 0
            maxedg = int(paras['maxedge']) 
            print(bcolors.IND + bcolors.UNDERLINE + 'Edge heilen:' + bcolors.ENDC)
            print('\n')
            print(bcolors.IND + 'Nach 8 Stunden Schlaf erhält der Charakter ' + bcolors.BLUEh + '1' + bcolors.ENDC + ' Edge zurück.\n\n\n')
            if int(paras['edge']) != maxedg:
                print(bcolors.IND + 'Wie viel Edge erhält der Charakter zurück?')
                liner()
                while funfunbreak < 1:
                    kaesheil = input(' < ' + bcolors.FAIL + '+' + bcolors.ENDC + ' > ')
                    if kaesheil.isdigit():
                        ge = int(paras['edge'])
                        ge += int(kaesheil)
                        if ge > maxedg:
                            ge = maxedg
                        paras['edge'] = str(ge)
                        funfunbreak = 1
                    elif kaesheil == 'q':
                        funfunbreak = 1
                    else:
                        print(bcolors.IND + bcolors.FAILh + 'Bitte eine Zahl eingeben!' + bcolors.ENDC)
            else:
                print(bcolors.IND + bcolors.WARNINGh + bcolors.BOLD + 'Der Charakter hat vollständiges Edge.' + bcolors.ENDC)
                print('')
                liner()
                kaesheil = input(' < ' + bcolors.FAIL + '+' + bcolors.ENDC + ' > ')
        elif choice == '8': ### HEIL.AUSR
            clscrn()
            headerprnt()
            print(bcolors.IND + bcolors.UNDERLINE + 'Ausrüstung:' + bcolors.ENDC + '\n')
            print(bcolors.IND + bcolors.BLUEh + ('Medkit' + bcolors.ENDC + ':').ljust(20) + '    ' + 'bis St. 3 Taschengroß, danach Aktenkoffergroß.'.ljust(100) + '\tSR5 455')
            print(bcolors.IND + bcolors.BLUEh + ' '.ljust(20) + bcolors.ENDC + 'muss alle (Stufe) Verwendungen wieder aufgefüllt werden.')
            print(bcolors.IND + bcolors.BLUEh + ' '.ljust(20) + bcolors.GREENh + 'WiFi-Vorteil' + bcolors.ENDC + ': WP-Bonus gleich seiner Stufe bei Erste Hilfe Proben.')
            print(bcolors.IND + bcolors.BLUEh + ' '.ljust(20) + bcolors.GREENh + ' '*12 + bcolors.ENDC + '  Es kann mit doppelter Stufe und Limit gleich der Stufe selbst agieren.')
            print('\n' + bcolors.IND + bcolors.BLUEh + ('Antidot-Patch' + bcolors.ENDC + ':').ljust(20) + '    ' + 'Toxinwiderstand + Stufe, wenn innerhalb 20 Min abgelegt.'.ljust(100) + '\tSR5 455')
            print('\n' + bcolors.IND + bcolors.BLUEh + ('Chem-Patch' + bcolors.ENDC + ':').ljust(20) + '    ' + 'Leeres Slap-Patch. Kann mit Chemikalie oder Toxin gefüllt werden.'.ljust(100) + '\tSR5 455')
            print('\n' + bcolors.IND + bcolors.BLUEh + ('Stim-Patch' + bcolors.ENDC + ':').ljust(20) + '    ' + 'Patch entfernt Anzahl an geistigen Schaden gleich der Stufe.'.ljust(100) + '\tSR5 455')
            print(bcolors.IND + bcolors.BLUEh + ' '.ljust(20) + bcolors.ENDC + 'Wirkung hält für ' + bcolors.GREENh + '(Stufe x 10) Minuten' + bcolors.ENDC + ', danach (' + bcolors.GREENh + 'Stufe + 1' + bcolors.ENDC + ') geistiger Schaden.')
            print(bcolors.IND + bcolors.BLUEh + ' '.ljust(20) + bcolors.ENDC + 'während Stim-Patch wirkt, kann sich Patient nicht ausruhen.')
            print(bcolors.IND + bcolors.BLUEh + ' '.ljust(20) + bcolors.ENDC + 'Häufige Verwendung führt zu Abhängigkeit [' + bcolors.GREENh + '2 (1)' + bcolors.ENDC + '].')
            print('\n' + bcolors.IND + bcolors.BLUEh + ('Tranq-Patch' + bcolors.ENDC + ':').ljust(20) + '    ' + 'Patch verursacht geistigen Schaden gleich der Stufe. Widerstand mit Konstitution.'.ljust(100) + '\tSR5 455')
            print('\n' + bcolors.IND + bcolors.BLUEh + ('Trauma-Patch' + bcolors.ENDC + ':').ljust(20) + '    ' + 'Patient kann selbst Stabilisierenprobe ablegen.'.ljust(100) + '\tSR5 455')
            print(bcolors.IND + bcolors.BLUEh + ' '.ljust(20) + bcolors.ENDC + 'Dabei benutzt er ' + bcolors.GREENh + 'Konstitution statt Erste Hilfe oder Medizin' + bcolors.ENDC + '.')
            print(bcolors.IND + bcolors.BLUEh + ' '.ljust(20) + bcolors.GREENh + 'WiFi-Vorteil' + bcolors.ENDC + ': Patient wird sofort stabilisiert.')
            print('')
            liner()
            print('')
            y = character['gears']['gear']
            print(bcolors.IND + bcolors.UNDERLINE + 'Charakterausrüstung:' + bcolors.ENDC + '\n')
            for i,nam in enumerate(y):
                if y[i]['category'] == 'Biotech':
                    print(bcolors.IND + bcolors.GREENh + ' {qty:>3}'.format(**y[i]) + bcolors.ENDC + ' x {name:30} Stufe: {rating:>2} {spacer} Kosten: {cost:>5} {spacer} {source:>3} {page:>3}'.format(**y[i], spacer=spacer))
            print('')
            liner()
            kaesheil = input(' < ' + bcolors.FAIL + '+' + bcolors.ENDC + ' > ')
    if imkampf == True:
        kampf()
    else:
        main_menu()
    return
        ## Natürliche Genesung
         # geistiger und körperlicher Schaden heilen von selbst, unterschidlich schnell
         # Medizinische Versorgung kann Prozess beschleunigen
         # Ausgedehnte Probe. Wenn keine Würfel mehr -> Medizinische Behandlung nötig
         # Medikits und Auto-doc-Drohnen beschleunigen 
         ### Geistiger Schaden:
            # Ausgedehnte Probe: KON + WIL (1 Std) Char muss ruhen. (Bewusstlos + erzwungener Schlaf zählen)
            # Jeder Erfolg reduziert Geistigen Schaden um 1 Kästchen
         ### Körperlicher Schaden:
            # Ausgedehnte Probe: KON*2 (1 Tag). Char muss ruhen
            # Jeder Erfolg reduziert Körperlichen Schaden um 1 Kästchen
            # Falls Char auch geistigen Schaden hat, muss dieser vor dem Körperlichen Schaden vollständig heilen

         # Patzer bei Genesungsprobe verdoppelt die nötige Ruhezeit
         # kritischer Patzer erhöht zusätzlich den Schaden um 1W6/2 (aufgerundet)

        ## Medizin 
         # Fertigkeit können Genesung beschl. Probe: Medizin + Logik [Geistig] (Modifikatoren)
         # Jeder Erfolg: Patient WP-Bonus +1 für Genesung
         # Bei körperlichen Schäden, muss Mediziner täglich min 30 Minuten kümmern
         # bei geistigem Schaden 10 Minuten pro Stunde
         # Medizin darf pro Satz von Verletzungen nur einmal eingesetzt werden.
         # Medizin kann wie Erste Hilfe zur Diagnose eingesetzt werden
         # Medizin kann nicht im Kampf eingesetzt werden.

        ## MEDKITS und AUTODOCS
         # Fähigkeiten moderner Medkits S 454 und Autodocdrohnen ähnlich ausgebldeter Sanitäter.
         # Diagnosen oder Therapie unterstützten oder selbst durchführen
         # Benutzung im Kampf ist zeitaufwendig.
         # 1. komplexe Handlung um Gerät mit Patienten zu verbinden
         # 2. WP-Bonus in Höhe Gerätestufe auf Erste Hilfe, wenn per Wifi oder Autosoft
         # Wenn Charakter nicht ausgebildet, improvisieren: Logik-1 + Gerätestufe
         # Wenn WiFi-Medkit verbunden mit Patienten und selbstständig arbeitet: Alle Proben mit Gerätestufe*2

        ## Magische Heilung
         # Zauberspruch Heilen S. 282
         # Schaden durch Entzug kann nicht magisch geheilt werden

        ## ÜBERSCHÜSSIGER Körperlicher Schaden
        # Chars, die so viel körperlichen Schaden erleiden, dass ihr Zustandsmonitor überschritten wird, befinden sich ohne Behandlung in Todesgefahr (S. 172) 
        # Wenn Char mehr überschüssigen Schaden erleidet als KON, ist es vorbei

        ## Stabilisieren
         # Wenn überschüssiger Schaden und nicht stabilisiert wird, dann erleidet er pro KON MINUTEN 1 zusütliches Kästchen Schaden durch Blutverlust, Schock und andere Dinge.
         # Um zu Stabilisieren, Probe auf: Erste Hilfe + Logik [Geistig](3) oder Medizin + Logik [Geistig](3) ablegen, Es gelten Situationsmodi!
         # Medkits und Autodocs können stabilisieren.
         # Wenn stabilisiert, kein weiterer Schaden
         # Probe darf mehrmals versucht werden, jedoch mit kummulativer WP-Malus von -2 pro Versuch
         # Zauber Stabilisieren S. 282 kann ebenfalls genutzt werden.

### MAIN_MENU
def main_menu():
    clscrn()
    headerprnt()
    print(bcolors.IND + 'Wähle Menü aus:\n')
    menus = [
    ['bio', 'Bio'],
    ['qual', 'Vor- und Nachteile'],
    ['att', 'Attribute'],
    ['skill', 'Skills'],
    ['spell', 'Spells'],
    ['waff', 'Waffen'],
    ['armor', 'Armor'],
    ['cont', 'Kontakte'],
    ['gear', 'Ausrüstung'],
    ['cyber', 'Cyberware'],
    ['drug', 'Drogen'],
    ['fahr', 'Fahrzeuge'],
    ['astral', 'Astrale Welt'],
    ['geist', 'Geister'],
    ['alch', 'Alchemy'],
    ['bar', 'Barrieren'],
    ['proben', 'Probenarten'],
    ['kampf', 'Kampfmenü'],
    ['kaufen', 'Kaufmenü'],
    ['eq', 'Ausrüsten'],
    ['ga', 'Charakter projiziert astral'],
    ['za', 'Zauber aufrechthalten'],
    ['dmg', 'Verwaltung von Schaden'],
    ['edg', 'Edge-Menü'],
    ['heil', 'Heil-Menü'],
    ['nach', 'Nachschlagen'],
    ['exit', 'Programm beenden']
    ]
    anz = len(menus)%2
    lm = len(menus)//2 + anz
    for i in range(len(menus)//2):
        print('\t\t' + bcolors.IND + bcolors.BLUEh + ('{:^10}'.format(menus[i][0]) + bcolors.ENDC + ' - ' + menus[i][1]).ljust(40), end='')
        print('\t\t\t' + bcolors.BLUEh + ('{:^10}'.format(menus[i + lm][0]) + bcolors.ENDC + ' - ' + menus[i + lm][1]).ljust(40))
    if anz != 0:
        print('\t\t' + bcolors.IND + bcolors.BLUEh + '{:^10}'.format(menus[lm - 1][0]) + bcolors.ENDC + ' - ' + menus[lm - 1][1].ljust(40), end='')
    print('')
    sch()
    return

#Exit
def exit():
    svsfile()
    os.sys.exit()

# Menue actions dict:
menu_actions = {
        'main_menu': main_menu,
        '1': bio,
        '2': skills,
        '3': spells,
        '4': weapons,
        '5': armor,
        '6': gear,
        '7': equip,
        '8': getastral,
        '9': zauberaufrecht,
        '0': kampf,
        'bio': bio,
        'qual': qualities,
        'att': atts,
        'skill': skills,
        'spell': spells,
        'waff': weapons,
        'armor': armor,
        'cont': cont,
        'gear': gear,
        'cyber': cyberw,
        'fahr': fahrzeuge,
        'bar': bar,
        'nach': nachschlagen,
        'drug': drogen,
        'dmg': dmg,
        'heil': heil,
        'edg': looseedg,
        'geist': geist,
        'astral': astral_menu,
        'alch': alchemy,
        'kampf': kampf,
        'kaufen': kaufen,
        'eq': equip,
        'ga': getastral,
        'za': zauberaufrecht,
        'proben': probenarten,
        'exit': exit
        }

chckfsf()
checksmrtlnk()

# Hauptprogramm
if __name__ == '__main__':
    main_menu()
