import math

logits = [0.0, math.log(2.0)]
correct_character = 1

shifted = [score - max(logits) for score in logits]
weights = [math.exp(score) for score in shifted]
probabilities = [weight / sum(weights) for weight in weights]
loss = -math.log(probabilities[correct_character])

print("Probabilities:", [round(p, 3) for p in probabilities])
print("Loss:", round(loss, 3))