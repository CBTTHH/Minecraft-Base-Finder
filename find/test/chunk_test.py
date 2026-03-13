import minescript as m
import math, time

start_time = time.perf_counter()
x, y, z = map(math.floor, m.player().position)

MAX_Y_LEVEL = 319
MIN_Y_LEVEL = -64

Y_LEVEL_SEARCHING_SKY_TH = (MAX_Y_LEVEL - 7, MAX_Y_LEVEL)
Y_LEVEL_SEARCHING_UNDERGROUND_TH = (MIN_Y_LEVEL + 4, -40)
Y_LEVEL_SEARCHING_SURFACE_TH = (60, 120)

SEARCHING_RADIUS = 4

block_x_min = x - 16 * SEARCHING_RADIUS
block_x_max = x + 16 * SEARCHING_RADIUS

block_z_min = z - 16 * SEARCHING_RADIUS
block_z_max = z + 16 * SEARCHING_RADIUS

m.await_loaded_region(block_x_min, block_z_min, block_x_max, block_z_max)
            
blocks_sky = m.get_block_region(
    (block_x_min, Y_LEVEL_SEARCHING_SKY_TH[0], block_z_min),
    (block_x_max, Y_LEVEL_SEARCHING_SKY_TH[1], block_z_max)
)

blocks_ground = m.get_block_region(
    (block_x_min, Y_LEVEL_SEARCHING_UNDERGROUND_TH[0], block_z_min),
    (block_x_max, Y_LEVEL_SEARCHING_UNDERGROUND_TH[1], block_z_max)
)

blocks_surface = m.get_block_region(
    (block_x_min, Y_LEVEL_SEARCHING_SURFACE_TH[0], block_z_min),
    (block_x_max, Y_LEVEL_SEARCHING_SURFACE_TH[1], block_z_max)
)

end_time = time.perf_counter()

m.echo(blocks_sky)
m.echo(blocks_ground)
m.echo(blocks_surface)
m.echo("pass")
m.echo(f"time taken: {end_time - start_time}")