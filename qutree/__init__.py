__version__ = "0.0.0"  # noqa
__author__ = "Alice Barthe"  # noqa
__email__ = "alice.barthe@cern.ch"  # noqa

from typing import Tuple, Union

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import qutip
from matplotlib import cm


def nphi_psi(psi: np.array) -> Tuple[np.array, np.array]:
    """
    decompose an array of complex into absolute value and angles

    Args:
        psi (np.array): array of complex values

    Returns:
        r (np.array) : array of absolute values
        phi (np.array) : array of angles from :math:`[0, 2\pi]`
    """

    r = np.abs(psi)
    phi = np.angle(psi) % (2 * np.pi)

    return r, phi


def nthe_n0n1(n0: np.array, n1: np.array) -> Tuple[np.array, np.array]:
    """
    Carthesian to Polar

    Compute :math:`n` and :math:`\theta` such that :math:`[n0,n1] = n[cos(\\theta),sin(\\theta)]`

    Args:
        n0 (np.array): array of absolute values
        n1 (np.array): array of absolute values

    Returns:
        n (np.array) : array of norm
        the (np.array) : array of angles from :math:`[0, \pi]`
    """

    n = np.sqrt(n0**2 + n1**2)
    the = 2 * np.arctan2(n1, n0)

    return n, the


def phimp_phi01(phi0, phi1):
    """
    go from two subspace phases to local and global phase

    Args:
        phi0 (np.array): array of subspace 0 phases
        phi1 (np.array): array of subspace 1 phases

    Returns:
        phig (np.array): array of global phases
        phil (np.array): array of local phases
    """
    phig = phi0
    phil = phi1 - phi0 + (phi1 < phi0) * 2 * np.pi
    return phil, phig


def thephi_to_xyz(the: np.array, phi: np.array) -> Tuple[np.array, np.array, np.array]:
    """
    spherical to carthesian

    Args:
        the (np.array): array of the angles :math:`[0,\pi]`
        phi (np.array): array of :math:`\phi` angles :math:`[0,2 \pi]`

    Returns:
        x (np.array): array of the x axis coordinate
        y (np.array): array of the y axis coordinate
        z (np.array): array of the z axis coordinate
    """

    z = np.cos(the)
    x = np.sin(the) * np.cos(phi)
    y = np.sin(the) * np.sin(phi)

    return x, y, z


def fun_recursive(
    psi: np.array,
    coord: str = "",
    tree_vals: list = [],
    tree_idxs: list = [],
    tol: float = 1e-4,
) -> Tuple[np.array, np.array, list, list]:
    """
    recursive function going down the hilbert schmidt decomposition

    Args:
        psi (np.array): array representing the state in the current subspace :math:`(2^N,M)`
        coord (str): string representing the current coordinate in the binary tree
        tree_vals (list) : register storing the :math:`\\theta` and :math:`\phi` of the Bloch sphere at each coordinate
        tree_idxs (list) : register storing the coordinates
        tol : tolerance to delete a subspace

    Returns:
        phip (np.array) : the global phases of the local subspace
        n (np.array) : the amplitude of the local subspace
        tree_vals (list) : register storing the :math:`\\theta` and :math:`\phi` of the Bloch sphere at each coordinate
        tree_idxs (list) : register storing the coordinates
    """

    N = psi.shape[0]

    if N == 2:
        ns, phis = nphi_psi(psi)
        n0 = ns[0, :]
        n1 = ns[1, :]
        phi0 = phis[0, :]
        phi1 = phis[1, :]

    else:
        psi0 = psi[: N // 2, :].copy()
        psi1 = psi[N // 2 :, :].copy()

        if tol is not None:
            n0 = np.sqrt(np.sum(np.abs(psi0) ** 2, axis=0))
            n1 = np.sqrt(np.sum(np.abs(psi1) ** 2, axis=0))

            i0 = np.where(n0 < tol)
            i1 = np.where(n1 < tol)

            psi0[:, i0] = psi1[:, i0]
            psi1[:, i1] = psi0[:, i1]

            phi0, _, tree_vals, tree_idxs = fun_recursive(
                psi0, coord + "0", tree_vals, tree_idxs, tol
            )
            phi1, _, tree_vals, tree_idxs = fun_recursive(
                psi1, coord + "1", tree_vals, tree_idxs, tol
            )

        else:
            phi0, n0, tree_vals, tree_idxs = fun_recursive(
                psi0, coord + "0", tree_vals, tree_idxs, tol
            )
            phi1, n1, tree_vals, tree_idxs = fun_recursive(
                psi1, coord + "1", tree_vals, tree_idxs, tol
            )

    n, the = nthe_n0n1(n0, n1)
    phim, phip = phimp_phi01(phi0, phi1)

    tree_vals.append(np.stack([the, phim]))
    tree_idxs.append(coord)

    return phip, n, tree_vals, tree_idxs


def bloch_points(
    xp: np.array,
    yp: np.array,
    zp: np.array,
    colors,
    ax: Union[mpl.axes.Axes, None] = None,
    azim: float = -40.0,
    elev: float = 30.0,
) -> None:
    """
    plot points on a bloch spere

    Args:
        xp (np.array) : array of the x axis coordinate
        yp (np.array) : array of the y axis coordinate
        zp (np.array) : array of the z axis coordinate
        colors (np.array) : array of colors for each point
        ax (matplotlib.axes.Axes) : ax where the Bloch Sphere will be plotted, if None one is created
        azim (float) : azimuth to plot the sphere
        elev (float) : azimuth to plot the sphere
    """

    if ax is None:
        fig = plt.figure(constrained_layout=True)
        ax = fig.add_subplot(1, 1, 1, projection="3d", azim=azim, elev=elev)

    b = qutip.Bloch(axes=ax)
    b.make_sphere()
    pnts = [xp, yp, zp]
    b.add_points(pnts, "m")
    b.point_color = list(colors)
    b.render()


class BBT:
    """
    Class containing the data to plot the Bloch Binary Tree

    Args:
        num_qubits (int) : number of qubits
    """

    def __init__(self, num_qubits: int) -> None:
        self.num_qubits = num_qubits

    def add_data(
        self, states: np.array, colors: Union[np.array, None] = None, cmap: str = "jet"
    ) -> None:
        """
        Add data of states to the tree computing the Bloch spheres parameters

        Args:
            states (np.array) : complex array of M samples
            colors (np.array,None) : complex array of either Mx4 for already generated colors, M for values between 0 and 1 that will follow the colormap, by default it will be the indexes.
            cmap (str) : string name of a matplotlib colormap (default : 'jet')
        """

        assert (
            states.shape[0] == 2**self.num_qubits
        ), "The data doesnt fit the expected number of qubits"
        assert len(states.shape) == 2, "the data must be a 2D tensor"

        self.num_samples = states.shape[1]

        tree_vals = []
        tree_idxs = []

        fun_recursive(states, tree_vals=tree_vals, tree_idxs=tree_idxs, tol=None)

        self.tree_vals = tree_vals
        self.tree_idxs = tree_idxs

        if colors is not None:
            assert (colors.max() <= 1) and (
                colors.min() >= 0
            ), "the colors values must be between 0 and 1"
            if (
                len(colors.shape) == 2
            ):  # case in which the color is a a 2D tensor, colors matrix directly
                assert (
                    colors.shape[0] == 4
                ), "the colors matrix must be a 2D tensor of 4 (RGBA) by the number of samples"
                assert (
                    colors.shape[1] == self.num_samples
                ), "the colors matrix must be a 2D tensor of 4 (RGBA) by the number of samples"
                self.samples_colors = colors
            elif (
                len(colors.shape) == 1
            ):  # case in which the color is a a 1D tensor, create colors matrix with cmap
                assert (
                    colors.shape[0] == self.num_samples
                ), "the colors must have the same legth as the number of samples"
                cm_custom = cm.get_cmap(cmap, 256)
                self.samples_colors = cm_custom(colors)
        else:
            cm_custom = cm.get_cmap(cmap, self.num_samples)
            self.samples_colors = cm_custom(np.linspace(0, 1, self.num_samples))

    def plot_tree(
        self, azim: float = -40.0, elev: float = 30.0, size_sphere: float = 2.0
    ) -> None:
        """
        Display the binary tree

        Args:
            azim (float) : viewing angle : azimuth (default:-40)
            elev (float) : viewing angle : elevation (default:30)
            size_sphere (float) : size of each single sphere.
        """

        dw = 1 / (2 ** (self.num_qubits - 1))
        dh = 1 / self.num_qubits
        fig = plt.figure(figsize=(size_sphere / dw, size_sphere / dh))

        _ = fig.add_axes([0, 0, 1, 1])
        _.axis("off")

        for i, d in enumerate(self.tree_idxs):
            nlevel = self.num_qubits - len(d)
            h = (nlevel - 1) * dh
            if len(d) == 0:
                w = 0.5 - dw / 2
            else:
                nbit = int(d, 2)
                if nlevel == 1:
                    w = dw * nbit
                else:
                    w = (1 + 2 * nbit) / 2 ** (len(d) + 1) - dw / 2
            ax = fig.add_axes([w, h, dw, dh], projection="3d", azim=azim, elev=elev)
            the = self.tree_vals[i][0, :]
            phi = self.tree_vals[i][1, :]
            x, y, z = thephi_to_xyz(the, phi)
            bloch_points(x, y, z, colors=self.samples_colors, ax=ax)
