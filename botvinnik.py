from __future__ import print_function


def time_remaining(init_min, incr_secs, move=15, percent=20, total_moves=40,
                   debug=True):
    """
    Calculate the time remaining on the clock after a given move if one is
    to have used a certain percentage of the time for the whole game after that
    move, taking into account a per-move increment.

    :Parameters:
      - init_min: initial clock time in minutes
      - incr_secs: per-move increment in seconds
      - move: the move number to calculate for, from 1 to total_moves (defaults
        to 15, for the botvnnik recommendation of 20% for first 15 moves)
      - percent: the percentage of total time to have spent after given move
        (defaults to 20%, which is the botvinnik recommendation for first
        15 moves)
      - total_moves: number of moves in entire game (default is 40)
      - debug: whether to print partial calculation debug info (default is
        false)

    @return The clock time remaining at the given move number, which is
            calculated as the initial clock time minus the target percentage
            of the total game time, with the increment time added for
            already played moves after the target move.
    """
    assert init_min > 0 and incr_secs >= 0 and move > 1 and total_moves > move

    def log(msg, *args):
        if debug:
            print(msg % args)

    incr = incr_secs / 60.0

    # total time for all moves
    total_time = init_min + (total_moves * incr)
    msg = "total time for %d moves: %0.2f min (initial + increments)"
    log(msg, total_moves, total_time)

    # time spent for given percentage of total time
    time_spent = (percent / 100.0) * total_time
    msg = "time spent for %d%% of total time: %d min"
    log(msg, percent, time_spent)

    # remaining time after given move without adding per-move increment
    remaining_time_no_incr = init_min - time_spent
    msg = ("remaining time at move %d ignoring per-move increment delta: "
           "%0.2f min")
    log(msg, move, remaining_time_no_incr)

    # time to be added for given move due to per-move increment
    incr_time_delta = move * incr
    msg = "increment delta for %d moves: %0.2f min"
    log(msg, move, incr_time_delta)

    # time remaining on clock at given move
    target_clock_time = remaining_time_no_incr + incr_time_delta
    msg = ("target clock time after move %d: %0.2f min (%d:%02d) "
           "[no_incr=%0.2f]")
    no_incr_time = init_min * (1 - (percent / 100.0))
    mins = int(target_clock_time)
    secs = int((target_clock_time - mins) * 60)
    log(msg, move, target_clock_time, mins, secs, no_incr_time)

    return target_clock_time
