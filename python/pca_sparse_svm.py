import os
import sys
from util import load_pca_proj, shuffle_in_unison, load_pca_test, write_results, load_labeled_training, standardize, load_unlabeled_training, load_public_test
from sklearn.decomposition import SparsePCA
from sklearn.decomposition import KernelPCA
from sklearn.decomposition import DictionaryLearning, MiniBatchDictionaryLearning
from sklearn.decomposition import SparseCoder
from sklearn.svm import SVC
from sklearn import cross_validation
import numpy as np

def main():
    images, labels = load_labeled_training(flatten=True)
    images = standardize(images)
    unl = load_unlabeled_training(flatten=True)
    unl = standardize(unl)
    test = load_public_test(flatten=True)
    test = standardize(test)
    shuffle_in_unison(images, labels)
    #d = DictionaryLearning().fit(images)
    d = MiniBatchDictionaryLearning(n_components=500, n_iter=500, verbose=True).fit(images)
    s = SparseCoder(d.components_)
    proj_test = s.transform(images)
    pt = s.transform(test)
    #kpca = KernelPCA(kernel="rbf")
    #kpca.fit(unl)
    #test_proj = kpca.transform(images)
    #pt = kpca.transform(test)
    #spca = SparsePCA().fit(unl)
    #test_proj = spca.transform(images)
    #pt = spca.transform(test)
    svc = SVC()
    scores = cross_validation.cross_val_score(svc, proj_test, labels, cv=10)
    print scores
    print np.mean(scores)
    print np.var(scores)
    svc.fit(proj_test, labels)
    pred = svc.predict(pt)
    write_results(pred, '../svm_res.csv')


if __name__ == '__main__':
    sys.exit(main())
