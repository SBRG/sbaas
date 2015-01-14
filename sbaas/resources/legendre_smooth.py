"""
    legendre_smooth.py - approximate noisy time series data by a smooth function

    Copyright (c) 2013 Greg von Winckel

    Permission is hereby granted, free of charge, to any person obtaining
    a copy of this software and associated documentation files (the
    "Software"), to deal in the Software without restriction, including
    without limitation the rights to use, copy, modify, merge, publish,
    distribute, sublicense, and/or sell copies of the Software, and to
    permit persons to whom the Software is furnished to do so, subject to
    the following conditions:

    The above copyright notice and this permission notice shall be
    included in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
    MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
    IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY 
    CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, 
    TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
    SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

    Created on Sun Nov 10 09:59:25 MST 2013

"""



import numpy as np
from numpy.polynomial.legendre import legvander,legder
from scipy.linalg import qr,solve_triangular,lu_factor,lu_solve

class legendre_smooth(object):
    def __init__(self,n,k,a,m):
        self.k2 = 2*k

        # Uniform grid points
        x = np.linspace(-1,1,n)

        # Legendre Polynomials on grid 
        self.V = legvander(x,m-1)

        # Do QR factorization of Vandermonde for least squares 
        self.Q,self.R = qr(self.V,mode='economic')

        I = np.eye(m)
        D = np.zeros((m,m))
        D[:-self.k2,:] = legder(I,self.k2)

        # Legendre modal approximation of differential operator
        self.A = I-a*D

        # Store LU factors for repeated solves   
        self.PLU = lu_factor(self.A[:-self.k2,self.k2:])


    def fit(self,z):

        # Project data onto orthogonal basis 
        Qtz = np.dot(self.Q.T,z)

        # Compute expansion coefficients in Legendre basis
        zhat = solve_triangular(self.R,Qtz,lower=False)

        # Solve differential equation       
        yhat = np.zeros(len(zhat))
        q = np.dot(self.A[:-self.k2,:self.k2],zhat[:self.k2])
        r = zhat[:-self.k2]-q
        yhat[:self.k2] = zhat[:self.k2]
        yhat[self.k2:] = lu_solve(self.PLU,r)
        y = np.dot(self.V,yhat)
        return y


