import sys
from collections import defaultdict
import numpy as N
import pylab as P
import math

def _blob(x,y,area,colour):
    """
    Draws a square-shaped blob with the given area (< 1) at
    the given coordinates.
    """
    hs = N.sqrt(area) / 2
    xcorners = N.array([x - hs, x + hs, x + hs, x - hs])
    ycorners = N.array([y - hs, y - hs, y + hs, y + hs])
    P.fill(xcorners, ycorners, colour, edgecolor=colour)

def hinton(W, labels=['',''], axes=[[],[]], name="", maxWeight=None):
    """
    Draws a Hinton diagram for visualizing a weight matrix. 
    Temporarily disables matplotlib interactive mode if it is on, 
    otherwise this takes forever.
    """
    reenable = False
    if P.isinteractive():
        P.ioff()
    P.clf()
    height, width = W.shape
    if not maxWeight:
        maxWeight = 2**N.ceil(N.log(N.max(N.abs(W)))/N.log(2))

    P.fill(N.array([0,width,width,0]),N.array([0,0,height,height]),'gray')
    #P.axis('off')
    P.axis('equal')
    P.axis('image')
    P.xlabel(labels[0])
    P.ylabel(labels[1])
    #fig = P.figure()
    #ax = fig.add_subplot(111)
    #ax.set_xticklabels(axes[0])
    #ax.set_yticklabels(axes[1])
    P.xticks(N.arange(len(axes[0]))+0.5, axes[0], fontsize=10)
    P.yticks(N.arange(len(axes[1]))+0.5, axes[1], fontsize=10)
    for x in xrange(width):
        for y in xrange(height):
            _x = x+1
            _y = y+1
            w = W[y,x]
            if w > 0:
                _blob(_x - 0.5, height - _y + 0.5, min(1,w/maxWeight),'white')
            elif w < 0:
                _blob(_x - 0.5, height - _y + 0.5, min(1,-w/maxWeight),'black')
    if reenable:
        P.ion()
    #P.show()
    if name == "":
        P.savefig("hinton.png")
    else:
        P.savefig(name+".png")


i = -1
skip = False
absolute_win_openings = defaultdict(lambda: 0)
relative_win_openings = defaultdict(lambda: defaultdict(lambda: 0))
n_games = defaultdict(lambda: defaultdict(lambda: 0))
absolute_n_games = defaultdict(lambda: 0)
openings = {'P': set(), 'T': set(), 'Z': set()}
loser_opening = ""
f = sys.stdin
if len(sys.argv) > 1:
    f = open(sys.argv[1])
for line in f:
    i += 1
    if skip == True:
        skip = False
        continue
    if (i % 2) == 0: # new match
        if 'Winner Yes' in line: # pass this match b/c we don't know the winner
            skip = True
            continue
        # here we have the loser
        l = line.rstrip(';\n\r').split(';')
        d = dict([e.strip(' ').split(' ') for e in filter(lambda x: len(x)>4, l) if not 'Name' in e[:5]]) # filter is a hack for names with ';'
        assert(d['Winner']=='No')
        loser_opening = d['Opening'].lower()
        loser_race = ''
        if 'Protoss_' in line:
            loser_race = 'P'
        elif 'Terran_' in line:
            loser_race = 'T'
        elif 'Zerg_' in line:
            loser_race = 'Z'
        openings[loser_race].add(loser_opening)

    else:
        # here we have the winner
        l = line.rstrip(';\n\r').split(';')
        try:
            d = dict([e.strip(' ').split(' ') for e in filter(lambda x: len(x)>4, l) if not 'Name' in e[:5]]) # filter is a hack for names with ';'
        except:
            print >> sys.stderr, l
        assert(d['Winner']=='Yes')
        o = d['Opening'].lower()
        winner_race = ''
        if 'Protoss_' in line:
            winner_race = 'P'
        elif 'Terran_' in line:
            winner_race = 'T'
        elif 'Zerg_' in line:
            winner_race = 'Z'
        openings[winner_race].add(o)
        absolute_win_openings[o] += 1
        relative_win_openings[o][loser_opening] += 1
        n_games[o][loser_opening] += 1
        n_games[loser_opening][o] += 1
        absolute_n_games[o] += 1
        absolute_n_games[loser_opening] += 1

r = defaultdict(lambda: defaultdict(lambda: 0.0))
l = []
for k, v in openings.iteritems():
    if v == set():
        openings.pop(k)
        break
for k, v in openings.iteritems(): # for mirror match-ups
    if v == set():
        openings.pop(k)
        break

#for op1 in openings[list(openings)[0]]:
#    ll = []
#    for op2 in openings[list(openings)[len(openings)-1]]:
#        v = relative_win_openings[op1][op2] #
#        if n_games[op1][op2] == 0:
#            r[op1][op2] = 0.0
#        else:
#            ratio = v*1.0 / n_games[op1][op2]
#            r[op1][op2] = ratio - 0.5
#        ll.append(r[op1][op2])
#    l.append(ll)

#print absolute_n_games
#print "============"
#print absolute_win_openings
#print "============"
#print n_games
#print "============"
#print relative_win_openings
#print "============"

import matplotlib.pyplot as plt
fig = plt.figure()
plotnumber = 211
fig.subplots_adjust(wspace=0.3, hspace=0.6)
width = 0.6
race1 = ""
for race, ops in openings.iteritems(): 
    ax = fig.add_subplot(plotnumber)
    ax.set_ylabel("win ratio (P(win|opening))")
    ax.set_xlabel("openings")
    ind = N.arange(len(ops))
    ax.set_xticks(ind+width/2)
    ax.set_xticklabels(list(ops))
    values = []
    for op in ops:
        if absolute_n_games[op] > 9:
            values.append(absolute_win_openings[op]*1.0 / absolute_n_games[op])
        else:
            values.append(0.5)
    print "============"
    print "Openings absolute win rates:"
    print list(ops)
    print values
    print "============"
    ax.bar(ind, values, width, color='r')
    plotnumber += 1
    if race1 == "":
        race1 = race
matchup = race1+'v'+race
plt.savefig("absolute_win_rates_openings"+matchup+".png")

print "=================== contingency latex table ==================="
print ""
print "\\begin{tabular}{|l|"+''.join(['c' for i in range(len(openings[list(openings)[0]]))])+"|}"
print "\\hline"
print " & "+' & '.join(list(openings[list(openings)[0]])) + "\\\\"
print "\\hline"
l = []
for op2 in openings[list(openings)[len(openings)-1]]:
    ll = []
    print op2 + ' & ',
    tmp = ""
    for op1 in openings[list(openings)[0]]:
        v = relative_win_openings[op1][op2] #
        if n_games[op1][op2] < 10:
            tmp += "NED" + ' & '
            ll.append(0.0)
        else:
            ratio = v*1.0 / n_games[op1][op2]
            tmp += str(ratio) + ' & '
            ll.append(ratio-0.5)
    tmp = tmp[:-2]
    tmp += '\\\\'
    print tmp
    l.append(ll)
print "\\hline"
print "NED stands for Not Enough Data"
print "Win rates of columns vs lines"

print ""
print ">>> Total Games:", sum(absolute_n_games.itervalues())/2
print ""

hinton(N.array(l), axes=[list(openings[list(openings)[0]]),list(openings[list(openings)[len(openings)-1]])], name="contingency"+matchup)
