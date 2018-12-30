class Group:
    def __init__(self, units, per_unit_hp, immunity, weakness, attack, attack_type, initiative):
        self.units = units
        self.per_unit_hp = per_unit_hp
        self.immunity = immunity
        self.weakness = weakness
        self.attack = attack
        self.attack_type = attack_type
        self.initiative = initiative
        self.targeted = False
        self.target = None
        self.name = ""
        self.effective_power = self.units * self.attack
        
    def select_target(self, t):
        assert self.target == None
        if t:
            print(self.name," targetting", t.name if t else "no one", self.get_effective_power() * (2 if self.attack_type in t.weakness else 1))
        self.target = t
    
    def do_attack(self):
        if self.units <= 0 or not self.target:
            return
        print(self.name, "attacking", self.target.name)
        self.target.take_damage(self.get_effective_power(), self.attack_type)
        self.targeted = False

    def take_damage(self, damage, damage_type):
#        assert self.units > 0
        if (self.units <= 0):
            return

        if damage_type in self.immunity:
            return
        
        if damage_type in self.weakness:
            damage *= 2

        delta =  damage // self.per_unit_hp
        print(self.name,"taking damage", damage,self.per_unit_hp, self.units, " -> ", end="")
        # while self.units > 0 and damage >= self.per_unit_hp:
        #     damage -= self.per_unit_hp
        #     self.units -= 1
        self.units -= delta
        self.units = max(0, self.units)
        print(self.units, "-", delta)

    def get_effective_power(self):
        assert self.units >= 0
        return max(0, self.units * self.attack)

def strip_parts(p):
    return p.replace(',', '').replace(';','')

def parse_parts(parts, i):
    i += 1 # skip to
    c = []
    
    has_more = "," in parts[i]
    c.append(strip_parts(parts[i]))
    while (has_more):
        i += 1
        has_more = "," in parts[i]
        c.append(strip_parts(parts[i]))

    return c

immune_system = []
infection = []
all_units = []

with open("input.txt", "rt") as file:
    data = file.readlines()

    group = immune_system
    prefix = "Immune"
    for j in range(1, len(data)):
        if data[j].strip() == "":
            continue
        if "Infection" in data[j]:
            group = infection
            prefix = "Infection"
            continue

        desc = data[j].strip()
        parts = desc.replace('(', '').replace(')','').split(' ')
        hp = int(parts[4])
        units = int(parts[0])
        initiative = int(parts[len(parts)-1])
        immunity = []
        weakness = []
        attack = -1
        i = 5
        while True:
            while (parts[i] not in ["weak", "immune", "attack"]):
                i += 1

            if ("weak" in parts[i]):
                i += 1
                weakness =  parse_parts(parts, i)
                print("weaks: ", weakness)
            elif ("immune" in parts[i]):
                i += 1
                immunity =  parse_parts(parts, i)
                print("imm: ", immunity)
            
            if ("attack" in parts[i]):
                break
        i += 3
        attack = int(parts[i])
        attack_type = parts[i+1]

        g = Group(units, hp, immunity, weakness, attack, attack_type, initiative)
        group.append(g)
        g.name = prefix + " Group " + str(len(group))
        all_units.append(g)
    # target

imm_alive = True
inf_alive = True
while imm_alive and inf_alive:
    all_units.sort(key=lambda x: (x.get_effective_power(), x.initiative), reverse=True)

    for imm in all_units:
        print(imm.name,imm.units, imm.get_effective_power(), imm.initiative)

    def get_target(unit, enemy_army):
        targets = []
        for e in enemy_army:
            damage = unit.get_effective_power()
            if e.targeted or e.units <= 0:
                continue
            if unit.attack_type in e.weakness:
                damage *= 2
            if unit.attack_type in e.immunity:
                damage = 0
            targets.append((damage,e))

        targets.sort(key=lambda x:(x[0], x[1].get_effective_power(), x[1].initiative), reverse=True)
        return targets[0][1] if len(targets) > 0 else None

    infection.sort(key=lambda x: (x.get_effective_power(), x.initiative), reverse=True)
    immune_system.sort(key=lambda x: (x.get_effective_power(), x.initiative), reverse=True)

    # find target
    for unit in all_units:
        if unit.get_effective_power() <= 0:
            continue
        target = get_target(unit, immune_system if unit in infection else infection)
        unit.select_target(target)
        if target:
            target.targeted = True

    # attack
    all_units.sort(key=lambda x:x.initiative, reverse=True)
    print ([x.name for x in all_units])
    for u in all_units:
        u.do_attack()
        u.target = None
        u.targeted = False

    imm_alive = sum([1 if x.units > 0 else 0 for x in immune_system]) > 0
    inf_alive = sum([1 if x.units > 0 else 0 for x in infection]) > 0
    print()
    print()
#    imm_alive = False
    
sum = 0
for u in all_units:
    if u.units > 0:
        sum += u.units
        print (u.name, "has ", u.units, " left")

print (sum)