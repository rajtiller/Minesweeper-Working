import random
import math
initials = ['Rohan', 'Raj', 'Deepa', 'Prema',
            'Meera', 'Alisha', 'Nina', 'Tisha', 'Rishi', "Mike"]  # Tisha, Prema ,Meera,Nina Paid, Rohan, Rishi
# I paid out Me, Rohan, Meera
nameDict = {}
nums = ['         0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
print('Eagles=>' + "        ".join(nums) + '\nChiefs \/')
for name in initials:
    nameDict[name] = 0
while max(*nameDict.values()) != 10 and min(*nameDict.values()) != 10:
    lines = []
    for line in range(10):
        currLine = '       ' + str(line) + '     '
        for square in range(10):
            name = random.choice(initials)
            while nameDict[name] >= 10:
                name = random.choice(initials)
            nameDict[name] += 1
            currLine += '|{:^8}'.format(name)
        currLine += '|\n--------------------------------------------------------------------------------------------------------'
        lines.append(currLine)
    if max(*nameDict.values()) == 10 and min(*nameDict.values()) == 10:
        print("\n".join(lines))
        break
    nameDict = {}
    for name in initials:
        nameDict[name] = 0
