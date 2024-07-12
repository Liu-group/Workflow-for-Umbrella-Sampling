import os
import matplotlib.pyplot as plt

with open("metadata.dat", "w") as f:
    for i in range(32, -1, -1):
        f.write(f"dist_{i}/dist.dat {i} 4\n")

os.system("wham 0 32 100 0.000001 300 0 metadata.dat out.pmf")

# Delete the first line of the file
os.system("tail -n +2 out.pmf > temp.pmf && mv temp.pmf out.pmf")

# Delete all lines after the "WindowFree" string
os.system("sed -i '/Window/,$d' out.pmf")

# Extract the first two columns of data and save to pmf.dat
os.system("awk '{print $1, $2}' out.pmf > pmf.dat")

# Load data from file
x, y = [], []
with open('pmf.dat') as f:
    for line in f:
        cols = line.split()
        x.append(float(cols[0]))
        y.append(float(cols[1]))

# Create plot
plt.plot(x, y)
plt.xlabel('PMF')
plt.ylabel('Distance (nm)')
plt.title('PMF vs distance')

# Save plot as PDF
plt.savefig('plot.pdf')
