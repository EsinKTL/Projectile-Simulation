import math
import matplotlib

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

# Constants
dt = 0.01  # time step in seconds
N = 2000  # initial array size

# USER INPUTS

# Planet selection with gravity values
while True:
	try:
		g = str(input(
			"Choose a planet \n a. EARTH = 9.8 m/s^2 \n b. MOON = 1.62 m/s^2 \n c. MARS = 3.71 m/s^2 \n d. JUPİTER = 24.79 \n e. MERCURY = 3.7 m/s^2 \n f. VENUS = 8.87 m/s^2 \n g. SATURN = 10.44 m/s^2 \n h. URANUS = 8.69 m/s^2 \n i. NEPTUNE = 11.15 m/s^2 \n please write your answers by bullets num a, b, c, d, e, f, g, h or i : ")).lower()
		if g == "a":
			g = 9.8
			planet_name = "Earth"
			break
		elif g == "b":
			g = 1.62
			planet_name = "MOON"
			break
		elif g == "c":
			g = 3.71
			planet_name = "MARS"
			break
		elif g == "d":
			g = 24.79
			planet_name = "JUPITER"
			break
		elif g == "e":
			g = 3.7
			planet_name = "MERCURY"
			break
		elif g == "f":
			g = 8.87
			planet_name = "VENUS"
			break
		elif g == "g":
			g = 10.44
			planet_name = "SATURN"
			break
		elif g == "h":
			g = 8.69
			planet_name = "URANUS"
			break
		elif g == "i":
			g = 11.15
			planet_name = "NEPTUNE"
			break
		else:
			print("Please enter a, b, c, d, e, f, g, h or i")
			continue
	
	except ValueError:
		print("Please enter a valid string")

# Object type selection
while True:
	try:
		print("\nChoose object type:")
		print("1. Ball")
		print("2. Arrow")
		print("3. Rocket")
		print("4. Default (red dot)")
		object_type = input("Enter your choice (1-4): ")
		if object_type in ["1", "2", "3", "4"]:
			break
		else:
			print("Please enter a valid choice (1-4)")
	except:
		print("Please enter a valid input")

# Object name
while True:
	try:
		object_name = str(input("Enter name of the object: "))
		break
	except ValueError:
		print("Please enter a valid string")

# Initial horizontal position
while True:
	try:
		x0 = float(input("Enter initial horizontal position (m): "))
		break
	except ValueError:
		print("Please enter a valid number")

# Initial vertical position
while True:
	try:
		y0 = float(input("Enter initial vertical position (m): "))
		break
	except ValueError:
		print("Please enter a valid number")

# Initial velocity (must be positive)
while True:
	try:
		v0 = float(input("Enter initial velocity (m/s): "))
		if v0 <= 0:
			print("Please enter a positive value")
			continue
		else:
			break
	except ValueError:
		print("Please enter a valid number")

# Launch angle in degrees
while True:
	try:
		theta = float(input("Enter angle (degrees): "))
		if 0 <= theta <= 90:
			break
		else:
			print("Please enter an angle between 0 and 90 degrees")
	except ValueError:
		print("Please enter a valid number")

# Aerodynamic drag coefficient
while True:
	try:
		k = float(input("Enter aerodynamic drag coefficient (0 if ignored): "))
		if k < 0:
			print("Please enter a non-negative number")
		else:
			break
	except ValueError:
		print("Please enter a valid number")

# Mass of the object
while True:
	try:
		m = float(input("Enter mass of the object (kg): "))
		if m <= 0:
			print("Mass must be a positive number. Please try again.")
		else:
			break
	except ValueError:
		print("Please enter a valid number (e.g., 5.0, 10, 2.5)")

# PHYSICS CALCULATIONS

# Convert angle from degrees to radians for trigonometric functions
theta_rad = math.radians(theta)

# Calculate estimated number of steps based on flight time
N = int((2 * v0 / g + 20) / dt)

# Initialize arrays for position, velocity, and acceleration
x = np.zeros(N)  # horizontal positions
y = np.zeros(N)  # vertical positions
vx = np.zeros(N)  # horizontal velocities
vy = np.zeros(N)  # vertical velocities
ax = np.zeros(N)  # horizontal accelerations
ay = np.zeros(N)  # vertical accelerations

# Set initial values
x[0] = x0
y[0] = y0
vx[0] = v0 * math.cos(theta_rad)  # initial horizontal velocity component
vy[0] = v0 * math.sin(theta_rad)  # initial vertical velocity component

# Simulation loop using Euler integration
for i in range(N - 1):
	# Calculate current speed magnitude
	v = math.sqrt(vx[i] ** 2 + vy[i] ** 2)
	
	# Calculate forces and accelerations (with drag if k != 0)
	if k != 0:
		fDrag = k * v ** 2  # drag force magnitude
		ax[i] = -(fDrag / m) * (vx[i] / v)  # horizontal drag acceleration
		ay[i] = -g - (fDrag / m) * (vy[i] / v)  # vertical acceleration (gravity + drag)
	else:
		ax[i] = 0  # no horizontal acceleration without drag
		ay[i] = -g  # only gravity in vertical direction
	
	# Euler integration: update velocities and positions
	vx[i + 1] = vx[i] + ax[i] * dt  # new horizontal velocity
	vy[i + 1] = vy[i] + ay[i] * dt  # new vertical velocity
	x[i + 1] = x[i] + vx[i] * dt  # new horizontal position
	y[i + 1] = y[i] + vy[i] * dt  # new vertical position
	
	# Stop simulation when object hits the ground (y < 0)
	if y[i + 1] < 0:
		y[i + 1] = 0  # set y to exactly 0
		# Linear interpolation for more accurate impact point
		x[i + 1] = x[i] + vx[i] * dt * (y[i] / (y[i] - y[i + 1]))
		# Trim arrays to actual simulation length
		x = x[:i + 2]
		y = y[:i + 2]
		break

# Calculate results: total flight time, range, and maximum height
t_total = len(x) * dt  # total time = number of steps × time step
r = x[-1]  # range = final x position
h_max = np.max(y)  # maximum height = highest y value

# VISUALIZATION & ANIMATION

# Create figure and axis for plotting
fig, ax_plot = plt.subplots(figsize=(12, 8))


# Function to add background image based on planet
def add_background_image(planet_name):
	try:
		image_path = f"images/{planet_name.lower()}.jpg"  # look for jpg file
		img = mpimg.imread(image_path)  # load image
		# Display image as background with proper extent
		ax_plot.imshow(img, extent=[0, max(x) * 1.1, 0, max(y) * 1.1],
		               aspect='auto', alpha=0.7, zorder=0)
	except FileNotFoundError:
		# Fallback to colors if image not found
		print(f"Background image for {planet_name} not found. Using color instead.")
		sky_colors = {
			"Earth": '#87CEEB', "MOON": '#000033', "MARS": '#FF6B6B',
			"JUPITER": '#FFA500', "MERCURY": '#A9A9A9', "VENUS": '#FFD700',
			"SATURN": '#FFDEAD', "URANUS": '#AFEEEE', "NEPTUNE": '#1E90FF'
		}
		ax_plot.set_facecolor(sky_colors.get(planet_name, '#e6f2ff'))


# Function to load object image based on type selection
def load_object_image(obj_type, x_pos, y_pos):
	object_images = {
		'1': 'ball.png',  # ball image
		'2': 'arrow.png',  # arrow image
		'3': 'rocket.png'  # rocket image
	}

	if obj_type in object_images:
		try:
			img = mpimg.imread(f"images/{object_images[object_type]}")  # load object image
			imagebox = OffsetImage(img, zoom=0.05)  # create image box with scaling
			# Create annotation box at specified position
			ab = AnnotationBbox(imagebox, (x_pos, y_pos), frameon=False)
			ax_plot.add_artist(ab)  # add to plot
			return ab
		except FileNotFoundError:
			# Fallback to red dot if image not found
			print(f"Object image {object_images[obj_type]} not found. Using default marker.")
			return ax_plot.plot([x_pos], [y_pos], 'ro', markersize=8)[0]
	else:
		# Default red dot for option 4
		return ax_plot.plot([x_pos], [y_pos], 'ro', markersize=8)[0]


# Set plot limits and labels
ax_plot.set_xlim(0, max(x) * 1.1)  # x-axis limit with 10% margin
ax_plot.set_ylim(0, max(y) * 1.1)  # y-axis limit with 10% margin
ax_plot.set_xlabel("Horizontal Distance (m)", fontsize=12)
ax_plot.set_ylabel("Vertical Height (m)", fontsize=12)
ax_plot.grid(True, alpha=0.3)  # grid with transparency

# Add background image or color
add_background_image(planet_name)

# Static points for start, landing, and max height positions
ax_plot.scatter([x[0]], [y[0]], color='green', s=100, label='Start', zorder=5)
ax_plot.scatter([x[-1]], [y[-1]], color='red', s=100, label='Landing', zorder=5)
max_y_index = np.argmax(y)  # index of maximum height
ax_plot.scatter([x[max_y_index]], [y[max_y_index]], color='orange', s=100,
                label='Max Height', zorder=5)

# Horizontal line at maximum height
ax_plot.axhline(y=h_max, color='violet', linestyle='--', alpha=0.5, label='Max Height Line')
# Annotation showing max height value
ax_plot.annotate(f'{h_max:.1f}m', xy=(x[max_y_index] / 2, h_max),
                 xytext=(0, 10), textcoords='offset points',
                 ha='center', color='orange', fontweight='bold')

# Vertical line at maximum height position and range line
ax_plot.plot([x[max_y_index], x[max_y_index]], [0, y[max_y_index]],
             'orange', linestyle='--', alpha=0.7, label='Max Height Line')
ax_plot.plot([0, x[-1]], [0, 0], 'red', linestyle='--', alpha=0.7, label='Range Line')

# Create object based on selection
if object_type in ['1', '2', '3']:
    # For image objects, we'll use a different approach
    point, = ax_plot.plot([], [], 'ro', markersize=0, alpha=0)  # invisible point
    # Load the initial object image
    try:
        obj_img = mpimg.imread({'1': 'ball.png', '2': 'arrow.png', '3': 'rocket.png'}[object_type])
        imagebox = OffsetImage(obj_img, zoom=0.10)
        ab = AnnotationBbox(imagebox, (x[0], y[0]), frameon=False)
        ax_plot.add_artist(ab)
    except FileNotFoundError:
        print(f"Object image not found. Using default marker.")
        point, = ax_plot.plot([], [], 'ro', markersize=8, label=f'{object_name} position', zorder=5)
        ab = None
else:
    # For default option, use regular point
    point, = ax_plot.plot([], [], 'ro', markersize=8, label=f'{object_name} position', zorder=5)
    ab = None

# Trajectory line
traj_line, = ax_plot.plot([], [], 'b-', linewidth=1.5, alpha=0.7, label='Trajectory')

# Information box with simulation parameters
info_text = (
	f"Object: {object_name}\n"
	f"Planet: {planet_name}\n"
	f"Initial Velocity: {v0:.2f} m/s\n"
	f"Angle: {theta:.2f}°\n"
	f"Flight Time: {t_total:.2f} s\n"
	f"Range: {r:.2f} m\n"
	f"Max Height: {h_max:.2f} m\n"
	f"Drag Coefficient: {k:.4f}"
)
# Style properties for info box
props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
ax_plot.text(0.02, 0.98, info_text, transform=ax_plot.transAxes, fontsize=10,
             verticalalignment='top', bbox=props)

# Time display during animation
time_text = ax_plot.text(0.02, 0.02, '', transform=ax_plot.transAxes, fontsize=12,
                         bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))


# Animation update function
def update(frame):
    if object_type in ['1', '2', '3'] and ab is not None:
        # For image objects, update the AnnotationBbox position
        ab.xybox = (x[frame], y[frame])
        ab.xy = (x[frame], y[frame])
    else:
        # For default object, update the point position
        point.set_data([x[frame]], [y[frame]])
    
    # Update trajectory and time
    traj_line.set_data(x[:frame + 1], y[:frame + 1])
    time_text.set_text(f'Time: {frame * dt:.2f} s')
    
    if object_type in ['1', '2', '3'] and ab is not None:
        return ab, traj_line, time_text
    else:
        return point, traj_line, time_text


# Create title based on simulation parameters
title_text = f"Projectile Motion of {object_name}"
if k != 0:
	title_text += " with Air Resistance"
title_text += f" at {planet_name}"
plt.title(title_text, fontsize=14, fontweight='bold')

# Add legend and adjust layout
plt.legend(loc='upper right')
plt.tight_layout()

# Create animation
ani = FuncAnimation(fig, update, frames=len(x), interval=10, blit=False, repeat=False)

# Display the animation
plt.show()