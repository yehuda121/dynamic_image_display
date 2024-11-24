from PIL import Image, ImageEnhance
import pygame
import random



# Load the image
image_path = "C:/Users/yehud/Desktop/image.jpg"
image = Image.open(image_path)
image_width, image_height = image.size

# Split the image into parts
def split_image(image, grid_size):
    parts = []
    part_width = image_width // grid_size
    part_height = image_height // grid_size
    for i in range(grid_size):
        for j in range(grid_size):
            box = (
                j * part_width,
                i * part_height,
                (j + 1) * part_width,
                (i + 1) * part_height,
            )
            parts.append((box, image.crop(box)))
    return parts

# Display the parts
def display_parts(parts, grid_size, window_size, num_parts_to_show):
    pygame.init()
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Image Display")
    running = True

    while running:
        screen.fill((0, 0, 0))  # Black background
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Randomly select parts to display
        visible_parts = random.sample(parts, num_parts_to_show)

        # Draw each part with dimming for non-visible parts
        for box, part in parts:
            x, y, _, _ = box
            if box in visible_parts:
                part_image = pygame.image.fromstring(
                    part.tobytes(), part.size, part.mode
                )
            else:
                dimmed_part = make_transparent(part, box)
                part_image = pygame.image.fromstring(
                    dimmed_part.tobytes(), dimmed_part.size, dimmed_part.mode
                )
            screen.blit(part_image, (x, y))

# Dim the part for the background
def make_transparent(image, transparency):
    enhancer = ImageEnhance.Brightness(image)
    transparent_image = enhancer.enhance(transparency)
    return transparent_image

# Configurations
grid_size = 10  # Divide the image into 10x10 parts
num_parts_to_show = grid_size * grid_size // 2  # Display 50% of parts

window_size = (image_width, image_height)
parts = split_image(image, grid_size)

# Run the display
display_parts(parts, grid_size, window_size, num_parts_to_show)
