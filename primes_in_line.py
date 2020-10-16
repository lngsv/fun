print(*(i for i in range(2, 1000) if not tuple(j for j in range(2, int(__import__("math").sqrt(i))+1) if not i%j)), sep='\n')
