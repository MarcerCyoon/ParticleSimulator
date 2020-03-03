import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

class Simulation:
    def __init__(self, numParticles, velocities, positions, masses, coeff=3):
       self.numParticles = numParticles
       self.velocities = np.zeros((numParticles, 2))
       self.positions = np.zeros((numParticles, 2))
       self.masses = np.zeros(numParticles)
       self.accelerations = np.zeros((numParticles, 2))
       self.coeff = coeff

       for i in range(0, numParticles):
            self.velocities[i] = velocities[i]
            self.positions[i] = positions[i]
            self.masses[i] = masses[i]

    def step(self):
        for i in range(0, self.numParticles):
            self.velocities[i] = self.accelerations[i] + self.velocities[i]
            self.positions[i] = self.velocities[i] + self.positions[i]

        for i in range(0, self.numParticles):
            for j in range(0, self.numParticles):
                if (i == j):
                    continue

                if (np.linalg.norm(self.positions[i] - self.positions[j]) < 1):
                    self.velocities[i] = -1 * self.velocities[i]
                    self.accelerations[i] = np.zeros(2)
                    self.velocities[j] = -1 * self.velocities[j]
                    self.accelerations[j] = np.zeros(2)

    def applyForce(self, particleNum):
        for i in range(0, self.numParticles):
            if i == particleNum:
                continue
            else:
                diff = self.positions[i] - self.positions[particleNum]

                dist = np.linalg.norm(diff)

                force = (G_CONST * self.masses[i] / (dist ** self.coeff)) * diff

                self.accelerations[particleNum] += force

    #def combine(particleOne, particleTwo):

# Using a slightly bigger G so that the forces apply more quickly, for the sake of nicer animations.
G_CONST = 6.67 * (10 ** -4)


def determineAx(positions):
    print(positions)
    xlow = min(positions[:,0]) - np.mean(positions[:,0]) - 30
    xhigh = max(positions[:,0]) + np.mean(positions[:,0]) + 30
    ylow = min(positions[:,1]) - np.mean(positions[:,1]) - 30
    yhigh = max(positions[:, 1]) + np.mean(positions[:,1]) + 30

    print(xlow)
    print(xhigh)
    print(ylow)
    print(yhigh)

    return (xlow, xhigh, ylow, yhigh)


def generate(numParticles, masses, vels, poss, time, coeff):
    # Setting some constants here.
    # A two-body simulation is what we are currently demonstrating.
    # Time Constant tells us how many steps to run.
    # A 1000 mass is assigned to both objects, for now, to simplify the prototype.
    sim = Simulation(numParticles, vels, poss, masses, coeff)

    fig = plt.figure()

    xlow, xhigh, ylow, yhigh = determineAx(poss)

    ax = plt.axes(xlim=(xlow, xhigh), ylim=(ylow, yhigh))
    points, = ax.plot([], [], 'bo', ms=6)

    def init():
        arr_x = []
        arr_y = []
        for i in range(0, sim.numParticles):
            arr_x.append(sim.positions[i][0])
            arr_y.append(sim.positions[i][1])

        points.set_data(np.array(arr_x), np.array(arr_y))

        return points,

    def animate(i):
        for i in range(0, sim.numParticles):
            sim.applyForce(i)

        sim.step()

        arr_x = []
        arr_y = []
        for i in range(0, sim.numParticles):
            arr_x.append(sim.positions[i][0])
            arr_y.append(sim.positions[i][1])

        points.set_data(np.array(arr_x), np.array(arr_y))
        return points,

    anim = animation.FuncAnimation(fig, animate, init_func=init, frames=time, interval=10, blit=True)

    fileName = "physics" + str(int(vels[0][0] + vels[0][1])) + str(int(vels[1][0] + vels[1][1])) + str(int(poss[0][0] + poss[0][1])) + str(int(poss[1][0] + poss[1][1])) + ".mp4"

    anim.save("static/" + fileName, writer='ffmpeg')

    return fileName
