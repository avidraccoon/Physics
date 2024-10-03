


def updateTrail(trail, pos, max_length):
    trail.append(pos)
    if len(trail) > max_length:
        trail.pop(0)

def updateTrails(trails, planets, max_length):
    for i in range(len(trails)):
        updateTrail(trails[i], planets[i].verlet_object.current_position, max_length)