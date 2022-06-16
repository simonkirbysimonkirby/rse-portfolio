import matplotlib.pyplot as plt


def visualise_fitness(min_distances):

    fig, ax = plt.subplots()
    fig.set_size_inches(16, 10)
    ax.plot(min_distances, c='deepskyblue', linewidth='3')
    plt.ylabel('Distance travelled by nurse, m')
    plt.xlabel('Epoch')
    plt.title("Improvement of distance travelled over epochs")
    plt.show()
