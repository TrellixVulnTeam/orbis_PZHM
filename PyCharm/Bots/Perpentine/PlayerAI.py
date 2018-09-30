"""PlayerAI"""
from PythonClientAPI.game.PointUtils import *
from PythonClientAPI.game.Entities import FriendlyUnit, EnemyUnit, Tile
from PythonClientAPI.game.Enums import Team
from PythonClientAPI.game.World import *
from PythonClientAPI.game.TileUtils import TileUtils
from PythonClientAPI.game.PathFinder import *
from copy import  deepcopy

class PlayerAI:
    """
    PlayerAI
    """

    def __init__(self):
        """Initialize! """
        self.turn_count = 0             # game turn count
        self.target = None              # target to send unit to!
        self.outbound = True            # is the unit leaving, or returning?
        self.units_from_territory_edge = -1            # body length of player currently
        self.current_direction = ''
        self.initial_quadrant = 0
        self.initial_ai_moves = 0
        self.has_killed = False
        self.turns_since_kill = 0


    # def get_dic(self, dic, friendly_unit, world):
    #     """
    #     decide direction when start or make a turn
    #     :param dic: virtical or horizontal
    #     :type dic: String
    #     :return: None
    #     :rtype: None
    #     """
    #     if dic == "Virtical":
    #         # If player is below or equal to half the height of the map, go up
    #         if friendly_unit.position[1] >= 14:
    #             # Set target to point 1 unit above player
    #             pointTargetted = (friendly_unit.position[0], friendly_unit.position[1] - 1)
    #
    #
    #             self.target = world.position_to_tile_map[pointTargetted]
    #             self.current_direction = 'N'
    #         # other wise go down
    #         else:
    #             # Set target to point 1 unit below player
    #             pointTargetted = (friendly_unit.position[0], friendly_unit.position[1] + 1)
    #             self.target = world.position_to_tile_map[pointTargetted]
    #             self.current_direction = 'S'
    #     else:
    #         # If player is below or equal to half the height of the map, go up
    #         if friendly_unit.position[0] >= 14:
    #             # Set target to point 1 unit above player
    #             pointTargetted = (friendly_unit.position[0] + 1, friendly_unit.position[1])
    #             self.target = world.position_to_tile_map[pointTargetted]
    #             self.current_direction = 'E'
    #         # other wise go down
    #         else:
    #             # Set target to point 1 unit below player
    #             pointTargetted = (friendly_unit.position[0] - 1, friendly_unit.position[1])
    #             self.target = world.position_to_tile_map[pointTargetted]
    #             self.current_direction = 'W'



    def do_move(self, world, friendly_unit, enemy_units):
        """
        This method is called every turn by the game engine.
        Make sure you call friendly_unit.move(target) somewhere here!

        Below, you'll find a very rudimentary strategy to get you started.
        Feel free to use, or delete any part of the provided code - Good luck!

        :param world: world object (more information on the documentation)
            - world: contains information about the game map.
            - world.path: contains various pathfinding helper methods.
            - world.util: contains various tile-finding helper methods.
            - world.fill: contains various flood-filling helper methods.

        :param friendly_unit: FriendlyUnit object
        :param enemy_units: list of EnemyUnit objects
        """

        initial_translation = 11
        nums_turns_since_kill = 20
        print(self.outbound)


        def is_point_enemy(point):
            return world.position_to_tile_map[point].is_enemy
        #
        # if self.turn_count == 0:
            # self.get_dic('Virtical', friendly_unit, world)

        # Initialize initial quadrant
        if self.turn_count == 0:
            if friendly_unit.position == (3,3):
                self.initial_quadrant = 1
            if friendly_unit.position == (26,3):
                self.initial_quadrant = 2
            if friendly_unit.position == (3,26):
                self.initial_quadrant = 3
            if friendly_unit.position == (26,26):
                self.initial_quadrant = 4

        self.turn_count += 1

        #self.target = world.position_to_tile_map[world.util.get_closest_point_from(friendly_unit.position, is_point_enemy)]

        # potential_dangers = set()
        #
        # for i in range(-self.units_from_territory_edge, self.units_from_territory_edge + 1):
        #     for j in range(-self.units_from_territory_edge, self.units_from_territory_edge + 1):
        #         if 29 > friendly_unit.position[0] + i > 0 and 29 > friendly_unit.position[1] + j > 0:
        #             potential_dangers.add((friendly_unit.position[0] + i, friendly_unit.position[1] + j))
        # for i in potential_dangers:
        #     if not world.position_to_tile_map[i].is_neutral:
        #         if self.current_direction == 'N' or self.current_direction == "S":
        #             self.get_dic("H", friendly_unit, world)
        #         else:
        #             self.get_dic("Virtical", friendly_unit, world)
        #
        # next_move = self.target.position





        # if unit is dead, stop making moves.
        if friendly_unit.status == 'DISABLED':
            print("Turn {0}: Disabled - skipping move.".format(str(self.turn_count)))
            self.target = None
            self.outbound = True
            return

        #HARD CODE THE INITIAL TURNS TO GET A GOOD POSITION
        if self.turn_count <= 4*(initial_translation - 1):
            if self.initial_quadrant == 1:
                self.outbound = True
                self.target = world.position_to_tile_map[(3,3 + initial_translation)]
                if self.turn_count == initial_translation:
                    self.initial_ai_moves += 1
                elif self.initial_ai_moves == 1:
                    self.target = world.position_to_tile_map[(3 + initial_translation, 3 + initial_translation)]
                    if self.turn_count == (2 * initial_translation)-1:
                        self.initial_ai_moves += 1
                elif self.initial_ai_moves == 2:
                    self.outbound = False
                    self.target = world.util.get_closest_friendly_territory_from(friendly_unit.position, friendly_unit.snake)
                    if self.turn_count == (4 * initial_translation)-1:
                        self.initial_ai_moves += 1

            if self.initial_quadrant == 2:
                self.outbound = True
                self.target = world.position_to_tile_map[(26, 3 + initial_translation)]
                if self.turn_count == initial_translation:
                    self.initial_ai_moves += 1
                elif self.initial_ai_moves == 1:
                    self.target = world.position_to_tile_map[(26 - initial_translation, 3 + initial_translation)]
                    if self.turn_count == (2 * initial_translation)-1:
                        self.initial_ai_moves += 1
                elif self.initial_ai_moves == 2 :
                    self.outbound = False
                    self.target = world.util.get_closest_friendly_territory_from(friendly_unit.position, friendly_unit.snake)
                    if self.turn_count == (4 * initial_translation)-1:
                        self.initial_ai_moves += 1

            if self.initial_quadrant == 3:
                self.outbound = True
                self.target = world.position_to_tile_map[(3,26 - initial_translation)]
                if self.turn_count == initial_translation:
                    self.initial_ai_moves += 1
                elif self.initial_ai_moves == 1:
                    self.target = world.position_to_tile_map[(3 + initial_translation, 26 - initial_translation)]
                    if self.turn_count == (2 * initial_translation) - 1:
                        self.initial_ai_moves += 1
                elif self.initial_ai_moves == 2:
                    self.outbound = False
                    self.target = world.util.get_closest_friendly_territory_from(friendly_unit.position, friendly_unit.snake)
                    if self.turn_count == (4 * initial_translation) - 1:
                        self.initial_ai_moves += 1
                # elif self.initial_ai_moves == 3:
                #     self.target = world.position_to_tile_map[(3 + initial_translation -1, 26)]
                #     if self.turn_count == 5 * initial_translation:
                #         self.initial_ai_moves += 1
                # elif self.initial_ai_moves == 4:
                #     self.target = world.position_to_tile_map[(3 + initial_translation, 26 - initial_translation)]
            if self.initial_quadrant == 4:
                self.outbound = True
                self.target = world.position_to_tile_map[(26 - initial_translation,26)]
                if self.turn_count == initial_translation:
                    self.initial_ai_moves += 1
                elif self.initial_ai_moves == 1:
                    self.target = world.position_to_tile_map[(26 - initial_translation, 26 - initial_translation)]
                    if self.turn_count == (2 * initial_translation)-1:
                        self.initial_ai_moves += 1
                elif self.initial_ai_moves == 2:
                    self.outbound = False
                    self.target = world.util.get_closest_friendly_territory_from(friendly_unit.position, friendly_unit.snake)
                    if self.turn_count == (4 * initial_translation)-1:
                        self.initial_ai_moves += 1
                # elif self.initial_ai_moves == 3 and self.turn_count == (4 * initial_translation) + 1:
                #     self.target = world.position_to_tile_map[(26 - initial_translation, 26)]
                #     if self.turn_count == 5 * initial_translation:
                #         self.initial_ai_moves += 1
                # elif self.initial_ai_moves == 4 and self.turn_count == (5 * initial_translation) + 1:
                #     self.target = world.position_to_tile_map[(26 - initial_translation, 26 - initial_translation)]
        # After 4*(initial_translation - 1), go aggressive into enemy territory
        else:
            print(self.turns_since_kill )
            self.turns_since_kill += 1
            #LOOK FOR KILL, WHEN KILL RETURN HOME, IF NO KILL, THEN NEVER GO HOME ):
            if self.has_killed is False:
                #Just assume killed and run away
                if self.turns_since_kill == nums_turns_since_kill - 1:
                    self.has_killed = True
                    self.turns_since_kill = 0
                    self.outbound = False
                # If there arent any bodies to take, go to closest territory
                if world.util.get_closest_enemy_body_from(friendly_unit.position, None) == None:
                    self.outbound = True
                    self.target = world.util.get_closest_enemy_territory_from(friendly_unit.position, friendly_unit.snake)
                else:
                    self.outbound = True
                    self.target = world.util.get_closest_enemy_body_from(friendly_unit.position, friendly_unit.snake)
                # # if target is already dead, go home
                # for enemy in self.old_enemy_clone:
                #     if enemy.position == self.target.position:
                #         print(enemy.status)
                #         if enemy.status == 'DISABLED':
                #             self.has_killed = True

            else:
                self.target = world.util.get_closest_friendly_territory_from(friendly_unit.position, None)
                if friendly_unit.position in friendly_unit.territory:
                    self.has_killed = False
                    self.outbound = True
                self.outbound = False


        # if unit reaches the target point, reverse outbound boolean and set target back to None
        # if self.target is not None and friendly_unit.position == self.target.position:
        #     self.outbound = not self.outbound
        #     self.target = None
        #

        # # if outbound and no target set, set target as the closest capturable tile at least 1 tile away
        # from your territory's edge.
        if self.outbound and self.target is None:
            self.target = world.position_to_tile_map((14,14))
        #
        # # else if inbound and no target set, set target as the closest friendly tile
        elif not self.outbound and self.target is None:
            self.target = world.util.get_closest_friendly_territory_from(friendly_unit.position, None)
        #
        # # set next move as the next point in the path to target
        #Construct the set to avoid
        avoid = set()
        avoid.union(friendly_unit.territory)
        avoid.union(friendly_unit.snake)
        # If going outbound, try to avoid own territory
        if self.outbound:
            next_move = world.path.get_shortest_path(friendly_unit.position, self.target.position, avoid)[0]
        else:
            next_move = world.path.get_shortest_path(friendly_unit.position, self.target.position, friendly_unit.snake)[0]

        # move!
        friendly_unit.move(next_move)
        self.units_from_territory_edge += 1
        print("Turn {0}: currently at {1}, making {2} move to {3}.".format(
            str(self.turn_count),
            str(friendly_unit.position),
            'outbound' if self.outbound else 'inbound',
            str(self.target.position)
        ))
