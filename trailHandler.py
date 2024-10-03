


def updateTrail(trail, pos, max_length):
    trail.append([pos[0], pos[1]])
    if (len(trail) > max_length):
        trail.pop(0)

def updateTrails(trails, poses, max_length):
    for i in range(len(trails)):
        updateTrail(trails[i], poses[i], max_length)