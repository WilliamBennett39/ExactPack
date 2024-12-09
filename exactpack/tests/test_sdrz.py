"""Unit tests for Steady Detonation Reaction (sdrz) solver.
"""

import pytest

import numpy as np

from exactpack.solvers.sdrz import SteadyDetonationReactionZone


class TestSDRZAssignments():
    """Tests :class:`exactpack.solvers.sdrz.SteadyDetonationReactionZone`.

    These tests confirm proper assignment of variables, including default
    values.
    """
    def test_defaults(self):

        # here are the defaults
        D = 0.85       # Detonation velocity of HE
        rho_0 = 1.6    # Initial density of HE
        gamma = 3.0      # Adiabatic index of HE

        solution = SteadyDetonationReactionZone()

        assert solution.D == D
        assert solution.rho_0 == rho_0
        assert solution.gamma == gamma

    def test_assignment(self):
        # tests proper assignment of parameters
        #
        #  These values are made up and not physically meaningful
        #  This is only an arbitrary test case
        #

        D = 2.00       # Detonation velocity of HE
        rho_0 = 1.75   # Initial density of HE
        gamma = 5.0     # Adiabatic index of HE

        solution = SteadyDetonationReactionZone(D=D, rho_0=rho_0, gamma=gamma)

        assert solution.D == D
        assert solution.rho_0 == rho_0
        assert solution.gamma == gamma

    #
    # Confirm that illegal parameter values raise an error
    #

    def test_illegal_value_D(self):
        with pytest.raises(ValueError):
            SteadyDetonationReactionZone(D=-1.0)

    def test_illegal_value_rho_0(self):
        with pytest.raises(ValueError):
            SteadyDetonationReactionZone(rho_0=-1.0)

    def test_illegal_value_gamma(self):
        with pytest.raises(ValueError):
            SteadyDetonationReactionZone(gamma=-1.0)

    def test_illegal_value_geometry(self):
        with pytest.raises(ValueError):
            SteadyDetonationReactionZone(geometry=2)

class TestSDRZSolution():
    """Tests :class:`exactpack.solvers.sdrz.SteadyDetonationReactionZone`.

    These tests confirm proper solution values for specific cases.
    """

    def test_fickett_table10_1(self):
        """Tests proper solution values

        This test compares the default case to the Table 10.1 in
        Fickett & Rivard
        """

        def compare_to_table(self, dataray):

            sigfigs = 6   # Number of significant figures in table

            time = dataray[:, 0]
            position = dataray[:, 1]
            pressure = dataray[:, 2]
            velocity = dataray[:, 3]
            density = dataray[:, 4]
            sound_speed = dataray[:, 5]
            shock_velocity = dataray[:, 6]
            reaction_progress = dataray[:, 7]

            solution = SteadyDetonationReactionZone()

            result = solution.run_tvec(time) # run_tvec method expects vector of times

            np.testing.assert_allclose(result['position_relative'], position, rtol=1.0e-6)
            np.testing.assert_allclose(result['pressure'], pressure, rtol=1.0e-6)
            np.testing.assert_allclose(result['velocity'], velocity, rtol=1.0e-6)
            np.testing.assert_allclose(result['density'], density, rtol=1.0e-6)
            np.testing.assert_allclose(result['sound_speed'], sound_speed, rtol=1.0e-6)
            np.testing.assert_allclose(result['reaction_progress'],
                                       reaction_progress, rtol=1.0e-6)

        # Table 10.1

        #   't',    'x', 'pressure', 'velocity', 'density', 'sound_speed',
        #       shockVel', 'reaction_progress'

        dataray=np.array([
           [0.0, 0.0000000, 0.57800000, 0.4250000, 3.200000, 0.7361216, 
               0.85, 0.000],
           [0.1, 0.0435625, 0.54910000, 0.4037500, 3.047619, 0.7352009,
               0.85, 0.19],
           [0.2, 0.0892500, 0.52020000, 0.3825000, 2.909091, 0.7324317,
               0.85, 0.36],
           [0.3, 0.1370625, 0.49130000, 0.3612500, 2.782609, 0.7277931,
               0.85, 0.51],
           [0.4, 0.1870000, 0.46240000, 0.3400000, 2.666667, 0.7212489,
               0.85, 0.64],
           [0.5, 0.2390625, 0.43350000, 0.3187500, 2.560000, 0.7127467,
               0.85, 0.75],
           [0.6, 0.2932500, 0.40460000, 0.2975000, 2.461538, 0.7022152,
               0.85, 0.84],
           [0.7, 0.3495625, 0.37570000, 0.2762500, 2.370370, 0.6895617,
               0.85, 0.91],
           [0.8, 0.4080000, 0.34680000, 0.2550000, 2.285714, 0.6746666,
               0.85, 0.96],
           [0.9, 0.4685625, 0.31790000, 0.2337500, 2.206897, 0.6573776,
               0.85, 0.99],
           [1.0, 0.5312500, 0.28900000, 0.2125000, 2.133333, 0.6375000,
               0.85, 1.00],
           [1.2, 0.6587500, 0.28900000, 0.2125000, 2.133333, 0.6375000,
               0.85, 1.00]
           ])

        # NOTE: CORRECTED VALUE 0.70125 to 0.65875 for x value at t=1.2
        # (Error in original table and formula)

        compare_to_table(self, dataray)

    def test_sdrz_reaction_progress_limit(self):
        """ Tests that burn rate is limited to be monotonic and cannot exceed 1.0.
        """

        solution = SteadyDetonationReactionZone()

        time = np.linspace(0.,2.0,21)

        result = solution.run_tvec(time) 

        answer = np.array(
                [ 0.  ,  0.19,  0.36,  0.51,  0.64,  0.75,  0.84,  0.91,  0.96,
                  0.99,  1.  ,  1.  ,  1.  ,  1.  ,  1.  ,  1.  ,  1.  ,  1.  ,
                  1.  ,  1.  ,  1.  ])

            
        np.testing.assert_allclose(result['reaction_progress'], answer)


class TestSDRZNumericalIntegration():
    """Tests :class:`exactpack.solvers.sdrz.SteadyDetonationReactionZone`.

    These tests verify that the numerical integration scheme is working correctly.
    """

    def test_numerical_versus_exact(self):

        solution = SteadyDetonationReactionZone()

        tvec = np.linspace(0.,2.0,21)

        resultExact = solution.run_tvec(tvec, useExactLambda=True) # Use exact formulation for reaction progress

        resultNumerical = solution.run_tvec(tvec, useExactLambda=False) # Use numerical integration to get reaction progress

        np.testing.assert_allclose(resultExact['position_relative'],
                                   resultNumerical['position_relative'])
        np.testing.assert_allclose(resultExact['pressure'],
                                   resultNumerical['pressure'])
        np.testing.assert_allclose(resultExact['velocity'],
                                   resultNumerical['velocity'])
        np.testing.assert_allclose(resultExact['density'],
                                   resultNumerical['density'])
        np.testing.assert_allclose(resultExact['sound_speed'],
                                   resultNumerical['sound_speed'])
        np.testing.assert_allclose(resultExact['reaction_progress'],
                                   resultNumerical['reaction_progress'])


class TestSDRZFullSolution():
    """Tests :class:`exactpack.solvers.sdrz.SteadyDetonationReactionZone`.

    These tests verify that the full solution to SDRZ is behaving as expected.
    """

    def test_full_solution(self):

        solution = SteadyDetonationReactionZone(D=0.85, rho_0=1.6, gamma=3.0)

        xvec = np.linspace(0., 3.0, 21)

        tfinal = 2.0

        result = solution._run(xvec, tfinal)

        answer_density = np.array(
            [ 2.13333333,  2.13333333,  2.13333333,  2.13333333,  2.13333333,  2.13333333,
              2.13333333,  2.13333333,  2.16907206,  2.36970464,  2.63880434,  3.02692195,
              1.6,         1.6,         1.6,         1.6,         1.6,         1.6,         1.6,
              1.6,         1.6       ])

        answer_velocity = np.array(
            [ 0.2125,      0.2125,      0.2125,      0.2125,      0.2125,      0.2125,
              0.2125,      0.2125,      0.22300338,  0.27608826,  0.33461289,  0.40069622,
              0.,          0.,          0.,          0.,          0.,          0.,          0.,
              0.,          0.        ])
            

        np.testing.assert_allclose(result['density'], answer_density)
        
        np.testing.assert_allclose(result['velocity'], answer_velocity)
