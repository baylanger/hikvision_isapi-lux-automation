import os
import re

def slugify(text):
    return re.sub(r'[\s\-]+', '_', text.strip().lower())

def configure_automation():
    print("==================================================")
    print("      Hikvision Create Camera YAML files          ")
    print("==================================================")
    
    # 1. Get Camera Name (e.g., "Cam Office")
    camera_name = input("Camera name (example: Camera Frontyard): ").strip()
    if not camera_name:
        print("ERROR: a camera name is required")
        exit(1)
    camera_name_slug = slugify(camera_name)
    print(f"\nSlugified camera name: '{camera_name_slug}'\n")

    # 2. Get Entity ID Prefix
    print("==================================================")
    print("After you add your camera, you need the 'entity ID prefix'")
    print("Example using the camera's brightness sensor:")
    print("  sensor.ds_2cd2385g1_i_camera_frontyard_brightness")
    print("The 'entity ID prefix' is ds_2cd2385g1_i_camera_frontyard")
    print("==================================================\n")

    entity_prefix = input(f"Camera entity ID prefix [default: {camera_name_slug}]: ").strip()
    if not entity_prefix:
        entity_prefix = f"{camera_name_slug}"

    # 3. Get Lux Sensor
    sensor_id = input("\nCamera's lux sensor entity ID (e.g., frontyard_sensor_illuminance): ").strip()
    if not sensor_id:
        print("ERROR: a lux sensor entity ID is required")
        exit(2)
    if sensor_id.startswith("sensor."):
        sensor_id = sensor_id.replace("sensor.", "", 1)

    files_to_process = [
        "hikvision_lux_automation.yaml",
        "hikvision_lux_automation_dashboard_card.yaml"
    ]

    print("\n--------------------------------------------------")
    for template_filename in files_to_process:
        if not os.path.exists(template_filename):
            print(f"[Warning] Template file '{template_filename}' not found, skipping.")
            continue

        with open(template_filename, "r", encoding="utf-8") as f:
            content = f.read()

        # Replace placeholders using exact uppercase names
        content = content.replace("CAMERA_NAME_SLUG", camera_name_slug)
        content = content.replace("CAMERA_NAME", camera_name)
        content = content.replace("CAMERA_ENTITY_ID_PREFIX", entity_prefix)
        content = content.replace("CAMERA_SENSOR_ILLUMINANCE", sensor_id)

        output_filename = f"{camera_name_slug}_{template_filename}"
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"Generated: '{output_filename}'")

    print("--------------------------------------------------")
    print("Setup complete!")

if __name__ == "__main__":
    configure_automation()
