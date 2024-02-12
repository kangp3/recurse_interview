def crackle_pop(n):
    if n % 15 == 0:
        return "CracklePop"
    if n % 5 == 0:
        return "Pop"
    if n % 3 == 0:
        return "Crackle"
    return str(n)

if __name__ == "__main__":
    assert crackle_pop(27) == "Crackle"
    assert crackle_pop(65) == "Pop"
    assert crackle_pop(75) == "CracklePop"
    assert crackle_pop(32) == "32"

    for n in range(1, 101):
        print(crackle_pop(n))
