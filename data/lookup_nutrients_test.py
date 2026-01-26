from lookup_nutrients import find_match

x = input("Food Item: ")

while x!='stop':
    x_match = find_match(x)
    print(x_match)
    x = input("Food Item: ")