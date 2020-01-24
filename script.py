import random, os, shutil, time, pickle, yaml

try:
    with open("config.yaml", 'r') as stream:
        config = yaml.safe_load(stream)
except:
    print("Invalid config file. Check config.yaml and redownload if necessary.")
    
    
classes_dict = {
'hero':{'type':'hero'},
'warrior':{'type':'physical'},
'fighter':{'type':'physical'},
'merchant':{'type':'physical'},
'thief':{'type':'physical'},
'mage':{'type':'magical'},
'cleric':{'type':'magical'},
'sage':{'type':'physical'},
'jester':{'type':'physical'},
        }

classes = list(classes_dict.keys())
classes.remove("hero")
classes_first = [i for i in classes if i != 'sage']

def setup_img():
    if config['hero_enabled']:
        shutil.copy(os.path.join('img','hero-%s.png' % config['hero_gender']),os.path.join('current','1_first.png'))
        shutil.copy(os.path.join('img','hero-%s_text.png' % config['hero_gender']),os.path.join('current','1_first_text.png'))
        shutil.copy(os.path.join('img','blank.png'),os.path.join('current','1_second.png'))
        shutil.copy(os.path.join('img','blank.png'),os.path.join('current','arrow_first.png'))
        for num in [2,3,4]:
            shutil.copy(os.path.join('img','blank.png'),os.path.join('current','%s_first.png' % num))
            time.sleep(.1)
            shutil.copy(os.path.join('img','question.png'),os.path.join('current','%s_second.png' % num))
            time.sleep(.1)
            shutil.copy(os.path.join('img','blank_text.png'),os.path.join('current','%s_first_text.png' % num))
            time.sleep(.1)
            shutil.copy(os.path.join('img','blank_text.png'),os.path.join('current','%s_second_text.png' % num))
            time.sleep(.1)
        
    else:
        shutil.copy(os.path.join('img','arrow.png'),os.path.join('current','arrow_first.png'))
        for num in [1,2,3,4]:
            shutil.copy(os.path.join('img','blank.png'),os.path.join('current','%s_first.png' % num))
            time.sleep(.1)
            shutil.copy(os.path.join('img','question.png'),os.path.join('current','%s_second.png' % num))
            time.sleep(.1)
            shutil.copy(os.path.join('img','blank_text.png'),os.path.join('current','%s_first_text.png' % num))
            time.sleep(.1)
            shutil.copy(os.path.join('img','blank_text.png'),os.path.join('current','%s_second_text.png' % num))
            time.sleep(.1)

def generate_img(char,gender,num,slot):
    time.sleep(.1)
    shutil.copy(os.path.join('img','%s-%s.png' % (char,gender)),os.path.join('current','%s_%s.png' % (num,slot)))
    time.sleep(.1)
    shutil.copy(os.path.join('img','%s-%s_text.png' % (char,gender)),os.path.join('current','%s_%s_text.png' % (num,slot)))
    

def generate_chosen():
    setup_img()
    chosen = random.choices(classes_first,k=4)
    chosen = check_class_validity(chosen)
    chosen = [{'first':i, 'second':''} for i in chosen]
    
    
    for idx, c in enumerate(chosen):
        if idx == 0 and config['hero_enabled']:
            c['gender'] = config['hero_gender']
        else:
            gender = random.choice(['m','f'])
            c['gender'] = gender
    chosen = dict(zip([1,2,3,4],chosen))
    chosen['sage_count'] = 0
    
    for num in [1,2,3,4]:
        generate_img(chosen[num]['first'],chosen[num]['gender'],num,'first')
    return chosen

def check_class_validity(chosen):
    
    if config['hero_enabled']:
        chosen[0] = 'hero'
    magical_score = 0
    for c in chosen:
        if classes_dict[c]['type'] == 'magical':
            magical_score += 1
            
    if magical_score < config['minimum_starting_magical']:
        print("classes did not hit minimum magical, rerolling classes")
        chosen = random.choices(classes_first,k=4)
        chosen = check_class_validity(chosen)
        
    jester_score = 0
    for c in chosen:
        if c == 'jester':
            jester_score += 1
            
    if jester_score > config['maximum_starting_jesters']:
        print("classes rolled too many jesters, rerolling classes")
        chosen = random.choices(classes_first,k=4)
        chosen = check_class_validity(chosen)
    return chosen



def promote(char_num, chosen,reroll=False):
    char = chosen[char_num]
    if char['first'] == 'jester' and config['force_jesters_to_sage']:
        char['second'] = 'sage'
        chosen['sage_count'] += 1
        generate_img(char['second'],chosen[char_num]['gender'],char_num,'second')
        return True

    if char['first'] == 'hero' and config['hero_enabled'] == True:
        print("Hero cannot be promoted.")
        return False
    if char['second'] != '' and reroll==False:
        print("Character already leveled up. Use reroll instead.")
        return False
    temp_classes = classes[:]
    if config['promote_enable_jesters'] == False:
        temp_classes.remove("jester")
    try:
        temp_classes.remove(chosen[char_num]['first']) # can't roll same class
    except:
        pass
    if chosen['sage_count'] > config['promote_sage_limit']:
        temp_classes.remove("sage")
    
    new_class = random.choice(temp_classes)
    if new_class == 'sage':
        chosen['sage_count'] += 1
    char['second'] = new_class
    
    generate_img(char['second'],chosen[char_num]['gender'],char_num,'second')
    return True
    
def print_chars(chosen):
    for k in [1,2,3,4]: 
        first = chosen[k]['first']
        second = chosen[k]['second']
        print("{:10}".format("Char #%s (%s): " % (k,chosen[k]['gender'])) + "{:10}".format("%s" % first) + "{:10}".format("->  %s" % second))
              





if config['autosave']:
    print("Autosave set. Every action will save to 'current_chars.save'. Settings can be toggled in 'config.yaml'")
else:
    print("Autosave not set. Settings can be toggled in 'config.yaml'")
    
print("Configs:")
for k, v in config.items():
    print("{:50}".format("%s: " % k) +  "{:10}".format("%s" % v))
    
    
while True:
    print("\n\nChoose an action. Choose from:\nnew | promote 1/2/3/4 | promote all | reroll 1/2/3/4 | reroll all | print | save | load | reload_config | end | help \n")
    raw = input().strip()
    if raw == 'help':
        print('''
        new: roll a new set of starting characters   
        promote 1/2/3/4: use promote [num] to promote a character. \n          intended to be used when character reaches level 20.
        promote all: promotes all characters together
        reroll 1/2/3/4: use if specifically rerolling. this program will \n          not allowed promote 1/2/3/4 and instead must use reroll to specifically do this action.
        reroll all: reroll all characters together
        print: print out current characters
        save: saves latest configuration to 'current_chars.save' in this program's folder
        load: loads latest configuration from 'current_chars.save' in this program's folder    
        reload_config: reloads configuration file
        end: terminate this program
        
        modify 'config.yaml' for setting changes
        ''')
    elif raw == 'load':
        try:
            with open('current_chars.save', 'rb') as f:
                chosen = pickle.load(f)
            print("Load successful:")
            print_chars(chosen)
        except:
            print("Error on load")
    elif raw == 'save':
        try:
            with open('current_chars.save', 'wb') as f:
                pickle.dump(chosen, f)
        except:
            print("Error on save")
    elif raw == 'new':
        chosen = generate_chosen()
        print_chars(chosen)
    elif raw.startswith("promote all"):
        try:
            promote(1,chosen)
            promote(2,chosen)
            promote(3,chosen)
            promote(4,chosen)
            print_chars(chosen)
        except:
            print("Error on promote all")
    elif raw.startswith("reroll all"):
        try:
            promote(1,chosen,reroll=True)
            promote(2,chosen,reroll=True)
            promote(3,chosen,reroll=True)
            promote(4,chosen,reroll=True)
            print_chars(chosen)
        except:
            print("Error on reroll all")
    elif raw.startswith("promote"):
        try:
            flag = promote(int(raw.split(" ")[-1]),chosen)
            if flag:
                print_chars(chosen)
        except:
            print("Error on promote")
    elif raw.startswith("reroll"):
        try:
            promote(int(raw.split(" ")[-1]),chosen,reroll=True)
            print_chars(chosen)
        except:
            print("Error on reroll")
    elif raw == 'print':
        try:
            print_chars(chosen)
        except:
            print("Use 'new' command first")
    elif raw == 'reload_config':
        try:
            with open("config.yaml", 'r') as stream:
                config = yaml.safe_load(stream)
        except:
            print("Invalid config file. Check config.yaml and redownload if necessary.")
    elif raw == 'end' or raw == 'q':
        break
    if config['autosave']:
        try:
            with open('current_chars.save', 'wb') as f:
                pickle.dump(chosen, f)
        except:
            print("Error on save")
