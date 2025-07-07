def sym_difference(set1, set2):
    print("\nOriginal sets:")
    print(set1)
    print(set2)
    result = set1.symmetric_difference(set2)
    print("\nSymmetric difference of setc1 - setc2:")
    return result


setb1 = set([1, 1, 2, 3, 4, 5])
setb2 = set([1, 5, 6, 7, 8, 9])

print("Result of B Sets")
print(sym_difference(setb1, setb2))
