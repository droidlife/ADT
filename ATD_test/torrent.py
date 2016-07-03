import re, os

s = raw_input('enter the torrent to be search : ').lower()
path = os.getcwd() + '/.follow'

if re.match(r'search\b', s, flags=re.IGNORECASE):
    print 'searching for torrent ... '
elif re.match(r'follow\b', s, flags=re.IGNORECASE):

    print 'torrent added...\n new torrent will be downloaded automatically'
    file_follow = open(path, 'a')
    file_follow.write(s[7:] + '\n')
    file_follow.close()


elif re.match(r'print follow\b', s, flags=re.IGNORECASE):
    file = open(path, 'r')
    for line in file:
        print line
    file.close
elif re.match(r'unfollow\b', s, flags=re.IGNORECASE):
    s = s[9:]
    file = open(path, 'r')
    lines = file.readlines()
    file.close()
    file = open(path, 'w')
    for line in lines:
        if s != line.strip():
            print line
            file.write(line)
    file.write("\n")
    file.close()
    print 'unfollwing '+s
else:
    print 'searching for torrent..'
