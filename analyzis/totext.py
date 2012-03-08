import sys

# Python License 2.0.1 http://www.python.org/download/releases/2.0.1/license/ 
# Copyright 2012 Gabriel Synnaeve

# takes a .lmr file as argument 1 (or stdin) and dumps a txt file with 
# one line for each players for each game as [building_name time_seconds; ...]
# counts buildings up to the 4th, counts expansions (not the first town hall)
# TODO less brute

f = sys.stdin
o = sys.stdout
if len(sys.argv) > 1:
    f = open(sys.argv[1], 'r')
    o = open(sys.argv[1][:-3]+'txt', 'w')

header = True
body = False
names = {}
races = {}
time_built = {}
buildings = {'T' : ['Expansion', 'Comsat_Station', 'Nuclear_Silo', 'Supply_Depot', 'Refinery', 'Barracks', 'Academy', 'Factory', 'Starport', 'Control_Tower', 'Science_Facility', 'Covert_Ops', 'Physics_Lab', 'Machine_Shop', 'Engineering_Bay', 'Armory', 'Missile_Turret', 'Bunker'],
        'P' : ['Expansion', 'Robotics_Facility', 'Pylon', 'Assimilator', 'Observatory', 'Gateway', 'Photon_Cannon', 'Citadel_of_Adun', 'Cybernetics_Core', 'Templar_Archives', 'Forge', 'Stargate', 'Fleet_Beacon', 'Arbiter_Tribunal', 'Robotics_Support_Bay', 'Shield_Battery'], 
        'Z' : ['Overlord', 'Infested_Command_Center', 'Expansion', 'Lair', 'Hive', 'Nydus_Canal', 'Hydralisk_Den', 'Defiler_Mound', 'Greater_Spire', 'Queens_Nest', 'Evolution_Chamber', 'Ultralisk_Cavern', 'Spire', 'Spawning_Pool', 'Creep_Colony', 'Spore_Colony', 'Sunken_Colony', 'Extractor']}

def write(tb, fo):
    print tb
    for p, t in tb.iteritems():
        for e in buildings[races[p][0]]:
            b = races[p] + '_' + e
            fo.write(b + ' ' + str(int(t.get(b, '0'))/24) + '; ')
        for e in buildings[races[p][0]]:
            b = races[p] + '_' + e + '2'
            fo.write(b + ' ' + str(int(t.get(b, '0'))/24) + '; ')
        for e in buildings[races[p][0]]:
            b = races[p] + '_' + e + '3'
            fo.write(b + ' ' + str(int(t.get(b, '0'))/24) + '; ')
        for e in buildings[races[p][0]]:
            b = races[p] + '_' + e + '4'
            fo.write(b + ' ' + str(int(t.get(b, '0'))/24) + '; ')
        fo.write('\n')

for line in f:
    if not header and line[0] == '_':
        write(time_built, o)
        time_built = {}
        names = {}
        races = {}
        header = True
        body = False
    if header and line[0].isdigit():
        header = False
        body = True
    if header:
        if "Human" in line: # lol
            l = line.split(',')
            names[l[1]] = l[0][1:]
            time_built[l[1]] = {}
            if l[2] == 'P':
                races[l[1]] = "Protoss"
            elif l[2] == 'T':
                races[l[1]] = "Terran"
            elif l[2] == 'Z':
                races[l[1]] = "Zerg"
    elif body:
        if "Build" in line:
            l = line.split(',')
            bname = l[-1].rstrip('\r\n')
            if bname == 'Hatchery' or bname == 'Command Center' or bname == 'Nexus':
                bname = 'Expansion'
            building = races[l[2]] + '_' + bname.replace(' ', '_')
            if not building in time_built:
                time_built[l[2]][building] = l[0] # in frames
            elif not building+'2' in time_built:
                time_built[building+'2'] = l[0]
            elif not building+'3' in time_built:
                time_built[building+'3'] = l[0]
            elif not building+'4' in time_built:
                time_built[building+'4'] = l[0]



