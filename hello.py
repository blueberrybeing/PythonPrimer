classmates = ['Michael', 'Bob', 'Tracy']

for name in classmates:
	print(name)
classmates.insert(1, 'shit')
classmates.insert(-1, 'John')

print("after insert two elements")
for name in classmates:
	print(name)


print("after insert diff element")
classmates.insert(0, True)

for name in classmates:
	print(name)

print("after pop index 1")
classmates.pop(1)
print(len(classmates))

for name in classmates:
	print(name)
