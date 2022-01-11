a = 5
print(f'адрес памяти объекта {id(a)}')
a + 5
print(a)
print(f'адрес памяти объекта {id(a)}')
a = a + 5
print(f'адрес памяти объекта {id(a)}')
print(a)
list = [1,2,3]
print(f'адрес памяти объекта {id(list)}')
list.append(20)
print(f'адрес памяти объекта {id(list)}')
[*list] + [2]
print(list)
print(f'адрес памяти объекта {id(list)}')