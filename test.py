students = {}

for _ in range(int(input())):
    name, *scores = input().split()
    students[name] = list(map(int, scores))

best_three = sorted(students.items(), key=lambda x: -sum(x[1]))[:3]

if best_three[2][1]:
    best_three.append(best_three[2])

for name, _ in best_three:
    print(name)