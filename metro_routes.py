from copy import deepcopy


class Stop(object):
    def __init__(self, station, line):
        self.station = station
        self.line = line

    def __repr__(self):
        return "Stop[%r, %r]" % (self.station, self.line)


class Move(object):
    def __init__(self, start_stop, end_stop):
        self.start_stop = start_stop
        self.end_stop = end_stop

    def __repr__(self):
        return "Move[From %r To %r]" % (self.start_stop, self.end_stop)


class Trip(object):
    def __init__(self, current_stop):
        self.current_stop = current_stop
        self.lines = 0
        self.moves = []

    def is_at_station(self, station):
        return self.current_stop.station == station

    def take_move(self, move):
        if stop_matches_current(move.start_stop, self.current_stop):
            next_stop = move.end_stop
        else:
            next_stop = move.start_stop

        if self.current_stop.line != next_stop.line:
            self.lines += 1

        self.current_stop = next_stop
        self.moves.append(move)

    def __repr__(self):
        current_stop = self.current_stop
        moves = self.moves.copy()
        # print(moves)
        moves.reverse()
        steps = []

        for move in moves[:-1]:
            if stop_matches_current(move.end_stop, current_stop):
                prev_stop = move.start_stop
            else:
                prev_stop = move.end_stop

            # if current_stop.line != prev_stop.line:
            steps.insert(0, "At %r, go to %r." % (prev_stop, current_stop))

            current_stop = prev_stop

        return ' '.join(steps)


def stop_matches_current(stop, current_top):
    return stop.station == current_top.station and (
        not current_top.line or stop.line == current_top.line
    )


def can_move_to_next_stop(lines, stop, current_stop):
    if lines > 2:
        return False

    return lines < 2 or stop.line == current_stop.line


def take_possible_paths(trip, poss_moves, end_station):
    for i, move in enumerate(poss_moves):
        # this move includes the station we are currently on and should be used
        start_eq = stop_matches_current(move.start_stop, trip.current_stop)
        end_eq = stop_matches_current(move.end_stop, trip.current_stop)

        # also, we can only take two lines; enforce that here
        end_line_ok = can_move_to_next_stop(
            trip.lines,
            move.end_stop,
            trip.current_stop
        )
        start_line_ok = can_move_to_next_stop(
            trip.lines,
            move.start_stop,
            trip.current_stop
        )

        if (start_eq and end_line_ok) or (end_eq and start_line_ok):
            new_trip = deepcopy(trip)
            new_poss_moves = poss_moves.copy()

            new_trip.take_move(new_poss_moves.pop(i))

            if new_trip.is_at_station(end_station):
                # trip complete, print it
                print('Trip Complete: ', new_trip)
            else:
                take_possible_paths(new_trip, new_poss_moves, end_station)


def print_routes():
    # parse map data
    poss_moves = []
    with open('map.txt') as file:
        for move in file:
            move = move.replace(',', '')
            move_parts = move.split()
            poss_moves.append(
                Move(
                    Stop(move_parts[0], move_parts[1]),
                    Stop(move_parts[2], move_parts[3])
                )
            )

    # parse input
    with open('input.txt') as file:
        start_station = file.read(1)
        file.seek(2)
        end_station = file.read(1)

    # create a trip
    trip = Trip(Stop(start_station, None))

    # take all possible paths
    take_possible_paths(trip, poss_moves, end_station)


if __name__ == '__main__':
    print_routes()
