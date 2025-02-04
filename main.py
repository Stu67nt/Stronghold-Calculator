import keyboard
import math
import pyperclip
import time

def read_location_data(location_data:str):
    """Returns a list with postiton data of player\n
    Format: [x,y,z,yaw,pitch]"""
    try:
        split_data = location_data.split(" ")
        for count in range(0, 6):
            split_data.pop(0)
        for index in range(0,len(split_data)):
            split_data[index] = float(split_data[index])
        split_data[3] = standarise_degrees(split_data[3])
        return split_data
    except Exception: # Copied data not in expected format. User likely copied something random
        return -2

def standarise_degrees(mc_ang:float):
    """Keeps angles between minecraft's normal -180 - 180 range"""
    while mc_ang < -180:
        mc_ang += 360
    while mc_ang >= 180:
        mc_ang -= 360
    return mc_ang

def gradient_calc(mc_ang:float):
    """Returns the gradient of the minecraft angle"""
    return -1/(math.tan(math.radians(mc_ang)))

def constant_calc(x:float, z:float, m:float):
    """Returns the constant in the line equation"""
    return z-(x*m)

def intersect_lines(m1:float, c1:float, m2:float, c2:float):
    """Returns the intersection of 2 different straight lines"""
    x = (c2-c1)/(m1-m2)
    z = (m1*x)+c1
    return x,z

def nether_portal_coords(x:float, z:float):
    """Converts overworld x and z coordinates into their nether counterparts"""
    return x/8,  z/8

def get_pos_data():
    """Returns the text gotten from f3+c if gotten from minecraft"""
    print("Waiting for F3+C...")
    text = ""
    while  text.find("/execute in minecraft:overworld run tp @s"):
        keyboard.wait("f3+c")
        time.sleep(0.01) # Sometimes clipboard is read too quick causing it to read same pos twice
        text = pyperclip.paste()
    return text

def main(pos1, pos2):
    filtered_pos1 = read_location_data(pos1)
    filtered_pos2 = read_location_data(pos2)
    if filtered_pos1 == -2 or filtered_pos2 == -2:
        print("Invalid position coordinates copied.")
        return -1
    m1 = gradient_calc(filtered_pos1[3])
    m2 = gradient_calc(filtered_pos2[3])
    c1 = constant_calc(filtered_pos1[0], filtered_pos1[2], m1)
    c2 = constant_calc(filtered_pos2[0], filtered_pos2[2], m2)
    if m1 != m2:
        x, z = intersect_lines(m1, c1, m2, c2)
        nx, nz = nether_portal_coords(x, z)
        print(f"Predicted Overworld Coords: x: {x}, z: {z}")
        print(f"Predicted Nether Portal Coords: x: {nx}, z: {nz}\n")
    else:
        print("Parallel lines lol\n")
        return -2

if __name__ == "__main__":
    while True:
        pos1 = get_pos_data()
        pos2 = get_pos_data()
        main(pos1, pos2)
