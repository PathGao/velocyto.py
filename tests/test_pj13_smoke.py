import numpy as np
import velocyto as vcy


def test_import_and_version():
    assert isinstance(vcy.__version__, str) and vcy.__version__


def test_balanced_knn_graph_shape():
    rs = np.random.RandomState(0)
    X = rs.normal(size=(60, 5))
    bknn = vcy.BalancedKNN(k=5, sight_k=20, maxl=10, mode="distance", n_jobs=1)
    bknn.fit(X)
    knn = bknn.kneighbors_graph(mode="distance")
    assert knn.shape == (60, 60)
    assert knn.nnz > 0


def test_fit_slope_shape():
    rs = np.random.RandomState(0)
    X = rs.uniform(1, 10, size=(7, 40))
    Y = 0.5 * X + rs.normal(scale=0.01, size=X.shape)
    gammas = vcy.fit_slope(Y, X)
    assert gammas.shape == (7,)
    assert np.allclose(gammas, 0.5, atol=0.05)
