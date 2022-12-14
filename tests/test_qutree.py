import numpy as np

import qutree


def test_nphi_psi() -> None:
    r = np.random.random(10)
    phi = np.random.random(10) * 2 * np.pi

    r_test, phi_test = qutree.nphi_psi(r * np.exp(1j * phi))

    assert np.allclose(r, r_test)
    assert np.allclose(phi, phi_test)


def test_nthe_n0n1() -> None:
    pass


def test_phimp_phi01() -> None:
    pass


def test_thephi_to_xyz() -> None:
    pass


def fun_recursive() -> None:
    pass


def test_bloch_points() -> None:
    pass


def test_BBT() -> None:
    pass


def test_add_data() -> None:
    pass


def test_fun_recursive() -> None:
    pass


def test_plot_tree() -> None:
    pass
