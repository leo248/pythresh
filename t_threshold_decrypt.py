"""
This module implements the decryption of the threshold scheme.
"""
import argparse
import ast
import numpy as np
import sage.all as Sage


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


def t_threshold_decrypt(splitted_secrets, secret_line):
    """
    This function implements the threshold scheme decryption. It reconstructs
    the hyperplane that intersects the secret line based on the subset of
    points provided, then finds the secret point as the intersection of
    this hyperplane and the secret line.

    Args:
        teilgeheimnisse: A subset of points, each represented as a list of
        coordinates.
        secret_line: The secret line, as a list of points.

    Returns:
        The decrypted secret point.
    """

    order = len(secret_line) - 1
    dimension = len(list(secret_line[0])) - 1
    n_secrets = len(splitted_secrets)
    if order <= 1 or dimension <= 1 or n_secrets <= 1:
        print('''Sorry, but the dimension of the space, the order of the space
              and number of secrets have to exceed 1.''')
    elif n_secrets < dimension:
        print('''Sorry, but number of secrets must be greater or equal to the
              number of dimensions''')
    elif not (Sage.is_prime(order)) is True:
        print("Sorry, q must be a prime number.")
    else:
        projective_space = Sage.ProjectiveSpace(dimension, Sage.GF(order))
        splitted_secrets = [projective_space(point) for
                            point in splitted_secrets]
        secret_line = [projective_space(point) for point in secret_line]
        splitted_secrets = list(splitted_secrets)
        hyperplaine_intersect_secret = reconstruct_hyperplane(splitted_secrets,
                                                              projective_space)
        print("restored hyperplane: "
              + str(hyperplaine_intersect_secret))
        secret = intersect_hyperplane_w_secret_line(
                hyperplaine_intersect_secret, secret_line)
        print("decrypted secret: " + str(secret))


def reconstruct_hyperplane(points, projective_space):
    """
    This function reconstructs the hyperplane that intersects the secret line
    """
    hyperplaine = {1: points}
    hyperplaine2 = {1: list(points)}

    for point1 in hyperplaine[1]:
        for point2 in hyperplaine[1]:
            if point1 != point2:
                new_points = points_on_line(point1, point2, projective_space)
                for point3 in new_points:
                    if point3 not in hyperplaine[1]:
                        hyperplaine[1].append(point3)

    if hyperplaine[1] == hyperplaine2[1]:
        return hyperplaine
    return reconstruct_hyperplane(hyperplaine[1], projective_space)


def intersect_hyperplane_w_secret_line(hyperplane_intersect_secret,
                                       secret_line):
    """
    This function finds the intersection of the hyperplane and the secret line.

    Args:
        hyperplane_intersect_secret: A dictionary containing the hyperplanes
        that intersect the secret line.
        secret_line: A list of points on the secret line.

    Returns:
        A set containing the points that are both in the hyperplane and on the
        secret line.
    """
    secret_line_set = set(secret_line)
    intersection_points = set()

    for _, points in hyperplane_intersect_secret.items():
        for point in points:
            if point in secret_line_set:
                intersection_points.add(point)

    return intersection_points


def main():
    """
    This function parses the arguments and calls the decryption function.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', required=True, help='the splitted secrets')
    parser.add_argument('-s', required=True, help='the secret line')
    args = parser.parse_args()
    splitted_secrets = ast.literal_eval(args.t)
    secret_line = ast.literal_eval(args.s)
    splitted_secrets = tuple(tuple(point) for point in splitted_secrets)
    secret_line = tuple(tuple(point) for point in secret_line)
    t_threshold_decrypt(splitted_secrets, secret_line)


if __name__ == '__main__':
    main()
