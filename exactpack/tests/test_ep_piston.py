#
#  tests the solver implementation for the elastic-plastic piston test problem
#
#

import pytest

import numpy as np

from exactpack.solvers.ep_piston import EPpiston


class TestEPpistonAssignments():
    """Tests :class:`exactpack.solvers.EPpiston`.

    These tests confirm proper assignment of variables, including default
    values
    """

    def test_defaults(self):

        # here are the defaults
        gamma = 2.0         # Gruneisen Gamma
        c0 = 0.533          # Gruneisen Parameter (cm/us)
        s0 = 1.34           # Gruneisen Parameter
        model = 'hyperIfin' # Elasticity Model
        G = 0.286           # Material Shear Modulus (Mbar)
        Y = 0.0026          # Material Yield Stress (Mbar)
        rho0 = 2.79         # Initial Density (g/cm^3)
        up = 0.01           # Piston Velocity (cm/us)

        solution = EPpiston()

        assert solution.gamma == gamma
        assert solution.c0 == c0
        assert solution.s0 == s0
        assert solution.G == G
        assert solution.Y == Y
        assert solution.rho0 == rho0
        assert solution.up == up
        assert solution.model == model

    def test_assignment(self):
        # tests proper assignment of parameters
        #
        #  These values are made up and not physically meaningful
        #  This is only an arbitrary test case
        #

        gamma = 2.2         # Gruneisen Gamma
        c0 = 0.5            # Gruneisen Parameter (cm/us)
        s0 = 1.4            # Gruneisen Parameter
        model = 'hyperFin'  # Elasticity Model
        G = 0.290           # Material Shear Modulus (Mbar)
        Y = 0.0030          # Material Yield Stress (Mbar)
        rho0 = 2.89         # Initial Density (g/cm^3)
        up = 0.015          # Piston Velocity (cm/us)

        solution = EPpiston(gamma=gamma, c0=c0, s0=s0, G=G, Y=Y,
                                      rho0=rho0, up=up, model=model)

        assert solution.gamma == gamma
        assert solution.c0 == c0
        assert solution.s0 == s0
        assert solution.G == G
        assert solution.Y == Y
        assert solution.rho0 == rho0
        assert solution.up == up
        assert solution.model == model

    #
    # Confirm that illegal parameter values raise an error
    #

    def test_illegal_value_G(self):
        with pytest.raises(ValueError):
            EPpiston(G=-1.0)
        
    def test_illegal_value_Y(self):
        with pytest.raises(ValueError):
            EPpiston(Y=-1.0)

    def test_illegal_value_rho0(self):
        with pytest.raises(ValueError):
            EPpiston(rho0=-1.0)

    def test_illegal_value_up(self):
        with pytest.raises(ValueError):
            EPpiston(up=-1.0)

    def test_illegal_value_model(self):
        with pytest.raises(ValueError):
            EPpiston(model='Hypoelastic')


class TestEPpistonSolution():
    """Tests :class:`exactpack.solvers.EPpiston`.

    These tests confirm proper solution values for specific inputs
    """

    def test_yield_density_funcs(self):
        G = 0.286
        Y = 0.0026
        rho0 = 2.79

        result_hypo = EPpiston().rho_hypoYield(G,Y,rho0)
        result_hyperIfin = EPpiston().rho_hyperIfinYield(G,Y,rho0)
        result_hyperFin = EPpiston().rho_hyperFinYield(G,Y,rho0)
        assert result_hypo == pytest.approx(2.8027106842157106, abs=1.0e-12)
        assert result_hyperIfin == pytest.approx(2.802739726027397, abs=1.0e-12)
        assert result_hyperFin == pytest.approx(2.802749184157357, abs=1.0e-12)

    def test_Gruneisen(self):
        gamma = 2.
        c0 = 0.533
        s0 = 1.34
        rho0 = 2.79
        rho = 2.802739726027397
        e = 4.3893303503475645e-06

        result_grun = EPpiston().Gruneisen(rho0,gamma,c0,s0,rho,e)
        assert result_grun == pytest.approx(0.003655008604753384, abs=1.0e-12)

    def test_residual(self):
        
        self.gamma = 2.
        self.c0 = 0.533
        self.s0 = 1.34
        self.rho0 = 2.79
        self.up = 0.01
        self.rho_y = 2.802739726027397
        self.e_y = 4.3893303503475645e-06
        self.p_y = 0.003655008604753384
        self.vel_y = 0.0029628804735755254
        self.sdev_y = -0.0017333333333333333

        assert EPpiston().Plastic_Residual(0.5505600903624002) < 1.e-12
