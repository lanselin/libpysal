"""
:mod:`ergodic` --- summary measures for ergodic Markov chains
=============================================================

"""

__author__  = "Sergio J. Rey <srey@asu.edu> "

import numpy as np
import numpy.linalg as la


def steady_state(P):
    """
    Calculates the steady state probability vector for a regular Markov
    transition matrix P

    Parameters
    ----------

    P        : matrix (kxk)
               an ergodic Markov transition probability matrix

    Returns
    -------

    implicit : matrix (kx1)
               steady state distribution

    Examples
    --------
    >>> import numpy as np
    >>> p=np.matrix([[.5, .25, .25],[.5,0,.5],[.25,.25,.5]])
    >>> steady_state(p)
    matrix([[ 0.4],
            [ 0.2],
            [ 0.4]])
    """

    v,d=la.eig(np.transpose(P))

    # for a regular P maximum eigenvalue will be 1
    mv=max(v)
    # find its position
    i=v.tolist().index(mv)

    # normalize eigenvector corresponding to the eigenvalue 1
    return d[:,i]/sum(d[:,i])

def fmpt(P):
    """
    Calculates the matrix of first mean passage times for an
    ergodic transition probability matrix.

    Parameters
    ----------

    P    : matrix (kxk)
           an ergodic Markov transition probability matrix

    Returns
    -------

    M    : matrix (kxk)
           elements are the expected value for the number of intervals
           required for  a chain starting in state i to first enter state j

    Examples
    --------
    
    Taken from Kemeny and Snell. Land of Oz example where the states are
    Rain, Nice and Snow - so there is 25 percent chance that if it
    rained in Oz today, it will snow tomorrow, while if it snowed today in
    Oz there is a 50 percent chance of snow again tomorrow and a 25
    percent chance of a nice day (nice, like when the witch with the monkeys
    is melting).

    >>> import numpy as np
    >>> p=np.matrix([[.5, .25, .25],[.5,0,.5],[.25,.25,.5]])
    >>> fm=fmpt(p)
    >>> fm
    matrix([[ 0.        ,  4.        ,  3.33333333],
            [ 2.66666667,  0.        ,  2.66666667],
            [ 3.33333333,  4.        ,  0.        ]])
    
    Notes
    -----

    Uses formulation (and examples on p. 218) in Kemeny and Snell (1976) [1]_

    References
    ----------
    
    .. [1] Kemeny, John, G. and J. Laurie Snell (1976) Finite Markov
       Chains. Springer-Verlag. Berlin
    """
    A=P**1000
    n,k=A.shape
    I=np.identity(k)
    Z=la.inv(I-P+A)
    M=np.zeros_like(Z)
    for i in range(k):
        for j in range(k):
            M[i,j]=(Z[j,j]-Z[i,j])/A[j,j]
    return M 

def _test():
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    _test()