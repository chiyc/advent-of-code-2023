from input import read_input


histories = []
for _line in read_input(9):
    histories.append(list(map(int, _line.split(' '))))

def get_differences(history):
    differences = []
    step = history
    while any(difference != 0 for difference in step):
        step = [a - b for a, b in zip(step[1:], step[:-1])]
        differences.append(step)
    return differences

def predict_next_value(history):
    differences = get_differences(history)
    next_value_difference = sum([step[-1] for step in differences])
    return history[-1] + next_value_difference

def predict_past_value(history):
    differences = get_differences(history)
    past_value_difference = 0
    for step in reversed(differences):
        past_value_difference = step[0] - past_value_difference
    return history[0] - past_value_difference

print('Part 1: ', sum(map(predict_next_value, histories))) # 1882395907
print('Part 2: ', sum(map(predict_past_value, histories))) # 1005
