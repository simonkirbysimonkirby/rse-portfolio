import matplotlib.pyplot as plt


def visualise_fitness(min_distances):
    """Creates simple plot showing the optimisation improvement across epochs

    Args:
        min_distances (list): list of the minimum distances travelled (best sequences identified) per epoch

    Returns:
        None
    """

    fig, ax = plt.subplots()
    fig.set_size_inches(16, 10)
    ax.plot(min_distances, c='deepskyblue', linewidth='3')
    plt.ylabel('Distance travelled by nurse, m')
    plt.xlabel('Epoch')
    plt.title("Improvement of distance travelled over epochs")
    plt.savefig("output/output_1_optimisation_of_travelling_person_problem.png")
    plt.show()
