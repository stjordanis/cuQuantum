import numpy as np
import cupy as cp

import cuquantum
from cuquantum import custatevec as cusv


nIndexBits = 3
nSvSize    = (1 << nIndexBits)
paulis     = [[cusv.Pauli.I], [cusv.Pauli.X, cusv.Pauli.Y]]
basisBits  = [[1], [1, 2]]
nBasisBits = [len(arr) for arr in basisBits]

exp_values = np.empty(len(paulis), dtype=np.float64)
expected   = np.asarray([1.0, -0.14], dtype=np.float64)

d_sv       = cp.asarray([0.0+0.0j, 0.0+0.1j, 0.1+0.1j, 0.1+0.2j,
                         0.2+0.2j, 0.3+0.3j, 0.3+0.4j, 0.4+0.5j], dtype=np.complex64)

####################################################################################

# cuStateVec handle initialization
handle = cusv.create()

# apply Pauli operator
cusv.expectations_on_pauli_basis(
    handle, d_sv.data.ptr, cuquantum.cudaDataType.CUDA_C_32F, nIndexBits, exp_values.ctypes.data,
    paulis, basisBits, nBasisBits, len(paulis))

# destroy handle
cusv.destroy(handle)

# check result
if not cp.allclose(expected, exp_values):
    raise ValueError("results mismatch")
else:
    print("test passed")