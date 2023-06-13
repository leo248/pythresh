"""
This module implements the threshold scheme encryption. It generates a random
secret point in a projective space and finds another point on the same line.
It then generates all hyperplanes in the space and finds those that intersect
the secret line. Finally, it selects a subset of points that are in a general
position with respect to the secret point.
"""
import argparse
import itertools
import random as r
import numpy as np
import sage.all as sage


def find_point_for_secret_line(secret, points):
    """
    This function finds a point from the points list that shares at least one
    coordinate with the secret point (geheimnis).

    Args:
        geheimnis: The secret point, as a list of coordinates.
        points: A list of available points, each represented as
        a list of coordinates.

    Returns:
        A randomly chosen point from the valid points list.
        If no valid point found, returns None.
    """
    valid_points = []

    for point in points:
        if point != secret:
            for i, _ in enumerate(point):
                if point[i] == secret[i]:
                    valid_points.append(point)
                    break
    if valid_points:
        return r.choice(valid_points)
    return None


def points_on_line(point1, point2, projective_space):
    """
    This function finds all the points on the line that passes through the
    two points provided.
    """
    line_points = []
    space_order = point1.parent().base_ring()
    for zeta in space_order:
        for alpha in space_order:
            if alpha != 0 or zeta != 0:
                p_1 = np.array(list(point1))
                p_2 = np.array(list(point2))
                new_point = zeta * p_1 + alpha * p_2
                new_point = np.ndarray.tolist(new_point)
                new_point_normalized = [space_order(x) for x in new_point]
                new_point_projective = projective_space(new_point_normalized)
                if new_point_projective not in line_points:
                    line_points.append(new_point_projective)
    return line_points


def all_hyperplaines(points):
    """
    This function finds all the hyperplanes in the projective space.
   """
    i = 1
    hyperplane_dict = {}
    for point1 in points:
        array_point1 = np.array(list(point1))
        hyperplane_list = []
        for point2 in points:
            array_point2 = np.array(list(point2))
            if np.dot(array_point1, array_point2) == 0:
                hyperplane_list.append(point2)
        hyperplane_dict.update({i: hyperplane_list})
        i += 1
    return hyperplane_dict


def point_in_plane(point, plane):
    """
    This function checks if a point is in a plane.
    """
    return point in plane


def line_in_plane(line, plane):
    """
    This function checks if a line is in a plane.
    """
    return all(point_in_plane(point, plane) for point in line)


def find_hyperplanes_for_secret_line(hyperplanes, secret_line):
    """
    This function finds all the hyperplanes that intersect the secret line.
    """
    result = {}
    for point in secret_line:
        result[point] = []
        for plane_id, plane in hyperplanes.items():
            if point_in_plane(point, plane) and not line_in_plane(secret_line,
                                                                  plane):
                result[point].append(hyperplanes[plane_id])
    return result


def get_secret_splitter(hyperplaines_cut_secret_line, secret, dimension,
                        order):
    """
    This function finds a secret splitter, i.e. a set of points that are in a
    general position with respect to the secret point. It does so by randomly
    selecting a hyperplane that intersects the secret line and then finding a
    subset of points that are in a general position with respect to the secret
    point.
    """
    random_number = r.randint(0, len(hyperplaines_cut_secret_line[secret]) - 1)

    hp_for_splitter = hyperplaines_cut_secret_line[secret][random_number]
    if secret in hp_for_splitter:
        hp_for_splitter.remove(secret)
    if dimension == 2:
        return hp_for_splitter
    secret_splitters = hp_for_splitter
    subset = find_largest_general_position_subset(secret_splitters,
                                                  secret, order)
    if subset is not None:
        if (sage.matrix(sage.GF(order), subset).rank() >= dimension):
            return subset
        else:
            return get_secret_splitter(hyperplaines_cut_secret_line, secret,
                                       dimension, order)

    else:
        return get_secret_splitter(hyperplaines_cut_secret_line, secret,
                                   dimension, order)


def find_largest_general_position_subset(secret_splitters, secret, order):
    """
    This function finds the largest subset of points where no three points are
    collinear. It starts with a subset that contains only the secret point, and
    then it tries to add each point from secret_splitters to the subset. After
    adding a point, it checks if the subset remains in general position. If it
    does, it keeps the point, otherwise, it discards it and tries with the next
    point.
    """
    arc = [secret]

    r.shuffle(secret_splitters)
    arc.append(secret_splitters[0])
    for point in secret_splitters:
        tmp_subset = arc + [point]
        if is_general_position(tmp_subset, order):
            arc.append(point)
    arc.remove(secret)
    return arc


def is_general_position(arc, order):
    """
    This helper function checks if a subset of points is in general position,
    i.e., no three points in the subset are collinear. It does this by checking
    the rank of every 3x3 submatrix.
    """
    for three_points in itertools.combinations(arc, 3):
        mat = sage.matrix(sage.GF(order), three_points)
        if mat.rank() < 3:
            return False
    return True


def t_threshold_encrypt(dimension, order):
    """
    This function implements the threshold scheme encryption. It generates a
    random secret point in a projective space and finds another point on the
    same line. It then generates all hyperplanes in the space and finds those
    that intersect the secret line. Finally, it selects a subset of points that
    are in a general position with respect to the secret point.

    Args:
        dimension: The number of dimensions in the projective space.
        order: The size of the field.

    Returns:
        A tuple containing the selected points (subset) and the secret line.
    """
    
    if order <= 1 or dimension <= 1:
        print('''Sorry, but dimension,
              order and the number of secrets have to exceed 1.''')

    elif (sage.is_prime(order)) is False:
        print("Sorry, q must be a prime number.")
    else:
        projective_space = sage.ProjectiveSpace(dimension, sage.GF(order))
        points = projective_space.rational_points()
        random_number = r.randint(0, (len(points) - 1))
        secret = points[random_number]
        second_point_for_secret_line = find_point_for_secret_line(secret,
                                                                  points)
        secret_line = points_on_line(secret, second_point_for_secret_line,
                                     projective_space)
        hyperplanes = all_hyperplaines(points)
        hyperplanes_cut_secret_line = find_hyperplanes_for_secret_line(
                hyperplanes, secret_line)
        secret_splitters = get_secret_splitter(hyperplanes_cut_secret_line,
                                               secret, dimension, order)
        secret_line = [list(point) for point in secret_line]
        secret_splitters = list(secret_splitters)
        secret_splitters = [list(split) for split in secret_splitters]
        print("Secret: " + str(secret))
        print("Secret line: " + str(secret_line))
        print("Splitters of the secret: " + str(secret_splitters))


def main():
    """
    This function parses the command line arguments and calls the
    t_threshold_encrypt function.
    """
    parser = argparse.ArgumentParser(description='''Encrypts a secret
                                     using the t-threshold scheme.''')
    parser.add_argument('-q', type=int, required=True,
                        help='Size of the field')
    parser.add_argument('-t', type=int, required=True,
                        help='Number of dimensionis in the projective space')

    args = parser.parse_args()
    t_threshold_encrypt(args.t, args.q)


if __name__ == '__main__':
    main()
