"""A Su-Olson solver.
"""

from ...base import ExactSolver, ExactSolution
from .timmes import suolson


class SuOlson(ExactSolver):
    """Computes the solution to the Su-Olson problem.
    """

    parameters = {
        'trad_bc_ev': r'radiation boundary condition, i.e. :math:`T(0,t)= \
        {\rm trad\_bc\_ev}`',
        'opac': r'constant opacity :math:`\kappa_0` in Eq. :eq:`cvkappaDef`',
        'alpha': r'coefficient :math:`\alpha` in Eq. :eq:`cvkappaDef` for \
         the specific heat (:math:`\alpha = 4 a`)',
        }

    alpha = 3.02636565993931701e-14 # alpha = 4 * a [erg/cm^3]
    trad_bc_ev = 1.0e3              # [ev]
    opac = 1.0                      # [cm^2/g]

    def __init__(self, **kwargs):
        """Initialize the Su-Olson solver class.
        """

        super(SuOlson, self).__init__(**kwargs)

    def _run(self, r, t):

        trad_ev, tmat_ev = suolson(t=t,
                                   x=r,
                                   trad_bc_ev=self.trad_bc_ev,
                                   opac=self.opac,
                                   alpha=self.alpha)

        return ExactSolution([r, trad_ev, tmat_ev],
                             names=['position',
                                    'temperature_rad',
                                    'temperature_mat'])
