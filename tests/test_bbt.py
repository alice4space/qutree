import numpy as np
from bbt import nphi_psi


def test_nphi_psi():
    r = np.random.random(10)
    phi = np.random.random(10) * 2 * np.pi

    r_test, phi_test = nphi_psi(r * np.exp(1j * phi))

    assert np.allclose(r, r_test)
    assert np.allclose(phi, phi_test)
