# This import registers the 3D projection, but is otherwise unused.
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

def update_line(lin):
    # line.set_data(data[..., :num])
    # lines.set_data()
    x, y = lx.get_data();
    x = 0
    y += 500
    lx.set_data(x, y);
    print("zxxxxxxxx");
    return lx,

def init_func():
	print("init_func")

if __name__ == '__main__':
	plt.rcParams['legend.fontsize'] = 10

	fig = plt.figure()
	ax = fig.gca(projection='3d')
	rotx = np.eye(3);

	theta = 0#np.pi/6;
	rotx[1,1] = np.cos(theta);
	rotx[1,2] = -np.sin(theta);
	rotx[2,1] = np.sin(theta);
	rotx[2,2] = np.cos(theta);


	# Prepare arrays x, y, z
	theta = np.linspace(-4 *np.pi + np.pi
		/180, 4 * np.pi, 100)
	z = np.linspace(-2, 2, 100)
	r = z*0
	x = r * np.sin(theta)
	y = r * np.cos(theta)

	vec = np.vstack([x,y,z])

	new_vec = np.matmul(rotx, vec);
	# lx, = ax.plot(new_vec[0,:], new_vec[1,:], new_vec[2,:], label='parametric curve');
	# ly, = ax.plot(new_vec[0,:], new_vec[2,:], new_vec[1,:], label='parametric curve');
	# lz, = ax.plot(new_vec[2,:], new_vec[0,:], new_vec[1,:], label='parametric curve');

	lin = np.linspace(-2, 2, 10)
	lx, = ax.plot(lin, 0*lin, 0*lin, label='parametric curve');
	ly, = ax.plot(0*lin, lin, 0*lin, label='parametric curve');
	lz, = ax.plot(0*lin, 0*lin, lin, label='parametric curve');

	# x, y = lx.get_data();
	# x = 0
	# y += 500
	# lx.set_data(x, y);

	line_ani = animation.FuncAnimation(fig, update_line, 5, blit=False, interval=5, repeat=False)
	print(lx.get_data())

	# ax.legend()
	plt.show()