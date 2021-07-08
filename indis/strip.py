import numpy as np

def strip(close, i=0, n=30 ): 
    """
    close - parent array
    i - index
    n - number of values before

    returns out - array of lenght n before index i
    """
    
    if i<n :
        return None
    
    out = np.array([])

    for j in range(n):
        val = close[ i-j ]
        out = np.append(out, val)
        
    return out

if __name__ == "__main__":
    a = np.array([[32610.,32580.43,32603.99],[32610.,32581.65,32607.28],[32609.11,32600.07,32601.25],[32610.,32580.43,32603.99],[32610.,32581.65,32607.28],[32609.11,32600.07,32601.25]])
    out = strip(a, i=4, n=3)

    x = out.reshape(3,3)
    print(type(a))
    print(out)

    print(x)
    