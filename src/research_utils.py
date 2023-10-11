import numpy as np


def compute_fleiss_kappa(data, raters=None, label_mappings=None):
    """
    Compute Fleiss' Kappa for a given DataFrame of raters' judgements.
    
    Parameters
    ----------
    data : pd.DataFrame
        A DataFrame where each row represents an item and each column represents a rater's judgement.
        
    raters : list of str, optional
        A list of column names in `data` that represent the raters. If None, assumes all columns
        represent raters. Default is None.
        
    label_mappings : dict, optional
        A dictionary that maps judgements to their descriptive labels.
        For example: {1: "Label_1", 0: "Label_0", 2: "Label_2"}. If None, mappings are automatically generated
        from unique values in `data`. Default is None.
    
    Returns
    -------
    kappa : float
        The computed Fleiss' Kappa score.
    
    Example
    -------
    >>> data = pd.DataFrame({
    ...     'Rater1': [1, 0, 1, 2],
    ...     'Rater2': [1, 2, 1, 0],
    ...     'Rater3': [1, 0, 1, 2]
    ... })
    >>> kappa = compute_fleiss_kappa(data)
    >>> print(kappa)
    """
    # If raters are not specified, assume all columns are raters
    if raters is None:
        raters = data.columns.tolist()
    
    # If label mappings are not specified, automatically generate them from unique values in data
    if label_mappings is None:
        unique_values = np.unique(data[raters].values)
        label_mappings = {val: f"Label_{val}" for val in unique_values}
    
    # Convert judgements into counts for each label
    for label, label_str in label_mappings.items():
        data[label_str] = data[raters].apply(lambda x: sum(x == label), axis=1)
    
    # Extract the columns corresponding to label counts and convert to a matrix M
    M = data[list(label_mappings.values())].values
    
    N, k = M.shape  # N is # of items, k is # of categories
    n_annotators = float(np.sum(M[0, :]))  # # of annotators
    
    p = np.sum(M, axis=0) / (N*n_annotators)  # proportions of all assignments to k categories
    P = (np.sum(M * M, axis=1) - n_annotators) / (n_annotators * (n_annotators - 1))  # proportions of agreement for each item
    
    Pbar = np.sum(P) / N  # mean proportion of agreement
    PbarE = np.sum(p * p)  # expected agreement if assignments are random
    
    kappa = (Pbar - PbarE) / (1 - PbarE)
    
    return kappa
