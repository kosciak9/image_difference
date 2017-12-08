"""
main.py

Example use of image_comp on samples provided

Nicholas Bochenski & Franciszek Madej
"""
import numpy as np

from image_comp import color_line, load_img, min_variance, perpendicular


print("which image compare to? 0-8")
index = int(input("> "))
# for i in range(9):
filename = 'samples/image' + str(index) + '.png'
img = load_img(filename)
best_perp_data = perpendicular(img, *min_variance(img))
color_lines = best_perp_data

x = np.array(color_line(img, *best_perp_data))
max_diff = (255**2) * len(x)

for i in range(9):
    filename = 'samples/image' + str(i) + '.png'
    img = load_img(filename)
    y = np.array(color_line(img, *best_perp_data))
    diff = x - y
    diff_sq = diff ** 2
    total_diff = np.sum(diff_sq)
    percentage_diff = str((1 - total_diff / max_diff) * 100) + "%"
    print("podobieństwo obrazka", i, "do obrazka", index,
          "to", percentage_diff)
