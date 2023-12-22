from collections import namedtuple
from input import read_input, sample_input


Pos = namedtuple('Pos', ['x', 'y', 'z'])

class Brick():
    def __init__(self, raw_input, id):
        self.id = chr(65 + (id % 26)) + str(id // 26)

        end, other_end = raw_input.split('~')
        _x, _y, _z = end.split(',')
        self.end = Pos(int(_x), int(_y), int(_z))

        _x, _y, _z = other_end.split(',')
        self.other_end = Pos(int(_x), int(_y), int(_z))

    def __repr__(self):
        return f'{self.end.x},{self.end.y},{self.end.z}~{self.other_end.x},{self.other_end.y},{self.other_end.z}'

    @property
    def is_vertical(self):
        return self.end.z != self.other_end.z

    def get_max_xy(self):
        return max(self.end.x, self.other_end.x), max(self.end.y, self.other_end.y)

    def get_min_z(self):
        return min(self.end.z, self.other_end.z)

    def xy_positions(self):
        x_start = min(self.end.x, self.other_end.x)
        x_end = max(self.end.x, self.other_end.x)

        y_start = min(self.end.y, self.other_end.y)
        y_end = max(self.end.y, self.other_end.y)

        for x in range(x_start, x_end + 1):
            for y in range(y_start, y_end + 1):
                yield x, y

    def z_positions(self):
        z_start = min(self.end.z, self.other_end.z)
        z_end = max(self.end.z, self.other_end.z)
        for z in range(z_start, z_end + 1):
            yield z


SupportPair = namedtuple('SupportPair', ['supported', 'support'])


class XY():
    def __init__(self):
        self.z_bricks = {} # Map z-position to brick id

    def __repr__(self):
        return str(self.z_bricks)

    def get_support_pairs(self):
        support_pairs = []
        occupied_z_levels = self.z_bricks.keys()
        for z in sorted(occupied_z_levels, reverse=True):
            if (z + 1) in self.z_bricks and self.z_bricks[z + 1] != self.z_bricks[z]:
                support_pairs.append(SupportPair(
                    self.z_bricks[z + 1],
                    self.z_bricks[z],
                ))
        return support_pairs

    def get_highest_z(self):
        occupied_z_levels = self.z_bricks.keys()
        return (
            max(occupied_z_levels)
            if occupied_z_levels
            else 0
        )

    def set_brick(self, z, brick_id):
        self.z_bricks[z] = brick_id


class World():
    def __init__(self, bricks, xy_positions):
        self.bricks = sorted(bricks, key=lambda b: b.get_min_z())
        self.xy_positions = xy_positions

    def resume_from_snapshot(self):
        for brick in self.bricks:
            self.let_fall(brick)

    def let_fall(self, brick: Brick):
        supporting_z = 0
        for x, y in brick.xy_positions():
            supporting_z = max(
                supporting_z,
                self.xy_positions[x][y].get_highest_z(),
            )

        if brick.is_vertical:
            brick_x = brick.end.x
            brick_y = brick.end.y
            min_z = brick.get_min_z()
            for z in brick.z_positions():
                self.xy_positions[brick_x][brick_y].set_brick(
                    supporting_z + 1 + (z - min_z),
                    brick.id,
                )
        else:
            for x, y in brick.xy_positions():
                self.xy_positions[x][y].set_brick(supporting_z + 1, brick.id)

    def count_redundant_bricks(self):
        supported_bricks = {}
        supporting_bricks = {brick.id: [] for brick in self.bricks}
        for x_positions in self.xy_positions:
            for xy_position in x_positions:
                for supported, support in xy_position.get_support_pairs():
                    if supported not in supported_bricks:
                        supported_bricks[supported] = []

                    if support not in supported_bricks[supported]:
                        supported_bricks[supported].append(support)

                    if supported not in supporting_bricks[support]:
                        supporting_bricks[support].append(supported)

        redundant_bricks = set()
        for supported, supports in supported_bricks.items():
            if len(supports) > 1:
                redundant_bricks = redundant_bricks | set(supports)

        critical_bricks = set()
        for supported, supports in supported_bricks.items():
            if len(supports) == 1:
                critical_bricks.add(supports[0])

        redundant_bricks = redundant_bricks - critical_bricks

        for support, supported in supporting_bricks.items():
            if len(supported) == 0:
                redundant_bricks.add(support)

        return len(redundant_bricks)


max_x = 0
max_y = 0
bricks = []
for i, raw_input in enumerate(read_input(22)):
    brick = Brick(raw_input, i)
    x, y = brick.get_max_xy()
    max_x = max(x, max_x)
    max_y = max(y, max_y)
    bricks.append(brick)

xy_positions = []
for x in range(max_x + 1):
    x_positions = []
    for y in range(max_y + 1):
        x_positions.append(XY())
    xy_positions.append(x_positions)


world = World(bricks, xy_positions)
world.resume_from_snapshot()
print('Part 1: ', world.count_redundant_bricks()) # 190 is too low, 521 too high, 439 just right!
