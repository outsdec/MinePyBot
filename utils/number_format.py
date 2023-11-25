def spaces_mine(number):
    n = str(number)[::-1]
    return(' '.join(n[i:i+3] for i in range(0, len(n), 3))[::-1])

def spaces(number):
    return('{:,.4f}'.format(number).replace(',', ' '))