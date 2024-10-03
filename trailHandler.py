


def updateTrail(trail, pos, max_length):
    trail.append([pos[0], pos[1]])
    if len(trail) > max_length:
        trail.pop(0)

