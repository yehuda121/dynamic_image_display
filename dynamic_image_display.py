from PIL import Image, ImageEnhance
import pygame
import random

# Load the image
image_path = "C:/Users/yehud/Desktop/high frinquncy picture/WIN_20241123_15_48_32_Pro.jpg"
image = Image.open(image_path)
image_width, image_height = image.size

# Split the image into parts and precompute dimmed versions
def split_image(image, grid_size, transparency):
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
            part_image = image.crop(box)
            dimmed_part = ImageEnhance.Brightness(part_image).enhance(transparency)
            parts.append((box, part_image, dimmed_part))
    return parts

# Display the parts
def display_parts(parts, grid_size, window_size, num_parts_to_show):
    pygame.init()
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Dynamic Image Display")
    running = True

    while running:
        screen.fill((255, 255, 255))  # White background
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Randomly select parts to display
        visible_parts = random.sample(parts, num_parts_to_show)
        visible_boxes = {box for box, _, _ in visible_parts}

        # Render each part
        for box, part, dimmed_part in parts:
            x, y, _, _ = box
            if box in visible_boxes:
                part_image = pygame.image.fromstring(
                    part.tobytes(), part.size, part.mode
                )
            else:
                part_image = pygame.image.fromstring(
                    dimmed_part.tobytes(), dimmed_part.size, dimmed_part.mode
                )
            screen.blit(part_image, (x, y))

        pygame.display.flip()

    pygame.quit()


# Configurations
grid_size = 10  # Divide the image into 10x10 parts
num_parts_to_show = grid_size * grid_size // 2  # Display 50% of parts
transparency = 0.3  # Transparency for non-visible parts
window_size = (image_width, image_height)
parts = split_image(image, grid_size, transparency)

# Run the display
display_parts(parts, grid_size, window_size, num_parts_to_show)
