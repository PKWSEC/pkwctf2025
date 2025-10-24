# ECC Challenge 1 - Simple curve (small prime)
# This challenge can be solved using brute force or discrete_log

def solve_ecc1(p, A, B, P_coords, Q_coords):
    # Create the elliptic curve
    E = EllipticCurve(GF(p), [A, B])
    
    # Create point objects
    P = E(P_coords)
    Q = E(Q_coords)
    
    # Since p is small, we can use brute force or discrete_log
    print("Solving discrete logarithm problem...")
    
    # Method 1: Use Sage's discrete_log (most efficient)
    k = discrete_log(Q, P, operation='+')
    
    return k

# Example usage:
if __name__ == "__main__":
    print("ECC Challenge 1 - Simple Curve Solver")
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
    
    k = solve_ecc1(p, A, B, (Px, Py), (Qx, Qy))
    print(f"Found k: {k}")
    print(f"Submit this value: {k}")