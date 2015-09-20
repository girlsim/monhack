import pygame
import random

from helpers import *

class Room:

    def __init__(self, ul_corner):

        self.corners = [] # ul, ll, ur, lr
        self.makeCorners(ul_corner)

    # sets room corners
    def makeCorners(self, ul_corner):

        # WARNING! HARDCODED GLOBALS! THIS IS BAD
        # width/height: 4-8
        # map size = 40x20
        height = random.randint(4,8)
        width = random.randint(4,8)
        if ul_corner[0]+width > 38: # cannot have walls against map edge
            width = 38 - ul_corner[0]
        if ul_corner[1]+height > 18:
            height = 18 - ul_corner[1]
        self.corners.append(ul_corner)
        self.corners.append([ul_corner[0], ul_corner[1]+height])
        self.corners.append([ul_corner[0]+width, ul_corner[1]])
        self.corners.append([ul_corner[0]+width, ul_corner[1]+height])

    # checks if a point is inside the room
    def contains(self, point):
        
        if point[0] < self.corners[0][0]:
            return False
        if point[0] > self.corners[2][0]:
            return False
        if point[1] < self.corners[0][1]:
            return False
        if point[1] > self.corners[3][1]:
            return False
        return True

    # checks if the given room overlaps with this one
    def doesOverlap(self, room):
        # checks if:
        # - all corners are to the right of this room
        # - all corners are below this room
        # - ...etc
        # if none of these four are the case, the rooms overlap
        # also ensures that no rooms are generated with walls touching
        for corner in room.corners:
            if corner[0] <= self.corners[2][0]+1:
                break
        else:
            return False
        for corner in room.corners:
            if corner[1] <= self.corners[1][1]+1:
                break
        else:
            return False
        for corner in room.corners:
            if corner[0] >= self.corners[0][0]-1:
                break
        else:
            return False
        for corner in room.corners:
            if corner[1] >= self.corners[0][1]-1:
                break
        else:
            return False
        return True
        # jesus CHRIST that is ugly

class Passage:

    def __init__(self, start_room, end_room):

        start = self.pickWallSpace(start_room)
        end = self.pickWallSpace(end_room)
        self.start_tile = [start[0], start[1]]
        self.end_tile = [end[0], end[1]]
        self.doors = [(start[2], start[3]), (end[2], end[3])]
        self.door_dirs = [start[4], end[4]]

    def pickWallSpace(self, room):
        # note that this actually picks a spot NEXT TO the wall
        # first, pick which wall it will be on
        wall = random.randint(0,3) # r, d, l, u
        # get the length of the wall
        length = 0
        if wall == 0 or wall == 2:
            length = room.corners[3][1] - room.corners[2][1]
        else: # wall == 1 or wall == 3
            length = room.corners[3][0] - room.corners[1][0]
        # pick a random spot on the wall. do NOT pick corners
        space = random.randint(1,length-1)
        # now turn all that into coords
        x = 0
        y = 0
        door_x = 0
        door_y = 0
        if wall == 0:
            x = room.corners[2][0] + 1
            y = room.corners[2][1] + space
            door_x = x - 1
            door_y = y
        elif wall == 2:
            x = room.corners[0][0] - 1
            y = room.corners[0][1] + space
            door_x = x + 1
            door_y = y
        elif wall == 1:
            x = room.corners[1][0] + space
            y = room.corners[1][1] + 1
            door_x = x
            door_y = y - 1
        else: # wall == 3
            x = room.corners[0][0] + space
            y = room.corners[0][1] - 1
            door_x = x
            door_y = y + 1
        return [x,y,door_x,door_y,wall]

class PassageNode:

    def __init__(self, coords):

        self.coords = coords
        self.prev = 0
        self.next = 0




