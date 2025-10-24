# ECC Challenge 2 - Smooth order curve (Pohlig-Hellman attack) with fixed generator

def solve_ecc2(p, A, B, P_coords, Q_coords):
    # Create the elliptic curve
    E = EllipticCurve(GF(p), [A, B])
    
    # Create point objects
    P = E(P_coords)
    Q = E(Q_coords)
    
    print(f"Full curve order: {E.order()}")
    print(f"Order of P: {P.order()}")
    
    # Use Sage's built-in discrete_log with full curve order
    print("Using Sage's built-in discrete_log with full curve order...")
    try:
        k = discrete_log(Q, P, ord=E.order(), operation='+')
        return k
    except Exception as e:
        print(f"Error with full curve order: {e}")
    
    # Fallback to using only P's order
    print("Falling back to using only P's order...")
    try:
        k = discrete_log(Q, P, ord=P.order(), operation='+')
        return k
    except Exception as e:
        print(f"Error with P's order: {e}")
    
    return None

# Example usage:
if __name__ == "__main__":
    print("ECC Challenge 2 - Smooth Order Curve Solver")
    print("Enter the parameters from the challenge:")
    
    p = int(input("p: "))
    A = int(input("A: "))
    B = int(input("B: "))
    
    print("Enter point P coordinates:")
    Px = int(input("Px: "))
    Py = int(input("Py: "))
    
    print("Enter point Q coordinates:")
    Qx = int(input("Qx: "))
    Qy = int(input("Qy: "))
    
    k = solve_ecc2(p, A, B, (Px, Py), (Qx, Qy))
    
    if k is not None:
        print(f"Found k: {k}")
        print(f"Submit this value: {k}")
        
        # Verification
        E = EllipticCurve(GF(p), [A, B])
        P = E(Px, Py)
        Q = E(Qx, Qy)
        if k * P == Q:
            print("Verification: SUCCESS - k * P = Q")
        else:
            print("Verification: FAILED - k * P != Q")
    else:
        print("Failed to find k.")