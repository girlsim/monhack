import pygame
import random
import math
import os, sys

from pygame.locals import *

import features
import tiles
import player

from helpers import *

class Main:

    def __init__(self):

        pygame.init()
        self.screen = pygame.display.set_mode((720,360))

        self.tile_group = pygame.sprite.Group()
        self.tile_dict = {}
        self.player = player.Nymph((0,0))
        self.player_group = pygame.sprite.RenderPlain((self.player))

        self.generate()

    def run(self):

        while True:
            # display stuff--move to own file later?
            pygame.display.flip()
            self.screen.fill((0,0,0))
            self.tile_group.draw(self.screen)
            self.player_group.draw(self.screen)

            # events
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN: # debug
                for tile in self.tile_group:
                    if tile.rect.collidepoint(event.pos):
                        print("%d,%d" % tile.coords)
            if event.type == pygame.KEYDOWN:
                if event.key == K_RIGHT: # TODO: right keys! and dvorak stuff...
                    self.player.checkMove(self.player.x+1,self.player.y,self.tile_dict)
                elif event.key == K_DOWN:
                    self.player.checkMove(self.player.x,self.player.y+1,self.tile_dict)
                elif event.key == K_LEFT:
                    self.player.checkMove(self.player.x-1,self.player.y,self.tile_dict)
                elif event.key == K_UP:
                    self.player.checkMove(self.player.x,self.player.y-1,self.tile_dict)


    # generates an example level
    def generate(self):

        # generate rooms
        # WARNING! HARDCODED GLOBALS!
        # rooms: 4-8
        rooms = []
        numRooms = random.randint(4,8)
        numOverlapped = 0 # safeguard to make sure we don't get stuck
        print("Generating %d rooms..." % numRooms)
        while len(rooms) < numRooms:
            # HARDCODED GLOBALS
            # map size = 40x20
            x = random.randint(1,34) # can't go off the map...
            y = random.randint(1,14) # also, don't allow walls against map edge
            # note that this generation is very stupid!
            newRoom = features.Room([x,y])
            for room in rooms:
                if room.doesOverlap(newRoom):
                    numOverlapped += 1
                    break
            else:
                numOverlapped = 0
                rooms.append(newRoom)
                print("Room %d generated successfully." % len(rooms))
            if numOverlapped == 100: # WARNING! technically a global...
                print("Failed to generated room %d! Giving up." % (len(rooms)+1))
                break

        # generate passages
        # basic algorithm: - index rooms, do union find, add a few extra paths
        reps = []
        ranks = []
        for i in range (0,len(rooms)):
            reps.append(i)
            ranks.append(0)
        paths = []
        # union find generating paths! remember, we need N-1 links for N objects...
        print("Generating %d-path passage tree..." % (len(rooms)-1))
        while len(paths) < len(rooms)-1:
            startRoom = random.randint(0,len(rooms)-1)
            endRoom = random.randint(0,len(rooms)-1)
            if startRoom == endRoom: # no paths going nowhere!
                continue
            # union find magic happens here
            startRoomRep = self.getRep(startRoom, reps)
            endRoomRep = self.getRep(endRoom, reps)
            if startRoomRep == endRoomRep: # already connected
                continue
            # otherwise, make the connection and change reps
            if ranks[startRoomRep] > ranks[endRoomRep]:
                reps[endRoomRep] = startRoomRep
            elif ranks[startRoomRep] < ranks[endRoomRep]:
                reps[startRoomRep] = endRoomRep
            else:
                reps[startRoomRep] = endRoomRep
                ranks[endRoomRep] += 1
            paths.append(features.Passage(rooms[startRoom], rooms[endRoom]))
            print("Path %d generated successfully." % len(paths))
 
        # just for fun: add some extra paths, with no restrictions
        for i in range(0, random.randint(0,3)):
            print("Adding additional path %d." % i)
            paths.append(features.Passage(rooms[random.randint(0,len(rooms)-1)],
                                          rooms[random.randint(0,len(rooms)-1)]))

        path_tiles = []
        covered = []
        # generate path tilelist
        for path in paths:
            # it's a little messy to generate doors right here, but it saves time...
            for i in range (0,2):
                if path.door_dirs[i] == 0:
                    new_door = tiles.DoorR(path.doors[i])
                elif path.door_dirs[i] == 1:
                    new_door = tiles.DoorD(path.doors[i])
                elif path.door_dirs[i] == 2:
                    new_door = tiles.DoorL(path.doors[i])
                else:
                    new_door = tiles.DoorU(path.doors[i])
                self.tile_group.add(new_door)
                self.tile_dict[new_door.coords] = new_door

            nodes = [features.PassageNode(list(path.start_tile))]
            curr = list(path.start_tile)
            end = path.end_tile
            travel_axis = -1 # -1 = not started, 0 = big, 1 = small
            travel_mode = "cross" # cross, skirt
            last_step = 0
            while curr != end:
                big = 0
                small = 1
                if abs(curr[0]-end[0]) < abs(curr[1]-end[1]):
                    big = 1
                    small = 0
                if travel_axis == -1:
                    travel_axis = big
                step = 1
                if curr[travel_axis] > end[travel_axis]:
                    step = -1
                next = list(curr)
                next[travel_axis] += step
                if travel_mode == "cross":
                    while (not self.isInRoom(next, rooms)
                        and curr[travel_axis] != end[travel_axis] and
                        next[0] >= 0 and next[0] <= 39 and next[1] >= 0 and
                        next[1] <= 19):
                        curr = list(next)
                        next[travel_axis] += step
                    if (curr[travel_axis] == end[travel_axis] and
                        not self.isInRoom(next, rooms)):
                        travel_axis = -1
                    else:
                        travel_mode = "skirt"
                        last_step = step
                elif travel_mode == "skirt":
                    not_travel = 0
                    if travel_axis == 0:
                        not_travel = 1
                    side = list(curr)
                    side[not_travel] += last_step
                    while (self.isInRoom(side, rooms) and curr != end and
                        next[0] >= 0 and next[0] <= 39 and next[1] >= 0 and
                        next[1] <= 19):
                        curr = list(next)
                        side[travel_axis] = curr[travel_axis]
                        next[travel_axis] += step
                    travel_mode = "cross"
                nodes.append(features.PassageNode(list(curr)))
                nodes[len(nodes)-2].next = nodes[len(nodes)-1]
                if travel_axis == 0:
                    travel_axis = 1
                elif travel_axis == 1:
                    travel_axis = 0

            for node in nodes:
                if node.next != 0:
                    for tile in self.tilesBetween(node.coords, node.next.coords):
                        path_tiles.append(tile)
        
                        
        # generate tiles...
        for room in rooms:
            # iterate from x coord of ul to x coord of lr
            for x in range (room.corners[0][0], room.corners[3][0]+1):
                # from y coord of ul to y coord of lr
                for y in range (room.corners[0][1], room.corners[3][1]+1):
                    if not (x,y) in self.tile_dict:
                        vert_wall = x == room.corners[0][0] or x == room.corners[3][0]
                        hori_wall = y == room.corners[0][1] or y == room.corners[3][1]
                        newTile = tiles.Floor((x,y)) # is this actually more efficient?
                        # both: it's a corner
                        if vert_wall and hori_wall:
                            newTile = tiles.WallCorner((x,y))
                        elif vert_wall:
                            newTile = tiles.WallUD((x,y))
                        elif hori_wall:
                            newTile = tiles.WallLR((x,y))
                        self.tile_group.add(newTile)
                        self.tile_dict[newTile.coords] = newTile
        # and the passages
        for tile in path_tiles:
            if not (tile[0],tile[1]) in self.tile_dict:
                newTile = tiles.Passage((tile[0],tile[1]))
                self.tile_dict[newTile.coords] = newTile
                self.tile_group.add(newTile)

        # add in player
        room = rooms[random.randint(0,len(rooms)-1)]
        x = random.randint(room.corners[0][0]+1,room.corners[3][0]-1)
        y = random.randint(room.corners[0][1]+1,room.corners[3][1]-1)
        self.player.move(x,y)


 
    # helpers for the above
    # find a room's representative
    def getRep(self, room, reps):
        while reps[room] != room:
            room = reps[room]
        return room

    # determine if the given tile is in any of the generated rooms
    # note that this works because the step size is never larger than the min
    # possible room width. BE CAREFUL if messing with generation params!
    def isInRoom(self, tile, rooms):
        for room in rooms:
            if room.contains(tile):
                return True
        return False

    def isInTiles(self, tile, tiles):
        for coord in tiles:
            if tile == coord:
                return True
        return False

    # get the tiles between the given two coords
    # they must differ on only one axis!
    # includes the end coord and start coord 
    def tilesBetween(self, start, end):
        ret = []
        diffAxis = 0
        sameAxis = 1
        if start[1] != end[1]:
            diffAxis = 1
            sameAxis = 0
        if start[diffAxis] > end[diffAxis]:
            for i in range(end[diffAxis], start[diffAxis] + 1):
                coord = list(end)
                coord[diffAxis] = i
                ret.append(coord)
        else:
            for i in range(start[diffAxis], end[diffAxis] + 1):
                coord = list(end)
                coord[diffAxis] = i
                ret.append(coord)
        return ret


# window init stuff
if __name__ == "__main__":
    MainWindow = Main()
    MainWindow.run()
