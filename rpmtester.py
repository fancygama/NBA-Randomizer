from __future__ import division
import csv, random

players = []

class Player(object):
    def __init__(self,name,pos,team,orpm,drpm):
        self.name = name.strip()
        self.pos = pos.strip()
        self.team = team.strip()
        self.orpm = float(orpm)
        self.drpm = float(drpm)
    def __str__(self):
        return '%s, %s %s: %s/%s' % (self.name, self.team, self.pos, self.orpm, self.drpm)
    def __repr__(self):
        return self.__str__()

with open('2014-15rpm.csv','rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar = '"')
    for row in reader:
        if len(row) != 0:
            if float(row[4]) >= 20 and float(row[5]) >= 20:
                players.append(Player(row[1],row[2],row[3],row[6],row[7]))

pos = ['PG','SG','SF','PF','C']
east = ['Boston Celtics', 'Brooklyn Nets', 'New York Knicks','Philadelphia 76ers','Toronto Raptors', 'Chicago Bulls', 'Cleveland Cavaliers', 'Detroit Pistons', 'Indiana Pacers', 'Milwaukee Bucks', 'Atlanta Hawks', 'Charlotte Hornets', 'Miami Heat', 'Orlando Magic', 'Washington Wizards']
west = ['Dallas Mavericks', 'Houston Rockets', 'Memphis Grizzlies', 'New Orleans Pelicans', 'San Antonio Spurs', 'Denver Nuggets', 'Minnesota Timberwolves', 'Oklahoma City Thunder', 'Portland Trailblazers', 'Utah Jazz', 'Golden State Warriors', 'Los Angeles Clippers', 'Los Angeles Lakers', 'Phoenix Suns', 'Sacramento Kings']
class Lineup(Player):
    def __init__(self):
        self.name = ''
        l = []
        for p in pos:
            player = random.choice(players)          
            while player.pos != p:
                player = random.choice(players)
            players.remove(player)
            l.append(player)
        self.lineup = l
        orpm,drpm = 105.6,105.6
        for player in l:
            orpm += player.orpm
            drpm -= player.drpm
        orpm = (2 * orpm)/3 + (103.9/3)
        drpm = (2 * drpm)/3 + (105.9/3)
        self.orpm, self.drpm = orpm,drpm
        self.wp = (self.orpm ** 13.91)/(self.orpm ** 13.91 + self.drpm ** 13.91)
    def __str__(self):
        s = self.name + ': '
        for i in range (4): s = s + self.lineup[i].name + ' | '
        s += self.lineup[4].name
        return s
    def __repr__(self):
         return self.__str__()
    def proj_rec(self):
        print self
        wp = self.wp
        w = int(round(82*wp, 0))
        l = 82-w
        print 'ORtg: %s, DRtg: %s, Projected Record: %s-%s, %s' % ('%0.1f' % self.orpm, '%0.1f' % self.drpm, w, l , '%0.3f' % wp)
teams = []
for i in range(30):
    teams.append(Lineup())    
ortg = 0
drtg = 0
for team in teams:
    ortg += team.orpm
    drtg += team.drpm
ortg /= 30
drtg /= 30
artg = (ortg+drtg)/2
for team in teams:
    oquo, dquo = team.orpm /ortg, team.drpm /drtg
    team.orpm = artg * oquo
    team.drpm = artg * dquo
    team.wp = (team.orpm ** 13.91)/(team.orpm ** 13.91 + team.drpm ** 13.91)
print '30 Teams are given 5 random starters (min 20 gp and 20 mpg) and a replacement level bench.'
print 'Who will prevail in this wild new NBA?'
print ''
c = []
for i in range(15):
    t = random.choice(teams)
    teams.remove(t)
    nm = random.choice(east)
    east.remove(nm)
    t.name = nm
    c.append(t)
for t in teams:
    nm = random.choice(west)
    west.remove(nm)
    t.name = nm
c = sorted(c, key = lambda team : team.wp, reverse = True)
teams = sorted(teams, key = lambda team : team.wp, reverse = True)
rk = 1

print ''
print ''
print  'EASTERN CONFERENCE STANDINGS: '
for t in c:
    print ''
    if rk == 9:
        print '_'*75
        print ''
    print str(rk) + '. ',
    t.proj_rec()
    rk += 1

    
rk = 1
print ''
print ''
print  'WESTERN CONFERENCE STANDINGS: '
for t in teams:
    print ''
    if rk == 9:
        print '_' * 75
        print ''
    print str(rk) + '. ',
    t.proj_rec()
    rk += 1

    
