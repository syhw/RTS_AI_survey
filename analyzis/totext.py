import sys

# Python License 2.0.1 http://www.python.org/download/releases/2.0.1/license/ 
# Copyright 2012 Gabriel Synnaeve

# takes a .lmr file as argument 1 (or stdin) and dumps a txt file with 
# one line for each players for each game as [building_name time_seconds; ...]
# counts buildings up to the 4th, counts expansions (not the first town hall)
# TODO less brute

f = sys.stdin
o = sys.stdout
do_bots = False
do_races = False
if len(sys.argv) > 1:
    f = open(sys.argv[1], 'r')
    o = open(sys.argv[1][:-3]+'txt', 'w')
    if "-bots" in sys.argv:
        do_bots = True
    if "-races" in sys.argv:
        do_races = True


header = True
body = False
loser = ""
names = {}
files_bots = {}
files_races = {}
races = {}
time_had = {}
buildings = {'T' : ['Expansion', 'Comsat_Station', 'Nuclear_Silo', 'Supply_Depot', 'Refinery', 'Barracks', 'Academy', 'Factory', 'Starport', 'Control_Tower', 'Science_Facility', 'Covert_Ops', 'Physics_Lab', 'Machine_Shop', 'Engineering_Bay', 'Armory', 'Missile_Turret', 'Bunker'],
        'P' : ['Expansion', 'Robotics_Facility', 'Pylon', 'Assimilator', 'Observatory', 'Gateway', 'Photon_Cannon', 'Citadel_of_Adun', 'Cybernetics_Core', 'Templar_Archives', 'Forge', 'Stargate', 'Fleet_Beacon', 'Arbiter_Tribunal', 'Robotics_Support_Bay', 'Shield_Battery'], 
        'Z' : ['Overlord', 'Infested_Command_Center', 'Expansion', 'Lair', 'Hive', 'Nydus_Canal', 'Hydralisk_Den', 'Defiler_Mound', 'Greater_Spire', 'Queens_Nest', 'Evolution_Chamber', 'Ultralisk_Cavern', 'Spire', 'Spawning_Pool', 'Creep_Colony', 'Spore_Colony', 'Sunken_Colony', 'Extractor']}
doubling = {'T' : ['Expansion', 'Refinery', 'Barracks', 'Factory', 'Armory'],
        'P' : ['Expansion', 'Pylon', 'Assimilator', 'Gateway'],
        'Z' : ['Expansion', 'Extractor']}
tripling = {'T' : ['Expansion', 'Barracks', 'Factory'],
        'P' : ['Expansion', 'Gateway'],
        'Z' : ['Expansion']}
quadrupling = {'T' : ['Expansion'],
        'P' : ['Expansion', 'Gateway'],
        'Z' : ['Expansion']}
units = {'T' : ['SCV', 'Dropship', 'Marine', 'Ghost', 'Vulture', 'Goliath', 'Siege_Tank_Tank_Mode', 'Wraith', 'Science_Vessel', 'Battlecruiser', 'Siege_Tank_Siege_Mode', 'Firebat', 'Medic', 'Valkyrie' ], 
        'P' : ['Probe', 'Shuttle', 'Observer', 'Dragoon', 'Zealot', 'Archon', 'Reaver', 'High_Templar', 'Arbiter', 'Carrier', 'Scout', 'Dark_Archon', 'Corsair', 'Dark_Templar'], 
        'Z' : ['Drone', 'Overlord', 'Zergling', 'Devourer', 'Guardian', 'Ultralisk', 'Queen', 'Hydralisk', 'Mutalisk', 'Scourge', 'Lurker', 'Defiler']}
rchupgs = {'T' : ['Spider_Mines', ],
        'P' : ['Ground_Weapons', 'Zealot_Speed', 'Psionic_Storm', 'Dragoon_Range'],
        'Z' : ['Zergling_Speed', 'Hydralisk_Speed', 'Hydralisk_Range']}

def write(tb, fo):
    #print tb
    def write_for_one(p, t):
        for e in buildings[races[p][0]]:
            b = races[p] + '_' + e
            twr = b + ' ' + str(t.get(b, -1)/24) + '; '
            fo.write(twr)
            if do_bots:
                files_bots[names[p]].write(twr)
            if do_races:
                files_races[races[p]].write(twr)
        for e in doubling[races[p][0]]:
            b = races[p] + '_' + e + '2'
            twr = b + ' ' + str(t.get(b, -1)/24) + '; '
            fo.write(twr)
            if do_bots:
                files_bots[names[p]].write(twr)
            if do_races:
                files_races[races[p]].write(twr)
        for e in tripling[races[p][0]]:
            b = races[p] + '_' + e + '3'
            twr = b + ' ' + str(t.get(b, -1)/24) + '; '
            fo.write(twr)
            if do_bots:
                files_bots[names[p]].write(twr)
            if do_races:
                files_races[races[p]].write(twr)
        for e in quadrupling[races[p][0]]:
            b = races[p] + '_' + e + '4'
            twr = b + ' ' + str(t.get(b, -1)/24) + '; '
            fo.write(twr)
            if do_bots:
                files_bots[names[p]].write(twr)
            if do_races:
                files_races[races[p]].write(twr)
        for e in units[races[p][0]]:
            u = races[p] + '_' + e
            twr = u + ' ' + str(t.get(u, -1)/24) + '; '
            fo.write(twr)
            if do_bots:
                files_bots[names[p]].write(twr)
            if do_races:
                files_races[races[p]].write(twr)
        for e in rchupgs[races[p][0]]:
            r = races[p] + '_' + e
            twr = r + ' ' + str(t.get(r, -1)/24) + '; '
            fo.write(twr)
            if do_bots:
                files_bots[names[p]].write(twr)
            if do_races:
                files_races[races[p]].write(twr)
        if do_bots:
            files_bots[names[p]].write('\n')
        if do_races:
            files_races[races[p]].write('\n')
        fo.write('\n')
    if loser != "":
        write_for_one(loser, tb.pop(loser))
    for p, t in tb.iteritems():
        write_for_one(p, t)

for line in f:
    if not header and line[0] == '_':
        write(time_had, o)
        time_had = {}
        names = {}
        races = {}
        header = True
        body = False
        loser = ""
        o.write('\n') # separate games
    if header and line[0].isdigit():
        header = False
        body = True
    if header:
        if "Human" in line: # lol
            l = line.split(',')
            names[l[-6]] = l[0][1:]
            if do_bots and not l[0][1:] in files_bots:
                files_bots[l[0][1:]] = open(l[0][1:]+".txt", 'w')
            time_had[l[-6]] = {}
            if l[-5] == 'P':
                races[l[-6]] = "Protoss"
            elif l[-5] == 'T':
                races[l[-6]] = "Terran"
            elif l[-5] == 'Z':
                races[l[-6]] = "Zerg"
            if do_races and not races[l[-6]] in files_races:
                files_races[races[l[-6]]] = open(races[l[-6]]+'_'+l[-5]+".txt", 'w')
    elif body:
        l = line.split(',')
        if "Build" in line or ("Train" in line and "Overlord" in line):
            bname = l[-1].rstrip('\r\n')
            if bname == 'Hatchery' or bname == 'Command Center' or bname == 'Nexus':
                bname = 'Expansion'
            plyr = l[l.index("Build") - 1]
            building = races[plyr] + '_' + bname.replace(' ', '_')
            if not building in time_had[plyr]:
                time_had[plyr][building] = max(24, int(l[0])) # in frames
            elif not building+'2' in time_had[plyr]:
                time_had[plyr][building+'2'] = max(24, int(l[0]))
            elif not building+'3' in time_had[plyr]:
                time_had[plyr][building+'3'] = max(24, int(l[0]))
            elif not building+'4' in time_had[plyr]:
                time_had[plyr][building+'4'] = max(24, int(l[0]))
        if "Train" in line:
            uname = l[-1].rstrip('\r\n')
            unit = races[l[-5]] + '_' + uname.replace(' ', '_')
            if not unit in time_had[l[-5]]:
                time_had[l[-5]][unit] = max(24, int(l[0]))
        if "Upgrade" in line or "Research" in line:
            rname = l[-1].rstrip('\r\n')
            if '(' in rname:
                rname = rname.split('(')[1].rstrip(')')
            rchupg = ""
            if "Weapons" in rname:
                rchupg += rname.replace(' ', '_')
            else:
                rchupg += races[l[-5]] + '_' + rname.replace(' ', '_')
            if not rchupg in time_had[l[-5]]:
                time_had[l[-5]][rchupg] = max(24, int(l[0]))
            if not rchupg+'2' in time_had[l[-5]]:
                time_had[l[-5]][rchupg+'2'] = max(24, int(l[0]))
            if not rchupg+'3' in time_had[l[-5]]:
                time_had[l[-5]][rchupg+'3'] = max(24, int(l[0]))
        if "Leaving" in line and "quit" in line and loser == "":
            loser = l[-5]

if do_bots:
    for p, f in files_bots.iteritems():
        f.close()
if do_races:
    for p, f in files_races.iteritems():
        f.close()
o.close()

