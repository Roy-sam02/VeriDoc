import math

logits = [0.0, math.log(2.0)]
correct = 1
learning_rate = 0.3

def probabilities(scores):
    shifted = [x - max(scores) for x in scores]
    weights = [math.exp(x) for x in shifted]
    return [x / sum(weights) for x in weights]

before = probabilities(logits)
gradient = [p - int(i == correct) for i, p in enumerate(before)]
updated_logits = [
    score - learning_rate * grad
    for score, grad in zip(logits, gradient)
]
after = probabilities(updated_logits)

print("Before:", [round(p, 3) for p in before])
print("Gradient:", [round(g, 3) for g in gradient])
print("After:", [round(p, 3) for p in after])